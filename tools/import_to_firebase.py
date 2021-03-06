import firebase_admin
from firebase_admin import credentials, firestore

from datetime import datetime

import sys
sys.path.append('../')

from SimpleLogger import SimpleLogger

logger = SimpleLogger(verbose = True, loggerName = f"Firebase importer")

logger.log(f"Connecting to Firestore.")
cred = credentials.Certificate("../home-sensors-credentials.json")
firebase_admin.initialize_app(cred)

firestore_db = firestore.client()
collection = firestore_db.collection('home_sensors_v1')

file_name = "Temperature_sensors_google_sheet.csv"
logger.log(f"Opening local database: `{file_name}`.")

try:
    fh = open(file_name, 'r')
    local_data = fh.readlines()
    fh.close()
except FileNotFoundError:
    logger.log("Local database doesn't exist.", messageType = "WARN")
    local_latest = None
    exit()

timestamp_format_origin = '%m/%d/%Y %H:%M:%S'
timestamp_format_target ='%Y%m%d-%H%M%S'
for i, row in enumerate(local_data):
    if i == 0:
        continue

    splitted_row = row.strip().split(",")
    #print(splitted_row)
    #print(splitted_row[0])
    date_time_obj = datetime.strptime(splitted_row[0], timestamp_format_origin)
    #print(date_time_obj.strftime(timestamp_format_target))

    logger.log(f"Importing line from: `{date_time_obj.strftime(timestamp_format_target)}`.")
    collection.add({'date': date_time_obj, 'timestamp': date_time_obj.strftime(timestamp_format_target), 
                'kitchen_temp': float(splitted_row[1]), 'kitchen_hum': float(splitted_row[2]), 'kitchen_bat': float(splitted_row[3]),
                'bathroom_temp': float(splitted_row[7]), 'bathroom_hum': float(splitted_row[8]), 'bathroom_bat': float(splitted_row[9]),
                'outside_temp': float(splitted_row[4]), 'outside_hum': float(splitted_row[5]), 'outside_bat': float(splitted_row[6]),
                'filament_temp': float(splitted_row[10]), 'filament_hum': float(splitted_row[11]), 'filament_bat': float(splitted_row[12])
    })