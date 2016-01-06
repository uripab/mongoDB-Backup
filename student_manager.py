__author__ = 'Uriel Pavlov'

import db_manager

class student_collection():
    """
    Class for accessing the students collection
    """
    def __init__(self,db_name,server_ip,port ="27017"):
        self.db_name=db_name
        self.server_ip=server_ip
        self.port =port
        self.collectionName="students"
        print "uri port  {}".format(port)
        self.db =db_manager.MongoDB(self.db_name,self.server_ip,self.port )
    def insert_students(self,doc):
        """
        Insert students object to database
        :param doc: json
        :return:bool True /False
        """
        res =self.db.insert_one_document(self.collectionName,doc)
        return res


    def get_students(self,key={},sort_key=[("_id",1)],count=False,num_of_document=100,column_list=None):
        """
        Get studentds from collection
        :param key: dictionary
        :param sort_key: dictionary
        :param count: bool
        :param num_of_document: Int
        :param column_list: list
        :return:dictionary /None
        """
        col_list =["student_id","first_name","last_name","course"]
        res =self.db.find_documents(self.collectionName,keys={},count=False,sort_key=[("_id", 1)],num_of_document=100)
        res =self.serialized_answer(res,col_list)
        return res

    def delete_students(self,key):
        """
        Delete students from collection
        :param key: json
        :return:int number of deleted document
        """
        res =self.db.delete_many_documents(self.collectionName,key)
        return res

    def update_students(self,filter,update):
        """
         Update students  from collection
        :param filter:dictionary
        :param update:dictionary
        :return:bool True /False
        """
        res =self.db.update_document (self.collectionName,filter,update,upsert)
        return res

    def serialized_answer(self,res,column_list):
        """
        Serialized dictionary to list of list by column list value
        :param res: dictionary
        :param column_list: list
        :return:list of list
        """
        doc_list=[]
        for item in res:
            doc =[]
            course_list=""
            for i,param in enumerate(column_list):
                if column_list[i] =="course":
                    print item[column_list[i]]
                    for key ,value in item[column_list[i]].items():
                        courses ="{}:{}   ".format(key,value)
                        course_list+=courses
                    doc.append(course_list)
                    # for key,value in item[column_list[i]]:
                    #     courses ="{} : {}".format(key,value)
                    #     courses.split(" ")
                    #     course_list.append(courses)
                elif column_list[i] in item:
                    doc.append(item[column_list[i]])
                else:
                    doc.append("")
            doc_list.append(doc)
        return doc_list

