# from django import forms

# class JSONFileUploadForm(forms.Form):
#     json_file = forms.FileField()


# json_app/forms.py
#correct code 20/01/2025
# from django import forms

# class JSONFileUploadForm(forms.Form):
#     json_file = forms.FileField(label='Select a JSON file')
    
    
    
# #forms.py
# from django import forms
# from django.contrib.auth.models import User

# class SourceMetadataForm(forms.Form):
#     import_url = forms.URLField(label='Import URL', widget=forms.TextInput(attrs={'placeholder': 'Enter source URL'}))
#     date_of_arrival = forms.DateField(label='Date of Arrival', widget=forms.TextInput(attrs={'placeholder': 'dd-mm-yyyy', 'type': 'date'}))
#     # assigned_to = forms.CharField(label='Assigned To', widget=forms.TextInput(attrs={'placeholder': 'Assigned person\'s name'}))
     
    
    
#     # update on 20-1-2025 Populate the "Assigned To" dropdown dynamically with all usernames
#     assigned_to = forms.ChoiceField(
#         label='Assigned To',
#         choices=[],  # Empty initially
#         widget=forms.Select(attrs={'placeholder': 'Assigned person\'s name'})
#     )
    
#     # Populate "Assigned To" field choices dynamically
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         # Query all active users (you can filter users if necessary, e.g., only active users)
#         user_choices = [(user.username, user.username) for user in User.objects.all()]
        
#         # Add a blank option for selection (optional)
#         user_choices.insert(0, ('', 'Select Assigned User'))
        
#         # Update the "Assigned To" field's choices with the list of usernames
#         self.fields['assigned_to'].choices = user_choices
        
    
    
#     frequency_of_site_updates = forms.ChoiceField(
#         label='Frequency of Site Updates',
#         choices=[('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('Quarterly', 'Quarterly')],
#         widget=forms.Select()
#     )
#     site_last_checked = forms.DateField(label='Site Last Checked', widget=forms.TextInput(attrs={'placeholder': 'dd-mm-yyyy', 'type': 'date'}))
#     source_file_upload = forms.FileField(label='Source File Upload', required=False)
#     json_file_name = forms.CharField(label='JSON File Name', widget=forms.TextInput(attrs={'placeholder': 'Enter JSON file name'}), required=False)
#     json_upload_date = forms.DateField(label='JSON Upload Date', widget=forms.TextInput(attrs={'placeholder': 'dd-mm-yyyy', 'type': 'date'}), required=False)
#     sup_id = forms.CharField(label='SUP ID', widget=forms.TextInput(attrs={'placeholder': 'Enter SUP ID'}), required=False)
#     sme_comments = forms.CharField(label='SME Comments', widget=forms.Textarea(attrs={'placeholder': 'Enter any comments', 'rows': 4}), required=False)
#     screenshots_taken = forms.ChoiceField(
#         label='Screenshots Taken',
#         choices=[('Yes', 'Yes'), ('No', 'No')],
#         widget=forms.Select()
#     )

# # New fields for QA
#     qa_comment = forms.CharField(label='QA Comment', widget=forms.Textarea(attrs={'placeholder': 'Enter QA comments', 'rows': 4}), required=False)
#     qa_name = forms.CharField(label='QA Name', widget=forms.TextInput(attrs={'placeholder': 'Enter QA person\'s name'}), required=False)
    
#     # QA issue selection field with predefined choices
#     QA_ISSUE_CHOICES = [
#         ('batchid', 'BatchID'),
#         ('title', 'Title'),
#         ('homepage', 'Home Page'),
#         ('ingestionid','IngestionId'),
#         ('other', 'Other'),
#     ]
    
#     qa_issue = forms.ChoiceField(
#         label='QA Issue',
#         choices=QA_ISSUE_CHOICES,
#         widget=forms.Select(),
#         required=False
#     )
    

#worked on 21/01/2025  source metadata form
from django import forms
from django.contrib.auth.models import User

class SourceMetadataForm(forms.Form):
    import_url = forms.URLField(label='Import URL', widget=forms.TextInput(attrs={'placeholder': 'Enter source URL'}))
    date_of_arrival = forms.DateField(label='Date of Arrival', widget=forms.TextInput(attrs={'placeholder': 'dd-mm-yyyy', 'type': 'date'}))

    # Dynamically populated "Assigned To" dropdown
    assigned_to = forms.ChoiceField(
        label='Assigned To',
        choices=[],  # Empty initially
        widget=forms.Select(attrs={'placeholder': 'Assigned person\'s name'})
    )

    # Dynamically populated "QA Name" dropdown
    qa_name = forms.ChoiceField(
        label='QA Name',
        choices=[],  # Empty initially
        widget=forms.Select(attrs={'placeholder': 'Enter QA person\'s name'})
    )

    frequency_of_site_updates = forms.ChoiceField(
        label='Frequency of Site Updates',
        choices=[('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('Quarterly', 'Quarterly')],
        widget=forms.Select()
    )
    site_last_checked = forms.DateField(label='Site Last Checked', widget=forms.TextInput(attrs={'placeholder': 'dd-mm-yyyy', 'type': 'date'}))
    
    source_file_upload = forms.FileField(label='Source File Upload', required=False)
    json_file_name = forms.CharField(label='JSON File Name', widget=forms.TextInput(attrs={'placeholder': 'Enter JSON file name'}), required=False)
    json_upload_date = forms.DateField(label='JSON Upload Date', widget=forms.TextInput(attrs={'placeholder': 'dd-mm-yyyy', 'type': 'date'}), required=False)
    sup_id = forms.CharField(label='SUP ID', widget=forms.TextInput(attrs={'placeholder': 'Enter SUP ID'}), required=False)
    sme_comments = forms.CharField(label='SME Comments', widget=forms.Textarea(attrs={'placeholder': 'Enter any comments', 'rows': 4}), required=False)
    screenshots_taken = forms.ChoiceField(
        label='Screenshots Taken',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        widget=forms.Select()
    )

    # QA issue selection field
     # New fields for QA
    file_status = forms.ChoiceField(
        label='File Status',
        choices=[('Accepted', 'Accepted'), ('Rejected', 'Rejected')],
        widget=forms.Select()
    )
    qa_comment = forms.CharField(label='QA Comment', widget=forms.Textarea(attrs={'placeholder': 'Enter QA comments', 'rows': 4}), required=False)
    QA_ISSUE_CHOICES = [
        ('batchid', 'BatchID'),
        ('title', 'Title'),
        ('homepage', 'Home Page'),
        ('ingestionid', 'IngestionId'),
        ('other', 'Other'),
    ]
    qa_issue = forms.ChoiceField(
        label='QA Issue',
        choices=QA_ISSUE_CHOICES,
        widget=forms.Select(),
        required=False
    )

    # Initialize the form and dynamically populate dropdowns
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate "Assigned To" dropdown
        assigned_user_choices = [(user.username, user.username) for user in User.objects.all()]
        assigned_user_choices.insert(0, ('', 'Select Assigned User'))
        self.fields['assigned_to'].choices = assigned_user_choices

        # Populate "QA Name" dropdown
        qa_user_choices = [(user.username, user.username) for user in User.objects.all()]
        qa_user_choices.insert(0, ('', 'Select QA Name'))
        self.fields['qa_name'].choices = qa_user_choices


#form code for ingestion of file#######################

# from django import forms

# class FileIngestionForm(forms.Form):
#     ingestion_type = forms.ChoiceField(
#         choices=[("single", "Single File Ingestion"), ("batch", "Batch Ingestion")],
#         label="Ingestion Type",
#         required=False,
#     )
#     file_location = forms.FileField(
#         required=False, label="Fingerprint File"
#     )
#     data_type = forms.ChoiceField(
#         choices=[
#             ("award", "Award"),
#             ("opportunity", "Opportunity"),
#             ("funding", "Funding"),
#         ],
#         label="Data Type",
#         required=False,
#     )
#     json_location = forms.FileField(
#         required=False, label="JSON File"
#     )
#     action = forms.CharField(widget=forms.HiddenInput())
    

#date 13-10-2025

# from django import forms
# class FileIngestionForm(forms.Form):
#     ingestion_type = forms.ChoiceField(
#         choices=[("single", "Single File Ingestion"), ("batch", "Batch Ingestion")],
#         label="Ingestion Type",
#         required=False,
#     )
#     file_location = forms.FileField(
#         required=False, label="Fingerprint File"
#     )
#     data_type = forms.ChoiceField(
#         choices=[
#             ("award", "Award"),
#             ("opportunity", "Opportunity"),
#             ("funding", "Funding"),
#         ],
#         label="Data Type",
#         required=False,
#     )
#     json_location = forms.FileField(
#         required=False, label="JSON File"
#     )
#     action = forms.CharField(widget=forms.HiddenInput())
#     user_name = forms.CharField(
#         max_length=100,
#         required=False,
#         label="User Name",
#         widget=forms.TextInput(attrs={"placeholder": "Enter your name"})
#     )

#now 13-01-2025
#uat form for ui
from django import forms

class FileIngestionForm(forms.Form):
    action = forms.CharField(widget=forms.HiddenInput())
    user_name = forms.CharField(required=False)  # Optional field
    file_location = forms.FileField(required=False)
    ingestion_type = forms.ChoiceField(
        choices=[("single", "Single File"), ("batch", "Batch")],
        required=False,
    )
    data_type = forms.ChoiceField(
        choices=[
            ("award", "Award"),
            ("opportunity", "Opportunity"),
            ("funding-body", "Funding"),
        ],
        required=False,
    )
    json_location = forms.FileField(required=False)
    
    
#prod form for ui
from django import forms

class IngestionProd(forms.Form):
    action = forms.CharField(widget=forms.HiddenInput())
    user_name = forms.CharField(required=False)  # Optional field
    file_location = forms.FileField(required=False)
    ingestion_type = forms.ChoiceField(
        choices=[("single", "Single File"), ("batch", "Batch")],
        required=False,
    )
    data_type = forms.ChoiceField(
        choices=[
            ("award", "Award"),
            ("opportunity", "Opportunity"),
            ("funding-body", "Funding"),
        ],
        required=False,
    )
    json_location = forms.FileField(required=False)
    
    
    
    
    
#user registration
# forms.py
from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
    
    
    
    
    
#json creator form code
from django import forms
class CSVInputForm(forms.Form):    
        csv_file = forms.FileField(label='Select a CSV file')    
        output_directory = forms.CharField(label="Output Directory", max_length=255, required=True)

