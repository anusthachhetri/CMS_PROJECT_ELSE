

# class JSONFile(models.Model):
#     batch_id = models.CharField(max_length=36, unique=True)  # Unique ID for the JSON file
#     file_name = models.CharField(max_length=255)
#     version = models.IntegerField(default=1)
#     uploaded_at = models.DateTimeField(auto_now_add=True)


# class JSONFile(models.Model):
#     uploader_name = models.CharField(max_length=100 )  # Uploader's name
#     batch_id = models.CharField(max_length=255, unique=True)  # Batch ID for the JSON file
#     file_name = models.CharField(max_length=255)  # File name
#     version = models.IntegerField(default=1)  # Versioning
#     uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp of upload
#     file_type = models.CharField(max_length=50)  # New field for file type
    
#     def __str__(self):
#         return self.file_name
#today    6/1/2024


from djongo import models as models

class JSONFile(models.Model):
    #_id = models.AutoField()
    ingestion_id = models.CharField(max_length=255, primary_key=True)
    uploader_name = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100)
    version = models.IntegerField(default=1)
    batch_id = models.CharField(max_length=255)
    unique_grant_id = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

    class Meta:
        db_table = "jsonfile"

    
    # def __str__(self):
    #     return f"{self.file_name} (Version {self.version})"
    
    
####################creating a new model for this 
# models.py
#from mongoengine import Document, StringField, DateField, DateTimeField, FileField, BooleanField
from bson import ObjectId
class SourceMetadata(models.Model):
    id = models.ObjectIdField(primary_key=True, default=ObjectId)
    #_id = models.AutoField()
    import_url = models.CharField(max_length=255)
    date_of_arrival = models.DateField()
    assigned_to = models.CharField(max_length=255, null=True, blank=True)
    frequency_of_site_updates = models.CharField(
        max_length=20,
        choices=[('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('Quarterly', 'Quarterly')],
    )
    site_last_checked = models.DateField()
    source_file_upload = models.CharField(max_length=255, null=True, blank=True)
    json_file_name = models.CharField(max_length=255, null=True, blank=True)
    json_upload_date = models.DateField(null=True, blank=True)
    sup_id = models.CharField(max_length=255, null=True, blank=True)
    sme_comments = models.TextField(null=True, blank=True)
    screenshots_taken = models.CharField(
        max_length=3,
        choices=[('Yes', 'Yes'), ('No', 'No')],
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # QA Fields
    file_status = models.CharField(
        max_length=10,
        choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected')],
        null=True,
        blank=True
    )
    qa_comment = models.TextField(null=True, blank=True)
    qa_name = models.CharField(max_length=255, null=True, blank=True)
    qa_issue = models.CharField(
        max_length=20,
        choices=[('batchid', 'Batch ID'), ('title', 'Title'), ('homepage', 'Homepage'), ('other', 'Other')],
        null=True,
        blank=True
    )

    class Meta:
        db_table = "source_metadata"

    def __str__(self):
        return self.import_url


    # def __str__(self):
    #     return f"{self.file_name} (Version {self.version})"
    
    
# model code for ingeston in uat db

from django.utils.timezone import now

class IngestionLog(models.Model):
    #_id = models.AutoField()
    user_name = models.CharField(max_length=255, default=None)
    ingestion_id = models.CharField(max_length=255, unique=True)
    ingestion_item_id = models.CharField(max_length=255, null=True, blank=True)
    batch_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Ingestion {self.ingestion_id} - {self.status}"

    class Meta:
        db_table = "ingestion_log"



# model code for ingeston in prod db

from django.utils.timezone import now

class IngestProd(models.Model):
    #_id = models.AutoField()
    user_name = models.CharField(max_length=255, default=None)
    ingestion_id = models.CharField(max_length=255, unique=True)
    ingestion_item_id = models.CharField(max_length=255, null=True, blank=True)
    batch_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Ingestion {self.ingestion_id} - {self.status}"

    class Meta:
        db_table = "ingestprod"



    
# class CustomUser(models.Model):
#     username = models.CharField(max_length=150, unique=True, null=True)  # Set null=True if needed
#     email = models.EmailField(max_length=255, null=True)
#     password = models.CharField(max_length=255)
    
################################################################################


#user login model code


# class JSONFileUpdateHistory(models.Model):
#     json_file = models.ForeignKey(
#         JSONFile,
#         on_delete=models.CASCADE,
#         related_name="update_history"
#     )  # Link to the original JSONFile
#     batch_id = models.CharField(max_length=36)               # Batch ID reference
#     version = models.IntegerField()                          # Updated version
#     updated_at = models.DateTimeField(auto_now_add=True)     # Timestamp for the update
#     update_details = models.JSONField()                      # Updated JSON content

#     def __str__(self):
#         return f"Update for {self.json_file.file_name} (Version {self.version})"

























# class Posts(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
#     caption = models.TextField(max_length=1000)
#     media = models.ImageField(blank=True, default="", upload_to="posts/")
#     tags = models.ManyToManyField('Tags', related_name='posts')