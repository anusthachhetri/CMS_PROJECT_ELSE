# from django.urls import path
# from . import views

# urlpatterns = [
#    path('upload/', views.upload_json, name='upload_json'),
#    path('getdata/', views.getdata, name='getdata'),  # Add this line
#     path('update/', views.update_json, name='update_json'),
#    path('download/<str:batch_id>/', views.download_json, name='download_json'),
   
  
#  ]
###############################


#################
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('upload-json/', views.upload_json, name='upload_json'),
# ]



# # json_app/urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('upload/', views.upload_json, name='upload_json'),
# ]


from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import scraper_view
from django.urls import include, path
from .views import web_scraper_view

from .views import asjc_matcher_view

from .views import csv_validator_view

from .views import scrapper_views, download_csv

# from .views import json_validator_view
from .views import user_list
from .views import ingestion_prod
from .views import ingestion_main_temp
from .views import ingestion_logs_view
from .views import ingest_prod_view





urlpatterns = [
  
  
    path('update_json/', views.update_json, name='update_json'), 
    path('getdata/', views.getdata, name='getdata'),
    
    path('upload/', views.upload_json, name='upload_json'),
     
    path('view/<str:batch_id>/', views.view_json, name='view_json'),
    path('download/<str:batch_id>/', views.download_json, name='download_json'),
    
    path('upload-source-metadata/', views.upload_source_metadata, name='upload_source_metadata'),
     
    path('view_source_metadata/', views.view_source_metadata, name='view_source_metadata'),  # Home page to view data
    #new for edit source metadata
    path('edit-source-metadata/<str:metadata_id>/', views.edit_source_metadata, name='edit_source_metadata'),
      
      
      
    path('funding_body/', views.funding_body, name='funding_body'),
    path('opportunity/', views.opportunity, name='opportunity'),
    path('awards/', views.awards, name='awards'),
      
    #only respective data urls
    path('funding_body_view/', views.funding_body_view, name='funding_body_view'),
    path('award_view/', views.award_view, name='award_view'),
    path('opportunity_view/', views.opportunity_view, name='opportunity_view'),
          
       
    
          
          
          
          
          
    #ingestion view path
    # path('ingestion_template/',views.file_ingestion, name='file_ingestion'),
    path('ingestion_template/', views.file_ingestion, name='ingestion_template'),
    # path('ingestion/', views.file_ingestion, name='file_ingestion'),
          
          
          
    #date 15/01/2025
    # path('admin/', admin.site.urls),
    # path('accounts/', include('allauth.urls')), 
               

    # path('manage-files/', views.manage_files, name='manage_files'),
    # path('updated-files/', views.updated_files, name='updated_files'),
    
   
   
    #new links
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   
    # Include allauth URLs
    path('accounts/', include('allauth.urls')),
    
    path('dashboard/', views.dashboard_view, name='dashboard'),
     
    path('qa-checklist/', views.qa_checklist, name='qa_checklist'),
      
    path('toolbox/', views.toolbox, name='toolbox'),  # Toolbox page URL
      
      
      
      
    path('pdf-viewer/', views.pdf_viewer, name='pdf_viewer'),
      
    path('upload_file/', views.upload_file, name='upload_file'),
     
     
     

    path('scraper/', scraper_view, name='scraper_tool'),
     
    path('web-scraper/', web_scraper_view, name='web_scraper_tool'),
      
    path('asjc-matcher/', asjc_matcher_view, name='asjc_matcher'),
       
    path("csv-validator/", csv_validator_view, name="csv_validator"),
       
    path("selenium_scrapper/", scrapper_views, name="selenium_scrapper"),
    path("selenium_scrapper/download-csv/", download_csv, name="download_csv"),   
       
    # path("json-validator/", json_validator_view, name="json_validator"),
    
    
      
    path('users/', user_list, name='user_list'),

    path('ingestemp_prod/', ingestion_prod, name='ingestemp_prod'),
    
    path('ingestion_main/', ingestion_main_temp, name='ingestion_main'),
    path('ingestion-logs/', ingestion_logs_view, name='ingestion_logs'),

    path('ingest_prod_logs/', ingest_prod_view, name='ingest_prod_logs'),


]




# path('view/<str:batch_id>/', views.view_file, name='view_json'),  # View JSON content
#     path('download/<str:batch_id>/', views.download_file, name='download_json'),  # Download JSON file
# ]