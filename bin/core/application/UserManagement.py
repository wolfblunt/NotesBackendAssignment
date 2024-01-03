"""
Cart Layer
"""
from bin.core.application.MongoOperations import NotesFormation
from bin.common.AppConfigurations import user_collection


def signup_user_details(input_json):
    """
    This method is for inserting usersignup details in db
    :return: User ID JSON
    """
    try:
        notes_obj = NotesFormation()
        response = dict()
        response_data = notes_obj.insert_data_mongo(input_json, user_collection)
        response["message"] = response_data
        response["status"] = "OK"
        print("response_data Data : ", response_data)
        return response
    except Exception as e:
        import traceback
        print("ERROR :", traceback.print_exc())
        print(str(e))
        raise Exception(str(e))


def fetch_user_details(input_json):
    """
    This method is for inserting usersignup details in db
    :return: User ID JSON
    """
    try:
        notes_obj = NotesFormation()
        response = dict()
        # input_dict = {"username":input_json["username"]}
        response_data = notes_obj.find_record(input_json, user_collection)
        print("response_data Data : ", response_data[0])
        return response_data[0]
    except Exception as e:
        import traceback
        print("ERROR :", traceback.print_exc())
        print(str(e))
        raise Exception(str(e))