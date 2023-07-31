
import os

def create_inventory_data_by_template_type(ivt,pdf_path):
    # general
    item_dict={
        'template_path':os.path.join(pdf_path,ivt.pm_inventory_template.template_file_name),
        'inventory_id':ivt.id,
        'serial_number':ivt.serial_number,
        'brand':ivt.brand.brand_name,
        'model':ivt.model.model_name,
        'product_type':ivt.product_type.productype_name
    }

    if ivt.pm_inventory_template_id==2 : # server
        item_dict['devicename_hostname']=ivt.devicename_hostname \
            if ivt.devicename_hostname is not None else ''
        item_dict['device_hs_version'] = ivt.device_hs_version \
            if ivt.device_hs_version is not None else ''
        item_dict['rack_position'] = ivt.rack_position \
            if ivt.rack_position is not None else ''
        item_dict['rack_unit'] = ivt.rack_unit \
            if ivt.rack_unit is not None else ''

    return  item_dict
