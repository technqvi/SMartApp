from django.db import connection
import pandas as pd
import datetime
import re
import pytz

# def report_inventory(listIDs) from report_manager.py
def export_non_pm_inventories_of_all_pm_plans(listIDs):
    listIDs=tuple(listIDs)
    sql = f"""
    
select ap.enq_id as "ENQ" ,ac.company_full_name as "Company",ap.project_name as"Project Name",
TO_CHAR(ap.project_start,'DD Mon YYYY') as "Start",TO_CHAR(ap.project_end,'DD Mon YYYY') as "End",
ap.customer_po as "Customer PO",ap.contract_no as "Contract-No Reference",

ai.serial_number as "Serial",
(select  productype_name from app_product_type where id=ai.product_type_id ) as "ProudctType",
(select  brand_name from app_brand where id=ai.brand_id ) as "Brand",
(select  model_name from app_model where id=ai.model_id ) as "Model",
TO_CHAR(ai.customer_warranty_start,'DD Mon YYYY') as "Cust Warranty Start",
TO_CHAR(ai.customer_warranty_end,'DD Mon YYYY') as "Cust Warranty End",
(select sla_name from app_sla where id=ai.customer_sla_id ) as "SLA(Customer)"

from  app_inventory ai
inner join app_project ap on ap.id = ai.project_id
inner join app_company ac on ac.id = ap.company_id
 
where ai.id in(
    select id from app_inventory
    where
    project_id in (select distinct project_id from app_preventivemaintenance where id in  {listIDs}  )
    and
    id not in ( select distinct inventory_id  from app_pm_inventory
    where is_pm=True and pm_master_id in (select id from app_preventivemaintenance where id in  {listIDs} )

))

order by ap.enq_id

"""
    with connection.cursor() as cursor:
      if len(listIDs)>0:
         cursor.execute(sql)
      else:
          cursor.execute(sql)

      columns = [col[0] for col in cursor.description]
      ivtList = [dict(zip(columns, row)) for row in cursor.fetchall()]

      # get inventory List to pass into SQL inventory

      df = pd.DataFrame(data=ivtList)

      return df


def export_pm_summary_by_company_project(listIDs):
    pmList = []
    sql="""
        select ap.enq_id as "ENQ" ,
            ac.company_full_name as "Company",
            ap.project_name as"Project Name",

            TO_CHAR(ap.project_start,'DD Mon YYYY') as "Start",TO_CHAR(ap.project_end,'DD Mon YYYY') as "End",
            ap.customer_po as "Customer PO",ap.contract_no as "Contract-No Reference",


            TO_CHAR(pm.planned_date,'Mon YYYY') as "PM Plan Date", 
            TO_CHAR(pm.ended_pm_date,'DD Mon YYYY') as "PM Ended Date",
           pm.remark as  "PM Period",
           (select count(*) from app_pm_inventory where pm_master_id=pm.id and is_pm=True ) as "PMItems",
           (select count(*) from app_pm_inventory where pm_master_id=pm.id and is_pm=False ) as "No-PMItems",
           (select count(*) from app_pm_inventory where pm_master_id=pm.id   ) as "Total Inventories"

       from app_preventivemaintenance pm
       left join app_project ap on ap.id = pm.project_id
       left join app_company ac on ac.id = ap.company_id
       where pm.id in %s 
       order by ac.id,ap.id,pm.planned_date,pm.remark
    """


    with connection.cursor() as cursor:
      if len(listIDs)>0:
       cursor.execute(sql, [tuple(listIDs)])
      else:
          cursor.execute(sql)

      columns = [col[0] for col in cursor.description]
      pmList = [dict(zip(columns, row)) for row in cursor.fetchall()]
      df = pd.DataFrame(data=pmList)

      return df
def export_pm_plan(listIDs):
    pmList = []
    with connection.cursor() as cursor:
      sql = """
        select ac.company_full_name as "ชื่อลูกค้า",
       ap.contract_no as "เลขที่สัญญา",ap.enq_id as "ENQ" ,
       ap.project_name as "ชื่อโครงการ",
       TO_CHAR(pm.planned_date,'Mon YYYY') as "แผนจะทำPM",
       TO_CHAR(pm.ended_pm_date,'DD Mon YYYY') as "วันสุดท้ายที่ทำPM",
       pm.remark as  "งวดPM",
       ae.employee_name as "หัวหน้าทีม",
       (select emp.employee_name emp from app_employee emp where emp.id=pm.engineer_id ) as "Engineer"

from app_preventivemaintenance pm
left join app_project ap on ap.id = pm.project_id
left join app_company ac on ac.id = ap.company_id
left join app_employee ae on ae.id =pm.team_lead_id
where pm.id in %s
"""

      cursor.execute(sql, [tuple(listIDs)])

      columns = [col[0] for col in cursor.description]
      pmList = [dict(zip(columns, row)) for row in cursor.fetchall()]
      df = pd.DataFrame(data=pmList)

      return df

def export_pm_iventory_item(itemIDs):
    itemList = []
    with connection.cursor() as cursor:
        sql = """
 select  ac.company_full_name as "ชื่อลูกค้า",
 ap.contract_no as "เลขที่สัญญา",ap.enq_id as "ENQ" , ap.project_name as "ชื่อโครงการ",

             ai.serial_number as "Serial",
             (select  productype_name from app_product_type where id=ai.product_type_id ) as "ProudctType",
             (select  brand_name from app_brand where id=ai.brand_id ) as "Brand",
              (select  model_name from app_model where id=ai.model_id ) as "Model",

             TO_CHAR(pm.planned_date,'Mon YYYY') as "แผนจะทำPM",TO_CHAR(pm.ended_pm_date,'DD Mon YYYY') as "วันสุดท้ายที่ทำPM",
             pm.remark as  "งวดPM",ae.employee_name as "หัวหน้าทีม",
             (select emp.employee_name emp from app_employee emp where emp.id=pm.engineer_id ) as "Planed Engineer",

           (select employee_name from app_employee eng_pm  where eng_pm.id=pm_item.pm_engineer_id ) as "Operation Engineer",
           TO_CHAR(pm_item.actual_date,'DD Mon YYYY') as "ActualDate",pm_item.call_number as "Call Number",

            (select employee_name from app_employee eng_doc  where eng_doc.id=pm_item.document_engineer_id ) as "Doc Engineer",
           TO_CHAR(pm_item.document_date,'DD Mon YYYY') as "DocumentDate",pm_item.pm_document_number as "Doc Number",
           pm_item.remark as "Remark"

from app_pm_inventory as pm_item
left join app_inventory ai on ai.id = pm_item.inventory_id
-- inner join app_product_type  product_type on ai.product_type_id = product_type.id
left join app_preventivemaintenance pm on pm.id = pm_item.pm_master_id
left join app_project ap on ap.id = pm.project_id
left join app_company ac on ac.id = ap.company_id
left join app_employee ae on ae.id =pm.team_lead_id

where  pm_item.id in %s and pm_item.is_pm=True
    """
#where  pm_item.id in (21797)  and is_pm=True
        cursor.execute(sql, [tuple(itemIDs)])
        # cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        itemList = [dict(zip(columns, row)) for row in cursor.fetchall()]
        df = pd.DataFrame(data=itemList)
        # df.to_csv("pm_items.csv")
        return df
