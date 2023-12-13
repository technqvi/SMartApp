from django.db import models
from django.contrib.auth.models import  User
#from django.contrib.auth import get_user_model

from django.conf import settings

from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver

from django.core.exceptions import ValidationError
import datetime

class Manager(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    #user = models.OneToOneField(get_user_model(), null=True, on_delete=models.CASCADE)
    #user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    manager_nickname= models.CharField('Nick Name',max_length=100)
    is_site_manager=models.BooleanField('Is SiteManager',default=True)

    #site = models.ManyToManyField(Company)

    def __str__(self):
        return f'{self.manager_nickname} - {self.user.first_name} {self.user.last_name}'
    def get_full_name(self):
        return f'{self.manager_nickname} - {self.user.first_name} {self.user.last_name} '
    class Meta:
        ordering = ['manager_nickname']


class Company(models.Model):
    company_name = models.CharField('Company Name', max_length=255,unique=True )
    company_full_name = models.CharField('Company Full Name', max_length=255, unique=True,null=True, blank=True)
    company_address=models.CharField('Company Address', null=True, blank=True,max_length=500)
    company_telephone = models.CharField('Company Telephone', max_length=255, null=True, blank=True)
    manager = models.ManyToManyField(Manager, null=True, blank=True,verbose_name="Site-Manager")

    is_customer =models.BooleanField('Is Customer',default=True)
    is_subcontractor = models.BooleanField('Is Sub Contractor', default=False)
    is_managed_by_admin=models.BooleanField('Is Managed By Admin', default=False)

    #is_for_office_admin = models.BooleanField('Is For Office Admin', default=False)
    def __str__(self):
        return f'{self.company_name} - {self.company_full_name}'

    def __unicode__(self):
        return f'{self.company_name}-{self.company_full_name}'

    class Meta:
        ordering = ['company_name']

class Engineer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    engineer_nickname = models.CharField('Nick Name', max_length=100)
    company = models.ManyToManyField(Company, null=True, blank=True, verbose_name="Company of Engineer")


class SubCompany(models.Model):
    sub_company_name = models.CharField(verbose_name='Sub Company Name', max_length=255,unique=True )
    sub_company_address=models.CharField(verbose_name='Sub Company Address', null=True, blank=True,max_length=500)
    head_company = models.ForeignKey(Company, on_delete=models.CASCADE,verbose_name='Head Company')
    def __str__(self):
        return f'{self.sub_company_name}'
    class Meta:
        ordering = ['sub_company_name']        

# class OfficeAdmin(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
#     admin_nickname= models.CharField('Nick Name',max_length=100)
#
#     company = models.ManyToManyField(Company)
#
#     def __str__(self):
#         return f'{self.admin_nickname} - {self.user.first_name} {self.user.last_name}'
#     class Meta:
#         ordering = ['admin_nickname']

class Customer(models.Model):
    customer_name=models.CharField(verbose_name='Customer Name', max_length=255)


    customer_telephone = models.CharField(verbose_name='Customer Telephone', max_length=255, default='-')
    customer_email = models.CharField(verbose_name='Customer Email', max_length=150, default='-')

    company = models.ForeignKey(Company, on_delete=models.CASCADE,verbose_name='Company')

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update At")

    remark = models.CharField('Remark', max_length=255, null=True, blank=True)

    def __str__(self):
        return  f'{self.customer_name} - {self.company.company_name}'
    class Meta:
        ordering = ['customer_name']

class Product(models.Model):
    product_name=models.CharField('Product-Supporter Name', max_length=255)

    product_telephone = models.CharField('Product-Supporter Telephone', max_length=255, default='-')
    product_email = models.CharField('Product-Supporter Email', max_length=150, default='-')
    #product_email = models.EmailField('Product Supporter Email', max_length=150, default='-')
    customer_company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='customer_company',
                                         verbose_name='Customer-Company')
    partner_company = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='partner_company',verbose_name='Partner-Company')


    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update At")

    remark = models.CharField('Remark', max_length=255, null=True, blank=True)

    def __str__(self):
        return  f'{self.product_name} - {self.partner_company.company_name}'

    class Meta:
        ordering = ['product_name']


class Employee(models.Model):

    employee_name = models.CharField('Name', max_length=150)
    is_team_lead=models.BooleanField(default=False, verbose_name='Is Team Lead')
    is_inactive=models.BooleanField(default=False, verbose_name='Is Not Active(ลาออก)')
    employee_nickname = models.CharField('Nickname', max_length=255, null=True, blank=True)
    employee_telephone = models.CharField('Telephone', max_length=255, null=True, blank=True)
    employee_email = models.EmailField('Email', max_length=150, null=True, blank=True)
    employee_position = models.CharField('Position', max_length=150, null=True, blank=True)

    # employee_team = models.ForeignKey(ServiceTeam, on_delete=models.CASCADE, related_name='employee_team',
    #                                    verbose_name='Employee Team')

    def __str__(self):
        if self.is_team_lead:
         return f'{self.employee_name} {self.employee_nickname}(Lead)'
        else:
         return f'{self.employee_name} {self.employee_nickname}'

    class Meta:
        ordering = ['employee_name']

class Branch(models.Model):
    branch_name = models.CharField('Branch Name', max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    address = models.CharField('Address', null=True, blank=True, max_length=500)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,verbose_name="Customer Support")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update At")

    def __str__(self):
        return f'{self.branch_name} - {self.customer.customer_name}'

    class Meta:
        ordering = ['branch_name']


class DataCenter(models.Model):
    datacenter_name = models.CharField('DataCenter Name', max_length=255)
    address = models.CharField('Address', null=True, blank=True,max_length=500)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,verbose_name="Customer Support")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update At")

    def __str__(self):
        return f'{self.datacenter_name} - {self.customer.customer_name}'

    class Meta:
        ordering = ['datacenter_name']

class Project(models.Model):
    enq_id=models.CharField('ENQ',max_length=100,unique=True)
    project_name=models.CharField('Project Name',max_length=255)

    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    is_dummy=models.BooleanField("Is Dummy" ,default=False)


    project_start = models.DateField( verbose_name= 'Project-Start')
    project_end = models.DateField(verbose_name= 'Project-End')

    customer_po = models.CharField('Cust-PO', max_length=255, null=True, blank=True)
    contract_no = models.CharField('Contract-NO/Reference', max_length=255, null=True, blank=True)

    has_pm=models.BooleanField("Has PM" ,default=False)
    pm_des= models.CharField('PM Des', max_length=255, null=True, blank=True,help_text="Describe detail(if it has PM)")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update At")


    def total_inventories(self):
        return  self.inventory_set.count()
    def total_pm_plans(self):
        return  self.preventivemaintenance_set.count()
    def __str__(self):
        return f'{self.company.company_name} : {self.enq_id}'

    class Meta:
        ordering = ['enq_id']

class Product_Type(models.Model):
    productype_name=models.CharField(max_length=100)
    def __str__(self):
        return self.productype_name

    class Meta:
        ordering = ['productype_name']

class Brand(models.Model):
    brand_name=models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.brand_name

    class Meta:
        ordering = ['brand_name']


class Model(models.Model):
    model_name=models.CharField(max_length=100)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    model_description = models.CharField(max_length=500,default='')
    model_updated_at = models.DateTimeField(auto_now=True, verbose_name="Update At")
    def __str__(self):
        return self.model_name

    class Meta:
        ordering = ['model_name']

class SLA(models.Model):
    sla_name = models.CharField(max_length=100)
    def __str__(self):
            return self.sla_name
class Function(models.Model):
    function_name = models.CharField(max_length=100)
    def __str__(self):
            return self.function_name

    class Meta:
        ordering = ['function_name']

class ServiceTeam(models.Model):
    service_team_name=models.CharField('Service Team Name ',max_length=255)
    service_team_telephone = models.CharField('Service Team Telephone', max_length=255, default='-')
    service_team_email = models.CharField('Service Team Email', max_length=150, default='-')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Company Name')
    def __str__(self):
        return f'{self.service_team_name} - {self.company.company_name}'

    class Meta:
        ordering = ['service_team_name']

class PM_Inventory_Template(models.Model):
    template_file_name = models.CharField(max_length=100,verbose_name='File Name',unique=True)
    template_des = models.CharField(max_length=255, blank=True, null=True,verbose_name='Template Name')
    sample_part_detail= models.JSONField("Sample JSON Format for Part Detail", null=True, blank=True,default={},help_text="default value = {}")
    def __str__(self):
        return self.template_des
class Inventory(models.Model):
    project=models.ForeignKey( Project,on_delete=models.CASCADE,verbose_name='Project')

    serial_number=models.CharField(verbose_name='Serial No',max_length=100,help_text='for no serial , -')
    asset_code = models.CharField(verbose_name='Asset Code', max_length=100, null=True, blank=True)

    quantity=models.PositiveIntegerField(verbose_name="QTY",default=1)

    product_type=models.ForeignKey( Product_Type,on_delete=models.CASCADE,verbose_name='Product Type')
    brand=models.ForeignKey( Brand,on_delete=models.CASCADE,verbose_name='Brand')
    model = models.ForeignKey( Model, on_delete=models.CASCADE,verbose_name='Model')

    # customer_support = models.ManyToManyField(Customer, related_name='customer_support',
    #                                           verbose_name='List Customer Support', blank=True)

    customer_support=models.ForeignKey( Customer,on_delete=models.CASCADE,verbose_name='Customer Support', related_name='customer_support')
    customer_pm_support = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Customer-PM Support',related_name='customer_pm_support',
                                            null=True, blank=True)
    product_support = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product-Partner Support',null=True, blank=True)

    cm_serviceteam = models.ForeignKey(ServiceTeam, on_delete=models.CASCADE, related_name='cm_serviceteam',verbose_name='Yit CM-Team')
    pm_serviceteam= models.ForeignKey(ServiceTeam, on_delete=models.CASCADE,related_name='pm_serviceteam',verbose_name='Yit PM-Team',null=True, blank=True)

    datacenter=models.ForeignKey(DataCenter, on_delete=models.CASCADE,verbose_name='DataCenter')
    branch=models.ForeignKey(Branch, on_delete=models.CASCADE,verbose_name='Branch')

    customer_warranty_start = models.DateField('Cust-Start')
    customer_warranty_end = models.DateField('Cust-End')
    customer_sla = models.ForeignKey(SLA, on_delete=models.CASCADE, related_name='customer_sla',verbose_name='Cust-SLA')

    yit_warranty_start = models.DateField('Yit-Start')
    yit_warranty_end = models.DateField('Yit-End')
    yit_sla = models.ForeignKey(SLA, on_delete=models.CASCADE, related_name='yit_sla',verbose_name='Yit-SLA')

    product_warranty_start = models.DateField('Product-Start')
    product_warranty_end = models.DateField('Product-End')
    product_sla = models.ForeignKey(SLA, on_delete=models.CASCADE, related_name='product_sla',verbose_name='Product-SLA')



    function = models.ForeignKey(Function, on_delete=models.CASCADE, verbose_name='Function',null=True, blank=True)

    building = models.CharField(verbose_name='Building', max_length=100, null=True, blank=True)
    floor = models.CharField('Floor', max_length=30, null=True, blank=True)
    room = models.CharField('Room', max_length=30, null=True, blank=True)
    rack_position = models.CharField('Rack Position', max_length=30, null=True, blank=True)
    rack_unit=models.CharField('Rack Unit',max_length=50, null=True, blank=True)

    devicename_hostname = models.CharField('Device Host Name', max_length=100, null=True, blank=True)
    device_hs_version = models.CharField('Device(HW/OS/SW) Version', max_length=100, null=True, blank=True)

    # update 10/02/23
    firmware_bios_version = models.CharField('HW(Firmware/Bios) Version', max_length=100, null=True, blank=True,help_text="Bios for Server,Firmware for Storage.")
    firmware_bundle_version = models.CharField('Firmware Bundle Version', max_length=100, null=True, blank=True,help_text="HPE=SPP,Dell=SUU,CISCO=HUU")

    hw_management_version = models.CharField('HW Management Version', max_length=100, null=True, blank=True,help_text="ILO Version,IDRAC Version.")
    sw_management_version = models.CharField('SW Management Version', max_length=100, null=True, blank=True,help_text="OVC Version,VDI Version.")


    install_date = models.DateField("Install Date", null=True, blank=True)
    eos_date = models.DateField("EOS Date", null=True, blank=True)

    ip_address=models.GenericIPAddressField('IP Address Management', null=True, blank=True)
    username=models.CharField('User Name Management', max_length=30, null=True, blank=True)
    password=models.CharField('Password Management', max_length=30, null=True, blank=True)

    # update 10/02/23
    ip_address2=models.GenericIPAddressField('IP Address 2', null=True, blank=True)
    username2=models.CharField('Username 2', max_length=30, null=True, blank=True)
    password2=models.CharField('Password 2', max_length=30, null=True, blank=True)
    ip_address3=models.GenericIPAddressField('IP Address 3', null=True, blank=True)
    username3=models.CharField('Username 3', max_length=30, null=True, blank=True)
    password3=models.CharField('Password 3', max_length=30, null=True, blank=True)

    backup_solution=models.CharField('Backup Solution',max_length=255, null=True, blank=True)

    remark = models.TextField('Remark/Note', null=True, blank=True)

    is_dummy = models.BooleanField("Is Dummy", default=False)


    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update At")

    storage_capacity=models.FloatField(verbose_name="Storage Size(TB)",default=0,help_text="If product type is storage,fill in this field")


    pm_inventory_template= models.ForeignKey( PM_Inventory_Template , on_delete=models.CASCADE, verbose_name='PM Template ',null=True, blank=True)

    # part_detail= models.JSONField("Part Detail", default={},help_text="default value = {} ")
    part_detail= models.JSONField("Part Detail", null=True, blank=True,default={},help_text="default value = {}")
    #google-extension :JSON formatter, viewer and URL Encoder tool
    # how to :https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON
    # https://www.w3schools.com/js/js_json_intro.asp
    # develop: https://thispointer.com/how-to-iterate-over-a-json-object-in-python/

    def total_incidents(self):
        return  self.incident_set.count()

    def __str__(self):
        return f'{self.serial_number} - {self.brand.brand_name} - {self.model.model_name}'


class Incident_Severity(models.Model):
    severity_level=models.IntegerField('Severity Level')
    severity_name = models.CharField('Severity Description',max_length=50)

    def __str__(self):
        return f'{self.severity_level}-{self.severity_name}'

class Incident_Status(models.Model):
    incident_status_name=models.CharField('Incident Status',max_length=50)

    def __str__(self):
        return self.incident_status_name

class Incident_Type(models.Model):
    incident_type_name=models.CharField('Incident Type',max_length=150)

    def __str__(self):
        return self.incident_type_name

class Service_Type(models.Model):
    service_type_name=models.CharField('Service Type',max_length=150)

    def __str__(self):
        return self.service_type_name



class Incident(models.Model):
    inventory=models.ForeignKey( Inventory,on_delete=models.CASCADE,verbose_name='Inventory')

    incident_no=models.CharField('Incident-No',max_length=30,unique=True)

    incident_datetime = models.DateTimeField('Incident-Date')
    incident_close_datetime = models.DateTimeField('Incident-Closed-Date', null=True, blank=True,help_text = "For closed status")
    incident_problem_start = models.DateTimeField('Response Date/Time')
    incident_problem_end = models.DateTimeField('Resolved Date/Time', null=True, blank=True)

    incident_owner = models.ForeignKey(Employee,on_delete=models.CASCADE,verbose_name='Engineer Incident Owner' )

    incident_reference_customer_caseNo = models.CharField('Customer Reference Case No.', max_length=150, null=True, blank=True)
    incident_customer_support = models.CharField('Customer Reference(Name,Tel)', max_length=300)


    incident_severity=models.ForeignKey(Incident_Severity,on_delete=models.CASCADE,verbose_name='Severity Level')
    incident_status=models.ForeignKey(Incident_Status,on_delete=models.CASCADE,verbose_name='Status')
    incident_type = models.ForeignKey(Incident_Type, on_delete=models.CASCADE, verbose_name='Incident Type',default=1)
    service_type = models.ForeignKey(Service_Type, on_delete=models.CASCADE, verbose_name='Service Type', default=1)
    incident_subject = models.CharField(verbose_name='Problem Subject', max_length=255)
    incident_description= models.TextField('Problem Description')
    failure_type= models.CharField(verbose_name='Failure Type', max_length=255,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update At")

    def total_details(self):
        return  self.incident_detail_set.count()
    def total_attachd_files(self):
        return  self.files.count()

    def __str__(self):
        return f'{self.incident_no}'
    class Meta:
        ordering = ['-incident_datetime']

#PRIVATE_STORAGE_ROOT = r'\\127.0.0.1\incident_docs'
#private_storage = FileSystemStorage(location=r'\\127.0.0.1\incident_docs')
#x_path = '{0}\{1}{2}\{3}'.format(settings.PRIVATE_STORAGE_ROOT,settings.INCIDENT_PREFIX_DOC, incidentID, incident_filename)
def incident_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/incident_<id>/<filename>
    incidentID=instance.incident_ref.id
    incident_filename= filename
    x_path='{0}{1}/{2}'.format(settings.INCIDENT_PREFIX_DOC, incidentID, incident_filename)
    return (x_path)


class Incident_File(models.Model):
    incident_file = models.FileField('Upload File', upload_to=incident_directory_path, blank=True, max_length=254)
    incident_ref = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='files',blank=True)
    # incident_file = models.FileField('Upload File',upload_to=incident_directory_path,blank=True,max_length=254)
    # incident_file = ContentTypeRestrictedFileField('Upload File', upload_to=incident_directory_path, blank=True, max_length=254,
    #                                                content_types=settings.UPLOAD_FILE_TYPES,max_upload_size=settings.UPLOAD_FILE_MAX_SIZE_MB)
    # incident_file = models.FileField('Upload File', storage=private_storage, blank=True, max_length=254)


class Incident_Detail(models.Model):

    incident_master=models.ForeignKey(Incident,on_delete=models.CASCADE,verbose_name='Incident')
    service_team= models.ForeignKey(ServiceTeam, on_delete=models.CASCADE, verbose_name='Service Team')
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE,verbose_name='Engineer')

    task_start = models.DateTimeField('Task Start Date')
    task_end = models.DateTimeField('Task End Date', null=True, blank=True)
    workaround_resolution = models.TextField('Resolution Description')


    reference_product_caseNo=models.CharField('Reference Case-No', max_length=30, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update At")

    def __str__(self):
        return f'{self.incident_master.incident_no}-{self.service_team.service_team_name}'

    class Meta:
        ordering = ['-task_start']

class XYZ_TestData(models.Model):
   my_title = models.CharField('XYZ Title',max_length=255)
   my_date= models.DateField('XYZ Date')
   my_date_time = models.DateTimeField('XYZ DateTime')


@receiver(post_delete, sender=Incident_File)
def submission_delete(sender, instance, **kwargs):
    instance.incident_file .delete(False)

import datetime

@receiver(post_save, sender=Company)
def add_one_dummy_commpany(sender, instance, **kwargs):

    try:
      if instance.is_customer==True:
        # Invalid operation because  it is not able to handle in case of  chanage name of master company( this first sub is master compnay)
        # but project inventory , both can be handle because there is only one dummy item , but sub compnay , three are more than ones
        # subCompResult = SubCompany.objects.filter(sub_company_name=instance.company_name)
        # if  subCompResult.count()==0:
        #  subComp= SubCompany.objects.create(sub_company_name=instance.company_name,head_company=instance,sub_company_address=instance.company_address)

        # initate proudct type with other and the remaining are yip in soi
        company_name =instance.company_name.strip().lower().replace(' ','_').replace(':','_').replace(',','_').replace('.','_')

        title=f"{settings.DUMMY_CODE}{company_name }"

        projectResults=Project.objects.filter(company__id=instance.id,is_dummy=True)
        dummy_end_date = datetime.datetime.strptime(settings.WARRANTY_EMD_DUMMY_INVENTORY, '%d/%m/%Y')
        dummy_start_date= datetime.datetime.now()
        if projectResults.count()==0:
         project_dummy=Project.objects.create(enq_id=title,project_name=title,customer_po=title
                                              ,company=instance,is_dummy=True,project_start=dummy_start_date,project_end=dummy_end_date)
        else    :
         # update
         projectResults.update(enq_id=title,project_name=title,customer_po=title,project_start=dummy_start_date
                               , project_end=dummy_end_date)
         project_dummy=projectResults[0]

        inventoryReulsts=Inventory.objects.filter(project__company__id=instance.id, is_dummy=True)
        if inventoryReulsts.count()==0:

            dummy_end_date=datetime.datetime.strptime(settings.WARRANTY_EMD_DUMMY_INVENTORY, '%d/%m/%Y')

            inventory_dummy=Inventory.objects.create(
            project=project_dummy,is_dummy=True,
            serial_number=title,product_type=Product_Type.objects.get(id=int(settings.DUMMY_INIT_ID)),
            brand=Brand.objects.get(id=int(settings.DUMMY_INIT_ID)), model=Model.objects.get(id=int(settings.DUMMY_INIT_ID)),
            customer_support_id=int(settings.DUMMY_INIT_ID ),product_support_id=int(settings.DUMMY_INIT_ID ),
            branch_id=   int(settings.DUMMY_INIT_ID ),datacenter_id= int(settings.DUMMY_INIT_ID ),
            quantity=int(settings.DUMMY_INIT_ID), cm_serviceteam_id=int(settings.DUMMY_INIT_ID),
            customer_warranty_start=datetime.datetime.now(), customer_warranty_end=dummy_end_date,customer_sla_id=int(settings.DUMMY_INIT_ID),
            yit_warranty_start=datetime.datetime.now(), yit_warranty_end=dummy_end_date, yit_sla_id=int(settings.DUMMY_INIT_ID),
            product_warranty_start=datetime.datetime.now(), product_warranty_end=dummy_end_date, product_sla_id=int(settings.DUMMY_INIT_ID)
            )
        else:
            # update
            inventoryReulsts.update(serial_number=title)

    except Exception as e:
        raise e


class ReportKeyValueWeight(models.Model):
    key = models.CharField(primary_key=True, max_length=20,verbose_name="Key")
    name = models.CharField(max_length=255, verbose_name="Name")
    weight_value = models.FloatField(verbose_name="Weight Value",help_text="0-100")

    is_used = models.BooleanField(verbose_name="Is Used",default=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update At")

    level1 = models.FloatField(verbose_name="Level 1",help_text=">= value")
    level2 = models.FloatField(verbose_name="Level 2",help_text=">= value")
    level3 = models.FloatField(verbose_name="Level 3",help_text=">= value")
    level4 = models.FloatField(verbose_name="Level 4",help_text=">= value")
    level5 = models.FloatField(verbose_name="Level 5",help_text=">= value")

    class Meta:
        managed = False
        db_table = 'report_key_value_weight'
    def __str__(self):
        return f'{self.name}'

class ReportLevelDefinition(models.Model):
    key = models.CharField(primary_key=True, max_length=20, verbose_name="Key",help_text="it must be exactly identical to the column name in report_key_value_weight table.")
    name = models.CharField(verbose_name="Name",max_length=255 , unique=True)
    level_value = models.IntegerField(verbose_name="Value",help_text="1,2,3 ... in sequence",unique=True)
    class Meta:
        managed = False
        db_table = 'report_level_definition'
    def __str__(self):
        return f'{self.name} - {self.level_value}'


class PreventiveMaintenance(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Project')
    planned_date = models.DateField(verbose_name='PM Plan(Month)',help_text='The first day of the month e.g. 1/12/2022')
    ended_pm_date =models.DateField(verbose_name='End PM(Day)',help_text='The last day of the month e.g. 31/12/2022' )

    postponed_date = models.DateField(verbose_name='Postpone PM', null=True, blank=True)

    remark = models.CharField('PM Period', max_length=255,help_text=' e.g. 1/2 ,2/4')
    team_lead = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='team_lead_engineer' ,
                                          verbose_name='Team Lead')
    engineer = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='operation_engineer',
                                  verbose_name='Engineer ', null=True, blank=True)
  
    customer_company=models.ForeignKey(SubCompany, verbose_name='Customer Company', on_delete=models.CASCADE)

    contact_name = models.CharField('Contact Name', max_length=255,default='')
    contact_telephone = models.CharField('Telephone', max_length=50,default='')
    site_branch = models.CharField('Site/Branch', max_length=255,null=True, blank=True)
    equipment_location=models.CharField('Equipment Location', max_length=255,null=True, blank=True)



    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update At")

    def total_pm_items(self):
        return  self.pm_inventory_set.filter(is_pm=True).count()
    def total_no_pm_items(self):
        return  self.pm_inventory_set.filter(is_pm=False).count()
    def all_pm_items(self):
        return  self.pm_inventory_set.all().count()

class PM_Inventory(models.Model):
    pm_master= models.ForeignKey(PreventiveMaintenance, on_delete=models.CASCADE, verbose_name='PM Master')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, verbose_name='Inventory')

    actual_date = models.DateField(verbose_name='ActualDate To PM', null=True, blank=True) # actually we  performed PM at any given date
    pm_engineer = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='pm_engineer' ,verbose_name='PM Engineer',null=True, blank=True)
    call_number = models.CharField('Call Number', max_length=50, null=True, blank=True)


    document_date = models.DateField(verbose_name='DocumentDate To PM', null=True,
                                     blank=True)  # actually customer accept PM at any given date
    document_engineer = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='document_engineer',
                                          verbose_name='Document Engineer', null=True, blank=True)
    pm_document_number = models.CharField('PM Doc Number', max_length=50, null=True, blank=True)

    remark = models.CharField('Remark', max_length=255, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update At")

    is_pm=models.BooleanField(default=True, verbose_name="Is PM")





# exceptonal case: To add new inventory after create pm plan
@receiver(post_save, sender=Inventory)
def add_new_inventory(sender, instance, created, **kwargs):
   if created:
       project_obj=instance.project
       list_pm=project_obj.preventivemaintenance_set.all()
       if len(list_pm)>0:
           for pm_master_obj in list_pm:
             pm_inventory=PM_Inventory.objects.create(
                inventory=instance, pm_master=pm_master_obj, is_pm=True
            )


class TaskSchedule_PMDoc(models.Model):

    created_date = models.DateTimeField(verbose_name='Create Date')
    complete_date = models.DateTimeField(verbose_name='Complete Date', null=True, blank=True)
    status = models.IntegerField(verbose_name='Status',default=0)  # 0=Pending 1=Complete -1=Error
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Owner')
    pm_id=models.IntegerField(verbose_name='PM ID' )
    file_name=models.CharField(verbose_name='File Name',max_length=255, null=True, blank=True)
    file_password = models.CharField(verbose_name='File Password', max_length=50,null=True, blank=True)

# class InventoryImport_SchemaMapping(models.Model):
#     DisplayName=models.CharField(verbose_name='DisplayName', max_length=50,null=True, blank=True)
#     ColumnName = models.CharField(verbose_name='ColumnName', max_length=50, null=True, blank=True)
# D:\PythonDev\Yit\InventoryImportApp\scripts\InventoryExport_Schema.xlsx


class Prediction_ML_Severity_Incident(models.Model):
    incident=models.ForeignKey(Incident,on_delete=models.CASCADE,verbose_name='Incident ID')
    severity_label = models.IntegerField(verbose_name='Severity Label Prediction')
    severity_name=models.CharField(verbose_name='Severity Label Prediction',max_length=50)
    prediction_at=models.DateTimeField( verbose_name="Prediction At")
    imported_at = models.DateTimeField(verbose_name="Imported At")
    model_version = models.CharField(verbose_name='Model Version', max_length=50,null=True, blank=True)
    def __str__(self):
        return self.severity_name

#class Prediction_ML2_Severity_Incident(models.Model): # Typo
class Prediction_ML2_everity_Incident(models.Model):
    incident=models.ForeignKey(Incident,on_delete=models.CASCADE,verbose_name='Incident ID')
    severity_label = models.IntegerField(verbose_name='Severity Label Prediction')
    severity_name = models.CharField(verbose_name='Severity Label Prediction', max_length=50)
    prediction_at=models.DateTimeField( verbose_name="Prediction At")
    imported_at = models.DateTimeField(verbose_name="Imported At")
    model_version = models.CharField(verbose_name='Model Version', max_length=50)
    def __str__(self):
        return self.severity_label
