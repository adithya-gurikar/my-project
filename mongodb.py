# import csv
# import pymongo
# import os
# import random
# import string
# from datetime import datetime
# from geopy.geocoders import Nominatim
# import ssl
# import certifi

# # MongoDB setup
# try:
#     print("🔄 Connecting to MongoDB...")
#     client = pymongo.MongoClient(
#         "mongodb+srv://data-ingestion-G:data-ingestion-G@imeuswe-data.xvw0h.mongodb.net/kutumbu-test?retryWrites=true&w=majority",
#         tls=True, tlsAllowInvalidCertificates=True
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
# ssl_context = ssl.create_default_context(cafile=certifi.where())

# # Config
# local_folder_path = '/Users/adithya/Desktop/Data Resources/List of Officers serving with 5th Battalion, 8th Punjabi Regiment Circa 1926'
# specific_csv = "ministers_of_state_for_railways.csv"
# csv_path = os.path.join(local_folder_path, specific_csv)

# if not os.path.exists(csv_path):
#     print(f"❌ File not found: {csv_path}")
#     exit()

# # Function: MongoDB + Geopy-based Place Lookup
# def get_location_details(place):
#     place = place.strip() if place else ""
#     if not place:
#         return None

#     # Step 1: Try MongoDB for District
#     district_doc = collection2.find_one({
#         "categoryName": {"$regex": f"^{place}$", "$options": "i"},
#         "categoryType": "District"
#     })

#     if district_doc:
#         parent_state_id = district_doc.get('parentID')
#         if parent_state_id:
#             state_doc = collection2.find_one({
#                 "id": parent_state_id,
#                 "categoryType": "State"
#             })
#             if state_doc:
#                 return {
#                     "district": district_doc.get("categoryName"),
#                     "state": state_doc.get("categoryName"),
#                     "country": "India",
#                     "countryCode": state_doc.get("categoryCode")
#                 }

#     # Step 2: Fallback to Geopy
#     try:
#         location = geolocator.geocode(place, exactly_one=True, timeout=10)
#         if location and hasattr(location, 'raw'):
#             address = location.raw.get('address', {})
#             state = address.get('state')
#             country = address.get('country')
#             country_code = address.get('country_code', '').upper()

#             if state and country:
#                 return {
#                     "state": state,
#                     "country": country,
#                     "countryCode": f"IN-{state[:2].upper()}" if country == "India" else country_code
#                 }
#     except Exception as e:
#         print(f"⚠️ Geopy error for '{place}': {e}")
#     return None

# # File metadata
# fileId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=26))
# created_at = datetime.today()
# week_number = created_at.isocalendar().week
# week_of_year = int(f"{created_at.year}{week_number}")

# file_doc = {
#     '_id': fileId,
#     'fileUrl': "https://fibis.ourarchives.online/bin/aps_browse_sources.php?mode=browse_components&id=1075&s_id=326",
#     'fileName': specific_csv,
#     'fileSource': 'IN-DL',
#     'fileType': 'CSV',
#     'language': 'EN',
#     'category': 'GDP',
#     'collectionName': 'Government Service Records',
#     'fstatus': 'PerC',
#     'smCode': 'GDP-IN-DL-2025',
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

#     place_index = headers.index("constituency") if "constituency" in headers else None

#     for row in reader:
#         if not row or len(row) != len(headers):
#             continue

#         row_data = dict(zip(headers, row))
#         row_data = {k: v.strip() for k, v in row_data.items()}

#         row_data['fileId'] = fileId                     # ✅ Added as requested
#         row_data['createdAt'] = datetime.today()
#         row_data['updatedAt'] = datetime.now()
#         row_data['fcatg'] = file_doc['category']
#         row_data['weekOfYear'] = week_of_year
#         row_data['stateCode'] = file_doc['fileSource']

#         # Add placeDetails from either MongoDB or Geopy
#         if place_index is not None and row[place_index].strip():
#             place_info = get_location_details(row[place_index])
#             if place_info:
#                 row_data['place'] = place_info

#         data_to_insert.append(row_data)

# # Insert records
# if data_to_insert:
#     collection.insert_many(data_to_insert)
#     collection1.update_one(
#         {'_id': fileId},
#         {"$set": {
#             'fileCount': len(data_to_insert),
#             'weekOfYear': week_of_year,
#             'smCode': file_doc['smCode']
#         }}
#     )

# print(f"✅ Inserted {len(data_to_insert)} rows from file: {specific_csv}")
# print("📦 Inserted File ID:", fileId)
# print("✅ Done.")



import csv
import pymongo
import os
import random
import string
from datetime import datetime
from geopy.geocoders import Nominatim
import ssl
import certifi

# MongoDB setup
try:
    print("🔄 Connecting to MongoDB...")
    client = pymongo.MongoClient(
        "mongodb+srv://data-ingestion-G:data-ingestion-G@imeuswe-data.xvw0h.mongodb.net/kutumbu-test?retryWrites=true&w=majority",
        tls=True, tlsAllowInvalidCertificates=True
    )
    db = client['kutumbh']
    collection = db['persons']
    collection1 = db['files']
    collection2 = db['placesdatas']
    print("✅ MongoDB Connected!")
except Exception as e:
    print(f"❌ MongoDB Connection Failed: {e}")
    exit()

# Geopy setup
geolocator = Nominatim(user_agent="kutumbh-app", timeout=5)
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Config
local_folder_path = '/Users/adithya/Desktop/Data Resources/Railway Ministers and Ministers of State for Railways of Independent India Since 1946'
specific_csv = "railway_ministers_of_independent_india.csv"
csv_path = os.path.join(local_folder_path, specific_csv)

if not os.path.exists(csv_path):
    print(f"❌ File not found: {csv_path}")
    exit()

# Function: MongoDB + Geopy-based Place Lookup
def get_location_details(place):
    place = place.strip() if place else ""
    if not place:
        return None

    # Step 1: Try MongoDB for District
    district_doc = collection2.find_one({
        "categoryName": {"$regex": f"^{place}$", "$options": "i"},
        "categoryType": "District"
    })

    if district_doc:
        parent_state_id = district_doc.get('parentID')
        if parent_state_id:
            state_doc = collection2.find_one({
                "id": parent_state_id,
                "categoryType": "State"
            })
            if state_doc:
                return {
                    "district": district_doc.get("categoryName"),
                    "state": state_doc.get("categoryName"),
                    "country": "India",
                    "countryCode": state_doc.get("categoryCode")
                }

    # Step 2: Fallback to Geopy
    try:
        location = geolocator.geocode(place, exactly_one=True, timeout=10)
        if location and hasattr(location, 'raw'):
            address = location.raw.get('address', {})
            state = address.get('state')
            country = address.get('country')
            country_code = address.get('country_code', '').upper()

            if state and country:
                return {
                    "state": state,
                    "country": country,
                    "countryCode": f"IN-{state[:2].upper()}" if country == "India" else country_code
                }
    except Exception as e:
        print(f"⚠️ Geopy error for '{place}': {e}")
    return None

# File metadata
fileId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=26))
created_at = datetime.today()
week_number = created_at.isocalendar().week
week_of_year = int(f"{created_at.year}{week_number}")

file_doc = {
    '_id': fileId,
    'fileUrl': "https://irfca.org/docs/railway-ministers.html",
    'fileSource': 'IN-DL',
    'fileType': 'CSV',
    'language': 'EN',
    'category': 'GDP',
    'collectionName': 'Government Service Records',
    'fstatus': 'PerC',
    'smCode': 'GDP-IN-DL-2025',
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

    # Check for available place-related column
    place_index = None
    place_column_candidates = ["place", "district", "constituency"]
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

        # Conditionally add place info
        if place_index is not None:
            raw_place_value = row[place_index].strip()
            if raw_place_value:
                place_info = get_location_details(raw_place_value)
                if place_info:
                    row_data['place'] = place_info

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
