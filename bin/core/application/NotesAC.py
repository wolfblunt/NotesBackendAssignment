"""
Cart Layer
"""
from bin.core.application.MongoOperations import NotesFormation
from bin.common.AppConfigurations import notes_collection, user_collection
from datetime import datetime


def fetch_current_user_all_notes(user_name):
    """
    This method is for fetching cart items
    :return: User ID JSON
    """
    try:
        notes_obj = NotesFormation()
        response = dict()
        input_dict = dict()
        input_dict["username"] = user_name
        results = notes_obj.list_query_records(input_dict)
        response["message"] = results
        response["status"] = "OK"
        print("Cart Data : ", results)
        return response
    except Exception as e:
        import traceback
        print("ERROR :", traceback.print_exc())
        print(str(e))
        raise Exception(str(e))


def fetch_current_user_note_by_id(user_name, note_id):
    """
    This method is for fetching authenticated user note by id
    :return: User ID JSON
    """
    try:
        notes_obj = NotesFormation()
        response = dict()
        input_dict = dict()
        input_dict["username"] = user_name
        input_dict["id"] = note_id
        results = notes_obj.list_query_records(input_dict)
        response["message"] = results
        response["status"] = "OK"
        print("Cart Data : ", results)
        return response
    except Exception as e:
        import traceback
        print("ERROR :", traceback.print_exc())
        print(str(e))
        raise Exception(str(e))


def add_user_notes(input_json):
    """
    This method is for adding notes into db
    :param input_json:
    :return:
    """
    try:
        notes_obj = NotesFormation()
        response = dict()
        cart_data = notes_obj.add_notes_into_collection(input_json, notes_collection)
        if cart_data:
            response["message"] = "Successfully inserted the cart in database"
            response["status"] = "OK"
        else:
            response["message"] = "Invalid user to perform this action"
            response["status"] = "ERROR"

        return response
    except Exception as e:
        import traceback
        print("ERROR :", traceback.print_exc())
        print(str(e))
        raise Exception(str(e))


def update_user_note(input_json, id, username):
    """
    This method is for updating the  user notes
    :param input_json:
    :return:
    """
    try:
        response = dict()
        notes_obj = NotesFormation()
        condition_dict = dict(id=id, username=username)
        cart_data = notes_obj.update_record_data(input_json, notes_collection, condition_dict)
        print("Cart Data : ", cart_data)
        if cart_data:
            response["message"] = cart_data
            response["status"] = "Successfully updated the cart item"
        else:
            response["message"] = "Invalid user to perform this action"
            response["status"] = "ERROR"
        return response
    except Exception as e:
        import traceback
        print("EROR :", traceback.print_exc())
        print(str(e))
        raise Exception(str(e))


def remove_user_notes(id, username):
    """
    This method is for removing the note with id
    :param input_json:
    :return:
    """
    try:
        response = dict()
        notes_obj = NotesFormation()
        input_json = dict(id=id, username=username)
        notes_data = notes_obj.remove_record_using_condition(input_json, notes_collection)
        print("Cart Data : ", notes_data)
        if notes_data:
            response["message"] = "Successfully Deleted the whole cart item"
            response["status"] = "OK"
        else:
            response["message"] = "Invalid user to perform this action"
            response["status"] = "ERROR"
        return response
    except Exception as e:
        import traceback
        print("EROR :", traceback.print_exc())
        print(str(e))
        raise Exception(str(e))


def share_notes_among_user(input_json, username, id):
    try:
        response = dict()
        notes_obj = NotesFormation()

        shared_user = notes_obj.find_record(input_json, user_collection)[0]
        print("shared user detail: ", shared_user)
        if shared_user:
            input_dict = dict()
            input_dict["username"] = username
            input_dict["id"] = id
            shared_note = notes_obj.list_query_records(input_dict)[0]
            print("shared note detail: ", shared_note)
            if shared_note:
                shared_note['username'] = input_json["username"]
                del shared_note["timestamp"]
                shared_note["timestamp"] = str(datetime.utcnow()).split('.')[0]

                cart_data = notes_obj.add_notes_into_collection(shared_note, notes_collection)
                if cart_data:
                    response["message"] = "Successfully shared the note with the user"
                    response["status"] = "OK"
                else:
                    response["message"] = "Note not shared with the user"
                    response["status"] = "ERROR"
        else:
            response["message"] = "User to share with not found!"
            response["status"] = "ERROR"

        return response
    except Exception as e:
        import traceback
        print("EROR :", traceback.print_exc())
        print(str(e))
        raise Exception(str(e))


def search_notes_using_query(current_user, query):
    try:
        response = dict()
        notes_obj = NotesFormation()
        input_dict = dict(id=current_user, query=query)
        notes_data = notes_obj.find_record_using_keyword(input_dict, notes_collection)
        if notes_data:
            result = [{'id': str(note['id']), 'title': note.get('title', ''), 'content': note.get('content', '')} for
                      note
                      in notes_data]

            if result:
                response["message"] = result
                response["status"] = "OK"
            else:
                response["message"] = "Not find any result"
                response["status"] = "ERROR"
        return response
    except Exception as e:
        import traceback
        print("EROR :", traceback.print_exc())
        print(str(e))
        raise Exception(str(e))