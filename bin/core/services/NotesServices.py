"""
NOTES Service Layer
"""
import json
# from base64 import b64encode, b64decode
# from bson import ObjectId
from flask import Blueprint, jsonify, request
# from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
from bin.core.application import NotesAC, UserManagement
from bin.common.AppConfigurations import secret_key
import datetime
from passlib.hash import sha256_crypt
import time
from bin.core.application.RateLimiting import rate_limited

notes = Blueprint("Notes", __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            print("Token : ", token)
            # data = jwt.decode(token, secret_key)
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            input_dict = {'username': data['username']}
            print("token : ", input_dict)
            current_user = UserManagement.fetch_user_details(input_dict)
        except Exception as e:
            print("Token Erorr : ", e)
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@notes.route('/api/auth/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        try:
            input_json = json.loads(request.get_data())
            print("Input JSON Type: ", input_json)
            input_json["password"] = sha256_crypt.encrypt(input_json["password"])

            # input_json["password"] = generate_password_hash(input_json["password"], method='sha256')

            results = UserManagement.signup_user_details(input_json)
            response = dict()
            response['status'] = "OK"
            response['message'] = results
            return response
        except Exception as e:
            print(str(e))
            message = 'Unable to SignUp User'
            return message


@notes.route('/api/auth/login', methods=['POST'])
@rate_limited()
def login():
    if request.method == 'POST':
        try:
            ################
            auth = request.authorization
            # input_json = json.loads(request.get_data())
            # username = input_json["username"]
            # password = input_json["password"]
            username = auth.username
            password = auth.password
            # print("input_json : ", input_json)
            if not auth or not username or not password:
                return jsonify({'message': 'Could not verify!'}), 401

            input_dict = {'username': username}
            results = UserManagement.fetch_user_details(input_dict)
            print("Results : ", results)
            # if not results or not check_password_hash(results['password'], auth.password):
            #     return jsonify({'message': 'Could not verify!'}), 401

            if not results or not sha256_crypt.verify(auth.password, results['password']):
                return jsonify({'message': 'Could not verify!'}), 401

            token = jwt.encode(
                {'username': results['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                secret_key)

            time.sleep(3000)

            return jsonify({'token': token}), 200

        except Exception as e:
            print(str(e))
            message = 'Unable to SignUp User'
            return message


@notes.route("/api/notes", methods=["GET"])
@rate_limited()
@token_required
def fetch_user_notes(current_user):
    """
    API Endpoint for fetching user notess
    :return:
    """
    if request.method == 'GET':
        print("Inside Fetch User Notes")
        try:
            user_name = current_user["username"]
            results = NotesAC.fetch_current_user_all_notes(user_name)
            response = dict()
            response['status'] = "OK"
            response['message'] = results
            return response
        except Exception as e:
            print(str(e))
            message = 'Unable to fetch cart items'
            return message


@notes.route('/api/notes/<id>', methods=['GET'])
@rate_limited()
@token_required
def get_note_by_id(current_user, id):
    if request.method == 'GET':
        print("Inside Fetch User Notes")
        try:
            user_name = current_user["username"]
            note_id = id
            results = NotesAC.fetch_current_user_note_by_id(user_name, note_id)
            response = dict()
            response['status'] = "OK"
            response['message'] = results
            return response
        except Exception as e:
            print(str(e))
            message = 'Note not found'
            return message


@notes.route('/api/notes', methods=['POST'])
@rate_limited()
@token_required
def create_note(current_user):
    if request.method == 'POST':
        print("Inside Create Notes")
        try:
            input_json = json.loads(request.get_data())
            input_json['username'] = current_user["username"]
            response = NotesAC.add_user_notes(input_json)
            return response
        except Exception as e:
            print(str(e))
            message = 'Note not found'
            return message


@notes.route('/api/notes/<id>', methods=['PUT'])
@rate_limited()
@token_required
def update_note(current_user, id):
    if request.method == 'PUT':
        print("Inside Update Notes")
        try:
            input_json = json.loads(request.get_data())
            username = current_user["username"]
            response = NotesAC.update_user_note(input_json, id, username)
            return response
        except Exception as e:
            print(str(e))
            message = 'Note not found'
            return message


@notes.route('/api/notes/<id>', methods=['DELETE'])
@rate_limited()
@token_required
def delete_note(current_user, id):
    if request.method == 'DELETE':
        print("Inside Update Notes")
        try:
            username = current_user["username"]
            response = NotesAC.remove_user_notes(id, username)
            return response
        except Exception as e:
            print(str(e))
            message = 'Note not found'
            return message


@notes.route('/api/notes/<id>/share', methods=['POST'])
@rate_limited()
@token_required
def share_note(current_user, id):
    if request.method == 'POST':
        print("Inside Share Notes")
        try:
            username = current_user["username"]
            input_json = json.loads(request.get_data())
            response = NotesAC.share_notes_among_user(input_json, username, id)
            return response
        except Exception as e:
            print(str(e))
            message = 'Note not found'
            return message


@notes.route('/api/search', methods=['GET'])
@rate_limited()
@token_required
def search_notes(current_user):
    if request.method == 'GET':
        print("Inside Search Notes")
        response = dict()
        try:
            username = current_user["username"]
            query = request.args.get('q')
            if query:
                response = NotesAC.search_notes_using_query(username, query)
            else:
                response["message"] = "Please provide a search query!"
                response["status"] = "ERROR"
            return response
        except Exception as e:
            print(str(e))
            response["message"] = 'Notes not found'
            return response
