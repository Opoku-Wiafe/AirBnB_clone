#!/usr/bin/python3
"""Module class for FileStorage"""

import datetime
import json
import os

class FileStorage:
    """Access and stor data passed by user"""

    __obj = {}
    __file_path = "file.json"
    

    def new(self, obj):
        """sets in __obj the obj with key <obj class name>.id"""
        keys = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__obj[keys] = obj

    def all(self):
        """show the dict __obj"""
        return FileStorage.__obj

    def save(self):
        """ convert __obj to the JSON file (path: __file_path)"""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as y:
            x = {i: j.to_dict() for i, j in FileStorage.__obj.items()}
            json.dump(x, y)

    def classes(self):
        """show a dict of valid classes that are referenced"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes

    def reload(self):
        """Reloads the stored objects"""
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as y:
            obj_dict = json.load(y)
            obj_dict = {i: self.classes()[j["__class__"]](**j)
                        for i, j in obj_dict.items()}
            FileStorage.__obj = obj_dict

    def attributes(self):
        """Returns the valid attributes and their types for classname"""
        attributes = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
        }
        return attributes
