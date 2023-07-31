from django.db import connection
import pandas as pd
import datetime
import re
import pytz

def report_project(listIDs):
    projectList = []
    with connection.cursor() as cursor:
        sql = """
               select ap.enq_id as "ENQ" ,
            ac.company_full_name as "Company",
            ap.project_name as"Project Name",

            TO_CHAR(ap.project_start,'DD Mon YYYY') as "Start",TO_CHAR(ap.project_end,'DD Mon YYYY') as "End",
            ap.customer_po as "Customer PO",ap.contract_no as "Contract-No Reference",

           (select count(*) from app_inventory where project_id=ap.id ) as "Total Inventories",
           (select count(*) from app_preventivemaintenance where project_id=ap.id  ) as "Total PM-Plans",
           (select count(*) from app_incident where inventory_id in
             (select id from app_inventory where app_inventory.project_id=ap.id )
           ) as "Total Incidents"


       from app_project ap
       left join app_company ac on ac.id = ap.company_id
       where    ap.id in %s
       order by  ap.enq_id

    """

        cursor.execute(sql, [tuple(listIDs)])

        columns = [col[0] for col in cursor.description]
        projectList = [dict(zip(columns, row)) for row in cursor.fetchall()]
        df = pd.DataFrame(data=projectList)

    return df

def report_inventory(listIDs):
    inventoryList = []
    with connection.cursor() as cursor:
        sql = """
        select  inventory.id as "ID",comp.company_name  as "Customer Name" ,project.enq_id as  "ENQ",
              inventory.serial_number as  "Serial No. / CD-Key"  ,inventory.asset_code  as "Asset Code",
              inventory.quantity as "QTY"  ,
         product_type.productype_name as "Type",
        brand.brand_name as "Brand",model.model_name as  "Model",
       datacenter.datacenter_name as "Data Center",branch.branch_name as "Branch",

       TO_CHAR(inventory.customer_warranty_start,'DD Mon YYYY') as "Cust Warranty Start",TO_CHAR(inventory.customer_warranty_end,'DD Mon YYYY') as "Cust Warranty End", (select sla_name from app_sla where id=inventory.customer_sla_id ) as "SLA(Customer)",

       TO_CHAR(inventory.yit_warranty_start,'DD Mon YYYY') as "Yit Warranty Start"   ,TO_CHAR(inventory.yit_warranty_end ,'DD Mon YYYY') as "Yit Warranty End",(select sla_name from app_sla where id=inventory.yit_sla_id ) as "SLA(Yit)",

      TO_CHAR(inventory.product_warranty_start,'DD Mon YYYY') as "Product Warranty Start"  , TO_CHAR(inventory.product_warranty_end ,'DD Mon YYYY') as "Product Warranty End",(select sla_name from app_sla where id=inventory.product_sla_id)  as "SLA(Product)",

      (select service_team_name  from app_serviceteam  where id=inventory.cm_serviceteam_id) as "CM Service Team",
      (select service_team_name  from app_serviceteam  where id=inventory.pm_serviceteam_id) as "PM Service Team",
      (select concat( customer_name,' | ',customer_telephone,' | ',customer_email) from app_customer where id= (select id from app_customer where id=inventory.customer_support_id)) as "Customer Support",
      (select concat( customer_name,' | ',customer_telephone,' | ',customer_email) from app_customer where id= (select id from app_customer where id=inventory.customer_pm_support_id)) as "Customer PM Support",
      (select concat( product_name,' | ',product_telephone,' | ',product_email) from app_product where id= (select id from app_product where id=inventory.product_support_id)) as "Product Support",

       function.function_name as "Function", 
       inventory.storage_capacity as  "Storage Capacity",
       inventory.backup_solution as "Solution Backup",
       
	   inventory.building as "Building",inventory.floor as "Floor",inventory.room as "Room",
	   inventory.rack_position as "Rack Position",inventory.rack_unit as "Rack Unit",

	   TO_CHAR(inventory.install_date,'DD Mon YYYY') as "Install Date", TO_CHAR( inventory.eos_date,'DD Mon YYYY')  as "EOS Date",
	  
       inventory.devicename_hostname as  "Device / Host name",
       inventory.device_hs_version as "Device(HW/OS/SW) Version",	  
       inventory.firmware_bios_version as "HW(Firmware/Bios) Version",
       inventory.firmware_bundle_version as "Firmware Bundle Version",	
       inventory.hw_management_version as "HW Management Version",
       inventory.sw_management_version "SW Management Version",	
       
       inventory.ip_address as "IP Address Management",inventory.username as "User Name Management",inventory.password as "Password Management",
       inventory.ip_address2 as "IP Address 2",inventory.username2 as "User Name 2",inventory.password2 as "Password 2",
       inventory.ip_address3 as "IP Address 3",inventory.username3 as "User Name 3",inventory.password3 as "Password 3",
       
	   project.customer_po as  "Customer Contract / PO" ,project.project_name as"Project Name",
	   
	   template.template_file_name as "PM-Template",
	   
	   inventory.remark as  "Remark"  

    from app_inventory inventory
    left join  app_project project on inventory.project_id=project.id
    left join app_company comp on project.company_id =comp.id

    left join app_product_type  product_type on inventory.product_type_id = product_type.id
    inner join  app_brand brand on inventory.brand_id =brand.id
    left join app_model model on inventory.model_id  = model.id

   left join app_datacenter datacenter on inventory.datacenter_id = datacenter.id
   left join app_branch branch on inventory.branch_id = branch.id
    left join app_function function on inventory.function_id = function.id
    left join app_pm_inventory_template as template on template.id=  inventory. pm_inventory_template_id     

   where project.is_dummy=false and inventory.id in  %s

  order by project.enq_id ,product_type.productype_name,brand.brand_name,model.model_name,inventory.serial_number
"""

        cursor.execute(sql, [tuple(listIDs)])
        # cursor.callproc('fn_list_inventory_report', (enq_id, 0, warranty_start_param, warranty_end_param))

        columns = [col[0] for col in cursor.description]
        inventoryList = [dict(zip(columns, row)) for row in cursor.fetchall()]
        df = pd.DataFrame(data=inventoryList)

        # incident_from='2020-09-18'
        # incident_to = '2020-09-20'
        # cursor.callproc('fn_list_incident_report', (comp_id , incident_from,incident_to))

    return df


def report_incident_detail(incident_id):
    detaiList = []
    df = None
    with connection.cursor() as cursor:
        sql = """
              select TO_CHAR(detail.task_start AT TIME ZONE 'Asia/Bangkok','DD Mon YYYY HH24:MI')  as task_start
              ,TO_CHAR(detail.task_end AT TIME ZONE 'Asia/Bangkok','DD Mon YYYY HH24:MI') as task_end
              ,detail.workaround_resolution
         ,team.service_team_name,engineer.employee_name as engineer_name
    
    from app_incident_detail detail
         inner join  app_serviceteam team on detail.service_team_id=team.id
         inner  join  app_employee engineer on detail.employee_id=engineer.id
    where detail.incident_master_id=%s 
    ORDER BY detail.task_start DESC
    
        """
        cursor.execute(sql, [incident_id])

        columns = [col[0] for col in cursor.description]
        detaiList = [dict(zip(columns, row)) for row in cursor.fetchall()]
        df = pd.DataFrame(data=detaiList)

    # if  df.empty==False:
    #  datetime_tz_columns =['task_start','task_end']
    #  # datetime_tz_columns = ['task_start',]
    #  for dt_col in  datetime_tz_columns :
    #     df[dt_col] = df[dt_col].apply(
    #         lambda x: x.replace(tzinfo=None) if not pd.isnull(x) else None)
    try:
        df = df.fillna(value='')
    except Exception as ex:
        error = str(ex)
        raise ex

    return df


def report_incident(listIDs):
    incidentList = []

    with connection.cursor() as cursor:
        sql = """
 select incident.id as "ID"
          ,incident.incident_no as "Incident-ID" ,incident.incident_subject as "Subject"
          
         ,TO_CHAR(incident.incident_datetime AT TIME ZONE 'Asia/Bangkok','DD Mon YYYY HH24:MI')   as "Incident Date"
         , TO_CHAR(incident.incident_problem_start AT TIME ZONE 'Asia/Bangkok','DD Mon YYYY HH24:MI') as "Response Date"
         , TO_CHAR(incident.incident_problem_end AT TIME ZONE 'Asia/Bangkok' ,'DD Mon YYYY HH24:MI') as "Resolved Date"
         ,TO_CHAR(incident.incident_close_datetime AT TIME ZONE 'Asia/Bangkok','DD Mon YYYY HH24:MI')   as "Incident Closed Date"
         
        , '' as "TotalTime To Service",'' as "TotalTime To Service(Minutes)"
       , '' as "TotalTime To SLA",'' as "TotalTime To SLA(Minutes)"
         
        ,incident."incident_reference_customer_caseNo" as  "CustRef-No"
        
        ,severity.severity_name as "Severity",status.incident_status_name as "Status"
        ,type.incident_type_name as "Type",service.service_type_name as "ServiceType"
        , product_type.productype_name AS  "Product Type", brand.brand_name as "Brand" ,model.model_name  as "Model"
       
        ,inventory.serial_number as "Serial No./CD-Key"    
         ,comp.company_name as "Company", project.enq_id as "ENQ"
      
       , datacenter.datacenter_name as "Data Center", branch.branch_name as "Branch"
       ,incident.incident_customer_support as "Customer Support Contact"
       ,incident.incident_description as "Problem Description"
     from  app_incident incident
     left join  app_incident_severity severity on incident.incident_severity_id=severity.id
     left join  app_incident_status status on incident.incident_status_id =status.id
     left join app_incident_type type on  incident.incident_type_id =type.id
     left join app_service_type service on incident.service_type_id =service.id
     left join app_inventory inventory on incident.inventory_id = inventory.id
	 left join app_project project on inventory.project_id = project.id
	 left join  app_company comp on project.company_id = comp.id
	 left join app_product_type product_type  on inventory.product_type_id  = product_type.id
     left join  app_brand brand on inventory.brand_id =brand.id
     left join app_model model on inventory.model_id  = model.id

    inner join app_datacenter datacenter on inventory.datacenter_id = datacenter.id
   inner join app_branch branch on inventory.branch_id = branch.id

      where incident.id in  %s  
      order by  incident.incident_datetime,project.enq_id,incident.incident_no
    """

        cursor.execute(sql, [tuple(listIDs)])
        # cursor.callproc('fn_list_inventory_report', (enq_id, 0, warranty_start_param, warranty_end_param))

        columns = [col[0] for col in cursor.description]
        incidentList = [dict(zip(columns, row)) for row in cursor.fetchall()]
        try:
            df = pd.DataFrame(data=incidentList)
        except Exception as ex:
            error = str(ex)
            raise ex

        # df['incident_datetime'] = df['incident_datetime'].dt.tz_localize(None)
        # datetime_tz_columns = ['Incident Date', 'Problem Date Start', 'Problem Date End']
        # for dt_col in datetime_tz_columns:
        #     df[dt_col] = df[dt_col].apply(lambda x: x.replace(tzinfo=None) if not pd.isnull(x) else None)

    def detail_by_incident(row):
        _ILLEGAL_CHARACTERS_RE = re.compile(r"[\000-\010]|[\013-\014]|[\016-\037]")
        id = row['ID']
        df_detail = report_incident_detail(id)
        des = ''
        if df_detail.empty == False:
            for index, detail in df_detail.iterrows():
                task_start = detail['task_start']
                task_end = detail['task_end']
                x = f"{detail['service_team_name']} | {detail['engineer_name']} | {task_start} - {task_end} \n {detail['workaround_resolution']}\n\n"
                des = des + x

        des_fix = ''
        des_fix = _ILLEGAL_CHARACTERS_RE.sub("", des)

        return des_fix

    df['Resolution Description'] = df.apply(detail_by_incident, axis=1)

    def convert_detal_datetime_to_xyz(item, from_date, to_date, action_type):
        if item[to_date] is not None:
            start = item[from_date]
            start = datetime.datetime.strptime(start, '%d %b %Y %H:%M')
            end = item[to_date]
            end = datetime.datetime.strptime(end, '%d %b %Y %H:%M')
            if action_type == 'to_str':
                str_delta = str(end - start)
                return str_delta
            elif action_type == 'to_minutes':
                x_delta = ((end - start).total_seconds()) / 60
                return x_delta
        return ''

    df['TotalTime To Service'] = df.apply(convert_detal_datetime_to_xyz, axis=1,
                                          args=('Incident Date', 'Incident Closed Date', 'to_str'))
    df['TotalTime To Service(Minutes)'] = df.apply(convert_detal_datetime_to_xyz, axis=1,
                                                   args=('Incident Date', 'Incident Closed Date', 'to_minutes'))

    df['TotalTime To SLA'] = df.apply(convert_detal_datetime_to_xyz, axis=1,
                                      args=('Incident Date', 'Response Date', 'to_str'))
    df['TotalTime To SLA(Minutes)'] = df.apply(convert_detal_datetime_to_xyz, axis=1,
                                               args=('Incident Date', 'Response Date', 'to_minutes'))

    return df
