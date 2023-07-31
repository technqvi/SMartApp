
from django.db import connection

import pandas as pd


# In[314]:
def build_report(start_support_param,end_support_param,):

    def get_postgres_conn():
      return connection

    # In[330]:

    def list_data(sql, params, connection):
        df = None
        with connection.cursor() as cursor:

            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)

                #     print(sql)
            #     print(params)

            columns = [col[0] for col in cursor.description]
            dataList = [dict(zip(columns, row)) for row in cursor.fetchall()]
            df = pd.DataFrame(data=dataList)
        return df

        # In[331]:

    # end_support_param = '2022-12-31'
    # start_support_param = '2022-01-01'
    init_param = {"end_support_param": end_support_param, "start_support_param": start_support_param}

    total_col = "Total Score"
    avg_col = "Avg Score"
    summary_cols = [avg_col, total_col]

    # In[332]:

    # company
    sql_company = """
        select id as company_id,company_name from app_company  where is_customer=true and is_managed_by_admin=false  order by id 
            """
    print("Get All Customer Company")

    df_company = list_data(sql_company, None, get_postgres_conn())
    df_company.head()

    # In[333]:

    # product type

    capacity_storage_sql = """
        select ac.id as company_id,  sum(app_inventory.storage_capacity) as  sum_x from app_inventory
    inner join  app_project ap on app_inventory.project_id = ap.id  inner join app_company ac on ac.id = ap.company_id

    where 
    app_inventory.customer_warranty_end>=%(end_support_param)s
    and app_inventory.customer_warranty_end>=%(start_support_param)s
    and app_inventory.product_type_id=%(product_type_param)s 
    group by  ac.id
    order by  ac.id 
     """

    qty_product_type_sql = """
        select ac.id as company_id,  sum(app_inventory.quantity) as  sum_x from app_inventory
    inner join  app_project ap on app_inventory.project_id = ap.id  inner join app_company ac on ac.id = ap.company_id

    where 
    app_inventory.customer_warranty_end>=%(end_support_param)s
    and app_inventory.customer_warranty_end>=%(start_support_param)s
    and app_inventory.product_type_id=%(product_type_param)s 
    group by  ac.id
    order by  ac.id 
            """

    qty_other_product_type_sql = """
        select ac.id as company_id,  sum(app_inventory.quantity) as  sum_x from app_inventory
    inner join  app_project ap on app_inventory.project_id = ap.id  inner join app_company ac on ac.id = ap.company_id
    where 
    app_inventory.customer_warranty_end>=%(end_support_param)s
    and app_inventory.customer_warranty_end>=%(start_support_param)s
    and app_inventory.product_type_id  not in %(product_type_param)s 
    group by  ac.id
    order by  ac.id 
            """

    # In[334]:

    qty_incident_sql = """
    select ac.id as company_id,count(*) as count_x from app_incident
    inner join app_inventory ai on ai.id = app_incident.inventory_id
    inner join app_project ap on ap.id = ai.project_id
    inner join app_company ac on ac.id = ap.company_id
    where
    
    app_incident.incident_datetime>=%(start_support_param)s
    and app_incident.incident_datetime<=%(end_support_param)s
    and app_incident.service_type_id=%(service_type_param)s 
    and  app_incident.incident_status_id <> 3
    
    group by  ac.id
    order by  ac.id
    """

    # In[335]:

    def agg_data(sql, additional_params, agg_old_name, agg_new_name, df_comp):
        print(agg_new_name)
        pt_param = (init_param.copy())
        pt_param.update(additional_params)

        df_xyz = list_data(sql, pt_param, get_postgres_conn())
        df_xyz = df_xyz.rename(columns={agg_old_name: agg_new_name})
        # print(df_xyz.info())
        # print(df_xyz.head())

        df_agg = df_comp.merge(df_xyz, how='left', on='company_id')
        # print(df_agg)
        # print("==================================")
        return df_agg

        # In[336]:

    df_company = agg_data(capacity_storage_sql, {"product_type_param": 1}, 'sum_x', 'storage', df_company)

    # In[337]:

    df_company = agg_data(qty_product_type_sql, {"product_type_param": 2}, 'sum_x', 'server', df_company)

    # In[338]:

    df_company = agg_data(qty_product_type_sql, {"product_type_param": 3}, 'sum_x', 'software', df_company)

    # In[339]:

    df_company = agg_data(qty_product_type_sql, {"product_type_param": 4}, 'sum_x', 'network', df_company)

    # In[340]:

    df_company = agg_data(qty_other_product_type_sql, {"product_type_param": tuple([1, 2, 3, 4])}, 'sum_x',
                          'others', df_company)

    # In[341]:

    df_company = agg_data(qty_incident_sql, {"service_type_param": 1}, 'count_x', 'incident', df_company)

    # In[342]:

    df_company = agg_data(qty_incident_sql, {"service_type_param": 2}, 'count_x', 'request', df_company)

    # In[343]:

    df_company = df_company.fillna(0)

    # df_company=df_company.head()

    df_company

    # In[344]:

    sql_level = "select * from report_level_definition order by level_value desc "
    df_level = list_data(sql_level, None, get_postgres_conn())
    df_level.set_index("key", inplace=True)
    levelCols = df_level.index.tolist()

    # df_level.loc['level1','name']
    print(levelCols)
    print(df_level)

    # In[345]:

    sql_weight = "select * from report_key_value_weight where is_used=true"
    df_weight = list_data(sql_weight, None, get_postgres_conn())

    # In[346]:

    key_name_mapping = df_weight[['key', 'name']].to_dict('records')
    key_name_cols = df_weight['key'].tolist()

    # In[347]:

    df_weight = df_weight.drop(columns=['updated_at', 'is_used'])
    df_weight.set_index("key", inplace=True)
    df_weight

    # In[348]:

    def cal_value_to_score(item, key_name):
        val = item[key_name]
        rank = 1

        for level in levelCols:
            if val >= df_weight.loc[key_name, level]:
                rank = df_level.loc[level, 'level_value']
                break
                # if val>=df_weight.loc[key_name,"level5"]:
        #   rank= 5
        # elif val>=df_weight.loc[key_name,"level4"]:
        #   rank= 4
        # elif val>=df_weight.loc[key_name,"level3"]:
        #   rank= 3
        # elif val>=df_weight.loc[key_name,"level2"]:
        #   rank= 2
        # else:
        #   rank= 1

        weight_vale = df_weight.loc[key_name, "weight_value"]
        score = weight_vale * rank
        # print(score)

        return score

    # In[349]:

    score_cols = []
    # print(key_name_cols)
    for key in key_name_cols:
        # dict_key_value_weight=df_weight.loc[key].to_dict()
        score_name = f"{key.title()}-Score"
        df_company[score_name] = df_company.apply(cal_value_to_score, axis=1, args=(key,))
        score_cols.append(score_name)

    # In[350]:

    def sum_score(item):
        total_score = 0
        for col in score_cols:
            total_score = total_score + item[col]
        return total_score

    # In[351]:

    df_company[total_col] = df_company.apply(sum_score, axis=1)
    df_company[avg_col] = df_company[total_col] / len(key_name_cols)
    df_company = df_company.round(2)
    df_company.drop(columns=['company_id'], inplace=True)
    # df_company[score_cols+["total_score"]]
    df_company.info()

    # In[352]:

    new_mapping = {}
    new_cols = []
    for item in key_name_mapping:
        old_col = item['key']
        new_col = item['name']
        new_mapping[old_col] = new_col
        new_cols.append(new_col)
    #     print(old_col,' : ',new_col)
    new_mapping['company_name'] = 'Company'

    df_company = df_company.rename(columns=new_mapping)
    df_company

    # In[353]:

    order_cols = ['Company'] + summary_cols + score_cols + new_cols
    order_cols

    # In[355]:

    df_company = df_company.sort_values(by=summary_cols[0], ascending=False)
    df_company = df_company[order_cols]
    df_company

    # In[356]:
    return  df_company,df_weight,df_company.columns.tolist()

