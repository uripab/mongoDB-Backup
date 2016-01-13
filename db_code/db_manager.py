__author__ = 'Uriel Pavlov'
import pymongo
from log_manager import db_log

class MongoDBManager:
    """
    Class for accessing the MongoDB database
    """
    def __init__(self, db_name,server_ip="localhost",port="27017"):
        self.db_name = db_name
        self.server_ip=server_ip
        self.port =port
        self.db = self.connectToMongoDB()

    def connectToMongoDB(self):
        """
        Connect To Mongo DataBase
        :return:connection
        """
        try:
            db_log.debug("server_ip ={} port ={}".format(self.server_ip,self.port))
            conn=pymongo.MongoClient('mongodb://{}:{}'.format(self.server_ip,self.port))
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s" % e
            db_log.error( "Could not connect to MongoDB: %s" % e)
        db_log.debug( "Connected successfully!!!")
        db = conn[self.db_name]
        return db

    def insert_one_document(self,collectionName,document):
        """
        Insert document to collection in database
        :param collectionName: char
        :param document: dictionary
        :return:acknowledged :True /False
        """
        collection =self.db[collectionName]
        result =collection.insert_one(document)
        return result.acknowledged

    def find_documents(self,collectionName,keys={},count=False, sort_key=[("_id", 1)],num_of_document=100):
        """
       Find specific document from database
        :param collectionName: char
        :param keys: dictionary
        :param count: bool
        :param sort_key: dictionary
        :param num_of_document: int
        :return:dictionary
        """
        collection =self.db[collectionName]
        if count == False:
            result=collection.find(keys).sort(sort_key).limit(num_of_document)
        else:
            result = collection.find(keys).count()
        return result

    def update_document(self,collectionName,filter,update, upsert ):
        """
        Update  document in collection
        :param collectionName: char
        :param filter: dictionary
        :param update: dictionary
        :param upsert: bool
        :return:bool
        """
        collection =self.db[collectionName]
        result =collection.update_one(filter,update,upsert)
        return result

    def delete_one_document(self,collectionName,keys):
        """
        Delete document from collection
        :param collectionName: char
        :param keys:dictionary
        :return:Int (number of document that deleted
        """
        collection =self.db[collectionName]
        result =collection.delete_one(keys)
        return result.deleted_count

    def delete_many_documents(self,collectionName,keys):
        """
        Delete documents from collection
        :param collectionName: char
        :param keys: dictionary
        :return:Int (number of document that deleted
        """
        collection =self.db[collectionName]
        result =collection.delete_many(keys)
        return result.deleted_count



