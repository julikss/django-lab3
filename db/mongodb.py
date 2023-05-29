from pymongo import MongoClient
from bson import ObjectId
from pymongo.errors import ConnectionFailure
from db.example import example_students

class MongoDB():
    def __init__(self):
        super().__init__()

        self.connect()
        self.create_collection()

    def connect(self):
        try:
            self.client = MongoClient('mongodb+srv://user1:gEvuNuoN8krJqYTe@cluster0.yzudw1f.mongodb.net/')
            self.db = self.client['decanat']
        except ConnectionFailure:
            print("Couldn't connect...")

    def create_collection(self):
        self.collection1 = self.db['students']
        self.collection2 = self.db['students_without_subjects']
        self.collection1.delete_many({})
        self.fill_with_example_values()

    def fill_with_example_values(self):
        self.collection1.insert_many(example_students)

    def get_student(self, id):
        data = self.read()
        for el in data:
            if (str(el[0]) == str(id)):
                return el
       
    def read(self):
        data = list(self.collection1.find())
        
        result = []
        for el in data:
            student = (el['student_id'], el['course'], el['group_name'], el['student'], el['subject'])
            result.insert(el['student_id'], student)
           
        return result

    def create(self, table, data):
        if (table == 1): 
            collection = self.collection1
        else: 
            collection = self.collection2
        collection.insert_one({'course': data[0], 'group_name': data[1], 'student': data[2], 'subject': data[3]})

    def update(self, data):
        self.collection1.update_one({'_id': data[0]}, {'$set': {'course': data[1], 'group_name': data[2], 'student': data[3], 'subject': data[4]}})

    def delete(self, id):
        self.collection1.delete_one({'_id': id})      

    def __del__(self):
        self.client.close()

mongodb = MongoDB()
