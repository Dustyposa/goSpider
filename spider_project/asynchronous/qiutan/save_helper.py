from dataclasses import dataclass

import pymongo


@dataclass
class MongoDb:
    mongo_session = pymongo.MongoClient(host="localhost", port=27017)
    mongo_db = mongo_session["qiutan"]
    mongo_col = mongo_db["qiutan"]
