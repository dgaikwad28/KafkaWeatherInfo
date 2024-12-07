from pymongo import MongoClient
from app.settings import MONGO_URI


class MongoDB:
    def __init__(self, uri, database, collection):
        """
         Initializes the MongoDB object with the provided URI, database name, and collection name.

         :param uri: The URI for connecting to the MongoDB server.
         :param database: The name of the MongoDB database.
         :param collection: The name of the MongoDB collection.
         """
        self.client = MongoClient(uri)
        self.db = self.client[database]
        self.collection = self.db[collection]

    def close_connection(self):
        """
        Closes the connection to the MongoDB client.
        """
        self.client.close()

    def purge_collection(self):
        """
        Removes all documents from the collection.
        """
        self.collection.drop()

    def get_user_location(self, user_id):

        return self.collection.find_one({'user_id': user_id})

    def update_user_data_from_email(self, filter_query, data_to_update):
        """
        Updates user data in the collection based on a filter query and new data.

        :param filter_query: The query to filter the data to be updated.
        :param data_to_update: The new data to be updated for the matched documents.
        """
        self.collection.update_one(filter_query, {"$set": data_to_update})


# Instantiating the MongoDB class
mongo_db = MongoDB(uri=MONGO_URI, database='user_db', collection='user_collection')
