from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime
from django.conf import settings

import os

import random
import pandas as pd
import app.pm_doc_manager.pdf_file_directory_manager as fd_manager

# import uuid
# myuuid = uuid.uuid4()
# print('Your UUID is: ' + str(myuuid))


def create_pdf(report_dict,overview_dict,item_dict_list):


    template_folder_path = os.path.join(settings.STATIC_ROOT, settings.PM_PHYSICAL_TEMPLATE_PATH)
    html_template_path=os.path.join(template_folder_path,settings.PM_OVERVIEW_TEMPLATE)
    css_path=os.path.join(template_folder_path,settings.PM_OVERVIEW_CSS)
    css_item_path=os.path.join(template_folder_path,settings.PM_ITEM_CSS)

    logo_path = os.path.join(template_folder_path, settings.PM_LOGO_IMAGE)

    pdf_path=os.path.join(settings.STATIC_ROOT,settings.PM_PHYSICAL_PDF_PATH)


    def get_content_template(template_fullpath, variable_data_dict):
        try:
            path_name = os.path.split(template_fullpath)
            template_path = path_name[0]
            template_file = path_name[1]
            # print(template_path)
            # print(template_file)

            env = Environment(loader=FileSystemLoader(template_path))
            template = env.get_template(template_file)

            if variable_data_dict is not None:
                output = template.render(variable_data_dict)
            else:
                output = template.render()

            return output

        except Exception as error:
            error_des = f"not found template file {template_fullpath}"
            raise error
    try:
        # create folder to store pm files
        report_time_stamp = report_dict['created_date_str']
        report_name = f"{report_dict['sm_user_name']}_pm{report_dict['pm_id']}_{report_time_stamp}"
        report_path = os.path.join(pdf_path, report_name)
        fd_manager.create_directory(report_path)

        # overview file name
        overview_file = f"{report_dict['enq_id']}.pdf"
        overview = os.path.join(report_path, overview_file)
        overview_dict['Report_Logo']=logo_path

        html_output = get_content_template(html_template_path, overview_dict)
        # print(html_output)
        HTML(string=html_output).write_pdf(overview, stylesheets=[css_path])


        print("Print inventory item")
        i=1

        def collect_intentory_parts_data(parts):
            str_parts={}
            dict_parts={}
            df_parts={}
            for key,value in parts.items():
                if isinstance(value,str):
                 str_parts[key]=str(value)
                elif isinstance(value,dict):
                 dict_parts[key]=value 
                elif isinstance(value,list):
                 df=pd.DataFrame(value)
                 df=df.fillna('')
                 #df_parts[key] = df
                 df.style.set_caption(key)
                 df_parts[key]=df.to_html(header=True, index=False)
                 
            return   str_parts,   dict_parts ,df_parts
        
        for item in item_dict_list:

            prefix_no=str(i).zfill(5)
            # item file name
            item_file = f"{prefix_no}_{item.serial_number}.pdf"
            item_file = item_file.strip().lower()

            inventory_item = os.path.join(report_path, item_file)

            inventory_parts=item.part_detail 
            str_parts,   dict_parts ,df_parts=collect_intentory_parts_data(inventory_parts)

            item_template=os.path.join(template_folder_path,item.pm_inventory_template.template_file_name)
            item_data_dict= {'Report_Logo':logo_path,'Item':item,'StrParts':str_parts,'DictParts':dict_parts,'DataframeParts':df_parts}

            html_output = get_content_template(item_template, item_data_dict)
            #print(html_output)
            HTML(string=html_output).write_pdf(inventory_item, stylesheets=[css_item_path])

            i=i+1

        print("Create Zip to attach file on email")
        zip_file_name = f"{report_name}.zip"
        zip_folder_path = os.path.join(pdf_path, zip_file_name)

        type_to_zip =settings.PM_DOC_FILE_TYPE

        result_zip = fd_manager.make_zip(report_path, type_to_zip, zip_folder_path)
        print(result_zip)


        fd_manager.delete_entire_directory(report_path)


        return zip_file_name,zip_folder_path
    except Exception as error:
        raise  error

    # # Way2: iterate to gen pdf and zip file  and return zip bytes
    # xBytes=HTML(string=html_output).write_pdf(stylesheets=[css_path])
    # return xBytes
