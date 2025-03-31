import json
import uuid
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from pymongo import MongoClient

from .models import JSONFile
from django.http import HttpResponse
from django.urls import reverse
from bson.json_util import dumps
from urllib.parse import quote_plus
import datetime


#adding home view 
from django.shortcuts import render
def home(request):
    return render(request, 'home.html')  # for our home template



#view for funding body /award/opportunity
from django.shortcuts import render

# def funding_body(request):
#     return render(request, 'funding_body.html')
def funding_body(request):
    return render(request, 'funding_body.html')
    # Replace this with your dynamic URL
    # external_url = "http://fa-macmillanlearning.highwire.org:8501/"
    # return render(request, 'funding_body.html', {'external_url': external_url})

def opportunity(request):
    return render(request, 'opportunity.html')

def awards(request):
    return render(request, 'awards.html')

#############QA PROCESS ######################
######QA  Page Render #############
def qa_process(request):
    return render(request, "qa_process.html")




#QA checklist##############################
#################################

def qa_checklist(request):
    return render(request, 'qa_checklist.html')



##########################end############################

#######url for toolbox##########
# def toolbox(request):
#       # return render(request, 'toolbox.html')
#       external_url = "http://fa-macmillanlearning.highwire.org:8502/"
     
    
#       return render(request, 'toolbox.html', {'external_url': external_url})
#updated code
def toolbox(request):
    # External URLs
    external_url_1 = "http://fa-macmillanlearning.highwire.org:8502/"
    external_url_2 = "http://fa-macmillanlearning.highwire.org:8501/"
    external_url_3 =  "http://fa-macmillanlearning.highwire.org:8503/"

    external_url_4 =  "http://fa-macmillanlearning.highwire.org:8504/"

    # Pass these external URLs to the template
    return render(request, 'toolbox.html', {
        'external_url_1': external_url_1,
        'external_url_2': external_url_2,
        'external_url_3': external_url_3,
        'external_url_4': external_url_4,
        
    })




from django.shortcuts import render
from django.templatetags.static import static

def pdf_viewer(request):
    """Renders the UI with the embedded PDF."""
    pdf_path = static("pdfs/Funding_Body.pdf")  # Adjust the path as needed
    return render(request, 'pdf_viewer.html', {'pdf_path': pdf_path})



# MongoDB setup
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['test']
collection = db['Elsevier_Batch']









# #upload json code for storing json data in mongodb
# def upload_json(request):
#     if request.method == 'POST':
#         # Access uploaded files
#         json_files = request.FILES.getlist('files')
#         if not json_files:
#             return JsonResponse({'error': 'No files uploaded'}, status=400)

#         response_data = []

#         try:
#             for json_file in json_files:
#                 try:
#                     # Load JSON content from the file
#                     json_data = json.load(json_file)
#                 except json.JSONDecodeError:
#                     response_data.append({
#                         'file': json_file.name,
#                         'status': 'error',
#                         'message': 'Invalid JSON format'
#                     })
#                     continue

#                 # Extract the batchId (for camelCase) or batch_id (for snake_case)
#                 batch_id = None
#                 if isinstance(json_data, list) and json_data:
#                     batch_id = json_data[0].get('batchId') or json_data[0].get('batch_id')
#                 elif isinstance(json_data, dict):
#                     batch_id = json_data.get('batchId') or json_data.get('batch_id')

#                 # Check if batch_id is found
#                 if not batch_id:
#                     response_data.append({
#                         'file': json_file.name,
#                         'status': 'error',
#                         'message': 'batchId or batch_id not found in the JSON file. Ensure "batchId" exists in the JSON object or list items.'
#                     })
#                     continue

#                 # Save metadata to the model
#                 JSONFile.objects.create(
#                     batch_id=batch_id,
#                     file_name=json_file.name,
#                     version=1
#                 )

#                 # Insert JSON data into MongoDB
#                 if isinstance(json_data, list):
#                     for item in json_data:
#                         item['batchId'] = batch_id  # Ensure batchId consistency in MongoDB
#                     collection.insert_many(json_data)
#                 else:
#                     json_data['batchId'] = batch_id  # Ensure batchId consistency in MongoDB
#                     collection.insert_one(json_data)

#                 # Append success response for the current file
#                 response_data.append({
#                     'file': json_file.name,
#                     'status': 'success',
#                     'batchId': batch_id
#                 })

#             return JsonResponse({'message': 'Files processed', 'details': response_data})

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     # Render the upload template for non-POST requests
#     return render(request, 'upload.html')

############code for uploading data into database
########################################################################

# def upload_json(request):
#     if request.method == 'POST':
#         # Access uploaded files
#         json_files = request.FILES.getlist('files')
#         if not json_files:
#             return JsonResponse({'error': 'No files uploaded'}, status=400)

#         response_data = []

#         try:
#             for json_file in json_files:
#                 try:
#                     # Load JSON content from the file
#                     json_data = json.load(json_file)
#                 except json.JSONDecodeError:
#                     response_data.append({
#                         'file': json_file.name,
#                         'status': 'error',
#                         'message': 'Invalid JSON format'
#                     })
#                     continue

#                 # Extract the batchId (for camelCase) or batch_id (for snake_case)
#                 batch_id = None
#                 if isinstance(json_data, list) and json_data:
#                     batch_id = json_data[0].get('batchId') or json_data[0].get('batch_id')
#                 elif isinstance(json_data, dict):
#                     batch_id = json_data.get('batchId') or json_data.get('batch_id')

#                 # Check if batch_id is found
#                 if not batch_id:
#                     response_data.append({
#                         'file': json_file.name,
#                         'status': 'error',
#                         'message': 'batchId or batch_id not found in the JSON file. Ensure "batchId" exists in the JSON object or list items.'
#                     })
#                     continue

#                 # Check if batchId already exists in MongoDB
#                 existing_record = collection.find_one({'batchId': batch_id})
#                 if existing_record:
#                     response_data.append({
#                         'file': json_file.name,
#                         'status': 'error',
#                         'message': f'File with batchId {batch_id} already exists in the database.'
#                     })
#                     continue

#                 # Save metadata to the model (using Django ORM)
#                 JSONFile.objects.create(
#                     batch_id=batch_id,
#                     file_name=json_file.name,
#                     version=1
#                 )

#                 # Insert JSON data into MongoDB
#                 if isinstance(json_data, list):
#                     for item in json_data:
#                         item['batchId'] = batch_id  # Ensure batchId consistency in MongoDB
#                     collection.insert_many(json_data)
#                 else:
#                     json_data['batchId'] = batch_id  # Ensure batchId consistency in MongoDB
#                     collection.insert_one(json_data)

#                 # Append success response for the current file
#                 response_data.append({
#                     'file': json_file.name,
#                     'status': 'success',
#                     'batchId': batch_id
#                 })

#             return JsonResponse({'message': 'Files processed', 'details': response_data})

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     # Render the upload template for non-POST requests
#     return render(request, 'upload.html')


def upload_json(request):
    if request.method == 'POST':
        uploader_name = request.POST.get('uploader_name')  # Retrieve the uploader's name
        file_type = request.POST.get('file_type')  # Retrieve the file type
        json_files = request.FILES.getlist('files')  # Get the list of uploaded files
 
        if not uploader_name or not file_type or not json_files:
            return JsonResponse({'error': 'Uploader name, file type, and files are required.'}, status=400)
 
        response_data = []
 
        try:
            for json_file in json_files:
                try:
                    # Load JSON content from the file
                    json_data = json.load(json_file)
                except json.JSONDecodeError:
                    response_data.append({
                        'file': json_file.name,
                        'status': 'error',
                        'message': 'Invalid JSON format'
                    })
                    continue
 
                # Extract batchId and other IDs from JSON
                batch_id = None
                funding_body_id = None
                grant_award_id = None
                grant_opportunity_id = None
                ingestion_id = None
                unique_grant_id = None
 
                if isinstance(json_data, list) and json_data:
                    batch_id = json_data[0].get('batchId') or json_data[0].get('batch_id')
                    funding_body_id = json_data[0].get('fundingBodyId')
                    grant_award_id = json_data[0].get('grantAwardId')
                    grant_opportunity_id = json_data[0].get('grantOpportunityId')
                    ingestion_id = json_data[0].get('ingestionId')
                elif isinstance(json_data, dict):
                    batch_id = json_data.get('batchId') or json_data.get('batch_id')
                    funding_body_id = json_data.get('fundingBodyId')
                    grant_award_id = json_data.get('grantAwardId')
                    grant_opportunity_id = json_data.get('grantOpportunityId')
                    ingestion_id = json_data.get('ingestionId')
 
                # If batch_id or ingestion_id is not found, return an error
                if not batch_id:
                    response_data.append({
                        'file': json_file.name,
                        'status': 'error',
                        'message': 'batchId or batch_id not found in the JSON file.'
                    })
                    continue
 
                if not ingestion_id:
                    response_data.append({
                        'file': json_file.name,
                        'status': 'error',
                        'message': 'ingestionId not found in the JSON file.'
                    })
                    continue
 
                # If none of the three IDs (fundingBodyId, grantAwardId, grantOpportunityId) is found, return error
                if not (funding_body_id or grant_award_id or grant_opportunity_id):
                    response_data.append({
                        'file': json_file.name,
                        'status': 'error',
                        'message': 'At least one of the following must be present: fundingBodyId, grantAwardId, or grantOpportunityId.'
                    })
                    continue
 
                # Determine which ID to use for the unique_grant_id field (store only one)
                if funding_body_id:
                    unique_grant_id = funding_body_id
                elif grant_award_id:
                    unique_grant_id = grant_award_id
                elif grant_opportunity_id:
                    unique_grant_id = grant_opportunity_id
 
                # Check for existing record in Django ORM based on batchId
                if JSONFile.objects.filter(batch_id=batch_id).exists():
                    response_data.append({
                        'file': json_file.name,
                        'status': 'error',
                        'message': f'A file with batchId {batch_id} already exists in the database.'
                    })
                    continue
 
                # Save metadata using Django ORM (Ingestion ID is used as the primary key)
                JSONFile.objects.create(
                    ingestion_id=ingestion_id,  # Ingestion ID as primary key
                    uploader_name=uploader_name,
                    file_name=json_file.name,
                    file_type=file_type,
                    version=1,
                    batch_id=batch_id,  # batchId for uniqueness check
                    unique_grant_id=unique_grant_id  # Store one of the IDs: fundingBodyId, grantAwardId, or grantOpportunityId
                )
 
                # Insert JSON data into MongoDB
                if isinstance(json_data, list):
                    for item in json_data:
                        item['batchId'] = batch_id  # Ensure batchId consistency
                        item['ingestionId'] = ingestion_id  # Ensure ingestionId consistency
                        # Avoid adding uniqueGrantId to the actual JSON data
                    collection.insert_many(json_data)
                else:
                    json_data['batchId'] = batch_id
                    json_data['ingestionId'] = ingestion_id  # Ensure ingestionId consistency
                    # Avoid adding uniqueGrantId to the actual JSON data
                    collection.insert_one(json_data)
 
                # Append success response
                response_data.append({
                    'file': json_file.name,
                    'status': 'success',
                    'batchId': batch_id,
                    'uniqueGrantId': unique_grant_id
                })
 
            return JsonResponse({'message': 'Files processed', 'details': response_data})
 
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
 
    # Render the upload template for non-POST requests
    return render(request, 'upload.html')

############################ending uplaod json file in db ##########################################################################
###################################################################################################################################



###########################code for view data in table view that is uplaoded by user##################################################################
###########################################################################################################################################
# from django.shortcuts import render
# from django.http import HttpResponse
# from django.urls import reverse
# from datetime import datetime, timedelta
# from .models import JSONFile

# def getdata(request):
#     try:
#         # Fetch date filters from the request
#         start_date = request.GET.get('start_date')
#         end_date = request.GET.get('end_date')

#         # Filter metadata based on date range
#         metadata = JSONFile.objects.all()

#         if start_date:
#             try:
#                 start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
#                 metadata = metadata.filter(uploaded_at__gte=start_date_obj)
#             except ValueError:
#                 return HttpResponse("Invalid start date format. Use YYYY-MM-DD.", status=400)

#         if end_date:
#             try:
#                 end_date_obj = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
#                 metadata = metadata.filter(uploaded_at__lte=end_date_obj)
#             except ValueError:
#                 return HttpResponse("Invalid end date format. Use YYYY-MM-DD.", status=400)

#         # Start building the metadata table
#         metadata_table = """
#         <h1 style="background-color:#f5a142; height: 50px; color: white; text-align: center; z-index: 1000; position: fixed; width: 100%; margin: 0; top: 0; left: 0;">Metadata Table</h1>
#         <div style="margin-top: 60px; padding: 10px; background-color: #f5a142; text-align: right; margin-right: 20px;">
#             <form method="get" style="display: flex; align-items: center; justify-content: flex-end; gap: 15px;">
#                 <h4 style="margin: 0; color: white;">Search Data</h4>
#                 <div>
#                     <label for="start_date" style="margin-right: 5px; color: white;">Start Date:</label>
#                     <input type="date" id="start_date" name="start_date" value="{start_date or ''}" class="filter-input">
#                 </div>
#                 <div>
#                     <label for="end_date" style="margin-right: 5px; color: white;">End Date:</label>
#                     <input type="date" id="end_date" name="end_date" value="{end_date or ''}" class="filter-input">
#                 </div>
#                 <button type="submit" class="filter-btn">Filter</button>
#             </form>
#         </div>
#         <table border="1" style="width: 100%; border-collapse: collapse; margin-top: 20px;">
#             <thead>
#                 <tr>
#                     <th>Sr. No</th>
#                     <th>MPS Id</th>
#                     <th>Uploader Name</th>
#                     <th>File Name</th>
#                     <th>File Type</th>
#                     <th>Version</th>
#                     <th>Uploaded At</th>
#                     <th>View File</th>
#                     <th>Download File</th>
#                 </tr>
#             </thead>
#             <tbody>
#         """

#         for idx, file in enumerate(metadata, start=1):
#             batch_id = file.batch_id
#             uploader_name = file.uploader_name
#             file_type = file.file_type
#             view_url = reverse('view_json', args=[batch_id])
#             download_url = reverse('download_json', args=[batch_id])

#             metadata_table += f"""
#             <tr>
#                 <td>{idx}</td>
#                 <td>{file.batch_id}</td>
#                 <td>{uploader_name}</td>
#                 <td>{file.file_name}</td>
#                 <td>{file_type}</td>
#                 <td>{file.version}</td>
#                 <td>{file.uploaded_at}</td>
#                 <td>
#                     <a href="{view_url}" style="text-decoration: none; color: blue;">View</a>
#                 </td>
#                 <td>
#                     <a href="{download_url}" style="text-decoration: none; color: green;">Download</a>
#                 </td>
#             </tr>
#             """
#         metadata_table += "</tbody></table>"

#         # Combine and return the complete HTML response
#         html_response = f"""
#         <html>
#         <head>
#             <title>Data Table</title>
#             <style>
#                 table {{ border: 1px solid black; border-collapse: collapse; width: 100%; background-color: #ffffff; }}
#                 th, td {{ padding: 10px; text-align: left; border: 1px solid black; background-color: #ffffff; border: 1px solid #ddd; }}
#                 th {{ background-color:#f5a142; color: white; }}

#                 .filter-input, .filter-btn {{
#                     padding: 8px 15px;
#                     border-radius: 5px;
#                     border: 1px solid #f5a142;
#                     font-size: 14px;
#                 }}

#                 .filter-input {{
#                     background-color: white;
#                     color: #333;
#                     transition: background-color 0.3s ease;
#                 }}

#                 .filter-input:hover {{
#                     background-color: #f5a142;
#                     color: white;
#                 }}

#                 .filter-btn {{
#                     background-color: #f5a142;
#                     color: white;
#                     border: none;
#                     cursor: pointer;
#                     transition: background-color 0.3s ease;
#                 }}

#                 .filter-btn:hover {{
#                     background-color: #e58a3d;
#                 }}
#             </style>
#         </head>
#         <body>
#             {metadata_table}
#         </body>
#         </html>
#         """
#         return HttpResponse(html_response)

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return HttpResponse(f"Error: {str(e)}", status=500)
#code edited  

from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime, timedelta
from .models import JSONFile


def getdata(request):
    try:
         
        # Fetch date filters from the request
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Filter metadata based on date range
        metadata = JSONFile.objects.all()

        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                metadata = metadata.filter(uploaded_at__gte=start_date_obj)
            except ValueError:
                return HttpResponse("Invalid start date format. Use YYYY-MM-DD.", status=400)

        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
                metadata = metadata.filter(uploaded_at__lte=end_date_obj)
            except ValueError:
                return HttpResponse("Invalid end date format. Use YYYY-MM-DD.", status=400)
             
          
            
        
        # Start building the metadata table
        metadata_table = """
        
         
        <h1 style="background-color:#f5a142; height: 50px; color: white; text-align: center; z-index: 1000; position: fixed; width: 100%; margin: 0; top: 0; left: 0;">Metadata Table</h1>
        <div style="margin-top: 60px; padding: 10px; background-color: #f5a142; text-align: right; margin-right: 20px;">
            <form method="get" style="display: flex; align-items: center; justify-content: flex-end; gap: 15px;">
                <h4 style="margin: 0; color: white;">Search Data</h4>
                <div>
                    <label for="start_date" style="margin-right: 5px; color: white;">Start Date:</label>
                    <input type="date" id="start_date" name="start_date" value="{start_date or ''}" class="filter-input">
                </div>
                <div>
                    <label for="end_date" style="margin-right: 5px; color: white;">End Date:</label>
                    <input type="date" id="end_date" name="end_date" value="{end_date or ''}" class="filter-input">
                </div>
                <button type="submit" class="filter-btn">Filter</button>
            </form>
        </div>
        <table border="1" style="width: 100%; border-collapse: collapse; margin-top: 20px;">
            <thead>
                <tr>
                    <th>Sr. No</th>
                    <th>MPS Id</th>
                    <th>Uploader Name</th>
                    <th>File Name</th>
                    <th>File Type</th>
                    <th>Version</th>
                    <th>Uploaded At</th>
                    <th>Unique Grant ID</th>
                    <th>Ingestion ID</th>
                    <th>View File</th>
                    <th>Download File</th>
                </tr>
            </thead>
            <tbody>
        """

        for idx, file in enumerate(metadata, start=1):
            batch_id = file.batch_id
            uploader_name = file.uploader_name
            file_type = file.file_type
            unique_grant_id = file.unique_grant_id
            ingestion_id = file.ingestion_id
            view_url = reverse('view_json', args=[batch_id])
            download_url = reverse('download_json', args=[batch_id])

            metadata_table += f"""
            <tr>
                <td>{idx}</td>
                <td>{batch_id}</td>
                <td>{uploader_name}</td>
                <td>{file.file_name}</td>
                <td>{file_type}</td>
                <td>{file.version}</td>
                <td>{file.uploaded_at}</td>
                <td>{unique_grant_id}</td>
                <td>{ingestion_id}</td>
                <td>
                    <a href="{view_url}" style="text-decoration: none; color: blue;">View</a>
                </td>
                <td>
                    <a href="{download_url}" style="text-decoration: none; color: green;">Download</a>
                </td>
            </tr>
            """
        metadata_table += "</tbody></table>"

        # Combine and return the complete HTML response
        html_response = f"""
        <html>
        <head>
            <title>Data Table</title>
            <style>
                table {{ border: 1px solid black; border-collapse: collapse; width: 100%; background-color: #ffffff; }}
                th, td {{ padding: 10px; text-align: left; border: 1px solid black; background-color: #ffffff; border: 1px solid #ddd; }}
                th {{ background-color:#f5a142; color: white; }}

                .filter-input, .filter-btn {{
                    padding: 8px 15px;
                    border-radius: 5px;
                    border: 1px solid #f5a142;
                    font-size: 14px;
                }}

                .filter-input {{
                    background-color: white;
                    color: #333;
                    transition: background-color 0.3s ease;
                }}

                .filter-input:hover {{
                    background-color: #f5a142;
                    color: white;
                }}

                .filter-btn {{
                    background-color: #f5a142;
                    color: white;
                    border: none;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                }}

                .filter-btn:hover {{
                    background-color: #e58a3d;
                }}
            </style>
        </head>
        <body>
           
            {metadata_table}
        </body>
        </html>
        """
        return HttpResponse(html_response)

    except Exception as e:
        print(f"Error: {str(e)}")
        return HttpResponse(f"Error: {str(e)}", status=500)

# from django.http import JsonResponse

# def view_json(request, batch_id):
#     try:
#         # Fetch the JSON data from MongoDB
#         json_data = collection.find_one({'batch_id': batch_id}, {'_id': 0})

#         if not json_data:
#             return JsonResponse({'error': f'No data found for batch_id: {batch_id}'}, status=404)

#         # Return the JSON data as an indented response
#         return JsonResponse(json_data, safe=False, json_dumps_params={'indent': 4})
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)
    
# from django.http import HttpResponse

# def view_json(request, batch_id):
#     try:
#         # Fetch JSON data from MongoDB for the given batch_id
#         json_data = collection.find_one({'batch_id': batch_id}, {'_id': 0})

#         if not json_data:
#             return HttpResponse(f"<h1 style='color:red;'>No data found for batch_id: {batch_id}</h1>", status=404)

#         # Convert JSON data to an HTML form
#         form_content = f"""
#         <html>
#         <head>
#             <title>JSON Form View</title>
#             <style>
#                 body {{
#                     font-family: Arial, sans-serif;
#                     margin: 0 auto;
#                     padding: 20px;
#                     width: 80%;
#                     background-color: #f7f7f7;
#                 }}
#                 h1 {{
#                     text-align: center;
#                     background-color: #2a9d8f;
#                     color: white;
#                     padding: 10px;
#                 }}
#                 .form-container {{
#                     background: #fff;
#                     border-radius: 8px;
#                     box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
#                     padding: 20px;
#                 }}
#                 .form-group {{
#                     margin-bottom: 15px;
#                 }}
#                 label {{
#                     font-weight: bold;
#                     color: #2a9d8f;
#                 }}
#                 input, textarea {{
#                     width: 100%;
#                     padding: 8px;
#                     border: 1px solid #ccc;
#                     border-radius: 4px;
#                     box-sizing: border-box;
#                 }}
#                 .nested-title {{
#                     color: #2a9d8f;
#                     font-style: italic;
#                 }}
#             </style>
#         </head>
#         <body>
#             <h1>JSON To HTML Form View</h1>
#             <div class="form-container">
#                 {json_to_form(json_data)}
#             </div>
#         </body>
#         </html>
#         """
#         return HttpResponse(form_content)
#     except Exception as e:
#         return HttpResponse(f"<h1 style='color:red;'>Error: {str(e)}</h1>", status=500)

# def json_to_form(json_data):
#     """
#     Converts JSON data into HTML form fields recursively.
#     Supports nested objects and lists.
#     """
#     html = ""
#     if isinstance(json_data, dict):
#         for key, value in json_data.items():
#             html += '<div class="form-group">'
#             html += f"<label>{key}</label>"

#             # Handle nested dictionaries or lists recursively
#             if isinstance(value, dict) or isinstance(value, list):
#                 html += f"<div class='nested-title'>{key} (Nested):</div>"
#                 html += json_to_form(value)
#             else:
#                 html += f'<input type="text" value="{value}" readonly>'
#             html += "</div>"
#     elif isinstance(json_data, list):
#         for index, item in enumerate(json_data):
#             html += f'<div class="form-group"><label>Item {index + 1}</label>'
#             html += json_to_form(item)
#             html += "</div>"
#     else:
#         html += f'<input type="text" value="{json_data}" readonly>'
#     return html



################functions for viewing data into table view and that data in html form format extracting in ui  ##########################
########################################################




# from django.http import HttpResponse, JsonResponse
# from pymongo import MongoClient
# def json_to_html_form(data, level=0, parent_id="root"):
#     """
#     Recursive function to generate an expandable/collapsible HTML form representation of JSON data.
#     """
#     html = ""
#     current_id = f"{parent_id}_{level}"

#     if isinstance(data, dict):
#         for key, value in data.items():
#             item_id = f"{current_id}_{key}"
#             if isinstance(value, (dict, list)):
#                 # Expandable section for nested fields
#                 html += f"""
#                 <div style="margin-left: {20 * level}px; padding: 5px;">
#                     <span style="cursor: pointer; color: blue;" onclick="toggle('{item_id}')">
#                         ▶ <b>{key}</b>
#                     </span>
#                     <div id="{item_id}" style="display: none; margin-top: 5px;">
#                         {json_to_html_form(value, level + 1, item_id)}
#                     </div>
#                 </div>
#                 """
#             else:
#                 # Form input for plain key-value pair
#                 html += f"""
#                 <div style="margin-left: {20 * level}px; padding: 5px;">
#                     <label style="font-weight: bold;" for="{item_id}">{key}:</label>
#                     <input type="text" id="{item_id}" value="{value}" 
#                            style="margin-left: 10px; padding: 7px; width:400px;" readonly/>
#                 </div>
#                 """

#     elif isinstance(data, list):
#         for idx, item in enumerate(data):
#             item_id = f"{current_id}_item_{idx}"
#             if isinstance(item, (dict, list)):
#                 # Expandable section for list items
#                 html += f"""
#                 <div style="margin-left: {20 * level}px; padding: 5px;">
#                     <span style="cursor: pointer; color: green;" onclick="toggle('{item_id}')">
#                         ▶ <b>Item {idx + 1}</b>
#                     </span>
#                     <div id="{item_id}" style="display: none; margin-top: 5px;">
#                         {json_to_html_form(item, level + 1, item_id)}
#                     </div>
#                 </div>
#                 """
#             else:
#                 # Form input for plain list items
#                 html += f"""
#                 <div style="margin-left: {20 * level}px; padding: 5px;">
#                     <label style="font-weight: bold; ">Item {idx + 1}:</label>
#                     <input type="text" value="{item}" style="margin-left: 10px; padding: 3px;" readonly/>
#                 </div>
#                 """

#     else:
#         # If value is plain text or a number
#         html += f"""
#         <div style="margin-left: {20 * level}px;">
#             <input type="text" value="{data}" style="padding: 3px;" readonly/>
#         </div>
#         """

#     return html

#correct code############date 31-01-2025  json view of html form 

# from django.http import HttpResponse, JsonResponse
# from pymongo import MongoClient


# def json_to_html_form(data, level=0, parent_id="root"):
#     """
#     Recursive function to generate an expandable/collapsible HTML form representation of JSON data.
#     Fields with missing data are highlighted in red.
#     """
#     html = ""
#     current_id = f"{parent_id}_{level}"

#     if isinstance(data, dict):
#         for key, value in data.items():
#             item_id = f"{current_id}_{key}"
#             if isinstance(value, (dict, list)):
#                 # Expandable section for nested fields
#                 html += f"""
#                 <div style="margin-left: {20 * level}px; padding: 5px;">
#                     <span style="cursor: pointer; color: blue;" onclick="toggle('{item_id}')">
#                         ▶ <b>{key}</b>
#                     </span>
#                     <div id="{item_id}" style="display: none; margin-top: 5px;">
#                         {json_to_html_form(value, level + 1, item_id)}
#                     </div>
#                 </div>
#                 """
#             else:
#                 # Highlight fields with missing or 'not found' data
#                 highlight_style = "border: 2px solid red; background-color: #ffe6e6;" if value in [None, "", "not found","not available","NOT FOUND"] else ""
#                 html += f"""
#                 <div style="margin-left: {20 * level}px; padding: 5px;">
#                     <label style="font-weight: bold;" for="{item_id}">{key}:</label>
#                     <input type="text" id="{item_id}" value="{value}" 
#                            style="margin-left: 10px; padding: 7px; width:400px; {highlight_style}" readonly/>
#                 </div>
#                 """

#     elif isinstance(data, list):
#         for idx, item in enumerate(data):
#             item_id = f"{current_id}_item_{idx}"
#             if isinstance(item, (dict, list)):
#                 # Expandable section for list items
#                 html += f"""
#                 <div style="margin-left: {20 * level}px; padding: 5px;">
#                     <span style="cursor: pointer; color: green;" onclick="toggle('{item_id}')">
#                         ▶ <b>Item {idx + 1}</b>
#                     </span>
#                     <div id="{item_id}" style="display: none; margin-top: 5px;">
#                         {json_to_html_form(item, level + 1, item_id)}
#                     </div>
#                 </div>
#                 """
#             else:
#                 # Highlight fields with missing or 'not found' data
#                 highlight_style = "border: 2px solid red; background-color: #ffe6e6;" if item in [None, "", "not found","not available","NOT FOUND"] else ""
#                 html += f"""
#                 <div style="margin-left: {20 * level}px; padding: 5px;">
#                     <label style="font-weight: bold; ">Item {idx + 1}:</label>
#                     <input type="text" value="{item}" style="margin-left: 10px; padding: 3px; {highlight_style}" readonly/>
#                 </div>
#                 """

#     else:
#         # Highlight if the plain value is missing or 'not found'
#         highlight_style = "border: 2px solid red; background-color: #ffe6e6;" if data in [None, "", "not found","not available","NOT FOUND"] else ""
#         html += f"""
#         <div style="margin-left: {20 * level}px;">
#             <input type="text" value="{data}" style="padding: 3px; {highlight_style}" readonly/>
#         </div>
#         """

#     return html


# def view_json(request, batch_id):
#     """
#     View function to fetch JSON data from MongoDB and render it as an expandable HTML form view.
#     """
#     try:
#         # Debugging: Print field names in MongoDB
#         sample_data = collection.find_one({}, {'_id': 0})
#         print("Sample Data Keys:", list(sample_data.keys()) if sample_data else "No sample data")

#         # Fetch JSON data from MongoDB - query for flexible batch_id fields
#         query = {
#             '$or': [
#                 {'batch_id': batch_id},
#                 {'batchId': batch_id},
#                 {'BatchId': batch_id},
#                 {'batchid': batch_id}
#             ]
#         }
#         json_data = collection.find_one(query, {'_id': 0})

#         # Debugging: Log the query result
#         print("Query Result:", json_data)

#         # Return error if no data is found
#         if not json_data:
#             return HttpResponse(
#                 f"<h1 style='color: red;'>No data found for batch_id: {batch_id}</h1>", status=404
#             )

#         # Generate HTML with expandable/collapsible functionality
#         html_content = f"""
#         <html>
#         <head>
#             <title>JSON Data View</title>
#             <style>
#                 body {{
#                     font-family: Arial, sans-serif;
#                     margin: 20px;
#                     background-color: #f7f7f7;
#                 }}
#                 h1 {{
#                     text-align: center;
#                     background-color:#f5a142;
#                     color: white;
#                     padding: 10px;
#                 }}
#                 .container {{
#                     background-color: #ffffff;
#                     padding: 10px;
#                     border: 1px solid #ddd;
#                     box-shadow: 0 2px 5px rgba(0,0,0,0.1);
#                 }}
#                 input {{
#                     border: 1px solid #ccc;
#                     border-radius: 4px;
#                     padding: 3px 5px;
#                 }}
#                 label {{
#                     font-weight: bold;
#                     display: inline-block;
#                     width: 150px;
#                 }}
#             </style>
#             <script>
#                 function toggle(id) {{
#                     var element = document.getElementById(id);
#                     var span = event.target;

#                     if (element.style.display === "none") {{
#                         element.style.display = "block";
#                         span.innerHTML = "▼ " + span.innerHTML.slice(2);
#                     }} else {{
#                         element.style.display = "none";
#                         span.innerHTML = "▶ " + span.innerHTML.slice(2);
#                     }}
#                 }}
#             </script>
#         </head>
#         <body>
#             <h1>JSON Data for Batch ID: {batch_id}</h1>
#             <div class="container">
#                 {json_to_html_form(json_data)}
#             </div>
#         </body>
#         </html>
#         """
#         return HttpResponse(html_content)

#     except Exception as e:
#         # Debugging: Log the exception
#         print("Error occurred:", str(e))
#         return JsonResponse({'error': str(e)}, status=500)

from django.http import HttpResponse, JsonResponse
from pymongo import MongoClient

# Static descriptions for key fields
FIELD_DESCRIPTIONS = {
    "batchId": "Its Internal Id Created at ingestion time",
    "ingestionId": "When File Ingested it Created at ingestion time",
    "grantAwardId": "Assigned by suppliers as the unique Elsevier identifier for the award",
    "fundingBodyAwardId": "Contains the unique identifier given to the award by the Funding Body. If not available, use 'Not available'.",
    "hasInstallment":"HasInstallment",
    "hasWorkPackage":"hasWorkPackage",
    "homePage":"URL of the funding body homepage where the award is capturing",
    "link":"URL pointing to a project page or to the funder page with further details about the funded project",
    "synopsis":" contains a description of the funding opportunity identifying the exact goal of the opportunity focusing on the research objectives. FBs use different names for synopses, such as Research objectives, Description, Purpose, Abstract, and Summary.",
    "abstract":"Abstract",
    "title":"Title",
    "language":"Language Type",
    "value":"Value",
    "hasProvenance":"All standard details for the opportunity records, such as the supplier details, status of the record, and the creation and update details can be found in the object Provenance",
    "createdOn":"Creation Date",
    "createdBy":"Created By",
    "createdWith":"Created With",
    "source":"Source",
    "licenseInformation":" FBs require that Elsevier cite the FB license when using their data in a commercial product. Use property licenseInformation to capture information attributing the data to the FB. Capture all data in the available fields.",
    "funds":"The property funds contains the object AwardFund with the sub-properties such as fundingProjectId,acronym,hasPart,title,startDate,endDate,hasPostalAddress,link,status",
    "fundingBodyProjectId":"ID of the project that is funded as defined by the funding organization.",
    "hasPart":"Used if some of the funding is derived from a subproject as mentioned by the FB.",
    "budget":" budget is used to indicate the total (sub)project cost whether funded or not and contains the object AmountWithCurrency",
    "currency":"currency contains a value indicating the award currency. If the currency type is not specified, use the currency for the country of the FB awarding the opportunity or award.",
    "amount":"amount is captured in positive integers only. If not indicated in the source, do not capture this object. ",
    "acronym":"Acronym of the project this award is funding",
    "hasPostalAddress":"Location where the award or project took place, contains the object PostalAddress",
    "addressCountry":"Capture the 3-letter codes in lowercase from Country Codes for OPSBANK (2 and 3 letters).",
    "addressRegion":"The administrative region, state or area used, for states or provinces in the USA, Canada,and Australia, use letter codes in uppercase in USA, Canada and Australia Province/State Abbreviations.",
    "addressLocality":"The locality such as the settlement name, city, town, or county (a territorial division of some countries)",
    "addressPostalCode":"A series of letters, digits, or both that specifies a geographic location included in a postal address. Basic US postal or ZIP codes contain 5 digits. ZIP codes may also be given as the IP+4 code in which the basic 5-digit code is extended with 4 extra digits, separated from the basic code with a hyphen, capture as written in the source.",
    "postOfficeBoxNumber":"A uniquely addressable lockable box located on the premises of a post office station included in a postal address.",
    "streetAddress":"The location of a building, apartment, or other structure on a street, including the house number, if available",
    "status":"status is used to indicate whether an FB is active or inactive. 'ACTIVE' indicates whether the funder is currently providing funding. 'INACTIVE' indicates a past funder that is no longer providing funding or no longer exists.The default value is 'ACTIVE'",
    "fundingDetail":"contains the funding details of the awards",
     "installment":"contains the information representing the awardedm amount for each installment or fiscal year.",
    "index":"index indicates the number of installments, with each new installment adding to the index. Default is 1.",
    "grantAwardInstallmentId":"GrantAwardInstallmentId",
    "financialYearStart":"FinancialYearStart",
    "financialYearEnd":"FinancialYearEnd",
    "fundedAmount":" fundedAmount contains the amount that was awarded in the installment.",
    "fundingTotal":"contains the digits representing the total funding assigned to a project through this award, if there are installments this number represents the sum of all yearly installments",
    "awardeeDetail":"contains information about these award recipients. If there are multiple awardees, capture each in a new set of sub-properties in awardeeDetail.",
    "activityType":"is an open text field used to indicate the type of organization activity as found in the award announcement, that is, research organization or industry.",
    "affiliationOf":"Awardees within the institution who received the award or will work on the funded project are captured in the property affiliationOf.",
    "awardeePersonId":" is a generated identifier for each instance of an awarded person or researcher. The supplier creates the awardeePersonId value by capturing the grantAwardId value, followed by _P_(sequence number),",
    "emailAddress":"Capture the email address of the awardee in the property emailAddress when available in the source.",
    "familyName:":"Capture the surname of the awardee, in most cases this is the last name.",
    "fundingBodyPersonId":"FundingBodyPersonId: ",
    "givenName":"Capture the first name of the awardee",
    "identifier":"The property identifier is a container property for referencing other organizational identifiers.",
    "type":"Type Of",
    "initials":"Capture the initials of the given name of an awardee in the property initials. Capture initials in uppercase and with a period. Hyphenated given names must include the hyphen. If more than one initial appears, capture the initials without spaces between them.",
    "name":"Name Capture the full name as it appears in the source in the property name using the object StringWithLanguage, ",
    "role":"role is used to indicate the role of the awarded institution in the project if provided by the FB. The default valueis 'COORDINATOR'. This information is normally provided for EU data.",
    "sourceRole":"sourceRole",
    "awardeeAffiliationId":"AwardeeAffiliationId:",
    "departmentName":"Any affiliation department mentioned in the announcement is captured in the property departmentName using object StringWithLanguage",
    "fundingBodyOrganizationId":"FundingBodyOrganizationId",
    "vatNumber":"The funder-specific VAT number is captured in the property vatNumber when found in the source.",
    "classification":"Classification contains classification types and codes for an opportunity or award. Classifications refers to the vocabularies that are applied to opportunities or awards in order to classify or categorize these records on their type,research area, funding mechanism, or focus area",
    "hasSubject":"In sub-property preferredLabel, capture the term of the classification code. In the sub-property identifier, capture the corresponding value and the type of classification",
    "preferredLabel":"capture the term of the classification code",
     "relatedOpportunity":" describes the relationship between an opportunity and any awards made from that opportunity. If described, capture this information",
     "grantOpportunityId":" grantOpportunityId is created and assigned by suppliers as the unique Elsevier identifier for the opportunity",
     "fundingBodyOpportunity":"fundingBodyOpportunityId is used to capture the unique identifier number given to the opportunity by the FB. If the FB does not publish an ID, a number, code, or other identifier for the opportunity, use the value 'Not available' in the property fundingBodyOpportunityId",
    "relatedFunder":"relatedFunder, capture FBs that have financed the award that resulted in this publication,such as  leadFunder and hasFunder",
    "leadFunder":"main funder of the award. If a funder has a complex hierarchy, take the lowest level of the hierarchy. If multiple funders are mentioned, capture the one which is reporting the award-to-publication link",
     "fundingBodyId":" fundingBodyId contains the unique identifier for the created FB, using the range of IDs provided by Elsevier",
     "sourceId":"SourceId",
     "sourceText":"SourceText",
     "hasProvenance":"All standard details for the award records, such as the supplier details, status of the record, and the creation and update details are captured in hasProvenance",
     "wasAttributedTo":"Identifier of the data provider for the record: SUP001, SUP002, SUP003, or NOTSPECIFIED",
     "derivedFrom":"Source URL of the record",
     "createdOn":"Date that the record was created (as per supplier CMS)",
     "lastUpdateOn":"Date when the record was updated (as per supplier CMS)",
     "contactPoint":"Contact email address of the supplier that can be used to address any issues regarding the record",
     "version":"Record version number, increased for each update ",
     "hidden":"Boolean; 'true' indicating that the record will not be displayed on customer-facing products",
     "defunct":"Boolean; 'true' indicating that the record has been tagged as invalid, such as a duplicate, and is no longer used by Elsevier products",
     "status":"Status of the record: 'NEW', 'UPDATE', or 'DELETE'",
     "options":"options",
     "additionalProp1":" AdditionalProp1",
     "additionalProp2":" AdditionalProp2",
     "additionalProp3":"AdditionalProp3",
     "hasFunder":" contains all funders listed as contributing to the award that funds the publication. The list must also contain the lead funder, and any other listed funders.",
    "description":"Description",
    "keyword":" Keywords normally reflect the main research topics that the funding opportunity covers. FB can also refer to tags, topics, categories, areas, and subjects.",
    "grantType": "contains only the opportunity type that is distributed by the funder in a structured manner. The default category is the value 'RESEARCH'",
    "funderSchemeType":" is used to indicate the type of funding provided by the funder for this opportunity as stated in the opportunity announcement. Supplier captures the original funder text or description that is used to determine the set,specific categories used in grantType.",
    "startDate":"The date from which applications for an opportunity will be accepted.",
}

def json_to_html_form(data, level=0, parent_id="root"):
    """
    Recursive function to generate an expandable/collapsible HTML form representation of JSON data.
    Adds hover descriptions for specific fields.
    """
    html = ""
    current_id = f"{parent_id}_{level}"

    if isinstance(data, dict):
        for key, value in data.items():
            item_id = f"{current_id}_{key}"
            description = FIELD_DESCRIPTIONS.get(key, "No description available")  # Default description

            if isinstance(value, (dict, list)):
                # Expandable section for nested fields
                html += f"""
                <div style="margin-left: {20 * level}px; padding: 5px;">
                    <span style="cursor: pointer; color: blue;" onclick="toggle('{item_id}')" title="{description}">
                        ▶ <b>{key}</b>
                    </span>
                    <div id="{item_id}" style="display: none; margin-top: 5px;">
                        {json_to_html_form(value, level + 1, item_id)}
                    </div>
                </div>
                """
            else:
                # Highlight missing or 'not found' data
                highlight_style = "border: 2px solid red; background-color: #ffe6e6;" if value in [None, "", "not found", "not available", "NOT FOUND"] else ""
                html += f"""
                <div style="margin-left: {20 * level}px; padding: 5px;">
                    <label style="font-weight: bold;" for="{item_id}" title="{description}">{key}:</label>
                    <input type="text" id="{item_id}" value="{value}" 
                           style="margin-left: 10px; padding: 7px; width:400px; {highlight_style}" readonly/>
                </div>
                """

    elif isinstance(data, list):
        for idx, item in enumerate(data):
            item_id = f"{current_id}_item_{idx}"
            if isinstance(item, (dict, list)):
                # Expandable section for list items
                html += f"""
                <div style="margin-left: {20 * level}px; padding: 5px;">
                    <span style="cursor: pointer; color: green;" onclick="toggle('{item_id}')">
                        ▶ <b>Item {idx + 1}</b>
                    </span>
                    <div id="{item_id}" style="display: none; margin-top: 5px;">
                        {json_to_html_form(item, level + 1, item_id)}
                    </div>
                </div>
                """
            else:
                # Highlight missing or 'not found' data
                highlight_style = "border: 2px solid red; background-color: #ffe6e6;" if item in [None, "", "not found", "not available", "NOT FOUND"] else ""
                html += f"""
                <div style="margin-left: {20 * level}px; padding: 5px;">
                    <label style="font-weight: bold;">Item {idx + 1}:</label>
                    <input type="text" value="{item}" style="margin-left: 10px; padding: 3px; {highlight_style}" readonly/>
                </div>
                """

    return html


def view_json(request, batch_id):
    """
    View function to fetch JSON data from MongoDB and render it as an expandable HTML form view.
    Also logs available batch IDs for debugging.
    """
    try:
        
        # Debug: Print available batch IDs
        available_batch_ids = collection.distinct("batchId")
        print("Available batch_ids in MongoDB:", available_batch_ids)

        # Query to fetch the data
        query = {
            '$or': [
                {'batch_id': batch_id},
                {'batchId': batch_id},
                {'BatchId': batch_id},
                {'batchid': batch_id}
            ]
        }
        json_data = collection.find_one(query, {'_id': 0})

        if not json_data:
            return HttpResponse(
                f"<h1 style='color: red;'>No data found for batch_id: {batch_id}</h1>", status=404
            )

        # Generate HTML with expandable/collapsible functionality
        html_content = f"""
        <html>
        <head>
            <title>JSON Data View</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f7f7f7;
                }}
                h1 {{
                    text-align: center;
                    background-color:#f5a142;
                    color: white;
                    padding: 10px;
                }}
                .container {{
                    background-color: #ffffff;
                    padding: 10px;
                    border: 1px solid #ddd;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                input {{
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 3px 5px;
                }}
                label {{
                    font-weight: bold;
                    display: inline-block;
                    width: 150px;
                }}
            </style>
            <script>
                function toggle(id) {{
                    var element = document.getElementById(id);
                    var span = event.target;

                    if (element.style.display === "none") {{
                        element.style.display = "block";
                        span.innerHTML = "▼ " + span.innerHTML.slice(2);
                    }} else {{
                        element.style.display = "none";
                        span.innerHTML = "▶ " + span.innerHTML.slice(2);
                    }}
                }}
            </script>
        </head>
        <body>
            <h1>JSON Data for Batch ID: {batch_id}</h1>
            <div class="container">
                {json_to_html_form(json_data)}
            </div>
        </body>
        </html>
        """
        return HttpResponse(html_content)

    except Exception as e:
        print("Error occurred:", str(e))
        return JsonResponse({'error': str(e)}, status=500)

####################end#################


# import json
# from django.http import HttpResponse
# from django.http import HttpResponse

# def download_json(request, batch_id):
#     json_data = collection.find_one({"batch_id": batch_id}, {"_id": 0})
#     if not json_data:
#         return JsonResponse({"error": f"No data found for batch_id: {batch_id}"}, status=404)
    
#     response = HttpResponse(content_type="application/json")
#     response['Content-Disposition'] = f'attachment; filename="{batch_id}.json"'
#     response.write(json.dumps(json_data, indent=4))
#     return response



############downlaod function to upload a file ####################
############################################
import json
from django.http import HttpResponse, JsonResponse
from pymongo import MongoClient


def download_json(request, batch_id):
    """
    View function to fetch JSON data from MongoDB and allow the user to download it as a .json file.
    """
    try:
        # Fetch JSON data based on batch_id (flexible query)
        query = {
            "$or": [
                {"batch_id": batch_id},
                {"batchId": batch_id},
                {"BatchId": batch_id}
            ]
        }
        json_data = collection.find_one(query, {"_id": 0})  # Exclude the MongoDB '_id' field

        if not json_data:
            # Return 404 response if no data is found
            return JsonResponse(
                {"error": f"No data found for batch_id: {batch_id}"},
                status=404
            )

        # Create the HTTP response with JSON content type
        response = HttpResponse(
            json.dumps(json_data, indent=4),  # Indented JSON for readability
            content_type="application/json"
        )
        # Set the 'Content-Disposition' header to force download
        response["Content-Disposition"] = f'attachment; filename="{batch_id}.json"'

        return response

    except Exception as e:
        print("Error while processing JSON file download:", str(e))
        return JsonResponse(
            {"error": "An internal error occurred while processing the request."},
            status=500
        )
#######################################################
########################################################################################
  
    
    
    
    
  # Update JSON File
def update_json(request):
    if request.method == 'POST':
        batch_id = request.POST['batch_id']
        json_file = request.FILES['file']

        try:
            # Read JSON content
            json_data = json.load(json_file)

            # Update metadata version
            file_metadata = JSONFile.objects.get(batch_id=batch_id)
            file_metadata.version += 1
            file_metadata.save()

            # Update MongoDB data (replace existing records for the batch)
            collection.delete_many({'batch_id': batch_id})
            if isinstance(json_data, list):
                for item in json_data:
                    item['batch_id'] = batch_id
                collection.insert_many(json_data)
            else:
                json_data['batch_id'] = batch_id
                collection.insert_one(json_data)

            return JsonResponse({'message': 'File updated successfully!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        
        
        
        
# #############adding view for source input data form #########################################
#############################################################################################
# # import datetime
# from datetime import datetime
# from django.shortcuts import render, redirect
# from .forms import SourceMetadataForm
# from .models import SourceMetadata  # Import the MongoDB model
# # MongoDB setup



# def upload_source_metadata(request):
#     if request.method == 'POST':
#         form = SourceMetadataForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Save form data to MongoDB
#             source_metadata = SourceMetadata(
#                 import_url=form.cleaned_data['import_url'],
#                 date_of_arrival=form.cleaned_data['date_of_arrival'],
#                 assigned_to=form.cleaned_data['assigned_to'],
#                 frequency_of_site_updates=form.cleaned_data['frequency_of_site_updates'],
#                 site_last_checked=form.cleaned_data['site_last_checked'],
#                 source_file_upload=form.cleaned_data.get('source_file_upload'),
#                 json_file_name=form.cleaned_data['json_file_name'],
#                 json_upload_date=form.cleaned_data['json_upload_date'],
#                 sup_id=form.cleaned_data['sup_id'],
#                 sme_comments=form.cleaned_data['sme_comments'],
#                 screenshots_taken=form.cleaned_data['screenshots_taken'],
                
                
#                  # New fields for QA
#                 qa_comment=form.cleaned_data.get('qa_comment'),
#                 qa_name=form.cleaned_data.get('qa_name'),
#                 qa_issue=form.cleaned_data.get('qa_issue'),
#                 # created_at=datetime.datetime.now() , 
#                 created_at = datetime.now()
#             )
#             source_metadata.save()  # Save the document into MongoDB
#             return redirect('/')  # Redirect after success
#     else:
#         form = SourceMetadataForm()

#     return render(request, 'upload_source_metadata.html', {'form': form})

# #########################################################
# ##########ending input source data##########################




# #######################function for viewing source inp[ut data into table view#########################################################

# def view_source_metadata(request):
#     # Fetch all source metadata records from MongoDB
#     source_metadata_list = SourceMetadata.objects.all()

#     return render(request, 'view_source_metadata.html', {'source_metadata_list': source_metadata_list})


#updated code for source metadata correct code
#date 13-1-2025


from django.shortcuts import render, redirect, get_object_or_404
from .forms import SourceMetadataForm
from .models import SourceMetadata
from django.http import Http404
from datetime import datetime
import os
from django.conf import settings
#Upload view
def upload_source_metadata(request):
    if request.method == 'POST':
        form = SourceMetadataForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get('source_file_upload')
            if uploaded_file:
                # Define the file path where the file will be saved
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'source_files')
                os.makedirs(upload_dir, exist_ok=True)  # Ensure the directory exists
                file_path = os.path.join(upload_dir, uploaded_file.name)

                # Save the file to the local file system
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
            # Save form data to MongoDB
            source_metadata = SourceMetadata(
                import_url=form.cleaned_data['import_url'],
                date_of_arrival=form.cleaned_data['date_of_arrival'],
                assigned_to=form.cleaned_data['assigned_to'],
                frequency_of_site_updates=form.cleaned_data['frequency_of_site_updates'],
                site_last_checked=form.cleaned_data['site_last_checked'],
                source_file_upload=uploaded_file.name if uploaded_file else None,
                json_file_name=form.cleaned_data['json_file_name'],
                json_upload_date=form.cleaned_data['json_upload_date'],
                sup_id=form.cleaned_data['sup_id'],
                sme_comments=form.cleaned_data['sme_comments'],
                screenshots_taken=form.cleaned_data['screenshots_taken'],
                
                # New fields for QA
                qa_comment=form.cleaned_data.get('qa_comment'),
                qa_name=form.cleaned_data.get('qa_name'),
                file_status =form.cleaned_data.get('file_status'),
                qa_issue=form.cleaned_data.get('qa_issue'),
                created_at=datetime.now()
            )
            source_metadata.save()  # Save the document into MongoDB
            # return redirect('/')  # Redirect after success
            return redirect('/funding_body/')

            
    else:
        form = SourceMetadataForm()

    return render(request, 'upload_source_metadata.html', {'form': form})




 # View source metadata
def view_source_metadata(request):
    # Fetch all source metadata records from MongoDB
    source_metadata_list = SourceMetadata.objects.all()
    for i in source_metadata_list:
        print(i)

    return render(request, 'view_source_metadata.html', {'source_metadata_list': source_metadata_list})
#worked on 22-01-2025

# Edit view
# def edit_source_metadata(request, metadata_id):
#     try:
#         # Try fetching the object from the MongoDB database
#         source_metadata = SourceMetadata.objects.get(id=metadata_id)
#     except SourceMetadata.DoesNotExist:
#         raise Http404("SourceMetadata not found")

#     if request.method == 'POST':
#         form = SourceMetadataForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Update the metadata object
#             source_metadata.import_url = form.cleaned_data['import_url']
#             source_metadata.date_of_arrival = form.cleaned_data['date_of_arrival']
#             source_metadata.assigned_to = form.cleaned_data['assigned_to']
#             source_metadata.frequency_of_site_updates = form.cleaned_data['frequency_of_site_updates']
#             source_metadata.site_last_checked = form.cleaned_data['site_last_checked']
#             source_metadata.source_file_upload = form.cleaned_data.get('source_file_upload') or source_metadata.source_file_upload
#             source_metadata.json_file_name = form.cleaned_data['json_file_name']
#             source_metadata.json_upload_date = form.cleaned_data['json_upload_date']
#             source_metadata.sup_id = form.cleaned_data['sup_id']
#             source_metadata.sme_comments = form.cleaned_data['sme_comments']
#             source_metadata.screenshots_taken = form.cleaned_data['screenshots_taken']
            
#             # QA fields
#             source_metadata.qa_comment = form.cleaned_data.get('qa_comment')
#             source_metadata.qa_name = form.cleaned_data.get('qa_name')
#             source_metadata.qa_issue = form.cleaned_data.get('qa_issue')
            
#             source_metadata.save()  # Save changes to the database
#             return redirect('view_source_metadata')  # Redirect to the list view after saving
#     else:
#         # Pre-fill the form with existing metadata
#         initial_data = {
#             'import_url': source_metadata.import_url,
#             'date_of_arrival': source_metadata.date_of_arrival,
#             'assigned_to': source_metadata.assigned_to,
#             'frequency_of_site_updates': source_metadata.frequency_of_site_updates,
#             'site_last_checked': source_metadata.site_last_checked,
#             'source_file_upload': source_metadata.source_file_upload,
#             'json_file_name': source_metadata.json_file_name,
#             'json_upload_date': source_metadata.json_upload_date,
#             'sup_id': source_metadata.sup_id,
#             'sme_comments': source_metadata.sme_comments,
#             'screenshots_taken': source_metadata.screenshots_taken,
#             'qa_comment': source_metadata.qa_comment,
#             'qa_name': source_metadata.qa_name,
#             'qa_issue': source_metadata.qa_issue,
#         }
#         form = SourceMetadataForm(initial=initial_data)

#     return render(request, 'upload_source_metadata.html', {'form': form, 'metadata': source_metadata})
# from django.http import HttpResponseForbidden

# def edit_source_metadata(request, metadata_id):
#     try:
#         # Try fetching the object from the MongoDB database
#         source_metadata = SourceMetadata.objects.get(id=metadata_id)
#     except SourceMetadata.DoesNotExist:
#         raise Http404("SourceMetadata not found")

#     # Restrict access: Only the assigned user or a superuser can edit
#     if request.user.username != source_metadata.assigned_to and not request.user.is_superuser:
#         return HttpResponseForbidden("You are not allowed to edit this entry.")

#     if request.method == 'POST':
#         form = SourceMetadataForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Update the metadata object
#             source_metadata.import_url = form.cleaned_data['import_url']
#             source_metadata.date_of_arrival = form.cleaned_data['date_of_arrival']
#             source_metadata.assigned_to = form.cleaned_data['assigned_to']
#             source_metadata.frequency_of_site_updates = form.cleaned_data['frequency_of_site_updates']
#             source_metadata.site_last_checked = form.cleaned_data['site_last_checked']
#             source_metadata.source_file_upload = form.cleaned_data.get('source_file_upload') or source_metadata.source_file_upload
#             source_metadata.json_file_name = form.cleaned_data['json_file_name']
#             source_metadata.json_upload_date = form.cleaned_data['json_upload_date']
#             source_metadata.sup_id = form.cleaned_data['sup_id']
#             source_metadata.sme_comments = form.cleaned_data['sme_comments']
#             source_metadata.screenshots_taken = form.cleaned_data['screenshots_taken']
            
#             # QA fields
#             source_metadata.qa_comment = form.cleaned_data.get('qa_comment')
#             source_metadata.qa_name = form.cleaned_data.get('qa_name')
#             source_metadata.qa_issue = form.cleaned_data.get('qa_issue')
            
#             source_metadata.save()  # Save changes to the database
#             return redirect('view_source_metadata')  # Redirect to the list view after saving
#     else:
#         # Pre-fill the form with existing metadata
#         initial_data = {
#             'import_url': source_metadata.import_url,
#             'date_of_arrival': source_metadata.date_of_arrival,
#             'assigned_to': source_metadata.assigned_to,
#             'frequency_of_site_updates': source_metadata.frequency_of_site_updates,
#             'site_last_checked': source_metadata.site_last_checked,
#             'source_file_upload': source_metadata.source_file_upload,
#             'json_file_name': source_metadata.json_file_name,
#             'json_upload_date': source_metadata.json_upload_date,
#             'sup_id': source_metadata.sup_id,
#             'sme_comments': source_metadata.sme_comments,
#             'screenshots_taken': source_metadata.screenshots_taken,
#             'qa_comment': source_metadata.qa_comment,
#             'qa_name': source_metadata.qa_name,
#             'qa_issue': source_metadata.qa_issue,
#         }
#         form = SourceMetadataForm(initial=initial_data)

#     return render(request, 'upload_source_metadata.html', {'form': form, 'metadata': source_metadata})

#code for edit sourcemetadata

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden
from .forms import SourceMetadataForm
from .models import SourceMetadata
from datetime import datetime

def edit_source_metadata(request, metadata_id):
    try:
        # Try fetching the object from the MongoDB database
        source_metadata = SourceMetadata.objects.get(id=metadata_id)
    except SourceMetadata.DoesNotExist:
        raise Http404("SourceMetadata not found")

    # Restrict access: Only the assigned user, QA user, or a superuser can edit
    if (request.user.username != source_metadata.assigned_to and 
        request.user.username != source_metadata.qa_name and 
        not request.user.is_superuser):
        return HttpResponseForbidden("You are not allowed to edit this entry.")

    if request.method == 'POST':
        form = SourceMetadataForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get('source_file_upload') 
            if uploaded_file:
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'source_files')
                os.makedirs(upload_dir, exist_ok=True)  # Ensure the directory exists
                file_path = os.path.join(upload_dir, uploaded_file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                source_metadata.source_file_upload = uploaded_file.name
            # Update the metadata object
            source_metadata.import_url = form.cleaned_data['import_url']
            source_metadata.date_of_arrival = form.cleaned_data['date_of_arrival']
            source_metadata.assigned_to = form.cleaned_data['assigned_to']
            source_metadata.frequency_of_site_updates = form.cleaned_data['frequency_of_site_updates']
            source_metadata.site_last_checked = form.cleaned_data['site_last_checked']
            #source_metadata.source_file_upload = uploaded_file.name if uploaded_file else None,
            source_metadata.json_file_name = form.cleaned_data['json_file_name']
            source_metadata.json_upload_date = form.cleaned_data['json_upload_date']
            source_metadata.sup_id = form.cleaned_data['sup_id']
            source_metadata.sme_comments = form.cleaned_data['sme_comments']
            source_metadata.screenshots_taken = form.cleaned_data['screenshots_taken']
            
            # QA fields
            source_metadata.qa_comment = form.cleaned_data.get('qa_comment')
            source_metadata.qa_name = form.cleaned_data.get('qa_name')
            source_metadata.file_status= form.cleaned_data.get('file_status')
            source_metadata.qa_issue = form.cleaned_data.get('qa_issue')
            
            source_metadata.save()  # Save changes to the database
            return redirect('view_source_metadata')  # Redirect to the list view after saving
    else:
        # Pre-fill the form with existing metadata
        initial_data = {
            'import_url': source_metadata.import_url,
            'date_of_arrival': source_metadata.date_of_arrival,
            'assigned_to': source_metadata.assigned_to,
            'frequency_of_site_updates': source_metadata.frequency_of_site_updates,
            'site_last_checked': source_metadata.site_last_checked,
            'source_file_upload': source_metadata.source_file_upload,
            'json_file_name': source_metadata.json_file_name,
            'json_upload_date': source_metadata.json_upload_date,
            'sup_id': source_metadata.sup_id,
            'sme_comments': source_metadata.sme_comments,
            'screenshots_taken': source_metadata.screenshots_taken,
            'qa_comment': source_metadata.qa_comment,
            'qa_name': source_metadata.qa_name,
            'file_status': source_metadata.file_status,
            'qa_issue': source_metadata.qa_issue,
        }
        form = SourceMetadataForm(initial=initial_data)

    return render(request, 'upload_source_metadata.html', {'form': form, 'metadata': source_metadata})



   #######################function for viewing source input data into table view#########################################################     
        

        
        
        

# def manage_files(request):
#     """
#     View to display all files and handle updates through inline editing.
#     """
#     if request.method == 'POST' and 'save_updates' in request.POST:
#         batch_id = request.POST['batch_id']
#         updated_data = request.POST['updated_data']  # Data from the form (as JSON string)

#         try:
#             # Fetch the original file metadata
#             file_metadata = get_object_or_404(JSONFile, batch_id=batch_id)

#             # Parse the updated data
#             updated_json = json.loads(updated_data)

#             # Increment version and save metadata
#             new_version = file_metadata.version + 1
#             file_metadata.version = new_version
#             file_metadata.save()

#             # Update MongoDB collection
#             collection.delete_many({'batch_id': batch_id})
#             if isinstance(updated_json, list):
#                 for item in updated_json:
#                     item['batch_id'] = batch_id
#                 collection.insert_many(updated_json)
#             else:
#                 updated_json['batch_id'] = batch_id
#                 collection.insert_one(updated_json)

#             # Save update to the history table
#             JSONFileUpdateHistory.objects.create(
#                 json_file=file_metadata,
#                 batch_id=batch_id,
#                 version=new_version,
#                 update_details=updated_json
#             )

#             return JsonResponse({'message': 'File updated successfully!'})

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     # Fetch all files for the table
#     files = JSONFile.objects.all()
#     return render(request, 'manage_files.html', {'files': files})


# def updated_files(request):
#     """
#     View to display the update history table.
#     """
#     updates = JSONFileUpdateHistory.objects.all()
#     return render(request, 'updated_files.html', {'updates': updates})


#code for viewing only funding /award/opportunity data
# View for Funding Body
def funding_body_view(request):
    if request.method == 'GET':
        # Extract funding_body_id from GET parameters
        funding_body_id = request.GET.get('funding_body_id')
        print(f"Received GET parameters: {request.GET}")  # Debugging
        
        # Base filter for funding body data
        filters = {'file_type__iexact': 'FundingBody'}  # Updated value
        
        # Add unique_grant_id filter if provided
        if funding_body_id:
            filters['unique_grant_id'] = funding_body_id
        print(f"Filters applied: {filters}")  # Debugging
        
        # Query the database
        files = JSONFile.objects.filter(**filters)
        print(f"Files Found: {files.count()}")  # Debugging
        
        # Handle case where no data is found
        if not files.exists():
            print("No funding body data found.")  # Debugging
            return JsonResponse({'message': 'No funding body data found.'}, status=404)
        
        # Prepare response data
        response_data = []
        for file in files:
            response_data.append({
                'ingestion_id': file.ingestion_id,
                'uploader_name': file.uploader_name,
                'file_type': file.file_type,
                'unique_grant_id': file.unique_grant_id,
                'batch_id': file.batch_id,
                'version': file.version,
                'uploaded_at': file.uploaded_at,
            })
        
        print(f"Response Data: {response_data}")  # Debugging
        
        # Render the results to the template
        return render(request, 'funding_body_view.html', {'files': response_data})

#award data view function################################################################

def award_view(request):
    if request.method == 'GET':
        # Extract award_id from GET parameters
        award_id = request.GET.get('award_id')
        print(f"Received GET parameters: {request.GET}")  # Debugging
        
        # Base filter for award data
        filters = {'file_type__iexact': 'Award'}  # Assuming 'Award' is the value for file_type
        
        # Add unique_grant_id filter if provided
        if award_id:
            filters['unique_grant_id'] = award_id
        print(f"Filters applied: {filters}")  # Debugging
        
        # Query the database
        files = JSONFile.objects.filter(**filters)
        print(f"Award Files Found: {files.count()}")  # Debugging
        
        # Handle case where no data is found
        if not files.exists():
            print("No award data found.")  # Debugging
            return JsonResponse({'message': 'No award data found.'}, status=404)
        
        # Prepare response data
        response_data = []
        for file in files:
            response_data.append({
                'ingestion_id': file.ingestion_id,
                'uploader_name': file.uploader_name,
                'file_type': file.file_type,
                'unique_grant_id': file.unique_grant_id,
                'batch_id': file.batch_id,
                'version': file.version,
                'uploaded_at': file.uploaded_at,
            })
        
        print(f"Response Data: {response_data}")  # Debugging
        
        # Render the results to the template
        return render(request, 'award_view.html', {'files': response_data})


def opportunity_view(request):
    if request.method == 'GET':
        # Extract opportunity_id from GET parameters
        opportunity_id = request.GET.get('opportunity_id')
        print(f"Received GET parameters: {request.GET}")  # Debugging
        
        # Base filter for opportunity data
        filters = {'file_type__iexact': 'Opportunity'}  # Assuming 'Opportunity' is the value for file_type
        
        # Add unique_grant_id filter if provided
        if opportunity_id:
            filters['unique_grant_id'] = opportunity_id
        print(f"Filters applied: {filters}")  # Debugging
        
        # Query the database
        files = JSONFile.objects.filter(**filters)
        print(f"Opportunity Files Found: {files.count()}")  # Debugging
        
        # Handle case where no data is found
        if not files.exists():
            print("No opportunity data found.")  # Debugging
            return JsonResponse({'message': 'No opportunity data found.'}, status=404)
        
        # Prepare response data
        response_data = []
        for file in files:
            response_data.append({
                'ingestion_id': file.ingestion_id,
                'uploader_name': file.uploader_name,
                'file_type': file.file_type,
                'unique_grant_id': file.unique_grant_id,
                'batch_id': file.batch_id,
                'version': file.version,
                'uploaded_at': file.uploaded_at,
            })
        
        print(f"Response Data: {response_data}")  # Debugging
        
        # Render the results to the template
        return render(request, 'opportunity_view.html', {'files': response_data})





#file ingestion view function for json ############################
###################################################################

# import base64
# import logging
# import requests
# import os
# from datetime import datetime
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from django.core.files.storage import default_storage
# from .forms import FileIngestionForm

# global_token = None

# def get_oauth_token(key, secret):
#     url = "https://uat.business.api.elsevier.com/token"
#     credentials = f"{key}:{secret}"
#     encoded_credentials = base64.b64encode(credentials.encode()).decode()
#     headers = {
#         "Authorization": f"Basic {encoded_credentials}",
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     data = {"grant_type": "client_credentials"}
#     response = requests.post(url, headers=headers, data=data)
#     if response.status_code == 200:
#         return response.json().get("access_token")
#     return None

# @csrf_exempt
# def file_ingestion(request):
#     global global_token
#     context = {"form": FileIngestionForm()}

#     if request.method == "POST":
#         form = FileIngestionForm(request.POST, request.FILES)
        
#         if form.is_valid():
#             action = form.cleaned_data["action"]

#             if action == "generate_token":
#                 key = "H0g93ZOVfg77MoAKCTLvCZZtTFoBir2o"  # Replace with your actual key
#                 secret = "T9wS2s4wUQG31k6kv2lJ0SCbNdhHuDgv"  # Replace with your actual secret
#                 global_token = get_oauth_token(key, secret)
#                 context["token"] = global_token
#                 context["message"] = "Token generated successfully!" if global_token else "Failed to generate token."

#             elif action == "create_batch":
#                 if not global_token:
#                     context["message"] = "Token is not available. Please generate a token first."
#                     return render(request, "ingestion_template.html", context)

#                 uploaded_file = request.FILES.get("file_location")
#                 if not uploaded_file:
#                     context["message"] = "No file uploaded."
#                     return render(request, "ingestion_template.html", context)

#                 headers = {
#                     "Authorization": f"Bearer {global_token}",
#                     "accept": "*/*",
#                 }

#                 # Save the uploaded file to a temporary location
#                 temp_file_path = os.path.join(default_storage.location, uploaded_file.name)
#                 if not os.path.exists(default_storage.location):
#                     os.makedirs(default_storage.location)

#                 with default_storage.open(temp_file_path, 'wb+') as temp_file:
#                     for chunk in uploaded_file.chunks():
#                         temp_file.write(chunk)

#                 # Open the saved file in binary mode and send the POST request
#                 with open(temp_file_path, 'rb') as file:
#                     files = {'file': file}
#                     response = requests.post(
#                         "https://uat.business.api.elsevier.com/v1/funding-ingestion/vtool",
#                         headers=headers,
#                         files=files,
#                     )

#                 if response.status_code == 200:
#                     batch_id = response.json().get("batchId")
#                     if batch_id:
#                         context["batch_id"] = batch_id
#                         context["message"] = f"Batch created successfully! Batch ID: {batch_id}"
#                     else:
#                         context["message"] = "Batch creation successful but no batch ID returned."
#                 else:
#                     context["message"] = f"Failed to create batch. Response Code: {response.status_code}"

#             elif action == "ingest_file":
#                 if not global_token:
#                     context["message"] = "Token is not available. Please generate a token first."
#                     return render(request, "ingestion_template.html", context)

#                 ingestion_type = form.cleaned_data["ingestion_type"]
#                 batch_id = request.POST.get("batch_id")
#                 file = request.FILES.get("json_location")
#                 data_type = form.cleaned_data["data_type"]

#                 if not file:
#                     context["message"] = "No file provided for ingestion."
#                     return render(request, "ingestion_template.html", context)

#                 base_url = "https://uat.business.api.elsevier.com/v1/funding-ingestion"
#                 url = f"{base_url}/{data_type}"
#                 if ingestion_type == "batch":
#                     url += "/bulk"
#                 headers = {
#                     "accept": "application/json",
#                     'callbackUrl': 'https://callbackapi-elsevier.mpsinsight.com/callbackapi/callback',
#                     "Content-Type": "application/json",
#                     "batchId": batch_id,
#                     "Authorization": f"Bearer {global_token}",
#                 }

#                 if ingestion_type == "batch":
#                     files = {"file": file}
#                     response = requests.post(url, headers=headers, files=files)
#                 else:
#                     response = requests.post(url, headers=headers, data=file.read())

#                 if response.status_code == 200:
#                     context["message"] = "File ingested successfully!"
#                 else:
#                     context["message"] = f"Failed to ingest file: {response.text}"

#     return render(request, "ingestion_template.html", context)



#code for adding ingestion 2 ##################
# import os
# import base64
# import logging
# import requests
# from datetime import datetime
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from django.core.files.storage import default_storage
# from .forms import FileIngestionForm

# # Create logs directory in the project root
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# LOG_DIR = os.path.join(BASE_DIR, "logs")
# if not os.path.exists(LOG_DIR):
#     os.makedirs(LOG_DIR)

# # Configure logging
# LOG_FILE = os.path.join(LOG_DIR, "ingestion_details.log")
# logging.basicConfig(
#     filename=LOG_FILE,
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

# # Global token variable
# global_token = None


# def get_oauth_token(key, secret):
#     url = "https://uat.business.api.elsevier.com/token"
#     credentials = f"{key}:{secret}"
#     encoded_credentials = base64.b64encode(credentials.encode()).decode()
#     headers = {
#         "Authorization": f"Basic {encoded_credentials}",
#         "Content-Type": "application/x-www-form-urlencoded",
#     }
#     data = {"grant_type": "client_credentials"}
#     response = requests.post(url, headers=headers, data=data)
#     if response.status_code == 200:
#         return response.json().get("access_token")
#     return None


# @csrf_exempt
# def file_ingestion(request):
#     global global_token
#     context = {"form": FileIngestionForm()}

#     if request.method == "POST":
#         form = FileIngestionForm(request.POST, request.FILES)

#         if form.is_valid():
#             action = form.cleaned_data["action"]

#             if action == "generate_token":
#                 key = "H0g93ZOVfg77MoAKCTLvCZZtTFoBir2o"  # Replace with your actual key
#                 secret = "T9wS2s4wUQG31k6kv2lJ0SCbNdhHuDgv"  # Replace with your actual secret
#                 global_token = get_oauth_token(key, secret)
#                 context["token"] = global_token
#                 context["message"] = "Token generated successfully!" if global_token else "Failed to generate token."
#                 logging.info("Token generated successfully!" if global_token else "Failed to generate token.")

#             elif action == "create_batch":
#                 if not global_token:
#                     context["message"] = "Token is not available. Please generate a token first."
#                     return render(request, "ingestion_template.html", context)

#                 uploaded_file = request.FILES.get("file_location")
#                 if not uploaded_file:
#                     context["message"] = "No file uploaded."
#                     return render(request, "ingestion_template.html", context)

#                 headers = {
#                     "Authorization": f"Bearer {global_token}",
#                     "accept": "*/*",
#                 }

#                 temp_file_path = os.path.join(default_storage.location, uploaded_file.name)
#                 if not os.path.exists(default_storage.location):
#                     os.makedirs(default_storage.location)

#                 with default_storage.open(temp_file_path, 'wb+') as temp_file:
#                     for chunk in uploaded_file.chunks():
#                         temp_file.write(chunk)

#                 with open(temp_file_path, 'rb') as file:
#                     files = {'file': file}
#                     response = requests.post(
#                         "https://uat.business.api.elsevier.com/v1/funding-ingestion/vtool",
#                         headers=headers,
#                         files=files,
#                     )

#                 if response.status_code == 200:
#                     batch_id = response.json().get("batchId")
#                     if batch_id:
#                         context["batch_id"] = batch_id
#                         context["message"] = f"Batch created successfully! Batch ID: {batch_id}"
#                         logging.info(f"Batch created successfully! Batch ID: {batch_id}")
#                     else:
#                         context["message"] = "Batch creation successful but no batch ID returned."
#                         logging.warning("Batch creation successful but no batch ID returned.")
#                 else:
#                     context["message"] = f"Failed to create batch. Response Code: {response.status_code}"
#                     logging.error(f"Failed to create batch. Response Code: {response.status_code}")

#             elif action == "ingest_file":
#                 if not global_token:
#                     context["message"] = "Token is not available. Please generate a token first."
#                     return render(request, "ingestion_template.html", context)

#                 ingestion_type = form.cleaned_data["ingestion_type"]
#                 batch_id = request.POST.get("batch_id")
#                 file = request.FILES.get("json_location")
#                 data_type = form.cleaned_data["data_type"]

#                 if not file:
#                     context["message"] = "No file provided for ingestion."
#                     return render(request, "ingestion_template.html", context)

#                 base_url = "https://uat.business.api.elsevier.com/v1/funding-ingestion"
#                 url = f"{base_url}/{data_type}"
#                 if ingestion_type == "batch":
#                     url += "/bulk"

#                 headers = {
#                     "accept": "application/json",
#                     "callbackUrl": "https://callbackapi-elsevier.mpsinsight.com/callbackapi/callback",
#                     "Content-Type": "application/json",
#                     "batchId": batch_id,
#                     "Authorization": f"Bearer {global_token}",
#                 }

#                 try:
#                     response = requests.post(url, headers=headers, data=file.read())
#                     ingestion_response = response.json()

#                     ingestion_id = ingestion_response.get("ingestionId")
#                     ingestion_item_id = ingestion_response.get("id")

#                     if ingestion_id and ingestion_item_id:
#                         log_message = (
#                             f"Timestamp: {datetime.now()} - "
#                             f"Ingestion ID: {ingestion_id}, ID: {ingestion_item_id}, Batch ID: {batch_id}"
#                         )
#                         logging.info(log_message)

#                     if response.status_code == 200:
#                         context["message"] = "File ingested successfully!"
#                     else:
#                         context["message"] = f"Failed to ingest file: {response.text}"
#                         logging.error(f"Failed to ingest file: {response.text}")

#                 except Exception as e:
#                     context["message"] = "An error occurred during file ingestion."
#                     logging.exception(f"Exception occurred during file ingestion: {e}")

#     return render(request, "ingestion_template.html", context)

#date 13-01-2025
# import os
# import base64
# import logging
# import requests
# from datetime import datetime
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from django.core.files.storage import default_storage
# from .forms import FileIngestionForm

# # Create logs directory in the project root
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# LOG_DIR = os.path.join(BASE_DIR, "logs")
# if not os.path.exists(LOG_DIR):
#     os.makedirs(LOG_DIR)

# # Configure logging
# LOG_FILE = os.path.join(LOG_DIR, "ingestion_details.log")
# logging.basicConfig(
#     filename=LOG_FILE,
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

# # Global token variable
# global_token = None


# def get_oauth_token(key, secret):
#     url = "https://uat.business.api.elsevier.com/token"
#     credentials = f"{key}:{secret}"
#     encoded_credentials = base64.b64encode(credentials.encode()).decode()
#     headers = {
#         "Authorization": f"Basic {encoded_credentials}",
#         "Content-Type": "application/x-www-form-urlencoded",
#     }
#     data = {"grant_type": "client_credentials"}
#     response = requests.post(url, headers=headers, data=data)
#     if response.status_code == 200:
#         return response.json().get("access_token")
#     return None


# @csrf_exempt
# def file_ingestion(request):
#     global global_token
#     context = {"form": FileIngestionForm()}

#     if request.method == "POST":
#         form = FileIngestionForm(request.POST, request.FILES)

#         if form.is_valid():
#             action = form.cleaned_data["action"]
#             user_name = form.cleaned_data.get("user_name", "Unknown User")  # Default to 'Unknown User' if not provided

#             if action == "generate_token":
#                 key = "H0g93ZOVfg77MoAKCTLvCZZtTFoBir2o"  # Replace with your actual key
#                 secret = "T9wS2s4wUQG31k6kv2lJ0SCbNdhHuDgv"  # Replace with your actual secret
#                 global_token = get_oauth_token(key, secret)
#                 context["token"] = global_token
#                 context["message"] = "Token generated successfully!" if global_token else "Failed to generate token."
#                 log_message = f"User: {user_name} - Token generation status: {'Success' if global_token else 'Failure'}"
#                 logging.info(log_message)

#             elif action == "create_batch":
#                 if not global_token:
#                     context["message"] = "Token is not available. Please generate a token first."
#                     return render(request, "ingestion_template.html", context)

#                 uploaded_file = request.FILES.get("file_location")
#                 if not uploaded_file:
#                     context["message"] = "No file uploaded."
#                     return render(request, "ingestion_template.html", context)

#                 headers = {
#                     "Authorization": f"Bearer {global_token}",
#                     "accept": "*/*",
#                 }

#                 temp_file_path = os.path.join(default_storage.location, uploaded_file.name)
#                 if not os.path.exists(default_storage.location):
#                     os.makedirs(default_storage.location)

#                 with default_storage.open(temp_file_path, 'wb+') as temp_file:
#                     for chunk in uploaded_file.chunks():
#                         temp_file.write(chunk)

#                 with open(temp_file_path, 'rb') as file:
#                     files = {'file': file}
#                     response = requests.post(
#                         "https://uat.business.api.elsevier.com/v1/funding-ingestion/vtool",
#                         headers=headers,
#                         files=files,
#                     )

#                 if response.status_code == 200:
#                     batch_id = response.json().get("batchId")
#                     if batch_id:
#                         context["batch_id"] = batch_id
#                         context["message"] = f"Batch created successfully! Batch ID: {batch_id}"
#                         log_message = f"User: {user_name} - Batch created successfully! Batch ID: {batch_id}"
#                         logging.info(log_message)
#                     else:
#                         context["message"] = "Batch creation successful but no batch ID returned."
#                         logging.warning(f"User: {user_name} - Batch creation successful but no batch ID returned.")
#                 else:
#                     context["message"] = f"Failed to create batch. Response Code: {response.status_code}"
#                     logging.error(f"User: {user_name} - Failed to create batch. Response Code: {response.status_code}")

#             elif action == "ingest_file":
#                 if not global_token:
#                     context["message"] = "Token is not available. Please generate a token first."
#                     return render(request, "ingestion_template.html", context)

#                 ingestion_type = form.cleaned_data["ingestion_type"]
#                 batch_id = request.POST.get("batch_id")
#                 file = request.FILES.get("json_location")
#                 data_type = form.cleaned_data["data_type"]

#                 if not file:
#                     context["message"] = "No file provided for ingestion."
#                     return render(request, "ingestion_template.html", context)

#                 base_url = "https://uat.business.api.elsevier.com/v1/funding-ingestion"
#                 url = f"{base_url}/{data_type}"
#                 if ingestion_type == "batch":
#                     url += "/bulk"

#                 headers = {
#                     "accept": "application/json",
#                     "callbackUrl": "https://callbackapi-elsevier.mpsinsight.com/callbackapi/callback",
#                     "Content-Type": "application/json",
#                     "batchId": batch_id,
#                     "Authorization": f"Bearer {global_token}",
#                 }

#                 try:
#                     response = requests.post(url, headers=headers, data=file.read())
#                     ingestion_response = response.json()

#                     ingestion_id = ingestion_response.get("ingestionId")
#                     ingestion_item_id = ingestion_response.get("id")

#                     if ingestion_id and ingestion_item_id:
#                         log_message = (
#                             f"User: {user_name} - Timestamp: {datetime.now()} - "
#                             f"Ingestion ID: {ingestion_id}, ID: {ingestion_item_id}, Batch ID: {batch_id}"
#                         )
#                         logging.info(log_message)

#                     if response.status_code == 200:
#                         context["message"] = "File ingested successfully!"
#                     else:
#                         context["message"] = f"Failed to ingest file: {response.text}"
#                         logging.error(f"User: {user_name} - Failed to ingest file: {response.text}")

#                 except Exception as e:
#                     context["message"] = "An error occurred during file ingestion."
#                     logging.exception(f"User: {user_name} - Exception occurred during file ingestion: {e}")

#     return render(request, "ingestion_template.html", context)


# import os
# import base64
# import logging
# import requests
# from datetime import datetime
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from django.core.files.storage import default_storage
# from .forms import FileIngestionForm

# # Create logs directory in the project root
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# LOG_DIR = os.path.join(BASE_DIR, "logs")
# if not os.path.exists(LOG_DIR):
#     os.makedirs(LOG_DIR)

# # Configure logging
# LOG_FILE = os.path.join(LOG_DIR, "ingestion_details.log")
# logging.basicConfig(
#     filename=LOG_FILE,
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

# # Global token variable
# global_token = None


# def get_oauth_token(key, secret):
#     url = "https://uat.business.api.elsevier.com/token"
#     credentials = f"{key}:{secret}"
#     encoded_credentials = base64.b64encode(credentials.encode()).decode()
#     headers = {
#         "Authorization": f"Basic {encoded_credentials}",
#         "Content-Type": "application/x-www-form-urlencoded",
#     }
#     data = {"grant_type": "client_credentials"}
#     response = requests.post(url, headers=headers, data=data)
#     if response.status_code == 200:
#         return response.json().get("access_token")
#     return None


# @csrf_exempt
# def file_ingestion(request):
#     global global_token
#     context = {"form": FileIngestionForm()}

#     if request.method == "POST":
#         form = FileIngestionForm(request.POST, request.FILES)

#         if form.is_valid():
#             action = form.cleaned_data["action"]
#             user_name = form.cleaned_data.get("user_name", "Unknown User")  # Default to 'Unknown User' if not provided

#             if action == "generate_token":
#                 key = "H0g93ZOVfg77MoAKCTLvCZZtTFoBir2o"  # Replace with your actual key
#                 secret = "T9wS2s4wUQG31k6kv2lJ0SCbNdhHuDgv"  # Replace with your actual secret
#                 global_token = get_oauth_token(key, secret)
#                 context["token"] = global_token
#                 context["message"] = "Token generated successfully!" if global_token else "Failed to generate token."
#                 log_message = f"User: {user_name} - Token generation status: {'Success' if global_token else 'Failure'}"
#                 logging.info(log_message)

#             elif action == "create_batch":
#                 if not global_token:
#                     context["message"] = "Token is not available. Please generate a token first."
#                     return render(request, "ingestion_template.html", context)

#                 uploaded_file = request.FILES.get("file_location")
#                 if not uploaded_file:
#                     context["message"] = "No file uploaded."
#                     return render(request, "ingestion_template.html", context)

#                 headers = {
#                     "Authorization": f"Bearer {global_token}",
#                     "accept": "*/*",
#                 }

#                 temp_file_path = os.path.join(default_storage.location, uploaded_file.name)
#                 if not os.path.exists(default_storage.location):
#                     os.makedirs(default_storage.location)

#                 with default_storage.open(temp_file_path, 'wb+') as temp_file:
#                     for chunk in uploaded_file.chunks():
#                         temp_file.write(chunk)

#                 with open(temp_file_path, 'rb') as file:
#                     files = {'file': file}
#                     response = requests.post(
#                         "https://uat.business.api.elsevier.com/v1/funding-ingestion/vtool",
#                         headers=headers,
#                         files=files,
#                     )

#                 if response.status_code == 200:
#                     batch_id = response.json().get("batchId")
#                     if batch_id:
#                         context["batch_id"] = batch_id
#                         context["message"] = f"Batch created successfully! Batch ID: {batch_id}"
#                         log_message = f"User: {user_name} - Batch created successfully! Batch ID: {batch_id}"
#                         logging.info(log_message)
#                     else:
#                         context["message"] = "Batch creation successful but no batch ID returned."
#                         logging.warning(f"User: {user_name} - Batch creation successful but no batch ID returned.")
#                 else:
#                     context["message"] = f"Failed to create batch. Response Code: {response.status_code}"
#                     logging.error(f"User: {user_name} - Failed to create batch. Response Code: {response.status_code}")

#             elif action == "ingest_file":
#                 if not global_token:
#                     context["message"] = "Token is not available. Please generate a token first."
#                     return render(request, "ingestion_template.html", context)

#                 ingestion_type = form.cleaned_data["ingestion_type"]
#                 batch_id = request.POST.get("batch_id")
#                 file = request.FILES.get("json_location")
#                 data_type = form.cleaned_data["data_type"]

#                 if not file:
#                     context["message"] = "No file provided for ingestion."
#                     return render(request, "ingestion_template.html", context)

#                 base_url = "https://uat.business.api.elsevier.com/v1/funding-ingestion"
#                 url = f"{base_url}/{data_type}"
#                 if ingestion_type == "batch":
#                     url += "/bulk"

#                 headers = {
#                     "accept": "application/json",
#                     "callbackUrl": "https://callbackapi-elsevier.mpsinsight.com/callbackapi/callback",
#                     "Content-Type": "application/json",
#                     "batchId": batch_id,
#                     "Authorization": f"Bearer {global_token}",
#                 }

#                 try:
#                     response = requests.post(url, headers=headers, data=file.read())
#                     ingestion_response = response.json()

#                     ingestion_id = ingestion_response.get("ingestionId")
#                     ingestion_item_id = ingestion_response.get("id")

#                     if ingestion_id and ingestion_item_id:
#                         log_message = (
#                             f"User: {user_name} - Timestamp: {datetime.now()} - "
#                             f"Ingestion ID: {ingestion_id}, ID: {ingestion_item_id}, Batch ID: {batch_id}"
#                         )
#                         logging.info(log_message)

#                     if response.status_code == 200:
#                         context["message"] = "File ingested successfully!"
#                     else:
#                         context["message"] = f"Failed to ingest file: {response.text}"
#                         logging.error(f"User: {user_name} - Failed to ingest file: {response.text}")

#                 except Exception as e:
#                     context["message"] = "An error occurred during file ingestion."
#                     logging.exception(f"User: {user_name} - Exception occurred during file ingestion: {e}")

#     return render(request, "ingestion_template.html", context)


#now 17:40

from django import forms
import os
import base64
import logging
import requests
from datetime import datetime
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .forms import FileIngestionForm

# Create logs directory in the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging
LOG_FILE = os.path.join(LOG_DIR, "ingestion_details.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Global token variable
global_token = None


def get_oauth_token(key, secret):
    url = "https://uat.business.api.elsevier.com/token"
    credentials = f"{key}:{secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None


@csrf_exempt
def file_ingestion(request):
    global global_token
    context = {"form": FileIngestionForm()}

    if request.method == "POST":
        form = FileIngestionForm(request.POST, request.FILES)

        if form.is_valid():
            action = form.cleaned_data["action"]
            # Ensure `user_name` defaults to "Unknown User" if not provided
            user_name = form.cleaned_data.get("user_name", "Unknown User")

            # Debugging log to verify if user_name is correctly passed from the form
            logging.info(f"Form submitted by user: {user_name}")

            if action == "generate_token":
                key = "H0g93ZOVfg77MoAKCTLvCZZtTFoBir2o"  # Replace with your actual key
                secret = "T9wS2s4wUQG31k6kv2lJ0SCbNdhHuDgv"  # Replace with your actual secret
                global_token = get_oauth_token(key, secret)
                context["token"] = global_token
                context["message"] = (
                    "Token generated successfully!" if global_token else "Failed to generate token."
                )
                log_message = f"User: {user_name} - Token generation status: {'Success' if global_token else 'Failure'}"
                logging.info(log_message)

            elif action == "create_batch":
                if not global_token:
                    context["message"] = "Token is not available. Please generate a token first."
                    return render(request, "ingestion_template.html", context)

                uploaded_file = request.FILES.get("file_location")
                if not uploaded_file:
                    context["message"] = "No file uploaded."
                    return render(request, "ingestion_template.html", context)

                headers = {
                    "Authorization": f"Bearer {global_token}",
                    "accept": "*/*",
                }

                temp_file_path = os.path.join(default_storage.location, uploaded_file.name)
                if not os.path.exists(default_storage.location):
                    os.makedirs(default_storage.location)

                with default_storage.open(temp_file_path, 'wb+') as temp_file:
                    for chunk in uploaded_file.chunks():
                        temp_file.write(chunk)

                with open(temp_file_path, 'rb') as file:
                    files = {'file': file}
                    response = requests.post(
                        "https://uat.business.api.elsevier.com/v1/funding-ingestion/vtool",
                        headers=headers,
                        files=files,
                    )

                if response.status_code == 200:
                    batch_id = response.json().get("batchId")
                    if batch_id:
                        context["batch_id"] = batch_id
                        context["message"] = f"Batch created successfully! Batch ID: {batch_id}"
                        log_message = f"User: {user_name} - Batch created successfully! Batch ID: {batch_id}"
                        logging.info(log_message)
                    else:
                        context["message"] = "Batch creation successful but no batch ID returned."
                        logging.warning(f"User: {user_name} - Batch creation successful but no batch ID returned.")
                else:
                    context["message"] = f"Failed to create batch. Response Code: {response.status_code}"
                    logging.error(f"User: {user_name} - Failed to create batch. Response Code: {response.status_code}")

            elif action == "ingest_file":
                if not global_token:
                    context["message"] = "Token is not available. Please generate a token first."
                    return render(request, "ingestion_template.html", context)

                ingestion_type = form.cleaned_data["ingestion_type"]
                batch_id = request.POST.get("batch_id")
                file = request.FILES.get("json_location")
                data_type = form.cleaned_data["data_type"]

                if not file:
                    context["message"] = "No file provided for ingestion."
                    return render(request, "ingestion_template.html", context)

                base_url = "https://uat.business.api.elsevier.com/v1/funding-ingestion"
                url = f"{base_url}/{data_type}"
                if ingestion_type == "batch":
                    url += "/bulk"

                headers = {
                    "accept": "application/json",
                    "callbackUrl": "https://callbackapi-elsevier.mpsinsight.com/callbackapi/callback",
                    "Content-Type": "application/json",
                    "batchId": batch_id,
                    "Authorization": f"Bearer {global_token}",
                }

                try:
                    response = requests.post(url, headers=headers, data=file.read())
                    ingestion_response = response.json()

                    ingestion_id = ingestion_response.get("ingestionId")
                    ingestion_item_id = ingestion_response.get("id")

                    if ingestion_id and ingestion_item_id:
                        log_message = (
                            f"User: {user_name} - Timestamp: {datetime.now()} - "
                            f"Ingestion ID: {ingestion_id}, ID: {ingestion_item_id}, Batch ID: {batch_id}"
                        )
                        logging.info(log_message)

                    if response.status_code == 200:
                        context["message"] = "File ingested successfully!"
                    else:
                        context["message"] = f"Failed to ingest file: {response.text}"
                        logging.error(f"User: {user_name} - Failed to ingest file: {response.text}")

                except Exception as e:
                    context["message"] = "An error occurred during file ingestion."
                    logging.exception(f"User: {user_name} - Exception occurred during file ingestion: {e}")

    return render(request, "ingestion_template.html", context)



# views.py   view for dashbaord
# import pandas as pd
# import matplotlib.pyplot as plt
# from io import BytesIO
# from django.shortcuts import render
# from .models import SourceMetadata
# from datetime import datetime
# import base64

# def dashboard_view(request):
#     # Fetch all source metadata records from MongoDB
#     source_metadata_list = SourceMetadata.objects.all()

#     # Convert QuerySet to list of dictionaries manually
#     data = []
#     for item in source_metadata_list:
#         data.append({
#             'import_url': item.import_url,
#             'date_of_arrival': item.date_of_arrival,
#             'assigned_to': item.assigned_to,
#             'frequency_of_site_updates': item.frequency_of_site_updates,
#             'site_last_checked': item.site_last_checked,
#             'source_file_upload': item.source_file_upload,
#             'json_file_name': item.json_file_name,
#             'json_upload_date': item.json_upload_date,
#             'sup_id': item.sup_id,
#             'sme_comments': item.sme_comments,
#             'screenshots_taken': item.screenshots_taken,
#             'qa_comment': item.qa_comment,
#             'qa_name': item.qa_name,
#             'file_status': item.file_status,
#             'qa_issue': item.qa_issue,
#             'created_at': item.created_at,
#         })

#     # Convert the data to a Pandas DataFrame for easy processing
#     df = pd.DataFrame(data)

#     # Calculate metrics for the dashboard
#     if not df.empty:
#         total_sources = len(df)
#         total_files = df['source_file_upload'].notna().sum()
#         qa_pending = df[df['file_status'] == 'Pending'].shape[0]
#         completed_tasks = df[df['file_status'] == 'Completed'].shape[0]
#         in_progress_tasks = df[df['file_status'] == 'In Progress'].shape[0]

#         # Prepare the data for chart (Tasks per User)
#         user_task_counts = df['assigned_to'].value_counts()

#         # Create Matplotlib chart (Bar Chart)
#         fig, ax = plt.subplots(figsize=(10, 6))
#         ax.bar(user_task_counts.index, user_task_counts.values, color='skyblue')

#         ax.set_xlabel('Users')
#         ax.set_ylabel('Number of Tasks')
#         ax.set_title('Tasks per User')

#         # Save the chart to a BytesIO object to embed it in the HTML
#         buf = BytesIO()
#         plt.tight_layout()
#         fig.savefig(buf, format='png')
#         buf.seek(0)
#         chart_data = base64.b64encode(buf.read()).decode('utf-8')
#         buf.close()
#     else:
#         total_sources = total_files = qa_pending = completed_tasks = in_progress_tasks = 0
#         chart_data = None

#     context = {
#         'total_sources': total_sources,
#         'total_files': total_files,
#         'qa_pending': qa_pending,
#         'completed_tasks': completed_tasks,
#         'in_progress_tasks': in_progress_tasks,
#         'source_metadata_list': source_metadata_list,
#         'chart_data': chart_data,  # Pass the chart data to the template
#     }

#     return render(request, 'dashboard.html', context)


#coreect code27-01-2025
# import pandas as pd
# import matplotlib.pyplot as plt
# from io import BytesIO
# from django.shortcuts import render
# from .models import SourceMetadata
# from datetime import datetime
# import base64

# def dashboard_view(request):
#     # Fetch all source metadata records from MongoDB
#     source_metadata_list = SourceMetadata.objects.all()

#     # Convert QuerySet to list of dictionaries manually
#     data = []
#     for item in source_metadata_list:
#         data.append({
#             'import_url': item.import_url,
#             'date_of_arrival': item.date_of_arrival,
#             'assigned_to': item.assigned_to,
#             'frequency_of_site_updates': item.frequency_of_site_updates,
#             'site_last_checked': item.site_last_checked,
#             'source_file_upload': item.source_file_upload,
#             'json_file_name': item.json_file_name,
#             'json_upload_date': item.json_upload_date,
#             'sup_id': item.sup_id,
#             'sme_comments': item.sme_comments,
#             'screenshots_taken': item.screenshots_taken,
#             'qa_comment': item.qa_comment,
#             'qa_name': item.qa_name,
#             'file_status': item.file_status,
#             'qa_issue': item.qa_issue,
#             'created_at': item.created_at,
#         })

#     # Convert the data to a Pandas DataFrame for easy processing
#     df = pd.DataFrame(data)

#     # Calculate metrics for the dashboard
#     if not df.empty:
#         total_sources = len(df)
#         total_files = df['source_file_upload'].notna().sum()
#         qa_pending = df[df['file_status'] == 'Pending'].shape[0]
#         completed_tasks = df[df['file_status'] == 'Completed'].shape[0]
#         in_progress_tasks = df[df['file_status'] == 'In Progress'].shape[0]
        
#         # Calculate Accepted and Rejected Files
#         accepted_files = df[df['file_status'] == 'Accepted'].shape[0]
#         rejected_files = df[df['file_status'] == 'Rejected'].shape[0]

#         # Prepare the data for chart (Tasks per User)
#         user_task_counts = df['assigned_to'].value_counts()

#         # Create Matplotlib chart (Bar Chart)
#         fig, ax = plt.subplots(figsize=(10, 6))
#         ax.bar(user_task_counts.index, user_task_counts.values, color='skyblue')

#         ax.set_xlabel('Users')
#         ax.set_ylabel('Number of Tasks')
#         ax.set_title('Tasks per User')

#         # Save the chart to a BytesIO object to embed it in the HTML
#         buf = BytesIO()
#         plt.tight_layout()
#         fig.savefig(buf, format='png')
#         buf.seek(0)
#         chart_data = base64.b64encode(buf.read()).decode('utf-8')
#         buf.close()
#     else:
#         total_sources = total_files = qa_pending = completed_tasks = in_progress_tasks = 0
#         accepted_files = rejected_files = 0
#         chart_data = None

#     context = {
#         'total_sources': total_sources,
#         'total_files': total_files,
#         'qa_pending': qa_pending,
#         'completed_tasks': completed_tasks,
#         'in_progress_tasks': in_progress_tasks,
#         'accepted_files': accepted_files,  # Pass accepted file count to the template
#         'rejected_files': rejected_files,  # Pass rejected file count to the template
#         'source_metadata_list': source_metadata_list,
#         'chart_data': chart_data,  # Pass the chart data to the template
#     }

#     return render(request, 'dashboard.html', context)


#corect code on 3:44 date 27-01-2025
# import pandas as pd
# import matplotlib.pyplot as plt
# from io import BytesIO
# from django.shortcuts import render
# from .models import SourceMetadata
# from collections import defaultdict
# import base64

# def dashboard_view(request):
#     # Fetch all source metadata records from MongoDB
#     source_metadata_list = SourceMetadata.objects.all()

#     # Convert QuerySet to list of dictionaries manually
#     data = []
#     for item in source_metadata_list:
#         data.append({
#             'import_url': item.import_url,
#             'date_of_arrival': item.date_of_arrival,
#             'assigned_to': item.assigned_to,
#             'frequency_of_site_updates': item.frequency_of_site_updates,
#             'site_last_checked': item.site_last_checked,
#             'source_file_upload': item.source_file_upload,
#             'json_file_name': item.json_file_name,
#             'json_upload_date': item.json_upload_date,
#             'sup_id': item.sup_id,
#             'sme_comments': item.sme_comments,
#             'screenshots_taken': item.screenshots_taken,
#             'qa_comment': item.qa_comment,
#             'qa_name': item.qa_name,
#             'file_status': item.file_status,
#             'qa_issue': item.qa_issue,
#             'created_at': item.created_at,
#         })

#     # Convert the data to a Pandas DataFrame for easy processing
#     df = pd.DataFrame(data)

#     # Initialize variables for dashboard metrics
#     total_sources = total_files = qa_pending = completed_tasks = in_progress_tasks = 0
#     accepted_files = rejected_files = 0
#     user_metrics = defaultdict(lambda: {
#         'total_files': 0,
#         'accepted': 0,
#         'rejected': 0,
#         'in_progress': 0,
#         'reprocessing': 0,
#         'qa_name': None,
#     })

#     # Calculate metrics if the DataFrame is not empty
#     if not df.empty:
#         total_sources = len(df)
#         total_files = df['source_file_upload'].notna().sum()
#         qa_pending = df[df['file_status'] == 'Pending'].shape[0]
#         completed_tasks = df[df['file_status'] == 'Completed'].shape[0]
#         in_progress_tasks = df[df['file_status'] == 'In Progress'].shape[0]

#         # Calculate Accepted and Rejected Files
#         accepted_files = df[df['file_status'] == 'Accepted'].shape[0]
#         rejected_files = df[df['file_status'] == 'Rejected'].shape[0]

#         # Prepare user-specific metrics
#         for _, row in df.iterrows():
#             user = row['assigned_to']
#             user_metrics[user]['total_files'] += 1
#             user_metrics[user]['qa_name'] = row['qa_name']

#             if row['file_status'] == 'Accepted':
#                 user_metrics[user]['accepted'] += 1
#             elif row['file_status'] == 'Rejected':
#                 user_metrics[user]['rejected'] += 1
#             elif row['file_status'] == 'In Progress':
#                 user_metrics[user]['in_progress'] += 1
#             elif row['file_status'] == 'Reprocessing':
#                 user_metrics[user]['reprocessing'] += 1

#         # Prepare the data for chart (Tasks per User)
#         user_task_counts = df['assigned_to'].value_counts()

#         # Create Matplotlib chart (Bar Chart)
#         fig, ax = plt.subplots(figsize=(10, 6))
#         ax.bar(user_task_counts.index, user_task_counts.values, color='#f5a142')

#         ax.set_xlabel('Users')
#         ax.set_ylabel('Number of Tasks')
#         ax.set_title('Tasks per User')

#         # Save the chart to a BytesIO object to embed it in the HTML
#         buf = BytesIO()
#         plt.tight_layout()
#         fig.savefig(buf, format='png')
#         buf.seek(0)
#         chart_data = base64.b64encode(buf.read()).decode('utf-8')
#         buf.close()

#     context = {
#         'total_sources': total_sources,
#         'total_files': total_files,
#         'qa_pending': qa_pending,
#         'completed_tasks': completed_tasks,
#         'in_progress_tasks': in_progress_tasks,
#         'accepted_files': accepted_files,
#         'rejected_files': rejected_files,
#         'chart_data': chart_data,
#         'user_metrics': user_metrics.items(),  # Ensure items() is passed
#     }

#     return render(request, 'dashboard.html', context)
from django.contrib.auth.models import User
from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from collections import defaultdict
import base64
from .models import SourceMetadata

def dashboard_view(request):
    # Fetch all source metadata records from MongoDB
    source_metadata_list = SourceMetadata.objects.all()

    # Convert QuerySet to list of dictionaries manually
    data = []
    for item in source_metadata_list:
        data.append({
            'import_url': item.import_url,
            'date_of_arrival': item.date_of_arrival,
            'assigned_to': item.assigned_to,
            'frequency_of_site_updates': item.frequency_of_site_updates,
            'site_last_checked': item.site_last_checked,
            'source_file_upload': item.source_file_upload,
            'json_file_name': item.json_file_name,
            'json_upload_date': item.json_upload_date,
            'sup_id': item.sup_id,
            'sme_comments': item.sme_comments,
            'screenshots_taken': item.screenshots_taken,
            'qa_comment': item.qa_comment,
            'qa_name': item.qa_name,
            'file_status': item.file_status,
            'qa_issue': item.qa_issue,
            'created_at': item.created_at,
        })

    # Convert the data to a Pandas DataFrame for easy processing
    df = pd.DataFrame(data)

    # Initialize variables for dashboard metrics
    total_sources = total_files = qa_pending = completed_tasks = in_progress_tasks = 0
    accepted_files = rejected_files = 0
    user_metrics = defaultdict(lambda: {
        'total_files': 0,
        'accepted': 0,
        'rejected': 0,
        'in_progress': 0,
        'reprocessing': 0,
        'qa_name': None,
    })

    # Calculate metrics if the DataFrame is not empty
    if not df.empty:
        total_sources = len(df)
        total_files = df['source_file_upload'].notna().sum()
        qa_pending = df[df['file_status'] == 'Pending'].shape[0]
        completed_tasks = df[df['file_status'] == 'Completed'].shape[0]
        in_progress_tasks = df[df['file_status'] == 'In Progress'].shape[0]

        # Calculate Accepted and Rejected Files
        accepted_files = df[df['file_status'] == 'Accepted'].shape[0]
        rejected_files = df[df['file_status'] == 'Rejected'].shape[0]

        # Prepare user-specific metrics
        for _, row in df.iterrows():
            user = row['assigned_to']
            user_metrics[user]['total_files'] += 1
            user_metrics[user]['qa_name'] = row['qa_name']

            if row['file_status'] == 'Accepted':
                user_metrics[user]['accepted'] += 1
            elif row['file_status'] == 'Rejected':
                user_metrics[user]['rejected'] += 1
            elif row['file_status'] == 'In Progress':
                user_metrics[user]['in_progress'] += 1
            elif row['file_status'] == 'Reprocessing':
                user_metrics[user]['reprocessing'] += 1

        # Prepare the data for chart (Tasks per User)
        user_task_counts = df['assigned_to'].value_counts()

        # Create Matplotlib chart (Bar Chart) for Tasks per User
        fig, ax = plt.subplots(figsize=(9, 6))
        ax.bar(user_task_counts.index, user_task_counts.values, color='#f5a142')

        ax.set_xlabel('Users')
        ax.set_ylabel('Number of Tasks')
        ax.set_title('Tasks per User')

        # Save the bar chart to a BytesIO object to embed it in the HTML
        buf = BytesIO()
        plt.tight_layout()
        fig.savefig(buf, format='png')
        buf.seek(0)
        chart_data = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        # Create Pie Chart for User Work Distribution
        user_work_distribution = user_task_counts.values
        user_labels = user_task_counts.index

        # Create Pie Chart
        fig_pie, ax_pie = plt.subplots(figsize=(6.5, 6.5))
        ax_pie.pie(user_work_distribution, labels=user_labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        ax_pie.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Save the pie chart to a BytesIO object to embed it in the HTML
        buf_pie = BytesIO()
        fig_pie.savefig(buf_pie, format='png')
        buf_pie.seek(0)
        pie_chart_data = base64.b64encode(buf_pie.read()).decode('utf-8')
        buf_pie.close()

    # Count total users
    total_users = User.objects.count()

    context = {
        'total_sources': total_sources,
        'total_files': total_files,
        'qa_pending': qa_pending,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'accepted_files': accepted_files,
        'rejected_files': rejected_files,
        'chart_data': chart_data,  # Bar chart
        'pie_chart_data': pie_chart_data,  # Pie chart
        'user_metrics': user_metrics.items(),  # Ensure items() is passed
        'total_users': total_users,  # Include total users
    }

    return render(request, 'dashboard.html', context)





#json creation view code
# import os
# import json
# from django.shortcuts import render
# from .forms import CSVInputForm
# from .utils import s_date,format_date,generate_small_hash_uuid,generate_small_hash_AID,get_and_update_ids,process_csv_to_json # Assuming you have these functions defined
 
# def upload_file(request):
#     if request.method == 'POST':
#         form = CSVInputForm(request.POST, request.FILES)
#         if form.is_valid():
#             csv_file_path = form.cleaned_data['csv_file_path']
#             output_directory = form.cleaned_data['output_directory']
 
#             # Ensure the output directory exists
#             os.makedirs(output_directory, exist_ok=True)
 
#             # Process the provided CSV file path
#             json_filename = os.path.splitext(os.path.basename(csv_file_path))[0] + '.json'
#             json_output_path = os.path.join(output_directory, json_filename)
 
#             # Process the CSV and generate JSON
#             process_csv_to_json(csv_file_path, json_output_path)
 
#             # Read the generated JSON file and clean it (if you have clean_data defined)
#             with open(json_output_path, 'r', encoding='utf-8-sig') as file:
#                 data = json.load(file)
 
#             cleaned_data = clean_data(data)  # Assuming this function is defined elsewhere
#             final_data = remove_outermost(cleaned_data)  # Assuming this function is defined elsewhere
#             # Save cleaned JSON data to a new file
#             cleaned_json_filename = os.path.splitext(json_filename)[0] + '_N.json'
#             cleaned_json_output_path = os.path.join(output_directory, cleaned_json_filename)
#             with open(cleaned_json_output_path, 'w', encoding='utf-8') as file:
#                 json.dump(final_data, file, ensure_ascii=False, separators=(',', ':'))
 
#             return render(request, 'upload_file.html', {'form': form, 'success': True,
#                                                              'cleaned_json_path': cleaned_json_output_path})
#     else:
#         form = CSVInputForm()
#     return render(request, 'upload_file.html', {'form': form})

#json creator  code ##############################

import os
import json
from django.shortcuts import render
from .forms import CSVInputForm
from .utils import process_csv_to_json

def upload_file(request):
    if request.method == 'POST':
        form = CSVInputForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']  # Get the uploaded file
            output_directory = form.cleaned_data['output_directory']

            os.makedirs(output_directory, exist_ok=True)  # Ensure output directory exists

            # Save the uploaded file to the output directory
            csv_file_path = os.path.join(output_directory, csv_file.name)
            with open(csv_file_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)

            # Process the CSV file
            json_filename = os.path.splitext(csv_file.name)[0] + '.json'
            json_output_path = os.path.join(output_directory, json_filename)

            process_csv_to_json(csv_file_path, json_output_path)

            return render(request, 'upload_file.html', {'form': form, 'success': True, 'cleaned_json_path': json_output_path})
    else:
        form = CSVInputForm()

    return render(request, 'upload_file.html', {'form': form})


################ending the json creator code#####################
#####################################################################



################# v tool code ##########################
#########################################################################
from django.shortcuts import render
from django.http import JsonResponse
import subprocess
 
def vtooltemp(request):
    if request.method == 'POST':
        input_file_path = request.POST.get('input_file')  # Get JSON file path from frontend
        log_file_path = request.POST.get('log_file')  # Get log file path from frontend

        try:
            # Define the path to the Vtool executable (change it if needed)
            vtool_path = r'X:/json_project_1/Vtool-5.93.1-p1/Vtool.jar'  # Adjust path as necessary

            # Build the command
            command = [vtool_path, '--vjson', 'grant', '-file', input_file_path, '-log', log_file_path]
            print(command)
            # Run the command
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            # Not Found: /run_java_tool/
            # Process the output
            output = result.stdout.strip()
            error = result.stderr.strip()

            return JsonResponse({'message': output, 'error': error})

        except Exception as e:
            return JsonResponse({'message': f'An error occurred: {str(e)}'}, status=500)

    return render(request, 'qa_process.html')