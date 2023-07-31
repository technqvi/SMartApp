from django.db import connection
import pandas as pd
import datetime
import pytz


def count_incident(listSiteID,incident_date_from,incident_date_end):

    #incident_date_from =01-Jan-21 00:00
    #incident_date_end = 01-Jan-22 00:00

    with connection.cursor() as cursor:
        sql = """
         select status.id, status.incident_status_name ,count(*)
     from app_incident x
    inner join app_inventory inv on inv.id = x.inventory_id
    inner join app_project proj on proj.id=inv.project_id
    inner join app_company comp on comp.id = proj.company_id

    inner join  app_incident_status status on x.incident_status_id = status.id
    
    where comp.id in %(param_listSiteID)s  and
    ( x.incident_datetime >= %(param_date_from)s and x.incident_datetime < %(param_date_end)s )
    
    group by  status.id,status.incident_status_name

"""
        xParams = {"param_listSiteID": tuple(listSiteID), "param_date_from": incident_date_from ,"param_date_end":incident_date_end}
        cursor.execute(sql,xParams)

        columns = [col[0] for col in cursor.description]
        statusList = [dict(zip(columns, row)) for row in cursor.fetchall()]
        count_status_df=pd.DataFrame(data=statusList)

    return count_status_df


def list_inventory(listSiteID,current_date):

    with connection.cursor() as cursor:
        #select x.serial_number
        # select x.serial_number,x.customer_warranty_start,x.customer_warranty_end ,proj.enq_id,comp.company_name
        sql = """
select x.serial_number,x.customer_warranty_start
from app_inventory  x  inner join app_project proj on proj.id=x.project_id
inner join app_company comp on comp.id = proj.company_id
where  comp.id in %(param_listSiteID)s and   
( x.customer_warranty_start<=  %(param_current_date)s and x.customer_warranty_end>=%(param_current_date)s )
"""
        xParams = {"param_listSiteID": tuple(listSiteID), "param_current_date": current_date}
        cursor.execute(sql,xParams)

        columns = [col[0] for col in cursor.description]
        inventoryList = [dict(zip(columns, row)) for row in cursor.fetchall()]
        count_inventory_df=pd.DataFrame(data=inventoryList)

    return count_inventory_df