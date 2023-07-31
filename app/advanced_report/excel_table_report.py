#!/usr/bin/env python
# coding: utf-8

# In[136]:


import psycopg2
import psycopg2.extras as extras
import pandas as pd
import numpy as np
import json
from datetime import datetime
import re
from django.db import connection


# In[137]:


def build_table_report(company_id_query,start_date_query,end_date_query):

    _ILLEGAL_CHARACTERS_RE = re.compile(r"[\000-\010]|[\013-\014]|[\016-\037]")
    is_production=True
    # In[138]:


    # for django
    def get_postgres_conn():
      return connection



    # In[139]:





    # In[140]:


    def list_data(sql,params,connection):
     df=None
     with connection.cursor() as cursor:

        if params is None:
           cursor.execute(sql)
        else:
           cursor.execute(sql,params)

    #     print(sql)
    #     print(params)

        columns = [col[0] for col in cursor.description]
        dataList = [dict(zip(columns, row)) for row in cursor.fetchall()]
        df = pd.DataFrame(data=dataList)
     return df


    # In[141]:


    today_x=datetime.now()

    datetime_cols=['open_datetime','response_datetime','resolved_datetime','close_datetime']
    #date_cols=['install_date','eos_date','customer_warranty_start','customer_warranty_end']
    date_cols=['install_date']


    # In[142]:


    # sheet=All Issue
    print("All Display columns in All Issues")
    All_Issue_Cols=[
    ["case_id","Case ID"], ["productype_name","Type"],["brand_name","Brand"], ["model_name","Model"] ,["serial_number","Serial"]
    ,["severity_name","Severity"],["datacenter_name","Site"],["incident_subject","Problem Summary"]
    ,["open_datetime","Issue Date"],['response_datetime','Respond Date']
    ,['resolved_datetime','Resolved Date'],['close_datetime','Close Date']
    ,['summary_work_around_str','Summary WorkAround Time'] ,['incident_customer_support','Case Owner']
    ,['detail','Resolution Description'],['customer_support','MA Owner']
    ,['service_type_name','Service Type']
    ,['is_update_sw','Update Software']
    ]
    dfAll_Issue_Cols=pd.DataFrame(data=All_Issue_Cols,columns=['name','display_name'])
    dictAll_Issue=dict(zip(dfAll_Issue_Cols['name'].tolist(),dfAll_Issue_Cols['display_name'].tolist()))
    dictAll_Issue


    # In[143]:


    # sheet=Incident Issue
    print("All Display columns in Incident")
    Incident_Issue_Cols=All_Issue_Cols.copy()
    Incident_Issue_Cols.extend([ ['sla','SLA In/Out'],['aging_year','Aging(Year)'], ['failure_type','HW or SW Failure type'],['install_date','Product start']] )
    Incident_Issue_Cols = [x for x in Incident_Issue_Cols if x  not in [['service_type_name','Service Type']] ]
    #Incident_Issue_Cols

    Incident_Issue_Cols.insert(0,['running_number','No.'])


    dfIncident_Issue_Cols=pd.DataFrame(data=Incident_Issue_Cols,columns=['name','display_name'])
    dictIncident=dict(zip(dfIncident_Issue_Cols['name'].tolist(),dfIncident_Issue_Cols['display_name'].tolist()))
    dictIncident


    # In[144]:


    # sheet=Request Issue
    print("All Display columns in Request to Preventive Maintainance")
    Include_ServiceCols=[['no.eng','No. Eng'] ]

    Exclude_ServiceCols=[["case_id","Case ID"],["serial_number","Serial"],["severity_name","Severity"]
    ,["incident_subject","Problem Summary"],['incident_customer_support','Case Owner']
    ,['service_type_name', 'Service Type'],['summary_work_around_str','Summary WorkAround Time']
    ,['customer_support','MA Owner'],["productype_name","Type"] ]
    Service_Issue_Cols=All_Issue_Cols.copy()
    Service_Issue_Cols= [x for x in Service_Issue_Cols if x  not in Exclude_ServiceCols ]

    Service_Issue_Cols.extend(Include_ServiceCols )

    Service_Issue_Cols.insert(0,['running_number','No.'])
    Service_Issue_Cols.insert(1,['service_type_name','Type'])
    Service_Issue_Cols.insert(2,['productype_name','Equipment Type'])
    Service_Issue_Cols.insert(6,["incident_subject","Task Description"])
    Service_Issue_Cols.insert(11,['summary_work_around_str','Summary WorkAround Time'])
    Service_Issue_Cols.insert(12,['incident_customer_support','Requestor'])

    #Service_Issue_Cols.insert(len(Service_Issue_Cols)-1,['is_update_sw', 'Update Software'])
    #Service_Issue_Cols
    dfService_Issue_Cols=pd.DataFrame(data=Service_Issue_Cols,columns=['name','display_name'])
    dictService=dict(zip(dfService_Issue_Cols['name'].tolist(),dfService_Issue_Cols['display_name'].tolist()))
    dictService


    # In[145]:


    print("All Display columns in Out-SLA")

    OutSLA_Issue_Cols=[['running_number','No.'], ["vender","Vender"],['case_id', 'Case ID']
     ,["productype_name","Type"],["brand_name","Brand"],["model_name","Model"]
    ,['severity_name', 'Severity'],['summary_work_around_str', 'Summary WorkAround Time']
     ,['problem','Problem'],['cause','Cause']
     ,['effect','Effect'],['solution','Solution'],['preventive_guideline','Preventive Guideline']]
    dfOutSLA_Cols=pd.DataFrame(data=OutSLA_Issue_Cols,columns=['name','display_name'])
    dictOutSLA=dict(zip(dfOutSLA_Cols['name'].tolist(),dfOutSLA_Cols['display_name'].tolist()))
    dictOutSLA


    # In[ ]:





    # In[ ]:





    # In[146]:


    sql_all="""
    
    select  incident.id, incident.incident_no, product_type.productype_name,brand.brand_name,model.model_name
    ,incident.incident_severity_id,severity.severity_name,incident.incident_type_id,xtype.incident_type_name
    ,incident.incident_status_id,status.incident_status_name,incident.service_type_id,service.service_type_name
    ,incident.incident_customer_support
    
    ,inventory.serial_number,datacenter.datacenter_name
    ,incident.incident_subject,incident_description
    
    ,TO_CHAR(incident.incident_datetime  AT TIME ZONE 'Asia/Bangkok','DD Mon YYYY HH24:MI') as open_datetime
    ,TO_CHAR(incident.incident_close_datetime  AT TIME ZONE 'Asia/Bangkok','DD Mon YYYY HH24:MI') as close_datetime
    
    ,TO_CHAR(incident.incident_problem_start  AT TIME ZONE 'Asia/Bangkok','DD Mon YYYY HH24:MI') as response_datetime
    ,TO_CHAR(incident.incident_problem_end  AT TIME ZONE 'Asia/Bangkok','DD Mon YYYY HH24:MI') as resolved_datetime
    
    
    
    ,TO_CHAR(inventory.install_date  AT TIME ZONE 'Asia/Bangkok','DD Mon YYYY HH24:MI') as install_date
    ,TO_CHAR(inventory.eos_date  AT TIME ZONE 'Asia/Bangkok','DD Mon YYYY HH24:MI') as eos_date
    
    ,TO_CHAR(inventory.customer_warranty_start  AT TIME ZONE 'Asia/Bangkok','DD Mon YYYY HH24:MI') as customer_warranty_start
    ,TO_CHAR(inventory.customer_warranty_end AT TIME ZONE 'Asia/Bangkok','DD Mon YYYY HH24:MI') as customer_warranty_end
    , (select customer_name from app_customer 
      where id= (select id from app_customer where id=inventory.customer_support_id)
      ) as customer_support
      
    ,failure_type
    
    from app_incident as incident
    inner join app_incident_type as  xtype on incident.incident_type_id = xtype.id
    inner join  app_incident_status as status on incident.incident_status_id = status.id
    inner join  app_incident_severity as severity on  incident.incident_severity_id = severity.id
    inner join  app_service_type as service on incident.service_type_id= service.id
    
    inner join app_inventory as inventory on incident.inventory_id = inventory.id
    inner join app_datacenter as datacenter on inventory.datacenter_id = datacenter.id
    inner join app_brand as brand on inventory.brand_id = brand.id
    inner join app_model as model on inventory.model_id = model.id
    inner join app_product_type as product_type on inventory.product_type_id = product_type.id
    inner join app_project as project on inventory.project_id = project.id
    inner join app_company as company on project.company_id = company.id
    
    where company.id=%(company_id_param)s
    and incident.incident_datetime>=%(start_date_param)s 
    and  incident.incident_datetime<=%(end_date_param)s
    and incident.incident_severity_id<>4
    and incident.incident_status_id <>3
    
    order by id
    
    """

    # exclude cancel status and severity costmatix


    # In[147]:


    def convert_datetime_to_timedelta(item):
        if item['resolved_datetime'] is not None:
            start = item['open_datetime']
            end = item['resolved_datetime']

            delta = end - start
            #print(type(delta))
            # str_delta = str(delta)

            return delta
        return None


    # In[148]:


    print("Create all issues dataframe")
    dict_params = {"company_id_param": company_id_query, "start_date_param": start_date_query,
                   "end_date_param": end_date_query}
    df_all=list_data(sql_all,dict_params,get_postgres_conn())
    df_all.info()


    # In[149]:


    df_all.head()


    # In[150]:


    #df_all['incident_subject']=df_all['incident_subject'].apply(lambda x: _ILLEGAL_CHARACTERS_RE.sub("", x))
    df_all['incident_description']=df_all['incident_description'].apply(lambda x: _ILLEGAL_CHARACTERS_RE.sub("", x))


    # In[151]:


    # add Datatime columns
    df_all['open_datetime']=pd.to_datetime(df_all['open_datetime'], format='%d %b %Y %H:%M')
    df_all['close_datetime']=pd.to_datetime(df_all['close_datetime'], format='%d %b %Y %H:%M')

    df_all['response_datetime']=pd.to_datetime(df_all['response_datetime'], format='%d %b %Y %H:%M')
    df_all['resolved_datetime']=pd.to_datetime(df_all['resolved_datetime'], format='%d %b %Y %H:%M')


    # In[152]:


    # for calculating aging today-instaall date
    df_all['install_date']=pd.to_datetime(df_all['install_date'], format='%d %b %Y %H:%M')
    # df_all['eos_date']=pd.to_datetime(df_all['eos_date'], format='%d %b %Y %H:%M')


    # In[153]:


    #incident_type_id=14 name=Upgrade Software
    df_all ['is_update_sw']=df_all['incident_type_id'].apply( lambda x : 'Update patch' if x==14 else '' )


    # In[154]:


    df_all['month_year']= df_all['open_datetime'].apply(lambda x: x.strftime('%m-%Y'))


    # In[155]:


    df_all['status']= df_all['incident_status_id'].apply(lambda x:  'Closed' if x==4 else 'Opened')
    # for pivot


    # In[156]:


    df_all['work_around_time_delta'] = df_all.apply(convert_datetime_to_timedelta, axis=1)


    # In[157]:


    df_all['work_around_hour'] = df_all['work_around_time_delta'].apply(lambda x:  x.total_seconds() / (60*60) if x is not np.nan else np.nan  )


    # In[158]:


    #df_all['summary_work_around_str']=df_all['work_around_time_delta'].astype(object).where(df_all['work_around_time_delta'].notnull(),None)

    df_all['summary_work_around_str']=df_all["work_around_time_delta"].apply( lambda x : str(x) )
    df_all['summary_work_around_str']=df_all['summary_work_around_str'].apply( lambda x : x.replace('NaT','') )


    # In[ ]:





    # In[159]:


    def sla_in_out(item):
        # add service type= incident
        # critical and by 4 hour
        if item["incident_severity_id"]==1 :
           if item['work_around_hour']<=4:
            return "in"
           else:
            return "out"

        elif item["incident_severity_id"]==2:
           if item['work_around_hour']<=  168 :
            return "in"
           else:
            return "out"

        elif item["incident_severity_id"]==3:
           if item['work_around_hour']<=  (168 * 3) :
            return "in"
           else:
            return "out"
        else:
            return "cosmatic"
    df_all['sla']=df_all.apply(sla_in_out,axis=1)


    # In[160]:


    def cal_againg(item):
        aging_year=0
        if  pd.isna(item["install_date"])==False  :
          aging_year= round( abs(today_x-item['install_date']).days/365,1)
          # print(f'{today_x} to {item["install_date"]}={aging_year}')
        else:
          aging_year= np.nan
          # print (np.nan)
        return aging_year

    df_all['today']=today_x
    df_all['aging_year']=df_all.apply( cal_againg,axis=1)


    # In[161]:


    # get data from incidenet detail
    sql_allDetail = """
    select TO_CHAR(detail.task_start AT TIME ZONE 'Asia/Bangkok','DD Mon YYYY HH24:MI')  as task_start
    ,TO_CHAR(detail.task_end AT TIME ZONE 'Asia/Bangkok','DD Mon YYYY HH24:MI') as task_end
    ,detail.workaround_resolution,team.service_team_name,engineer.employee_name as engineer_name
    from app_incident_detail detail
         inner join  app_serviceteam team on detail.service_team_id=team.id
         inner  join  app_employee engineer on detail.employee_id=engineer.id
    where detail.incident_master_id=%(incident_id_param)s  
    ORDER BY detail.task_start DESC
    """



    def all_detail_by_incident(row):

        id = row['id']
        df_detail = list_data(sql_allDetail,{"incident_id_param": id},get_postgres_conn())
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

    df_all['detail'] = df_all.apply(all_detail_by_incident, axis=1)
    #df_all['detail']=''


    # In[162]:


    sql_caseIDDetail="""
    select  app_incident_detail.incident_master_id as incident_id, app_incident_detail."reference_product_caseNo" as case_id from app_incident_detail
    where app_incident_detail.incident_master_id  in %(incident_id_param)s 
    """

    dfDetailCaseIDs=list_data(sql_caseIDDetail,{"incident_id_param": tuple(df_all['id'].tolist())},get_postgres_conn())
    dfDetailCaseIDs.dropna(axis=0, how='any',inplace=True)
    dfDetailCaseIDs.drop_duplicates(inplace=True)
    dfDetailCaseIDs=dfDetailCaseIDs.groupby(['incident_id'], as_index=False).agg({'case_id' : ','.join  })

    #dfDetailCaseIDs

    df_all=df_all.merge(dfDetailCaseIDs,left_on="id",right_on="incident_id",how='left')


    # In[163]:


    # 982=for 4 items and 2 team but 3 eng ,987 =no enginerr ,883= for 2 items and 1 team  and 1 eng

    sql_count_eng="""
    select app_incident_detail.incident_master_id as incident_id, count(distinct employee_id) as "no.eng"  from app_incident_detail
    where app_incident_detail.incident_master_id in %(incident_id_param)s 
    group by  app_incident_detail.incident_master_id
    """

    dfNoEng=list_data(sql_count_eng,{"incident_id_param": tuple(df_all['id'].tolist())},get_postgres_conn())
    # dfNoEng
    df_all=df_all.merge(dfNoEng,left_on="id",right_on="incident_id",how='left')

    df_all["no.eng"] = df_all["no.eng"].fillna(0)


    # In[164]:


    df_all['issue_datetime']=df_all['open_datetime']
    df_all=df_all.sort_values(by=['issue_datetime'],ascending=True)


    # In[165]:


    for d in date_cols:
     df_all[d]=df_all[d].dt.strftime('%d-%b-%y')


    # In[166]:


    for d in datetime_cols:
     df_all[d]=df_all[d].dt.strftime('%d-%b-%y %H:%M')


    # In[ ]:





    # # splite all issues dataframe to others

    # In[167]:


    print("Create incident issues dataframe")
    #service_type=incident
    dfIncident=df_all.query("service_type_id==1")

    dfIncident=dfIncident.reset_index(drop=True)
    dfIncident = dfIncident.reset_index(level=0)
    dfIncident.rename(columns={"index": "running_number"},inplace=True)
    dfIncident['running_number']=dfIncident['running_number']+1


    # In[168]:


    print("Create Out-SLA incident issues dataframe")
    outSLA_str='out'
    dfOutSLA=dfIncident.query("sla==@outSLA_str")


    # In[169]:


    dfOutSLA['problem']=dfOutSLA.apply( lambda x :  f"{x.incident_subject}\n\n{x.incident_description}",axis=1 )
    dfOutSLA['cause']=''
    dfOutSLA['effect']=''
    dfOutSLA['solution']=''
    dfOutSLA['preventive_guideline']=''
    dfOutSLA['vender']='Yip In Tsoi'


    # In[170]:


    #service_type=incident
    print("Create request service to maintainance dataframe")
    dfService=df_all.query("service_type_id==2")
    dfService=dfService.reset_index(drop=True)
    dfService = dfService.reset_index(level=0)
    dfService.rename(columns={"index": "running_number"},inplace=True)
    dfService['running_number']=dfService['running_number']+1

    #incident type 15=Report error
    # dfService['service_type_name']= dfService.apply( lambda x: 'Report' if x.incident_type_id==15 else x.service_type_name ,axis=1)


    # In[ ]:





    # # Export Excel Report as Customer Format & Name

    # # All Issue

    # In[171]:


    dfAllIssue=df_all[dfAll_Issue_Cols['name'].tolist()]
    dfAllIssue=dfAllIssue.rename(columns=dictAll_Issue)
    dfAllIssue=dfAllIssue[dfAll_Issue_Cols['display_name'].tolist()]


    # In[172]:


    dfIncident=dfIncident[dfIncident_Issue_Cols['name'].tolist()]
    dfIncident=dfIncident.rename(columns=dictIncident)
    dfIncident=dfIncident[dfIncident_Issue_Cols['display_name'].tolist()]


    # In[173]:


    dfOutSLA=dfOutSLA[dfOutSLA_Cols['name'].tolist()]
    dfOutSLA=dfOutSLA.rename(columns=dictOutSLA)
    dfOutSLA=dfOutSLA[dfOutSLA_Cols['display_name'].tolist()]


    # In[174]:


    dfService=dfService[dfService_Issue_Cols['name'].tolist()]
    dfService=dfService.rename(columns=dictService)
    dfService=dfService[dfService_Issue_Cols['display_name'].tolist()]


    # In[175]:


    # dev eviroemnt
    if is_production==False:
        print("Developement result")

        writer=pd.ExcelWriter("AIS-Table-Report.xlsx",engine='xlsxwriter')

        dfAllIssue.to_excel(writer, sheet_name="AllIssues",index=False)
        dfIncident.to_excel(writer, sheet_name="IncidentIssues",index=False)
        dfOutSLA.to_excel(writer, sheet_name="OutSLA",index=False)
        dfService.to_excel(writer, sheet_name="PreventiveServiceRequest",index=False)
        writer.save()

        df_all.to_excel('df_all.xlsx',index=False)
        return None,None
    # production
    else:
        print("Production result")
        dfTableReportDict={
            "AllIssues": dfAllIssue,         "IncidentIssues": dfIncident,         "OutSLA": dfOutSLA,         "PreventiveServiceRequest": dfService
        }
        return  df_all,dfTableReportDict

    # In[ ]:





    # In[ ]:





    # In[ ]:




