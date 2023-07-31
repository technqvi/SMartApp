from django.shortcuts import  get_object_or_404, render
from app.models import *
import os

from django.core.mail import BadHeaderError
from django.core.mail import EmailMessage
from django.http import HttpResponse

import pandas as pd
import app.pm_doc_manager.pdf_creator as xyz_pdf
import app.pm_doc_manager.pdf_file_directory_manager as fd_manager
import app.pm_doc_manager.data_template_mapper as data_mapper

import app.utility as util

pdf_path = os.path.join(settings.STATIC_ROOT, settings.PM_PHYSICAL_TEMPLATE_PATH)
def send_mail_pm_doc(email_info):
    try:
         email = EmailMessage(
                email_info['subject'],
                email_info['message'],
                'smartapp-service@yipintsoigroup.com',
                email_info['send_to']
            )

         email.send()
    except BadHeaderError as ex:
        raise ex
    return True


def process_pm_doc_task():

    list_task=TaskSchedule_PMDoc.objects.filter(status=0)
    for task in list_task:
      try:
        id=task.pm_id

        user=task.owner
        user_email = user.email
        user_name=user.username.replace(settings.YIP_DOMAIN_NAME,'')

        created_date=task.created_date.strftime('%d%m%y-%H%M%S')

        pm_obj = get_object_or_404(PreventiveMaintenance, pk=id)

        enq_id=  pm_obj.project.enq_id.replace('/','')
        report_data = {'sm_user_name': user_name, 'pm_id': pm_obj.id,'enq_id':enq_id,'created_date_str':created_date}

        item_vals_overview = []
        item_inventories = []
        inventoryPMList = pm_obj.pm_inventory_set.filter(is_pm=True)
        for item in inventoryPMList:
                # add inventory to PM Summary docuement(overview pdf)
                item_vals_overview.append([
                                  item.inventory.brand.brand_name,
                                  item.inventory.model.model_name,
                                  item.inventory.serial_number
                ])

                # item_dict = data_mapper.create_inventory_data_by_template_type(item.inventory,pdf_path) # deprecated
                # check whether exists template to create PDF file
                if item.inventory.pm_inventory_template is not None:
                 item_inventories.append(item.inventory)

        # create datafraome to Table in PM Summary document
        overview_pm_items_df = pd.DataFrame(data=item_vals_overview, columns=['Brand', 'Model','Serial'])
        overview_pm_items_df = overview_pm_items_df.reset_index(level=0,drop=False)
        overview_pm_items_df.rename(columns={"index": "RowNumber"}, inplace=True)
        overview_pm_items_df['RowNumber'] = overview_pm_items_df['RowNumber'] + 1
        overview_pm_items_df=overview_pm_items_df[['RowNumber','Brand', 'Model','Serial']]

        overview_dict = {'PMInfo': pm_obj , 'PMItemList': overview_pm_items_df}
        zip_file_name,zip_report_path = xyz_pdf.create_pdf(report_data, overview_dict, item_inventories)


        zip_report_target_path=os.path.join(settings.PM_DOC_FILE_LOCAL_PATH, zip_file_name)

        url_for_zip_download=f"{settings.PM_DOC_FILE_HTTP_PATH}/{zip_file_name}"
        fd_manager.move_file(zip_report_path, zip_report_target_path)

        mdate = datetime.datetime.fromtimestamp(os.path.getmtime(zip_report_target_path))
        expiration_doc_date=mdate + datetime.timedelta(hours=settings.PURGE_DOC_HOUR_PERIOD)



        content=f'<a href="{url_for_zip_download}"  target="_blank"><h1>Click To Download PM Document</h1></a><br>'
        content += f"This file will expire in {expiration_doc_date.strftime('%d %b %Y %H:%M')}"
        title=f'SmartPM-Doc: {pm_obj.project.enq_id} - PM{id} '
        email_info={'subject':title ,'message':content,'send_to':[user_email]}

        is_sussessful = send_mail_pm_doc(email_info)
        #is_sussessful=True

        if is_sussessful:
            task.complete_date=datetime.datetime.now()
            task.status=1
            task.file_name= zip_file_name
            task.save()

      except Exception as ex:
        error_msg=f"{task.owner} - {task.pm_id} - {task.created_date} | {str(ex)}"
        task.status = -1
        task.save()
        util.add_error_to_file(error_msg)

    return True


def delete_pm_doc_task():
    folder_path = settings.PM_DOC_FILE_LOCAL_PATH
    list_ext = settings.PURGE_FILE_TYPE
    xperiod_to_purge = settings.PURGE_DOC_HOUR_PERIOD
    second_to_hour = 60 * 60

    now_date = datetime.datetime.now()
    print(now_date)

    fileList = os.listdir(folder_path)

    for file in fileList:
        for ext in list_ext:
            if file.endswith(ext):
                file_path = os.path.join(folder_path, file)
                file_name= os.path.basename(file_path)
                mdate = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                # diff_day=(now_date - mdate).days
                diff_day = (now_date - mdate).total_seconds() / (second_to_hour)
                # print(f"{file_path} - {mdate} - {diff_day}")
                if diff_day > xperiod_to_purge:
                    os.remove(file_path)
                    TaskSchedule_PMDoc.objects.filter(file_name=file_name).delete()
                    print(f'Delete file and transaction record : {file_name} : {diff_day} days')
                else:
                    print(f'Not time to delete file : {file_name} : {diff_day} days')





