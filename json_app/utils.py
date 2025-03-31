from django.http import QueryDict
import json
# from rest_framework import parsers

# class MultipartJsonParser(parsers.MultiPartParser):

#     def parse(self, stream, media_type=None, parser_context=None):
#         result = super().parse(
#             stream,
#             media_type=media_type,
#             parser_context=parser_context
#         )
#         data = {}
#         # find the data field and parse it
#         data = json.loads(result.data["data"])
#         qdict = QueryDict('', mutable=True)
#         qdict.update(data)
#         return parsers.DataAndFiles(qdict, result.files)
    
    
#json creation code
import pandas as pd
import json
import os
from collections import defaultdict
import hashlib
 
from datetime import datetime
import sqlite3
from django.shortcuts import render
 
def s_date(date_obj):
    return date_obj.strftime('%Y-%m-%dT%H:%M:%S')
 
formatted_date = s_date(datetime.now())
 
def format_date(date_str):
    try:
       date_obj = datetime.strptime(date_str, '%m-%d-%Y')
       return date_obj.strftime('%Y-%m-%dT%H:%M:%S')
    except ValueError:
       return date_str
 
def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return value
database_file = "C://Users//mac010865//Downloads//sqlite-tools-win-x64-202501281250//UNIQUE_ID.db"  # Ensure this path is correct
 
def generate_small_hash_uuid(value, max_length=7):
    """Generates a smaller hash-based integer from the provided string."""
    hash_object = hashlib.sha256(value.encode())
    hash_int = int(hash_object.hexdigest(), 16)
    small_hash = hash_int % (10**max_length)  # Limit to 'max_length' digits
    return small_hash
 
def generate_small_hash_AID(title, synposis, leadfunder, awardee, max_length=7):
    concatenated_values = str(title) + str(synposis) + str(leadfunder) + str(awardee)
    hash_object = hashlib.sha256(concatenated_values.encode())
    hash_int = int(hash_object.hexdigest(), 16)
    small_hash = hash_int % (10**max_length)
    return small_hash
 
# def get_and_update_ids(database_file, initial_value_F, initial_value_A, funding_id, AID):
    
#     """
#     Connects to SQLite database, retrieves last values, increments them by 1, generates new IDs,
#     and stores the updated values along with `funding_id` and `AID`.
#     """
#     try:
#         conn = sqlite3.connect(database_file)
#         cursor = conn.cursor()
       
#         # Create table if it doesn't exist
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS id_values (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 value_F INTEGER NOT NULL,
#                 value_A INTEGER NOT NULL,
#                 funding_id INTEGER NOT NULL,
#                 AID INTEGER NOT NULL
#             )
#         """)
#         conn.commit()
#         print("✅ Table created successfully or already exists.")
 
#         # Retrieve last stored values
#         cursor.execute("SELECT value_F, value_A FROM id_values ORDER BY id DESC LIMIT 1")
#         row = cursor.fetchone()
 
#         if row is None:
#             # Use initial values if no records exist
#             value_F = initial_value_F
#             value_A = initial_value_A
#         else:
#             # Increment values by 1
#             value_F = row[0] + 1
#             value_A = row[1] + 1
 
#         # Insert new values along with generated IDs
#         cursor.execute("INSERT INTO id_values (value_F, value_A, funding_id, AID) VALUES (?, ?, ?, ?)",
#                     (value_F, value_A, funding_id, AID))
#         conn.commit()
#         print(f"✅ Data Inserted: Value_F = {value_F}, Value_A = {value_A}")
 
#     except sqlite3.Error as e:
#         print(f"❌ SQLite Error: {e}")
#     finally:
#         conn.close()
   
#     return value_F, value_A
import sqlite3
def clean_data(data):
    if isinstance(data, dict):
        return {key: clean_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [clean_data(item) for item in data]
    elif isinstance(data, str):
        return data.replace('\u0091', "'").replace('\u0092', "'").replace('\r', '')
    return data
def remove_outermost(data):
    if isinstance(data, list) and len(data) == 1:
        return data[0]
    return data
def get_and_update_ids(database_file, initial_value_F, initial_value_A, funding_id, AID):
    """
    Connects to SQLite database, retrieves last values, increments them by 1, generates new IDs,
    and stores the updated values along with `funding_id` and `AID`.
    """
    conn = None  # ✅ Ensure `conn` is defined even if an error occurs

    try:
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()
       
        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS id_values (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value_F INTEGER NOT NULL,
                value_A INTEGER NOT NULL,
                funding_id INTEGER NOT NULL,
                AID INTEGER NOT NULL
            )
        """)
        conn.commit()
        print("✅ Table created successfully or already exists.")

        # Retrieve last stored values
        cursor.execute("SELECT value_F, value_A FROM id_values ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()

        if row is None:
            # Use initial values if no records exist
            value_F = initial_value_F
            value_A = initial_value_A
        else:
            # Increment values by 1
            value_F = row[0] + 1
            value_A = row[1] + 1

        # Insert new values along with generated IDs
        cursor.execute("INSERT INTO id_values (value_F, value_A, funding_id, AID) VALUES (?, ?, ?, ?)",
                    (value_F, value_A, funding_id, AID))
        conn.commit()
        print(f"✅ Data Inserted: Value_F = {value_F}, Value_A = {value_A}")

    except sqlite3.Error as e:
        print(f"❌ SQLite Error: {e}")
        value_F, value_A = None, None  # ✅ Ensure function always returns something

    finally:
        if conn:  # ✅ Close connection only if it's open
            conn.close()

    return value_F, value_A

 
def process_csv_to_json(csv_file, json_output_path):
    df = pd.read_csv(csv_file, encoding='ISO-8859-1')
   
 
    initial_value_F = 80000500
    initial_value_A = 80000501
   
    # --- Funding ID Generation ---
    column_value_TITLE = df.iloc[50]
    value_F_T = column_value_TITLE["Value from the Source or as determined by Supplier"]
    result_uuid = generate_small_hash_uuid(value_F_T)
    print("RESULT_UUID::::::::",result_uuid)
    # --- AID Generation ---
    column_value_TITLE_A = df.iloc[2]
    A_Title = column_value_TITLE_A["Value from the Source or as determined by Supplier"]
   
    column_value_synposis_A = df.iloc[9]
    A_synposis = column_value_synposis_A["Value from the Source or as determined by Supplier"]
   
    column_leadfunder = df.iloc[40]
    A_leadfunder = column_leadfunder["Value from the Source or as determined by Supplier"]
   
    column_Awardee = df.iloc[18]
    A_Awardee = column_Awardee["Value from the Source or as determined by Supplier"]
   
    hash_id =  generate_small_hash_AID(A_Title, A_synposis, A_leadfunder, A_Awardee)
    print("hash_id:::::::",hash_id)
    print(hash_id)
    print(hash_id,60*"$")
    funding_id=(initial_value_F + result_uuid)
    print("funding_id::::::::",funding_id)
    AID=(initial_value_A + hash_id)
    print("AID:::::::::::::",AID)
 
    # Retrieve last values and store new data
    value_F, value_A = get_and_update_ids(database_file, initial_value_F, initial_value_A,
                                          funding_id=(initial_value_F + result_uuid),
                                          AID=(initial_value_A + hash_id))
   
    print("✅ Stored in DB -> Value_F:", value_F, " Value_A:", value_A)
     
    batch_id_value90= str(df.loc[69, 'Value from the Source or as determined by Supplier'])
    json_data = [
        {
    "batchId": "",
    "ingestionId": "",
    "grantAwardId":AID,
    "fundingBodyAwardId": "not found",
    "hasInstallment": [
      0
    ],
    "hasWorkPackage": [
      0
    ],
    "title": [
      {
        "language":"en",
        "value": "",
        "hasProvenance": {
          "createdOn": format_date(batch_id_value90),
          "createdBy": "MPS",
          "createdWith": "MPS SERVICES"
        }
      }
    ],
    "identifier": [
      {
        "type": "DOI",
        "value": "not found"
      }
    ],
    "noticeDate": "",
    "startDate": "",
    "endDate": "",
    "grantType": "",
    "funderSchemeType": "",
    "homePage": {
      "link": "string",
      "publishedDate": "",
      "modifiedDate": ""
    },
    "synopsis": [
      {
        "abstract": {
          "language": "en",
          "value": "",
          "hasProvenance": {
            "createdOn": format_date(batch_id_value90),
            "createdBy": "MPS",
            "createdWith": "MPS SERVICES"
          }
        },
        "source": ""
      }
    ],
    "keyword": [
      {
        "language": "en",
        "value": "",
        "hasProvenance": {
          "createdOn": format_date(batch_id_value90),
          "createdBy": "MPS",
          "createdWith": "MPS SERVICES"
        }
      }
    ],
    "licenseInformation": [
      {
        "abstract": {
          "language": "en",
          "hasProvenance": {
            "createdOn": format_date(batch_id_value90),
            "createdBy": "MPS",
            "createdWith": "MPS SERVICES"
          }
        },
        "source": ""
      }
    ],
    "funds": [
      {
        "fundingBodyProjectId": "not found",
        "hasPart": [
          {
            "fundingBodyProjectId": "not found",
            "budget": [
              {
                "currency": "",
                "amount": 0
              }
            ]
          }
        ],
        "title": [
          {
            "language": "en",
            "value": "",
            "hasProvenance": {
              "createdOn": format_date(batch_id_value90),
              "createdBy": "MPS",
              "createdWith": "MPS SERVICES"
            }
          }
        ],
        "acronym": "",
        "startDate": "",
        "endDate": "",
        "hasPostalAddress": {
          "addressCountry": "",
          "addressRegion": "",
          "addressLocality": "",
          "addressPostalCode": "",
          "postOfficeBoxNumber": "",
          "streetAddress": ""
        },
        "link": "",
        "budget": [
          {
            "currency": "",
            "amount": 0
          }
        ],
        "status": ""
      }
    ],
    "fundingDetail": {
      "installment": [
        {
          "index": 0,
          "grantAwardInstallmentId": 1,
          "financialYearStart": 0,
          "financialYearEnd": 0,
          "fundedAmount": [
            {
              "currency": "",
              "amount": 0
            }
          ]
        }
      ],
      "fundingTotal": [
        {
          "currency": "",
          "amount": 0
        }
      ]
    },
    "awardeeDetail": [
      {
        "awardeeAffiliationId": "",
        "name": [
          {
            "language": "en",
            "value": "",
            "hasProvenance": {
              "createdOn": format_date(batch_id_value90),
              "createdBy": "MPS",
              "createdWith": "MPS SERVICES"
            }
          }
        ],
        "role": "",
        "sourceRole": "",
        "fundingTotal": [
          {
            "currency": "",
            "amount": 0
          }
        ],
        "fundingBodyOrganizationId": "",
        "vatNumber": "",
        "link": "",
        "hasPostalAddress": {
          "addressCountry": "",
          "addressRegion": "",
          "addressLocality": "",
          "addressPostalCode": "",
          "postOfficeBoxNumber": "",
          "streetAddress": ""
        },
        "identifier": [
          {
            "type": "DUNS",
            "value": ""
          }
        ],
        "departmentName": [
          {
            "language": "en",
            "value": "",
            "hasProvenance": {
              "createdOn": format_date(batch_id_value90),
              "createdBy": "MPS",
              "createdWith": "MPS SERVICES"
            }
          }
        ],
        "activityType": "",
        "affiliationOf": [
          {
            "awardeePersonId": "",
            "name": [
              {
                "language": "en",
                "value": "",
                "hasProvenance": {
                  "createdOn": format_date(batch_id_value90),
                  "createdBy": "MPS",
                  "createdWith": "MPS SERVICES"
                }
              }
            ],
            "role": "",
            "sourceRole": "",
            "initials": "",
            "givenName": "",
            "familyName": "",
            "emailAddress": "",
            "identifier": [
              {
                "type": "ORCID",
                "value": ""
              }
            ],
            "fundingBodyPersonId": ""
          }
        ]
      }
    ],
    "classification": [
      {
        "type": "Classification",
        "hasSubject": {
          "preferredLabel": "",
          "orgSpecificClassification": "not found",
          "identifier": {
            "type": "ASJC",
            "value": ""
          }
        }
      }
    ],
    "relatedOpportunity": [
      {
        "grantOpportunityId": 0,
        "fundingBodyOpportunityId": "not found",
        "title": [
          {
            "language": "en",
            "value": "",
            "hasProvenance": {
              "createdOn": format_date(batch_id_value90),
              "createdBy": "MPS",
              "createdWith": "MPS SERVICES"
            }
          }
        ],
        "description": ""
      }
    ],
    "relatedFunder": {
      "leadFunder": {
        "fundingBodyId":funding_id,
        "sourceId": "not found",
        "sourceText": "not found"
      },
      "hasFunder": [
        {
          "fundingBodyId": 0,
          "sourceId": "not found",
          "sourceText": "not found"
        }
      ]
    },
    "hasProvenance": {
      "wasAttributedTo":"SUP005",
      "derivedFrom": "not found",
      "createdOn": format_date(batch_id_value90),
      "lastUpdateOn": "",
      "contactPoint": "robin.bhandari@highwirepress.com",
      "version": "0",
      "hidden": False,
      "defunct": False,
      "status": "NEW"
    },
    "options": {
      "additionalProp1": {},
      "additionalProp2": {},
      "additionalProp3": {}
    }
  }
       
 
    ]
    # if batch_id_value41 != "not found":
    #     json_data[0]['grantAwardId']= AID
       
    column_value = df.iloc[15]
    column_value2 = df.iloc[17]
    raw_asjc= column_value["Value from the Source or as determined by Supplier"]
    asjc_list = [value.strip() for value in raw_asjc.split(",,")]
 
    raw_preffered_lable = column_value2["Value from the Source or as determined by Supplier"]
    preferred_list = [value.strip() for value in raw_preffered_lable.split(",,")]
    classification_data = []
    print(len(asjc_list),len(preferred_list),200*("++"))
 
    if len(asjc_list) == len(preferred_list):
        for asjc_code, preferred_label in zip(asjc_list, preferred_list):
            classification_entry = {
                "type": "Annotation",
                "hasSubject":
                    {
                        "preferredLabel": preferred_label,
                        "identifier": {
                            "value": asjc_code,
                            "type": "ASJC"
                        }
                    }
               
            }
            classification_data.append(classification_entry)
    else:
        print("Mismatched ASJC codes and Preferred Labels. Check the data.")
 
    print("Classification Data:")
    for entry in classification_data:
        print(entry)
    json_data[0]['classification'] = classification_data
 
 
    column_value3 = df.iloc[10]
    raw_keyword = column_value3["Value from the Source or as determined by Supplier"]
    keyword_list = [value.strip() for value in raw_keyword.split(",,")]
    keyword_data = []      
 
    if keyword_list:
        batch_id_value90= str(df.loc[69, 'Value from the Source or as determined by Supplier'])
        for keyword in keyword_list:
           
            keyword_entry = {
                "language": "en",
                "value": keyword,
                "hasProvenance": {
                    "createdOn": format_date(batch_id_value90),
                    "createdBy": "MPS",
                    "createdWith": "MPS SERVICES"
                }
            }
            keyword_data.append(keyword_entry)
    else:
        batch_id_value90= str(df.loc[69, 'Value from the Source or as determined by Supplier'])
        keyword_entry = {
            "language": "en",
            "value": "not found",
            "hasProvenance": {
                "createdOn": format_date(batch_id_value90),
                "createdBy": "MPS",
                "createdWith": "MPS SERVICES"
            }
        }
        keyword_data.append(keyword_entry)
 
    print("Keyword Data:")
    for entry in keyword_data:
        print(entry)
    if isinstance(json_data, list) and len(json_data) > 0:
        json_data[0]['keyword'] = keyword_data
    else:
        json_data = [{"relatedFunder": {"hasFunder": hasFunder_data}}]
   
    column_value15 = df.iloc[41]
    raw_hasFunder = column_value15["Value from the Source or as determined by Supplier"]
    hasFunder_list = [value.strip() for value in raw_hasFunder.split(",,")]
    hasFunder_data = []
 
    if hasFunder_list:
        for hasfunder in hasFunder_list:
            hasfunder_entry = {
                "fundingBodyId": 0,
                "sourceId": "not found",
                "sourceText": hasfunder
            }
         
            hasFunder_data.append(hasfunder_entry)
    else:
        hasfunder_entry = {
            "fundingBodyId": 0,
            "sourceId": "not found",
            "sourceText": ""
        }
        hasFunder_data.append(hasfunder_entry)
 
    print("hasFunder data:")
    for entry in hasFunder_data:
        print(entry)
 
    if isinstance(json_data, list) and len(json_data) > 0:
        json_data[0]['relatedFunder']['hasFunder'] = hasFunder_data
    else:
        json_data = [{"relatedFunder": {"hasFunder": hasFunder_data}}]
 
     
    batch_id_value1 = df.loc[22, 'Value from the Source or as determined by Supplier']
    json_data[0]["activityType"]= batch_id_value1
   
    batch_id_value10 = to_int(df.loc[23, 'Value from the Source or as determined by Supplier'])
    batch_id_value12 = df.loc[24, 'Value from the Source or as determined by Supplier']
    batch_id_value13 = df.loc[56, 'Value from the Source or as determined by Supplier']  
    batch_id_value14 = df.loc[57, 'Value from the Source or as determined by Supplier']
    batch_id_value15 = df.loc[58, 'Value from the Source or as determined by Supplier']
    batch_id_value16 = df.loc[59, 'Value from the Source or as determined by Supplier']
    batch_id_value17 = df.loc[60, 'Value from the Source or as determined by Supplier']
    batch_id_value18 = df.loc[61, 'Value from the Source or as determined by Supplier']
    batch_id_value19 = df.loc[27, 'Value from the Source or as determined by Supplier']
    batch_id_value20 = df.loc[26, 'Value from the Source or as determined by Supplier']
    batch_id_value23= df.loc[28, 'Value from the Source or as determined by Supplier']
    batch_id_value26= df.loc[4, 'Value from the Source or as determined by Supplier']
 
    if batch_id_value26 != "not found":
        json_data[0]['endDate'] = format_date(batch_id_value26)
    else:
        json_data[0].pop('endDate', None)
     
    batch_id_value27= df.loc[14, 'Value from the Source or as determined by Supplier']
    json_data[0]['funderSchemeType']=batch_id_value27
 
    batch_id_value28= df.loc[11, 'Value from the Source or as determined by Supplier']
    json_data[0]['fundingDetail']['fundingTotal'][0]['amount'] = to_int(batch_id_value28)
 
    batch_id_value29= df.loc[24, 'Value from the Source or as determined by Supplier']
    json_data[0]['fundingDetail']['fundingTotal'][0]['currency'] = batch_id_value29  
 
    json_data[0]['fundingDetail']['installment'][0]['fundedAmount'][0]['currency']=batch_id_value29
   
    batch_id_value30= df.loc[23, 'Value from the Source or as determined by Supplier']
    json_data[0]['funds'][0]['budget'][0]['amount'] = to_int(batch_id_value30)
 
    json_data[0]['fundingDetail']['installment'][0]['fundedAmount'][0]['amount'] = to_int(batch_id_value30)
 
    batch_id_value31= df.loc[24, 'Value from the Source or as determined by Supplier']
    json_data[0]['funds'][0]['budget'][0]['currency'] = batch_id_value31  
 
    batch_id_value32= df.loc[4, 'Value from the Source or as determined by Supplier']
    if batch_id_value32 != "not found":
        json_data[0]['funds'][0]['endDate']= format_date(batch_id_value32)
    else:
        json_data[0]['funds'][0].pop('endDate', None)
 
    batch_id_value33= df.loc[23, 'Value from the Source or as determined by Supplier']
    json_data[0]['funds'][0]['hasPart'][0]['budget'][0]['amount']= to_int(batch_id_value33)
 
    batch_id_value34= df.loc[24, 'Value from the Source or as determined by Supplier']
    json_data[0]['funds'][0]['hasPart'][0]['budget'][0]['currency']= batch_id_value34
 
    batch_id_value35= df.loc[62, 'Value from the Source or as determined by Supplier']
    json_data[0]['funds'][0]['hasPostalAddress']['addressCountry'] = batch_id_value35
   
    batch_id_value36= df.loc[63, 'Value from the Source or as determined by Supplier']
    json_data[0]['funds'][0]['hasPostalAddress']['addressLocality'] = batch_id_value36
 
    batch_id_value37= df.loc[64, 'Value from the Source or as determined by Supplier']
    json_data[0]['funds'][0]['hasPostalAddress']['addressPostalCode'] = batch_id_value37
 
    batch_id_value38= df.loc[65, 'Value from the Source or as determined by Supplier']
    json_data[0]['funds'][0]['hasPostalAddress']['addressRegion'] = batch_id_value38
 
    batch_id_value39= df.loc[66, 'Value from the Source or as determined by Supplier']
    json_data[0]['funds'][0]['hasPostalAddress']['postOfficeBoxNumber'] = batch_id_value39
 
    batch_id_value40= df.loc[67, 'Value from the Source or as determined by Supplier']
    json_data[0]['funds'][0]['hasPostalAddress']['streetAddress'] = batch_id_value40
 
    batch_id_value41= df.loc[53, 'Value from the Source or as determined by Supplier']
    json_data[0]['funds'][0]['link']= batch_id_value41
 
    batch_id_value41= df.loc[52, 'Value from the Source or as determined by Supplier']
    if batch_id_value41 != "not found":
        json_data[0]['funds'][0]['startDate']= format_date(batch_id_value41)
    else:
        json_data[0]['funds'][0].pop('startDate', None)
   
    batch_id_value72= df.loc[3, 'Value from the Source or as determined by Supplier']
    if batch_id_value72!= "not found":
        json_data[0]['startDate']=format_date(batch_id_value72)
    else:
        json_data[0].pop('startDate', None)    
 
 
    batch_id_value42= df.loc[55, 'Value from the Source or as determined by Supplier']
    json_data[0]['funds'][0]['status']= batch_id_value42
 
    batch_id_value43= df.loc[2, 'Value from the Source or as determined by Supplier']
    json_data[0]['funds'][0]['title'][0]['value']= batch_id_value43
 
    batch_id_value45=df.loc[1, 'Value from the Source or as determined by Supplier']
    json_data[0]['grantType'] = batch_id_value45
   
    batch_id_value48=df.loc[6, 'Value from the Source or as determined by Supplier']
    json_data[0]['homePage']['link'] = batch_id_value48
 
    json_data[0]['hasProvenance']['derivedFrom'] = batch_id_value48
 
    batch_id_value49=df.loc[7, 'Value from the Source or as determined by Supplier']
    if batch_id_value49 != "not found":
        json_data[0]['homePage']['modifiedDate'] = format_date(batch_id_value49)
    else:
        json_data[0]['homePage'].pop('modifiedDate', None)
 
    batch_id_value50=df.loc[8, 'Value from the Source or as determined by Supplier']
    if batch_id_value50 != "not found":
        json_data[0]['homePage']['publishedDate'] = format_date(batch_id_value50)
    else:
        json_data[0]['homePage'].pop('publishedDate', None)    
   
    batch_id_value53=df.loc[68, 'Value from the Source or as determined by Supplier']
    json_data[0]['licenseInformation'][0]['abstract']['value']=batch_id_value53
   
    batch_id_value54=df.loc[39, 'Value from the Source or as determined by Supplier']
    json_data[0]['licenseInformation'][0]['source']=batch_id_value54    
 
    batch_id_value55=df.loc[5, 'Value from the Source or as determined by Supplier']
    if batch_id_value55 != "not found":
        json_data[0]['noticeDate']=format_date(batch_id_value55)
    else:
        json_data[0].pop('noticeDate', None)
 
    batch_id_value57=df.loc[40, 'Value from the Source or as determined by Supplier']
    json_data[0]['relatedFunder']['leadFunder']['sourceText']=batch_id_value57
 
    batch_id_value58=df.loc[44, 'Value from the Source or as determined by Supplier']
    json_data[0]['relatedOpportunity'][0]['description']=batch_id_value58
 
    batch_id_value59=df.loc[43, 'Value from the Source or as determined by Supplier']
    json_data[0]['relatedOpportunity'][0]['title'][0]['value']=batch_id_value59  
   
    batch_id_value61=df.loc[9, 'Value from the Source or as determined by Supplier']
    json_data[0]['synopsis'][0]['abstract']['value']=batch_id_value61
 
    batch_id_value62=df.loc[6, 'Value from the Source or as determined by Supplier']
    json_data[0]['synopsis'][0]['source']=batch_id_value62
   
    batch_id_value70=df.loc[47, 'Value from the Source or as determined by Supplier']
    json_data[0]['funds'][0]['acronym']=batch_id_value70    
 
    batch_id_value71= df.loc[2, 'Value from the Source or as determined by Supplier']
    json_data[0]['title'][0]['value']=batch_id_value71
 
 
    # batch_id_value73 = df.loc[0, 'Value from the Source or as determined by Supplier']
    # json_data[0]['grantAwardId'] = to_int(batch_id_value73)
 
 
    json_data[0].pop('activityType', None)
 
    batch_id_value90= str(df.loc[69, 'Value from the Source or as determined by Supplier'])
    json_data[0]['relatedOpportunity'][0]['title'][0]['hasProvenance']['createdOn']=format_date(batch_id_value90)
    json_data[0]['keyword'][0]['hasProvenance']['createdOn']= format_date(batch_id_value90)
    json_data[0]['hasProvenance']['createdOn'] = format_date(s_date(datetime.now()))
    json_data[0]['hasProvenance']['lastUpdateOn'] = format_date(s_date(datetime.now()))
    json_data[0]['funds'][0]['title'][0]['hasProvenance']['createdOn']= format_date(batch_id_value90)
 
   
    column_value4 = df.iloc[30]
    column_value5 = df.iloc[31]
    column_value6 = df.iloc[32]
    column_value7 = df.iloc[33]
    column_value8 = df.iloc[34]
    column_value9 = df.iloc[20]
    column_value10 = df.iloc[18]
    column_value11 = df.iloc[21]
    column_value12 = df.iloc[35]
    column_value13 = df.iloc[36]
    column_value14 = df.iloc[22]
 
    raw_initials = column_value4["Value from the Source or as determined by Supplier"]
    raw_Aname = column_value5["Value from the Source or as determined by Supplier"]
    raw_givenname=column_value6["Value from the Source or as determined by Supplier"]
    raw_familyname=column_value7["Value from the Source or as determined by Supplier"]
    raw_Arole = column_value8["Value from the Source or as determined by Supplier"]
    raw_orole = column_value9["Value from the Source or as determined by Supplier"]
    raw_Oname = column_value10["Value from the Source or as determined by Supplier"]
    raw_departmentName = column_value11["Value from the Source or as determined by Supplier"]
    raw_email = column_value12["Value from the Source or as determined by Supplier"]
    raw_identifier = column_value13["Value from the Source or as determined by Supplier"]
    raw_activity_type = column_value14["Value from the Source or as determined by Supplier"]
 
 
    initials_list = [value.strip() for value in raw_initials.split(",,")]
    print("initials_list:",initials_list)
    Aname_list = [value.strip() for value in raw_Aname.split(",,")]
    print("Aname_list:",Aname_list)
    givenname_list = [value.strip() for value in raw_givenname.split(",,")]
    print("givenname_list:",givenname_list)
    familyname_list = [value.strip() for value in raw_familyname.split(",,")]
    print("familyname_list:",familyname_list)
    Arole_list = [value.strip() for value in raw_Arole.split(",,")]
    print("Arole_list:",Arole_list)
    orole_list = [value.strip() for value in raw_orole.split(",,")]
    print("orole_list:",orole_list)
    Oname_list = [value.strip() for value in raw_Oname.split(",,")]
    print("Oname_list:",Oname_list)
    departmentName_list = [value.strip() for value in raw_departmentName.split(",,")]
    print("departmentName_list:",departmentName_list)
    email_list = [value.strip() for value in raw_email.split(",,")]
    print("email_list:",email_list)
    identifier_list =[value.strip() for value in raw_identifier.split(",,")]
    print("raw_identifier:",raw_identifier)
    activity_type_list =[value.strip() for value in raw_activity_type.split(",,")]
    print("activity_type_list:",activity_type_list)
 
    grouped_awardees = defaultdict(list)
 
    global_person_counter = 0                      
    global_affiliation_counter = 0
    if len(initials_list) == len(Aname_list) == len(givenname_list) == len(familyname_list) == len(Arole_list) == len(orole_list) == len(Oname_list) == len(departmentName_list) == len(email_list) == len(identifier_list) == len(activity_type_list):
        for initials, Aname, givenname, familyname, Arole, orole, Oname, departmentName, email, identifier, activity in zip(
            initials_list, Aname_list, givenname_list, familyname_list, Arole_list, orole_list, Oname_list, departmentName_list, email_list, identifier_list, activity_type_list
        ):
            grouped_awardees[Oname].append({
                "activityType": activity if activity else "not found",
                "emailAddress": email,
                "familyName": familyname,
                "givenName": givenname,
                "identifier": identifier if identifier else "not found",
                "initials": initials if initials else "not found",
                "name": Aname if Aname else "not found",
                "role": Arole if Arole else "not found",
                "role1":orole if orole else "not found",
                "sourceRole": "not found",
                "departmentName": departmentName if departmentName else "not found"  # Add departmentName to awardee
            })
 
        awardeeDetail = []
        print(hash_id,50*"%")
        for Oname, awardees in grouped_awardees.items():
            affiliation_of_list = []
            for awardee in awardees:
                affiliation_of_list.append({
                    "awardeePersonId": f"{AID}_P_{global_person_counter}",
                    "emailAddress": awardee["emailAddress"],
                    "familyName": awardee["familyName"],
                    "fundingBodyPersonId": "not found",
                    "givenName": awardee["givenName"],
                    "identifier": [{"type": "ORCID", "value": awardee["identifier"]}],
                    "initials": awardee["initials"],
                    "name": [{"language": "en", "value": awardee["name"]}],
                    "role": awardee["role"],
                    "sourceRole": awardee["sourceRole"]
                })
                global_person_counter += 1
 
            json_entry = {
                "activityType": awardees[0]["activityType"],
                "affiliationOf": affiliation_of_list,
                "awardeeAffiliationId": f"{AID}_A_{global_affiliation_counter}",
                "departmentName": [
                    {
                        "language": "en",
                        "value": awardees[0]["departmentName"],
                        "hasProvenance": {
                            "createdOn": format_date(batch_id_value90),
                            "createdBy": "MPS",
                            "createdWith": "MPS SERVICES"
                        }
                    }
                ],
                "fundingBodyOrganizationId": "not found",
                "fundingTotal": [
                    {
                        "amount": batch_id_value10,
                        "currency": batch_id_value12
                    }
                ],
                "hasPostalAddress": {
                    "addressCountry": batch_id_value13,
                    "addressLocality": batch_id_value14,
                    "addressPostalCode": batch_id_value15,
                    "addressRegion": batch_id_value16,
                    "postOfficeBoxNumber": batch_id_value17,
                    "streetAddress": batch_id_value18
                },
                "identifier": [
                    {
                        "type": batch_id_value19,
                        "value": "not found"
                    }
                ],
                "link": batch_id_value20,
                "name": [
                    {
                        "language": "en",
                        "value": Oname
                    }
                ],
                "role":awardees[0]["role1"],
                "sourceRole": "not found",
                "vatNumber": batch_id_value23
            }
 
            awardeeDetail.append(json_entry)
            global_affiliation_counter += 1
    else:
            print("Mismatched data length. Please check the input.")
 
    json_data[0]['awardeeDetail'] = awardeeDetail
 
    if json_data and isinstance(json_data, list) and len(json_data) > 0:
        json_data[0]['awardeeDetail'] = awardeeDetail
    else:
        print("json_data is not in the expected format.")
 
    with open(json_output_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
    print(f"Raw JSON data has been written to {json_output_path}")
 
    cleaned_json_data = clean_data(json_data)
    cleaned_json_data = remove_outermost(cleaned_json_data)

    # Save cleaned JSON data
    clean_json_output_path = json_output_path.replace(".json", "_cleaned.json")
    with open(clean_json_output_path, 'w', encoding='utf-8') as file:
        json.dump(cleaned_json_data, file, ensure_ascii=False, separators=(',', ':'))
    print(f"Compact cleaned JSON data has been written to {clean_json_output_path}")
