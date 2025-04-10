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
####################### grant award id generator ###############################
import os
import json
import hashlib
import html
import csv


def clean_data(data):
    if isinstance(data, dict):
        return {key: clean_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [clean_data(item) for item in data]
    elif isinstance(data, str):
        decoded_str = html.unescape(data)
        return decoded_str.replace("\n", " ").replace("\t", " ").strip()
    return data


def generate_unique_id(base_value, title, synopsis, leadfunder, awardee, max_length=7):
    title = title or "Unknown"
    synopsis = synopsis or "Unknown"
    awardee = awardee or "Unknown"
    concatenated_values = f"{title}-{synopsis}-{leadfunder}-{awardee}"
    hash_object = hashlib.sha256(concatenated_values.encode("utf-8"))
    hash_int = int(hash_object.hexdigest(), 16)
    small_hash = hash_int % (10 ** max_length)
    return base_value + small_hash


def process_bulk_json_folder(folder_path, base_value=80000630):
    try:
        csv_path = os.path.join(folder_path, "IDS.csv")
        json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
        json_files.sort()

        with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Original File Name", "New File Name", "Base Value", "Title", "grantAwardId"])

            for index, json_file in enumerate(json_files):
                current_base_value = base_value + index
                json_file_path = os.path.join(folder_path, json_file)

                with open(json_file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                json_list = [data] if isinstance(data, dict) else data if isinstance(data, list) else None
                if not json_list:
                    continue

                for item in json_list:
                    title = clean_data(item.get("title", [{}])[0].get("value", ""))
                    synopsis = clean_data(item.get("synopsis", [{}])[0].get("abstract", {}).get("value", ""))
                    awardee = clean_data(item.get("awardeeDetail", [{}])[0].get("name", [{}])[0].get("value", ""))

                    unique_id = generate_unique_id(current_base_value, title, synopsis, 501100001291, awardee)
                    item["grantAwardId"] = unique_id

                    if 'awardeeDetail' in item:
                        for idx, awardee_item in enumerate(item["awardeeDetail"]):
                            awardee_item["awardeeAffiliationId"] = f"{unique_id}_A_{idx}"
                            if "affiliationOf" in awardee_item and awardee_item["affiliationOf"]:
                                awardee_item["affiliationOf"][0]["awardeePersonId"] = f"{unique_id}_P_{idx}"

                    new_json_filename = f"{json_file.rsplit('.', 1)[0]}_{unique_id}.json"
                    csv_writer.writerow([json_file, new_json_filename, current_base_value, title, unique_id])

                new_json_file_path = os.path.join(folder_path, new_json_filename)
                with open(new_json_file_path, 'w', encoding='utf-8') as file:
                    json.dump(json_list if isinstance(data, list) else json_list[0], file, ensure_ascii=False, separators=(',', ':'))

                os.remove(json_file_path)

        return csv_path  # Return path for download

    except Exception as e:
        raise RuntimeError(f"Error processing JSONs: {str(e)}")



