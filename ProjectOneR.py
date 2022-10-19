from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint #print pretty for ease of reading

class AnimalShelter(object):
    """CRUD Operations for Animal collection in MongoDB"""
    
    def __init__(self,username, password):
        """Initialize the MongoClient to access the MongoDB databases and collections."""
        self.client = MongoClient('mongodb://%s:%s@localhost:46243/AAC' % (username, password))
        self.database = self.client['AAC']
        
    def create(self, data):
        """Create a new document in the animals collection using a set of key/value pairs."""
        if data is not None:
            create_result = self.database.animals.insert_one(data)            
            pprint(create_result.inserted_id)#prints unique id created for the new document
            return True #Boolean for successful document creation
        else:
            return False #Boolean for unsuccessful document creation
            raise Exception("Nothing to save, data parameter is empty.")
            
    def read(self, query):
        """Read/find a document(s) in the animals collection."""
        if query is not None:
            #search animal collection for match to key/value query
            #read_result = list(self.database.animals.find(query))
            read_result = self.database.animals.find(query,{"_id":False}) #revised for Dash
            return read_result
        else:
            raise Exception("Nothing to read, data parameter is empty.")
            
    def update(self, original_value, new_value, count):
        """Update document(s) in the animals collection."""
        if original_value is not None:            
           
            if count == 1: #Check for updating one document
                value_result = self.database.animals.update_one(original_value, {"$set":new_value})
                pprint("Document updated successfully.")
                return value_result.raw_result #Outputs JSON
            
            elif count >= 2:  #Check for updating many documents
                value_result = self.database.animals.update_many(original_value, {"$set":new_value})
                pprint(str(value_result.modified_count) + " documents have been successfully updated.")
                return value_result.raw_result #Outputs JSON
        else:
            raise Exception("Nothing to update, data parameter is empty.")
                
        
    def delete(self, delete_query, count):
        """Delete document from the animals collection."""
        if delete_query is not None:
                         
            if count == 1: #Check for delete one document
                delete_result = self.database.animals.delete_one(delete_query)
                if delete_result.deleted_count == 0:
                    return ("No such document exists, please try again.")
                else:
                    pprint("Document successfully deleted.")
                    return delete_result
                
            elif count >= 2: #Check for delete multiple documents
                delete_result = self.database.animals.delete_many(delete_query)
                if delete_result.deleted_count == 0:
                    return ("No such document exists, please try again.")
                else:
                    pprint(str(delete_result.deleted_count) + " documents successfully deleted.")
                    return delete_result          
        else:
            raise Exception("Nothing to delete, data parameter is empty.")
        