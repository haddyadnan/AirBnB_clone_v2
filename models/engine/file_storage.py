#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""

    __file_path = "file.json"
    __objects = {}
    __tmp_object = {}

    def all(self, obj=None):
        """Returns a dictionary of models currently in storage"""
        if obj:
            for key, value in FileStorage.__objects.items():
                if obj.__name__ == key.split(".")[0]:
                    FileStorage.__tmp_object[key] = value
            return FileStorage.__tmp_object
        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()["__class__"] + "." + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        if "_sa_instance_state" in FileStorage.__objects.keys():
            del FileStorage.__objects["_sa_instance_state"]
        with open(FileStorage.__file_path, "w") as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def delete(self, obj=None):
        """DELETE obj FROM _object if obj exists"""
        if obj:
            cls_key = obj.__class__.__name__ + "." + obj.id
            if cls_key in FileStorage.__objects.keys():
                del FileStorage.__objects[cls_key]
            if cls_key in FileStorage.__tmp_object.keys():
                del FileStorage.__tmp_object[cls_key]
            self.save()

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review,
        }
        try:
            temp = {}
            with open(FileStorage.__file_path, "r") as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val["__class__"]](**val)
        except FileNotFoundError:
            pass

    def close(self):
        """close method for deserializing the JSON file to objects"""
        self.reload()
