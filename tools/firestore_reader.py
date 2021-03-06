import firebase_admin
from firebase_admin import credentials, firestore

import sys
sys.path.append('../')

from SimpleLogger import SimpleLogger

logger = SimpleLogger(verbose = True, loggerName = f"Firebase reader")

logger.log(f"Connecting to Firestore.")
cred = credentials.Certificate("../home-sensors-credentials.json")
firebase_admin.initialize_app(cred)

firestore_db = firestore.client()
collection = firestore_db.collection('home_sensors_v1')

# Checking the latest sample in Firestore
logger.log(f"Check the latest sample in Firestore.")
result = collection.order_by('date',direction='DESCENDING').limit(1).get()
firestore_latest = result[0].to_dict()['timestamp']
logger.log(f"Latest data timestamp in Firestore: {firestore_latest}")

# Checking the latest sample in local database
file_name = "home_sensors_v1.csv"
logger.log(f"Checking the latest sample in local database.")
try:
    fh = open(file_name, 'r')
    local_data = fh.readlines()
    local_latest = local_data[-1].split(",")[0]
    logger.log(f"Latest data timestamp in local csv: {local_latest}")
    fh.close()
except FileNotFoundError:
    logger.log("Local database doesn't exist.", messageType = "WARN")
    local_latest = None

if firestore_latest == local_latest:
    logger.log("You have the latest database, nothing to do.", messageType = "OK")
    exit()
else:
    logger.log("There are new samples in Firestore, updating local csv.", messageType = "WARN")

    logger.log(f"Downloading data from Firestore.")
    results = collection.order_by('date',direction='ASCENDING').get() # another way - get the last document by date

    logger.log(f"Writing data to `{file_name}`.")
    # csv example: 19980102,0,3.31397,3.95098,3.28236,3.95098,24947201.1
    fh = open(file_name, 'w')

    for item in results:
        #print(item.to_dict())
        fh.write(f"{item.to_dict()['timestamp']},{item.to_dict()['kitchen_temp']},{item.to_dict()['kitchen_hum']},{item.to_dict()['kitchen_bat']}," \
                f"{item.to_dict()['outside_temp']},{item.to_dict()['outside_hum']},{item.to_dict()['outside_bat']}," \
                f"{item.to_dict()['filament_temp']},{item.to_dict()['filament_hum']},{item.to_dict()['filament_bat']}," \
                f"{item.to_dict()['bathroom_temp']},{item.to_dict()['bathroom_hum']},{item.to_dict()['bathroom_bat']}\n")

    fh.close()
    logger.log(f"Local databased was updated.")