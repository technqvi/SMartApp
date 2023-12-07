from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views,views_report,views_pm
from .pm_doc_manager import pm_doc_builder

# from . import views_api

urlpatterns = [

    path('search/', views_report.search_entry, name='search_entry'),
    path('search/result/<int:incident_id>/',views_report.search_result,name='search_result'),

    path('projects/', views.manage_project, name='manage_project'),
    path('projects/<int:id>/', views.manage_project, name='manage_project'),
    path('projects/delete_project/<int:id>/', views.delete_project, name='delete_project'),
    path('projects/<int:proj_id>/add_inventory/', views.add_inventory, name='add_inventory'),
    path('projects/<int:proj_ref_id>/copy_inventory/', views.copy_inventoryList_by_existingProject,
         name='copy_inventory'),

    path('inventories/', views.manage_inventory, name='manage_inventory'),
    path('inventories/update_inventory/<int:id>/', views.update_inventory, name='update_inventory'),
    path('inventories/<int:inventory_id>/add_incident', views.add_incident, name='add_incident'),
    path('inventories/delete_inventory/<int:id>/', views.delete_inventory, name='delete_inventory'),


    path('incidents/', views.manage_incident, name='manage_incident'),

    path('incidents/update_incident/<int:id>/', views.update_incident, name='update_incident'),
    path('incidents/<int:incident_id>/manage_incident_detail/<int:id>/', views.manage_incident_detail, name='manage_incident_detail'),

    path('incidents/<int:id>/change_inventory/<int:inventory_id>/', views.change_inventory_for_incident, name='change_inventory_for_incident'),
    path('incidents/delete_incident/<int:id>/', views.delete_incident, name='delete_incident'),
    path('incidents/delete_incident_detail/<int:id>/', views.delete_incident_detail, name='delete_incident_detail'),
    path('incidents/delete_incident_file/<int:id>/',views.delete_incident_file,name='delete_incident_file'),

    path('import_models/', views.import_models, name='import_models'),
    path('import_models/download_template/',views.create_model_template,name='do_modeltemplate'),
    path('import_models/upload_models/',views.upload_models_template,name='upload_models_template'),


    path('site_manager/<int:support_type>/supporter/<int:id>/', views.manage_supporter,
         name='manage_supporter'),
    path('site_manager/branch/<int:id>/', views.manage_branch,
         name='manage_branch'),
    path('site_manager/datacenter/<int:id>/', views.manage_datacenter,
         name='manage_datacenter'),

    path('pm/<int:project_id>/<int:id>/', views_pm.manage_pm, name='manage_pm'),
    path('pm/<int:pm_id>/inventory/<int:id>/', views_pm.update_pm_inventory, name='update_pm_inventory'),
    path('pm/delete_pm/<int:id>/', views_pm.delete_pm, name='delete_pm'),
    path('pm/pm_copy_inventory/<int:pm_id>/', views_pm.copy_pm_inventory, name='copy_pm_inventory'),

    path('pm/pdf/<int:id>/', views_pm.build_weasyprint_pm_doc_pdf, name='build_pdf_pm_doc'),
    path('pm/task/', views_pm.run_process_pm_doc_task, name='run_process_pm_doc_task'),

    path('pm/pm_report', views_pm.report_pm, name='report_pm'),
    path('pm/template/',views.list_inventory_template_for_pm,name='inventory_template'),

    path('report/site-grade/', views_report.report_site_grade, name="report_site_grade"),
    path('report/advance-report/', views_report.build_ais_excel_report, name='build_ais_excel_report'),

    path('report/export_project/', views.export_project, name='export_project'),
    path('report/export_all_project/', views.export_all_project, name='export_all_project'),
    path('report/export_inventory/', views.export_inventory, name='export_inventory'),
    path('report/export_incident/', views.export_incident, name='export_incident'),
    path('report/export_pm_plan/', views_pm.export_pm_plan, name='export_pm_plan'),
    path('report/export_pm_item/', views_pm.export_pm_item, name='export_pm_item'),
    path('report/summarize_project_pm', views_pm.summarize_project_pm, name='summarize_project_pm'),
    path('report/summarize_all', views_pm.summarize_all, name='summarize_all'),
    # path('report/export_none_pm_inventory', views_pm.export_none_pm_inventory, name='export_none_pm_inventory'),


    path('ajax/load-models/', views.load_models_by_brand, name='ajax_load_models'),
    path('ajax/load-customers/', views.load_customers_support_by_company, name='ajax_load_customers'),


    path('manage_sm/', views.manage_sm, name='manage_sm'),

    path('xyz/<int:id>/', views.manage_xyz, name='manage_xyz'),
    path('xyz/', views.manage_xyz, name='manage_xyz'),

]

# it cause to be inaccessible throuh admin page
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)