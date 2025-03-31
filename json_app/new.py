def upload_json(request):
    if request.method == 'POST':
        json_file = request.FILES.get('file')  # Safely access the file key
        if not json_file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        try:
            # Read JSON content
            json_data = json.load(json_file)

            # Detect or generate a batch ID
            if isinstance(json_data, list) and json_data:
                batch_id = json_data[0].get('batch_id', str(uuid.uuid4()))  # Use existing or generate a new batch_id
            elif isinstance(json_data, dict):
                batch_id = json_data.get('batch_id', str(uuid.uuid4()))
            else:
                return JsonResponse({'error': 'Invalid JSON format. Must be a list or dictionary.'}, status=400)

            # Save metadata to the model
            JSONFile.objects.create(
                batch_id=batch_id,
                file_name=json_file.name,
                version=1
            )

            # Insert JSON data into MongoDB
            if isinstance(json_data, list):
                for item in json_data:
                    item['batch_id'] = batch_id
                collection.insert_many(json_data)
            else:
                json_data['batch_id'] = batch_id
                collection.insert_one(json_data)

            return JsonResponse({'message': 'File uploaded successfully!', 'batch_id': batch_id})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON file format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    # Render the upload template for non-POST requests
    return render(request, 'upload.html')
