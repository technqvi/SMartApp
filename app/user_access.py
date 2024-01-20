from app.models import *
from django.shortcuts import  get_object_or_404
# https://ridwanray.medium.com/decorators-in-python-68500cf0f746
def check_user_to_do(request,id,operation):
    x_user=request.user
    x_accessible=f'<h2>{x_user} are not authorized to {operation} of this company.</h2><b>Contact administrator to add this user to the manager OR engineer table in company</b>'
    if operation in ["UpdatePMItem","DeletePM","CopyPM"]: # pm_id
        obj = get_object_or_404(PreventiveMaintenance, pk=id)
        if obj.project.company.manager.filter(user_id=x_user.id).exists()  \
            or obj.project.company.engineer_set.filter(user_id=x_user.id).exists():
            x_accessible=None
    elif operation  in ["UpdateInventory","DeleteInventory","ChangeInventory","AddIncident"]:  # inventory_id
        obj=get_object_or_404(Inventory,pk=id)
        if obj.project.company.manager.filter(user_id=x_user.id).exists():
            x_accessible = None
    elif operation in ["UpdateIncident","DeleteIncident","UpdateDetail"]: # incident_id
        obj=get_object_or_404(Incident,pk=id)
        if obj.inventory.project.company.manager.filter(user_id=x_user.id).exists():
            x_accessible = None
    # improve 20024
    elif operation in ["AddInventory","ManageProject","AddPM"]:  # project_id
        # obj = get_object_or_404(Project, pk=id)
        obj = Project.objects.select_related("company").get(pk=id)
        if obj.company.manager.filter(user_id=x_user.id).exists():
            return obj
        else:
            return False

    elif operation in ["UpdateDetail","DeleteDetail"]:
        obj = get_object_or_404(Incident_Detail, pk=id)
        if obj.incident_master.inventory.project.company.manager.filter(user_id=x_user.id).exists():
            x_accessible = None

    return x_accessible