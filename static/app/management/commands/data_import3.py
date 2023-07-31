from app.models import *
import pandas as pd
# Inventory Data
def importInventoryMaster(filename):
    Severity_master(filename)


def Severity_master(filename):
    x_df=pd.read_excel(filename, sheet_name='Product_Type')
    for index, row in x_df.iterrows():
        try:
          obj=Product_Type.objects.create(productype_name=row["productype_name"])
          print(row)
        except Exception as e:
         print(e)
         print(row)
    print("****************Add Product_Type*************************")
def Partner_master(filename):
    x_df=pd.read_excel(filename, sheet_name='Partner')
    for index, row in x_df.iterrows():
        try:
          obj=Partner.objects.create(partner_name=row["partner_name"])
          print(row)
        except Exception as e:
         print(e)
         print(row)
    print("****************Add Partner*************************")
def SLA_master(filename):
    x_df=pd.read_excel(filename, sheet_name='SLA')
    for index, row in x_df.iterrows():
        try:
          obj=SLA.objects.create(sla_name=row["sla_name"])
          print(row)
        except Exception as e:
         print(e)
         print(row)
    print("****************Add SLA*************************")
def Function_master(filename):
    x_df=pd.read_excel(filename, sheet_name='Function')
    for index, row in x_df.iterrows():
        try:
          obj=Function.objects.create(function_name=row["function_name"])
          print(row)
        except Exception as e:
         print(e)
         print(row)
    print("****************Add Function*************************")

def Brand_master(filename):
    x_df=pd.read_excel(filename, sheet_name='Brand')
    for index, row in x_df.iterrows():
        try:
          obj=Brand.objects.create(brand_name=row["brand_name"])
          print(row)
        except Exception as e:
         print(e)
         print(row)
    print("****************Add Brand*************************")


def Model_master(filename):
    df = pd.read_excel(filename, sheet_name='Model',
                                dtype={'brand_id': int, 'model_name': str})

    for index, row in df.iterrows():
        try:
            brand_obj = Brand.objects.get(pk=row['brand_id'])
            obj = Model.objects.create(brand=brand_obj, model_name=row["model_name"])
            print(row)
        except Exception as e:

            print(e)
            print(row)
    print("****************Add Model*************************")


def Serviceteam_master(filename):
    df = pd.read_excel(filename, sheet_name='ServiceTeam',
                       dtype={'company_id': int, 'service_team_name': str})

    for index, row in df.iterrows():
        try:
            comp_obj = Company.objects.get(pk=row['company_id'])
            obj = ServiceTeam.objects.create(company=comp_obj, service_team_name=row["service_team_name"])
            print(row)
        except Exception as e:

            print(e)
            print(row)
    print("****************Add ServiceTeam*************************")