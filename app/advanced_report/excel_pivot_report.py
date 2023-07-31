#!/usr/bin/env python
# coding: utf-8

# In[55]:


import pandas as pd
# In[56]:


def build_pivot_report(df):


# In[57]:


    is_production=True


    # In[58]:


    # get from get_table_report
    #df=pd.read_excel('df_all.xlsx')
    df.info()


    # In[59]:


    def create_x_pivot(df_source,selected_cols,pv_indexes,pv_columns):
        dfx=df_source[selected_cols]
        dfx=dfx.rename(columns={'id':'item'})
        # dfx=dfx.sample(20)
        # dfx.to_excel("dfx.xlsx",index=False)

        print(dfx.head())

        xpivot=pd.pivot_table(dfx,index=pv_indexes
                   ,columns=pv_columns,values=["item"],aggfunc='count',fill_value=0,margins=True)
        return xpivot


    # In[60]:


    # test query  pivot inout_status
    # ptype_pm='Software'
    # brand_pm='VMWare'
    # status_pm='Closed'
    # sla_pm='in'
    # print(len(df.query('productype_name==@ptype_pm and  brand_name==@brand_pm and status==@status_pm')))
    # print(len(df.query('productype_name==@ptype_pm and  brand_name==@brand_pm and status==@status_pm and sla==@sla_pm')))


    # In[61]:


    pv_sla_status=create_x_pivot(df,["id","productype_name","brand_name","status","sla"],
                          ["productype_name","brand_name","status"],
                          ["sla"])



    pv_sla_status


    # In[62]:


    # test query  pivot inout_status
    # ptype_pm='Server'
    # brand_pm='DELL'
    # status_pm='Closed'
    # sla_pm='in'
    # severity_pm='Minor'
    # period_pm='Mar 2022'
    # str_qry='productype_name==@ptype_pm and  brand_name==@brand_pm and status==@status_pm and  severity_name==@severity_pm  and month_year==@period_pm'
    # df_qry=df.query(str_qry)
    # print(len(df_qry))


    # In[63]:



    pv_sla_period=create_x_pivot(df,["id","productype_name","brand_name","status","sla","severity_name","month_year"],
                          ["productype_name","brand_name","status"],["month_year","severity_name","sla"])

    pv_sla_period


    # In[64]:


    # for item in pv_sla_period.columns:
    #    print( type(item))
    #     dmy=datetime.datetime.strptime(month_year_1,'%m-%Y')
    # dmy_xxx=dmy.strftime('%b-%Y')
    # dmy_xxx


    # In[ ]:





    # In[65]:


    pv_type=create_x_pivot(df,["id","productype_name","incident_type_name","month_year"],
                          ["productype_name","incident_type_name"],["month_year"])

    pv_type


    # In[66]:


    #df_trasns.to_excel(tran2s_path2,index=False)

    if is_production==False:
        writer=pd.ExcelWriter("AIS-Pivot-Report.xlsx",engine='xlsxwriter')
        pv_sla_status.to_excel(writer, sheet_name="Pivot1")
        pv_sla_period.to_excel(writer, sheet_name="Pivot2")
        pv_type.to_excel(writer, sheet_name="Pivot3")
        writer.save()
        return None
    else:
        print("Production result")
        dfPivotReportDict={          "Pivot1": pv_sla_status,         "Pivot2": pv_sla_period,         "Pivot3":pv_type,

        }
        return  dfPivotReportDict


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




