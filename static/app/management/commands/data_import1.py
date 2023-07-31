from app.models import *
import pandas as pd
# Company Data
def importCompanyMaster(filename):
    company_master(filename)
    customer_master(filename)
    branch_master(filename)
    datacenter_master(filename)

def company_master(filename):
    df_company = pd.read_excel(filename, sheet_name='company', dtype={'name': str, 'address=': str,'telephone':str})
    #df_company.info()
    for index, row in df_company.iterrows():
        try:
         company = Company(company_name=row["name"], company_address=row["address"],
                          company_telephone = row["telephone"])

         company.save()
         print(row)
        except Exception as e:
         print(row)
         print(e)
    print("*************Add Company********************************")

def customer_master(filename):
    df_customer = pd.read_excel(filename, sheet_name='customer',
                                dtype={'company_id': int, 'name': str, 'surname=': str, 'telephone': str, 'email': str})
    #df_customer.info()
    for index, row in df_customer.iterrows():
        try:
            comp_obj = Company.objects.get(pk=row['company_id'])
            # print(comp_obj.company_name)
            customer = Customer(company=comp_obj, customer_name=row["name"], customer_surname=row["surname"],
                                customer_telephone=row["telephone"], customer_email=row["email"])
            customer.save()
            print(row)
        except Exception as e:

            print(e)
            print(row)
    print("****************Add Customer*************************")

def branch_master(filename):
    branch_df = pd.read_excel(filename, sheet_name='branch', dtype={'company_id': int, 'name': str,'code':str,'customer_id':int})
    for index, row in branch_df.iterrows():
        try:
            comp_obj = Company.objects.get(pk=row['company_id'])
            cust_obj = Customer.objects.get(pk=row['customer_id'])
            bch = Branch(company=comp_obj, branch_name=row["name"],branch_code=row["code"],customer=cust_obj)
            bch.save()

        except Exception as e:
            print(e)
            print(row)

    print("****************Add Branch*************************")

def datacenter_master(filename):
    datacenter_df=pd.read_excel(filename, sheet_name='datacenter', dtype={'company_id':int, 'name': str,'customer_id':int})
    for index, row in datacenter_df.iterrows():
        try:
          comp_obj=Company.objects.get(pk=row['company_id'])
          cust_obj = Customer.objects.get(pk=row['customer_id'])
          dc = DataCenter(company=comp_obj,datacenter_name=row["name"],customer=cust_obj)
          dc.save()
          print(row)
        except Exception as e:
         print(e)
         print(row)
    print("****************Add DataCenter*************************")