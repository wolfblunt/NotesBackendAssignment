from bin.common.AppConfigurations import mongo_host, mongo_port, db_name, cart_collection, notes_collection
from bin.core.utilities.mongo_utility import MongoUtility
from datetime import date, datetime


class NotesFormation(object):
    def __init__(self):
        self.mongo_client = MongoUtility(_mongo_port=mongo_port, _mongo_host=mongo_host)

    def list_cart_item_from_collection(self):
        try:
            print("Fetching endpoint details from mongo")
            mongo_content = self.mongo_client.find_all(database_name=db_name,
                                                       collection_name=cart_collection)
            response = list()
            for content in mongo_content:
                del content["_id"]
                response.append(content)
            return response
        except Exception as e:
            import traceback
            print("EROR :", traceback.print_exc())
            print("Failure to fetch cart collection --> {}".format(str(e)))
            raise Exception("Error when fetching cart collection!")

    def add_item_into_collection(self, input_json):
        try:
            if input_json.get("user_name") == "admin":
                mongo_content = self.mongo_client.insert_one(json_data=input_json, database_name=db_name,
                                                             collection_name=cart_collection)
                print("mongo_content : ", mongo_content)
                return True
            else:
                return False
        except Exception as e:
            import traceback
            print("EROR :", traceback.print_exc())
            print("Failure to fetch cart collection --> {}".format(str(e)))
            raise Exception("Error when fetching cart collection!")

    #############
    def insert_data_mongo(self, input_json, collection_name):
        try:
            mongo_content = self.mongo_client.insert_one(json_data=input_json, database_name=db_name,
                                                         collection_name=collection_name)
            print("mongo_content : ", mongo_content)
            return True
        except Exception as e:
            import traceback
            print("EROR :", traceback.print_exc())
            print("Failure to fetch cart collection --> {}".format(str(e)))
            raise Exception("Error when fetching cart collection!")

    def find_record(self, input_json, collection_name):
        try:
            mongo_content = self.mongo_client.find_json(json_data=input_json, database_name=db_name,
                                                        collection_name=collection_name)
            print("mongo_content : ", mongo_content)
            response = list()
            for content in mongo_content:
                del content["_id"]
                response.append(content)
            return response
        except Exception as e:
            import traceback
            print("EROR :", traceback.print_exc())
            print("Failure to fetch cart collection --> {}".format(str(e)))
            raise Exception("Error when fetching cart collection!")

    def list_query_records(self, input_json):
        try:
            print("Fetching list_query_records from mongo for JSON : ", input_json)
            mongo_content = self.mongo_client.query_by_condition(database_name=db_name,
                                                                 collection_name=notes_collection,
                                                                 input_json=input_json)
            response = list()
            for content in mongo_content:
                del content["_id"]
                response.append(content)

            print("Response : ", response)
            return response
        except Exception as e:
            import traceback
            print("EROR :", traceback.print_exc())
            print("Failure to fetch cart collection --> {}".format(str(e)))
            raise Exception("Error when fetching cart collection!")

    def add_notes_into_collection(self, input_json, collection_name):
        try:
            mongo_content = self.mongo_client.insert_one(json_data=input_json, database_name=db_name,
                                                         collection_name=collection_name)
            if mongo_content:
                return True
            else:
                return False
        except Exception as e:
            import traceback
            print("EROR :", traceback.print_exc())
            print("Failure to fetch cart collection --> {}".format(str(e)))
            raise Exception("Error when fetching cart collection!")

    def update_record_data(self, input_json, collection_name, condition_dict):
        try:
            print("Type InputJson : ", type(input_json))
            input_json["timestamp"] = str(datetime.utcnow()).split('.')[0]
            # condition = dict(id=input_json.get("id", ""), username=input_json.get("username", ""))
            mongo_content = self.mongo_client.update_one(condition=condition_dict, json_data=input_json,
                                                         _database_name=db_name,
                                                         collection_name=collection_name)
            return mongo_content
        except Exception as e:
            import traceback
            print("EROR :", traceback.print_exc())
            print("Failure to fetch cart collection --> {}".format(str(e)))
            raise Exception("Error when fetching cart collection!")

    def remove_record_using_condition(self, input_json, collection_name):
        try:
            print("Type InputJson : ", type(input_json))
            # condition = dict(id=input_json.get("id", ""))
            mongo_content = self.mongo_client.remove(json_data=input_json,
                                                     _database_name=db_name,
                                                     collection_name=collection_name)
            print("mongo_content : ", mongo_content)
            # flask.jsonify(message="success", insertedIds=todo_many.inserted_ids)
            response = list()
            print("REMOVE CART mongoCOntent : ", mongo_content)
            return mongo_content
        except Exception as e:
            import traceback
            print("EROR :", traceback.print_exc())
            print("Failure to fetch cart collection --> {}".format(str(e)))
            raise Exception("Error when fetching cart collection!")

    def find_record_using_keyword(self, input_json, collection_name):
        try:
            mongo_content = self.mongo_client.find_using_keyword(json_data=input_json, database_name=db_name,
                                                        collection_name=collection_name)
            response = list()
            for content in mongo_content:
                del content["_id"]
                response.append(content)

            return response
        except Exception as e:
            import traceback
            print("EROR :", traceback.print_exc())
            print("Failure to fetch cart collection --> {}".format(str(e)))
            raise Exception("Error when fetching cart collection!")

    #############

    def add_multiple_item_into_collection(self, input_json):
        try:
            print("Type InputJson : ", type(input_json))
            flag = False
            for data in input_json:
                print("data : ", data)
                if data.get("user_name", "") == "admin":
                    flag = True
                    if not data.get("id", ""):
                        data["timestamp"] = str(datetime.utcnow()).split('.')[0]
                        data["id"] = self.mongo_client.generating_ramdon_id(cart_collection)
                else:
                    flag = False
                    break
            print("FLAG : ", flag)
            print("INPUT JSON MULTI : ", input_json)
            if flag:
                mongo_content = self.mongo_client.insert_many(json_data=input_json, database_name=db_name,
                                                              collection_name=cart_collection)
                return True
            else:
                return False

        except Exception as e:
            import traceback
            print("ERROR :", traceback.print_exc())
            print("Failure to fetch cart collection --> {}".format(str(e)))
            raise Exception("Error when fetching cart collection!")