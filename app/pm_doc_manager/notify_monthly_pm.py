# To run this file correctly, do the following
# indent : entire code inside to function
# delete : is_only_admin=0  and For Dev psycopg2 and dotnet env
# uncomment: For Production running on Python Enviroment
# uncomment : return and dtNow=datetime.now()

def send_email_with_excel_file(email_info,file_path,file_name):
    from django.core.mail import BadHeaderError
    from django.core.mail import EmailMessage
    #https://stackoverflow.com/questions/34661771/django-emailmessage-attachments-attribute
    #https://studygyaan.com/django/how-to-send-email-with-attachments-in-django
    # create the attachment triple for this filename and add the attachment to the list
    listAttachedFile = []  # start with an empty list
    content = open(file_path, 'rb').read()
    attachment = (file_name, content, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    listAttachedFile.append(attachment)
    try:
        email = EmailMessage(
        email_info['subject'],email_info['message'],
        'smartapp-service@yipintsoigroup.com',email_info['send_to'],attachments=listAttachedFile
    )
        email.send()
    except BadHeaderError as ex:
        raise ex
    return True

def notify_monthly_pm_to_admin(is_only_admin):


    # In[51]:


    import pandas as pd
    from dotenv import dotenv_values

    from datetime import datetime,date
    from dateutil import relativedelta
    import os


    # # Paramter & Config values

    # In[52]:

    is_only_admin=bool(is_only_admin)

    temp_doc="temp_pm_notifcation"


    # # Retrive data from SMartDB Postgresql
    #

    # In[53]:


    # For Production running on Python Enviroment
    from django.db import connection
    def get_postgres_conn():
      return connection

    # In[54]:


    def list_data(sql,params,connection):
     df=None
     with connection.cursor() as cursor:

        if params is None:
           cursor.execute(sql)
        else:
           cursor.execute(sql,params)

        columns = [col[0] for col in cursor.description]
        dataList = [dict(zip(columns, row)) for row in cursor.fetchall()]
        df = pd.DataFrame(data=dataList)
     return df


    # # Get the next month
    # * Set Window Sheduler to monthly run at the fist dsate of The month
    # * No matter what day you run this job , the program will  get only all PMs over the current month

    # In[55]:


    dtNow= datetime.strptime(datetime(2023,12,1,6,0).strftime('%Y-%m-%d'),'%Y-%m-%d')
    # dtNow=datetime.now()

    dt = datetime.strptime(dtNow.strftime('%Y-%m-%d'),'%Y-%m-%d')
    print(dt)

    first_day_next_month = datetime(dt.year,dt.month,1)
    first_day_2next_month = dt + relativedelta.relativedelta(months=1, day=1)
    print(first_day_next_month )
    print(first_day_2next_month )


    # # Create File Name and Path to attach to email

    # In[56]:


    file_name=f"PM_{first_day_next_month.strftime('%b%y')}_{dtNow.strftime('%d%m%y%H%M')}.xlsx"
    if is_only_admin==False:
       file_name=f"SM-{file_name}"
    else:
       file_name=f"NoneSM-{file_name}"
    file_path=f"{temp_doc}/{file_name}"
    print(file_path)
    # In[ ]:





    # # Retrive  and Transaform data

    # In[57]:


    def do_something_df(df):
        df = df.fillna(value='')
        df = df.reset_index(drop=False)
        df.insert(0, "No", df["index"]+1,True)
        df=df.drop(columns=["index"])
        return df


    # In[58]:


    # https://github.com/technqvi/SMartApp/blob/main/app/pm_doc_manager/pm_export.py

    sql_pm=f"""
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
        where  pm.planned_date>='{first_day_next_month}' and pm.planned_date<'{first_day_2next_month}'
        and ac.is_managed_by_admin = {is_only_admin}
        order by  ac.company_full_name,ap.enq_id,pm.remark
        """
    # print(sql_pm)


    # In[59]:


    dfPM=list_data(sql_pm,None,get_postgres_conn())
    dfPM=do_something_df(dfPM)
    dfPM.info()
    dfPM.head()


    # In[60]:


    sql_item = f"""
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
    
    where pm_item.is_pm=True and ac.is_managed_by_admin = {is_only_admin}
    and  pm.planned_date>='{first_day_next_month}' and pm.planned_date<'{first_day_2next_month}'
    
    order by  ac.company_full_name,ap.enq_id,pm.remark
    
        """

    # print(sql_item)


    # In[61]:


    dfItem=list_data(sql_item,None,get_postgres_conn())
    dfItem=do_something_df(dfItem)
    dfItem.info()
    dfItem.head()


    # # Excel file
    with pd.ExcelWriter(file_path) as writer:
        dfPM.to_excel(writer, sheet_name="PM-Plan",index=False)
        dfItem.to_excel(writer, sheet_name="PM-Item",index=False)
        print(f"Exported {file_name} file for email successfully.")

    # # Email Office 365
    title = f'SmartPM : Monthly Notification To Admin - {file_name}'
    content = f'Download  PM-Plan excel file'
    email_info = {'subject': title, 'message': content, 'send_to': ["pongthorn.sa@yipintsoi.com"]}
    is_sussessful = send_email_with_excel_file(email_info,file_path,file_name)
    print("Sent mail successfully.")

    # In[ ]:


    # In[ ]:





    # In[ ]:





    # # Delete attach files : if sent email with excel file completely

    # In[48]:


    os.remove(f"{file_path}")
    print("Deleted file for email attachemnt  succesfully.")


    # In[ ]:





    # In[64]:


    return is_sussessful


# In[ ]:




