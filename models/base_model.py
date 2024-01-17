#!/usr/bin/python3
"""Module that defines the BaseModel class"""

import uuid
from models import storage
from datetime import datetime

class BaseModel:
    """
    This class represents the BaseModel class of the HBnB(AirBnB clone)
    project
    """

    def __init__(self, *args, **kwargs):
        """The initial instance of the class attribute
        Arguments:
            -*args: the Lists all arguments of the class
            -**kwargs: Dictionary arguments (key-values)
        """
        if kwargs is not None and kwargs != {}:
            keys_i = iter(kwargs)
        while True:
            try:
                key = next(keys_i)
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]
            except StopIteration:
                break
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
    
    def to_dict(self):
        """Display all dictionary content with keys-values of __dict__"""

        myDict = self.__dict__.copy()
        myDict["__class__"] = type(self).__name__
        myDict["created_at"] = myDict["created_at"].isoformat()
        myDict["updated_at"] = myDict["updated_at"].isoformat()
        return myDict
    
    def __str__(self):
        """Return the user entered string representation"""

        return "[{}] ({}) {}".\
            format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """save the public instance class attribute <updated_at>"""

        self.updated_at = datetime.now()
        storage.save()