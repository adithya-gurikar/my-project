import csv
import pymongo
import os
import random
import string
from datetime import datetime
import ssl
import certifi

# MongoDB setup
try:
    print("🔄 Connecting to MongoDB...")
    client = pymongo.MongoClient(
        "mongodb+srv://data-ingestion-G:data-ingestion-G@imeuswe-data.xvw0h.mongodb.net/kutumbu-test?retryWrites=true&w=majority",
        tls=True, tlsAllowInvalidCertificates=True
    )
    db = client['kutumbh-test']
    collection = db['persons']
    collection1 = db['files']
    collection2 = db['placesdatas']
    print("✅ MongoDB Connected!")
except Exception as e:
    print(f"❌ MongoDB Connection Failed: {e}")
    exit()

# Config
local_folder_path = '/Users/adithya/Desktop/Data Resources'
specific_csv = "List of Muslim Rulers (1206–1526).csv"
csv_path = os.path.join(local_folder_path, specific_csv)

if not os.path.exists(csv_path):
    print(f"❌ File not found: {csv_path}")
    exit()

# Function: MongoDB-only Place Lookup with ordered keys
def get_location_details(place):
    place = place.strip() if place else ""
    if not place:
        return None

    # Match District
    district_doc = collection2.find_one({
        "categoryName": {"$regex": f"^{place}$", "$options": "i"},
        "categoryType": "District"
    })

    if district_doc:
        place_details = {
            "district": district_doc.get("categoryName"),
            "state": "",
            "country": "",
            "countryCode": district_doc.get("categoryCode")
        }
        parent_state_id = district_doc.get("parentID")
        if parent_state_id:
            state_doc = collection2.find_one({
                "id": parent_state_id,
                "categoryType": "State"
            })
            if state_doc:
                place_details["state"] = state_doc.get("categoryName")
                place_details["country"] = "India"
        return place_details

    # Match State
    state_doc = collection2.find_one({
        "categoryName": {"$regex": f"^{place}$", "$options": "i"},
        "categoryType": "State"
    })

    if state_doc:
        return {
            "district": "",
            "state": state_doc.get("categoryName"),
            "country": "India",
            "countryCode": state_doc.get("categoryCode")
        }

    return None

# File metadata
fileId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=26))
created_at = datetime.today()
week_number = created_at.isocalendar().week
week_of_year = int(f"{created_at.year}{week_number}")

file_doc = {
    '_id': fileId,
    'fileName': specific_csv,
    'fileUrl': "https://www.jatland.com/home/List_of_Muslim_Rulers",
    'fileSource': 'IN-DL',
    'fileType': 'CSV',
    'category': 'CCM',
    'collectionName': 'Community and Club Members List',
    'fstatus': 'PerC',
    'smCode': 'CCM-IN-DL-2025',
    'fileSourceDate': datetime(2025, 1, 1, 0, 0, 0),
    'weekOfYear': week_of_year,
    'createdAt': created_at,
    'updatedAt': datetime.now(),
    'fileCount': 0
}

# Insert file metadata
if collection1.find_one({"fileName": specific_csv}):
    print(f"⚠️ File '{specific_csv}' already exists in MongoDB. Skipping.")
    exit()

collection1.insert_one(file_doc)
print(f"📄 Inserted file metadata for: {specific_csv}")
print(f"🆔 fileId: {fileId}")

# Read CSV and prepare upload
data_to_insert = []
with open(csv_path, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)
    headers = [h.strip() for h in headers]

    # Check for place-related column
    place_index = None
    place_column_candidates = ["place", "district", "constituency","location"]
    for col in place_column_candidates:
        if col in headers:
            place_index = headers.index(col)
            break

    for row in reader:
        if not row or len(row) != len(headers):
            continue

        row_data = dict(zip(headers, row))
        row_data = {k: v.strip() for k, v in row_data.items()}

        row_data['fileId'] = fileId
        row_data['createdAt'] = datetime.today()
        row_data['updatedAt'] = datetime.now()
        row_data['fcatg'] = file_doc['category']
        row_data['weekOfYear'] = week_of_year
        row_data['stateCode'] = file_doc['fileSource']

        # Add place object if valid column present
        if place_index is not None:
            raw_place_value = row[place_index].strip()
            if raw_place_value:
                place_info = get_location_details(raw_place_value)
                if place_info:
                    # Ensure fixed order: district, state, country, countryCode
                    row_data['place'] = {
                        "district": place_info.get("district", ""),
                        "state": place_info.get("state", ""),
                        "country": place_info.get("country", ""),
                        "countryCode": place_info.get("countryCode", "")
                    }

        data_to_insert.append(row_data)

# Insert records
if data_to_insert:
    collection.insert_many(data_to_insert)
    collection1.update_one(
        {'_id': fileId},
        {"$set": {
            'fileCount': len(data_to_insert),
            'weekOfYear': week_of_year,
            'smCode': file_doc['smCode']
        }}
    )

print(f"✅ Inserted {len(data_to_insert)} rows from file: {specific_csv}")
print("📦 Inserted File ID:", fileId)
print("✅ Done.")



# import csv
# import pymongo
# import os
# import random
# import string
# from datetime import datetime
# import ssl
# import certifi
# from geopy.geocoders import Nominatim

# # MongoDB setup
# try:
#     print("🔄 Connecting to MongoDB...")
#     client = pymongo.MongoClient(
#         "mongodb+srv://data-ingestion-G:data-ingestion-G@imeuswe-data.xvw0h.mongodb.net/kutumbu-test?retryWrites=true&w=majority",
#         tls=True,
#         tlsAllowInvalidCertificates=True
#     )
#     db = client['kutumbh']
#     collection = db['persons']
#     collection1 = db['files']
#     collection2 = db['placesdatas']
#     print("✅ MongoDB Connected!")
# except Exception as e:
#     print(f"❌ MongoDB Connection Failed: {e}")
#     exit()

# # Geopy setup
# geolocator = Nominatim(user_agent="kutumbh-app", timeout=5)

# # Config
# local_folder_path = '/Users/adithya/Desktop/Data Resources/List Of Successor District Magistrate Of Lakhimpur Kheri District Of Uttar Pradesh From 1904 To 2024'
# specific_csv = "List Of Successor District Magistrate Of Lakhimpur Kheri District Of Uttar Pradesh From 1904 To 2024.csv"
# csv_path = os.path.join(local_folder_path, specific_csv)

# if not os.path.exists(csv_path):
#     print(f"❌ File not found: {csv_path}")
#     exit()

# # Function: MongoDB-only Place Lookup for persons
# def get_location_details(place):
#     place = place.strip() if place else ""
#     if not place:
#         return None

#     # Match District
#     district_doc = collection2.find_one({
#         "categoryName": {"$regex": f"^{place}$", "$options": "i"},
#         "categoryType": "District"
#     })

#     if district_doc:
#         place_details = {
#             "district": district_doc.get("categoryName"),
#             "state": "",
#             "country": "",
#             "countryCode": district_doc.get("categoryCode")
#         }
#         parent_state_id = district_doc.get("parentID")
#         if parent_state_id:
#             state_doc = collection2.find_one({
#                 "id": parent_state_id,
#                 "categoryType": "State"
#             })
#             if state_doc:
#                 place_details["state"] = state_doc.get("categoryName")
#                 place_details["country"] = "India"
#         return place_details

#     # Match State
#     state_doc = collection2.find_one({
#         "categoryName": {"$regex": f"^{place}$", "$options": "i"},
#         "categoryType": "State"
#     })

#     if state_doc:
#         return {
#             "district": "",
#             "state": state_doc.get("categoryName"),
#             "country": "India",
#             "countryCode": state_doc.get("categoryCode")
#         }

#     return None

# # -------------------
# # Geolocate fileSource based on filename
# # -------------------
# csv_filename_lower = specific_csv.lower()
# filename_words = set(csv_filename_lower.replace("-", " ").replace("_", " ").split())

# place_query = None
# places_cursor = collection2.find({"categoryType": {"$in": ["District", "State"]}})

# for place_doc in places_cursor:
#     place_name = place_doc.get("categoryName", "").lower()
#     place_words = set(place_name.replace("-", " ").replace("_", " ").split())

#     if any(word in filename_words for word in place_words):
#         place_query = place_doc
#         break

# fileSource_final = 'IN-DL'  # default
# if place_query:
#     fileSource_final = place_query.get('categoryCode', 'IN-DL')
# else:
#     # Use Geopy fallback
#     try:
#         location = geolocator.geocode(specific_csv, exactly_one=True, timeout=10)
#         if location and hasattr(location, 'raw'):
#             address = location.raw.get('address', {})
#             state = address.get('state')
#             if state:
#                 state_doc = collection2.find_one({
#                     "categoryName": {"$regex": f"^{state}$", "$options": "i"},
#                     "categoryType": "State"
#                 })
#                 if state_doc:
#                     fileSource_final = state_doc.get("categoryCode", 'IN-DL')
#     except Exception as e:
#         print(f"⚠️ Geopy fallback failed: {e}")

# # -------------------

# # Calculate smCode correctly
# try:
#     state_code_part = fileSource_final.split("-")[1]
# except IndexError:
#     state_code_part = "DL"

# smCode_final = f"GDP-IN-{state_code_part}-2025"

# # File metadata
# fileId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=26))
# created_at = datetime.today()
# week_number = created_at.isocalendar().week
# week_of_year = int(f"{created_at.year}{week_number}")

# file_doc = {
#     '_id': fileId,
#     'fileName': specific_csv,
#     'fileUrl': "https://kheri.nic.in/collectrate/",
#     'fileSource': fileSource_final,
#     'fileType': 'CSV',
#     'language': 'EN',
#     'category': 'GDP',
#     'collectionName': 'Government Service Records',
#     'fstatus': 'PerC',
#     'smCode': smCode_final,
#     'fileSourceDate': datetime(2025, 1, 1, 0, 0, 0),
#     'weekOfYear': week_of_year,
#     'createdAt': created_at,
#     'updatedAt': datetime.now(),
#     'fileCount': 0
# }

# # Insert file metadata
# if collection1.find_one({"fileName": specific_csv}):
#     print(f"⚠️ File '{specific_csv}' already exists in MongoDB. Skipping.")
#     exit()

# collection1.insert_one(file_doc)
# print(f"📄 Inserted file metadata for: {specific_csv}")
# print(f"🆔 fileId: {fileId}")

# # Read CSV and prepare upload
# data_to_insert = []
# with open(csv_path, 'r', encoding='utf-8') as csvfile:
#     reader = csv.reader(csvfile)
#     headers = next(reader)
#     headers = [h.strip() for h in headers]

#     place_index = None
#     place_column_candidates = ["place", "district", "constituency", "location"]
#     for col in place_column_candidates:
#         if col in headers:
#             place_index = headers.index(col)
#             break

#     for row in reader:
#         if not row or len(row) != len(headers):
#             continue

#         row_data = dict(zip(headers, row))
#         row_data = {k: v.strip() for k, v in row_data.items()}

#         row_data['fileId'] = fileId
#         row_data['createdAt'] = datetime.today()
#         row_data['updatedAt'] = datetime.now()
#         row_data['fcatg'] = file_doc['category']
#         row_data['weekOfYear'] = week_of_year
#         row_data['stateCode'] = file_doc['fileSource']

#         if place_index is not None:
#             raw_place_value = row[place_index].strip()
#             if raw_place_value:
#                 place_info = get_location_details(raw_place_value)
#                 if place_info:
#                     row_data['place'] = {
#                         "district": place_info.get("district", ""),
#                         "state": place_info.get("state", ""),
#                         "country": place_info.get("country", ""),
#                         "countryCode": place_info.get("countryCode", "")
#                     }

#         data_to_insert.append(row_data)

# # Insert records
# if data_to_insert:
#     collection.insert_many(data_to_insert)
#     collection1.update_one(
#         {'_id': fileId},
#         {"$set": {
#             'fileCount': len(data_to_insert),
#             'weekOfYear': week_of_year,
#             'smCode': smCode_final
#         }}
#     )

# print(f"✅ Inserted {len(data_to_insert)} rows from file: {specific_csv}")
# print("📦 Inserted File ID:", fileId)
# print("✅ Done.")
