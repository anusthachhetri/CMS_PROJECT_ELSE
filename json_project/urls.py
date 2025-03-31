"""
URL configuration for json_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('json_app.urls')),
# ]
from django.contrib import admin
from django.urls import path, include
from json_app import views  # Import views from your app
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
  path('admin/', admin.site.urls),
  path('upload/', views.upload_json, name='upload_json'),
  path('getdata/', views.getdata, name='getdata'),  # Add this line for the get-json-files view
  path('update/', views.update_json, name='update_json'),
  path('download/<str:batch_id>/', views.download_json, name='download_json'),
  path('', views.home, name='home'),  # Add this line to set the home view for the root URL
  path('view/<str:batch_id>/', views.view_json, name='view_json'),  # Add this line
  path('upload-source-metadata/', views.upload_source_metadata, name='upload_source_metadata'),
  path('view_source_metadata/', views.view_source_metadata, name='view_source_metadata'),  # Home page to view data
  #new 
  path('edit-source-metadata/<str:metadata_id>/', views.edit_source_metadata, name='edit_source_metadata'),
 
 
 
  path('funding_body/', views.funding_body, name='funding_body'),
  path('opportunity/', views.opportunity, name='opportunity'),
  path('awards/', views.awards, name='awards'),
 
 
 
   #only respective data urls
  path('funding_body_view/', views.funding_body_view, name='funding_body_view'),
  path('award_view/', views.award_view, name='award_view'),
  path('opportunity_view/',views.opportunity_view, name='opportunity_view'),
  
  
  
  #ingestion view path
  # path('ingestion_template/', views.file_ingestion, name='file_ingestion'),
  path('ingestion_template/', views.file_ingestion, name='ingestion_template'),
 
  # path('ingestion/', views.file_ingestion, name='file_ingestion'),

  #path('manage-files/', views.manage_files, name='manage_files'),
   #   path('updated-files/', views.updated_files, name='updated_files'),
  
  
  
 #date 15/01/2025
          # path('admin/', admin.site.urls),
          # path('accounts/', include('allauth.urls')), 
          
          
  #new links
  path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   
  # Include allauth URLs
  path('accounts/', include('allauth.urls')),
   
  path('dashboard/', views.dashboard_view, name='dashboard'), 
   
  path('qa-checklist/', views.qa_checklist, name='qa_checklist'),
    
  path('toolbox/', views.toolbox, name='toolbox'),  # Toolbox page URL
   
  path('pdf-viewer/', views.pdf_viewer, name='pdf_viewer'),
   
   
  path('upload_file/', views.upload_file, name='upload_file'), #route for json creater
    
    
  path("qa_process/", views.qa_process, name="qa_process"),  #QA PROCESS
     
  # path("qa_process/", views.vtooltemp, name="vtooltemp"),  #V TOOL 
    
  path('run_java_tool/', views.run_java_tool, name='run_java_tool'),
  path('toolbox/', include('json_app.urls')),
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

# # json_project/urls.py
# from django.contrib import admin
# from django.urls import path, include
# from json_app import views  # Add this import to use views in the URL patterns

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('upload-json/', include('json_app.urls')),  # Include app-specific URLs
#     path('', views.home, name='home'),  # Route the root URL to the home view
# ]


