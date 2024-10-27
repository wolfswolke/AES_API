import base64
import secrets

import pymongo
import uuid
import hashlib
from logic.date_handler import get_current_date


def generate_secure_token_base64(length=64):
    token_bytes = secrets.token_bytes(length)
    token_base64 = base64.urlsafe_b64encode(token_bytes).decode('utf-8')
    return token_base64


class Mongo:
    def __init__(self):
        self.dyn_server = ""
        self.dyn_db = ""
        self.user_collection = ""
        self.aes_collection = ""
        self.user = {
            "user_id": "",
            "username": "",
            "password_hash": "",
            "token": ""
        }
        self.game_item = {
            "game": "",
            "mainKey": "",
            "dynamicKeys": [],
            "version": "",
            "last_updated": "",
            "last_updated_by": ""
        }
        self.aes_item = {
            "guid": "",
            "key": "",
            "name": "",
        }
        self.mapping_collection = ""
        self.mapping_item = {} # This shit is not documented well... https://github.com/4sval/FModel/wiki/Settings-Explanation#mapping

    def setup(self, server, db, user_collection, aes_collection):
        self.dyn_server = server
        self.dyn_db = db
        self.user_collection = user_collection
        self.aes_collection = aes_collection

    def user_handling(self, username, password, register=False):
        try:
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.user_collection]
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if register:
                username_document = dyn_collection.find_one({'username': username})
                if username_document:
                    return {"status": "ERROR", "message": "Username already taken"}
                user_id = str(uuid.uuid4())
                existing_document = dyn_collection.find_one({'user_id': user_id})
                if existing_document:
                    print(f"ERROR. Generated non unique ID. retrying...")
                    client.close()
                    return self.user_handling(username, password, register)
                new_user = {}
                for key, default_value in self.user.items():
                    new_user[key] = default_value

                new_user["user_id"] = user_id
                new_user["password_hash"] = password_hash
                new_user["username"] = username
                new_user["token"] = generate_secure_token_base64()
                dyn_collection.insert_one(new_user)
                # logger.graylog_logger(level="info", handler="mongodb", message=f"New user added to database: {username}")
                client.close()
                return {"status": "OK", "user_id": user_id, "token": new_user["token"]}
            else:
                existing_document = dyn_collection.find_one({'username': username, 'password_hash': password_hash})
                if existing_document:
                    userid = existing_document["user_id"]
                    token = existing_document["token"]
                    client.close()
                    return {"status": "OK", "user_id": userid, "token": token}
                else:
                    print(f"User not found: {username}")
                    client.close()
                    return {"status": "ERROR", "message": "Username or password incorrect"}
        except Exception as e:
            # logger.graylog_logger(level="error", handler="mongodb_user_db_handler", message=e)
            return {"status": "ERROR", "message": "INTERNAL SERVER ERROR"}

    def get_data_with_list(self, user_id, items, collection):
        try:
            document = {}
            user_id = f"{user_id}"
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[collection]
            existing_document = dyn_collection.find_one({"user_id": user_id})
            if existing_document:
                for item in items:
                    document[item] = existing_document.get(item)
            else:
                print(f"No user found with userId: {user_id}")
                client.close()
                return None
            client.close()
            return document
        except Exception as e:
            # logger.graylog_logger(level="error", handler="mongo_get_data_with_list", message=e)
            return None

    def validate_token(self, token):
        try:
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.user_collection]
            existing_document = dyn_collection.find_one({"token": token})
            if existing_document:
                client.close()
                return {"status": "success", "message": "Token found", "user_id": existing_document["user_id"]}
            else:
                print(f"Token not found: {token}")
                client.close()
                return {"status": "error", "message": "Token not found"}
        except Exception as e:
            print(e)
            # logger.graylog_logger(level="error", handler="mongo_validate_token", message=e)
            return {"status": "error", "message": "Internal Server Error"}

    def get_all_aes(self):
        try:
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.aes_collection]
            aes_list = dyn_collection.find()
            aes_list = list(aes_list)
            client.close()
            return aes_list
        except Exception as e:
            print(e)
            # logger.graylog_logger(level="error", handler="mongo_get_all_aes", message=e)
            return None

    def get_aes_by_game(self, game):
        try:
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.aes_collection]
            aes_list = dyn_collection.find({"game": game})
            aes_list = list(aes_list)
            client.close()
            return aes_list
        except Exception as e:
            print(e)
            # logger.graylog_logger(level="error", handler="mongo_get_aes_by_game", message=e)
            return None

    def add_aes(self, mainKey, game, dynamicKeys, uploader):
        try:
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.aes_collection]
            # check if game already exists
            existing_document = dyn_collection.find_one({"game": game})
            if existing_document:
                print(f"Game already exists: {game}")
                client.close()
                return {"status": "error", "message": "Game already exists"}
            new_aes = {}
            for key, default_value in self.game_item.items():
                new_aes[key] = default_value
            new_aes["game"] = game
            new_aes["mainKey"] = mainKey
            new_aes["dynamicKeys"] = dynamicKeys
            new_aes["last_updated"] = get_current_date()
            new_aes["last_updated_by"] = uploader
            new_aes["version"] = "0.1"
            dyn_collection.insert_one(new_aes)
            client.close()
            return {"status": "success", "message": "AES Item added"}
        except Exception as e:
            print(e)
            # logger.graylog_logger(level="error", handler="mongo_add_aes", message=e)
            return {"status": "error", "message": "Internal Server Error"}

    def update_aes(self, guid, key, name, game, uploader):
        try:
            # todo implement me
            client = pymongo.MongoClient(self.dyn_server)
            dyn_client_db = client[self.dyn_db]
            dyn_collection = dyn_client_db[self.aes_collection]
            existing_document = dyn_collection.find_one({"game": game})
            if existing_document:
                update_query = {
                    '$set': {
                        'last_updated': get_current_date(),
                        'last_updated_by': uploader
                    },
                    '$push': {
                        'aes_collection': {
                            "guid": guid,
                            "key": key,
                            "name": name,
                        }
                    }
                }
                dyn_collection.update_one({"game": game}, update_query)
                client.close()
                return {"status": "success", "message": "AES Item updated"}
            else:
                print(f"No game found with name: {game}")
                client.close()
                return None
        except Exception as e:
            print(e)
            # logger.graylog_logger(level="error", handler="mongo_update_aes", message=e)
            return None


mongo = Mongo()
