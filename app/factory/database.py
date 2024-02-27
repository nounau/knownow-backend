from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

from config import Config


class Database(object):
    def __init__(self):
        self.client = MongoClient(Config.MONGO_DB_URL)  # configure db url
        self.db = self.client[Config.MONGO_DB_NAME]  # configure db name
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)


    def insert(self, element, collection_name):
        element["created"] = datetime.now()
        element["updated"] = datetime.now()
        inserted = self.db[collection_name].insert_one(element)  # insert data to db
        # inserted.__setattr__("inserted_id", str(inserted.inserted_id))
        return self.find_by_id(str(inserted.inserted_id), collection_name)

    def find(self, criteria, collection_name, projection=None, sort=None, limit=0, cursor=False):  # find all from db

        if "_id" in criteria:
            criteria["_id"] = ObjectId(criteria["_id"])

        found = self.db[collection_name].find(filter=criteria, projection=projection, limit=limit, sort=sort)

        if cursor:
            return found

        found = list(found)

        for i in range(len(found)):  # to serialize object id need to convert string
            if "_id" in found[i]:
                found[i]["_id"] = str(found[i]["_id"])

        return found

    def find_by_id(self, id, collection_name):
        found = self.db[collection_name].find_one({"_id": ObjectId(id)})
        
        if found is None:
            return not found
        
        if "_id" in found:
             found["_id"] = str(found["_id"])

        return found
    
    def find_one_by_fieldname(self, fieldname, fieldvalue, collection_name):
        found = self.db[collection_name].find_one({fieldname: fieldvalue})
        
        if found is None:
            return not found
        
        if "_id" in found:
             found["_id"] = str(found["_id"])

        return found

    def find_many_by_fieldname(self, fieldname, fieldvalue, collection_name):
        found = self.db[collection_name].find({fieldname: fieldvalue})
        
        if found is None:
            return not found

        return found

    def update(self, id, element, collection_name):
        criteria = {"_id": ObjectId(id)}

        element["updated"] = datetime.now()
        set_obj = {"$set": element}  # update value

        updated = self.db[collection_name].update_one(criteria, set_obj)
        if updated.matched_count == 1:
            return  self.find_by_id(str(id), collection_name)

    def delete(self, id, collection_name):
        deleted = self.db[collection_name].delete_one({"_id": ObjectId(id)})
        return bool(deleted.deleted_count)

    def aggregate(self, pipeline, collection_name):
        collection = self.db[collection_name]
        result = collection.aggregate(pipeline)
        return list(result)
