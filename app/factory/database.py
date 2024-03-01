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

    def insert(self, element, collection_name, model_class=None):
        element["created"] = datetime.now()
        element["updated"] = datetime.now()
        inserted = self.db[collection_name].insert_one(element)
        return self.find_by_id(str(inserted.inserted_id), collection_name, model_class)

    def find(self, criteria, collection_name, projection=None, sort=None, limit=0, cursor=False, model_class=None):
        found = self.db[collection_name].find(filter=criteria, projection=projection, limit=limit, sort=sort)

        if cursor:
            return found

        found = list(found)

        for i in range(len(found)):
            if "_id" in found[i]:
                found[i]["_id"] = str(found[i]["_id"])
        if model_class:
            return [model_class().map_document_to_instance(doc) for doc in found]

        return found
    
    def find_one(self, criteria, collection_name, projection=None, sort=None, limit=0, cursor=False, model_class=None):
        found = self.db[collection_name].find_one(filter=criteria, projection=projection, limit=limit, sort=sort)
        if found is None:
            return False
        if "_id" in found:
            found["_id"] = str(found["_id"])

        if model_class:
            return model_class().map_document_to_instance(found)

        return found

    def find_by_id(self, id, collection_name, model_class=None):
        found = self.db[collection_name].find_one({"_id": ObjectId(id)})
        if found is None:
            return False
        if "_id" in found:
            found["_id"] = str(found["_id"])

        if model_class:
            return model_class().map_document_to_instance(found)

        return found

    def find_one_by_fieldname(self, fieldname, fieldvalue, collection_name, model_class=None):
        found = self.db[collection_name].find_one({fieldname: fieldvalue})
        print(found)
        if found is None:
            return False
        if "_id" in found:
            found["_id"] = str(found["_id"])

        if model_class:
            return model_class().map_document_to_instance(found)

        return found

    def find_many_by_fieldname(self, fieldname, fieldvalue, collection_name, model_class=None):
        found = self.db[collection_name].find({fieldname: fieldvalue})
        if found is None:
            return False

        if model_class:
            return [model_class().map_document_to_instance(doc) for doc in found]

        return found

    def update(self, id, element, collection_name, model_class=None):
        criteria = {"_id": ObjectId(id)}

        element["updated"] = datetime.now()
        set_obj = {"$set": element}

        updated = self.db[collection_name].update_one(criteria, set_obj)
        if updated.matched_count == 1:
            return self.find_by_id(str(id), collection_name, model_class)
        
    # for OTP, includes upsert
    def upsert_by_criteria(self, criteria, element, collection_name):
        set_obj = {"$set": element}

        # Try to update the document, if not found, insert a new one (upsert)
        updated = self.db[collection_name].update_one(criteria, set_obj, upsert=True)

        if updated.matched_count == 1:
            return True
        else:
            return False

    def update_by_criteria(self, criteria, element, collection_name):
        set_obj = {"$set": element}

        # Try to update the document
        updated = self.db[collection_name].update_one(criteria, set_obj)

        if updated.matched_count == 1:
            return True
        else:
            return False

    def delete(self, id, collection_name):
        deleted = self.db[collection_name].delete_one({"_id": ObjectId(id)})
        return bool(deleted.deleted_count)

    def aggregate(self, pipeline, collection_name, model_class=None):
        collection = self.db[collection_name]
        result = collection.aggregate(pipeline)

        if model_class:
            return [model_class().map_document_to_instance(doc) for doc in result]

        return list(result)
