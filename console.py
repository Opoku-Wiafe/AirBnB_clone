#!/usr/bin/python3
"""HBnB console module, a console replica of the AirBnB"""

import cmd
from models.base_model import BaseModel
from models import storage
import re
import json


class HBNB_command (cmd.Cmd):
    """This is a command line interpreter"""

    prompt = "(hbnb) "
  
    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """do nothing when the users do leaves line blank"""
        pass

    def default(self, line):
        """Goto point when the user enters an invalid statement"""
        self._precmd(line)
    
    def do_EOF(self, line):
        """End Of Function command to exit the program"""
        print("")
        return True
    
    def do_create(self, line):
        """Creates a new instance of BaseModel, save it as <class>"""
        if not line:
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class doesn't exist **")
        else:
            new_instance = storage.classes()[line]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, line):
        """Prints the string representation of an instance as <class>
        """
        if not line:
            print("** class name missing **")
            return

        words = line.split(' ')
        class_name, instance_id = words[0], words[1] if len(words) > 1 else None

        if class_name not in storage.classes():
            print("** class doesn't exist **")
        elif not instance_id:
            print("** instance id missing **")
        else:
            key = f"{class_name}.{instance_id}"
            instance = storage.all().get(key)
            print("** no instance found **" if instance is None else str(instance))
    
    def do_destroy(self, line):
        """Deletes an instance based on the class name and id"""
    
        if not line:
            print("** class name missing **")
            return
        words = line.split(' ')
        c_name, inst_id = words[0], words[1] if len(words) > 1 else None

        if c_name not in storage.classes():
            print("** class doesn't exist **")
        elif not inst_id:
            print("** instance id missing **")
        else:
            key = f"{c_name}.{inst_id}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                del storage.all()[key]
                storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances based or not
        on the class name"""
        if not line:
            n_list = [str(obj) for obj in storage.all().values()]
        else:
            words = line.split(' ')
            c_name = words[0]
            if c_name not in storage.classes():
                print("** class doesn't exist **")
                return
            new_list = [str(obj) for obj in storage.all().values() if type(obj).__name__ == c_name]
        print(n_list)
        
    def do_count(self, line):
        """Counts the instances of a class.
        """
        words = line.split(' ')
        if not words[0]:
            print("** class name missing **")
        elif words[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            matches = [
                k for k in storage.all() if k.startswith(
                    words[0] + '.')]
            print(len(matches))

    def do_update(self, line):
        """Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file).
        """
        if line == "" or line is None:
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        find = re.search(rex, line)
        class_name = find.group(1)
        uid = find.group(2)
        attribute = find.group(3)
        value = find.group(4)
        if not find:
            print("** class name missing **")
        elif class_name not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(class_name, uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[class_name]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass  # fine, stay a string then
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

        def _precmd(self, line):
            """Intercepts commands to test for class.syntax()"""
            # print("PRECMD:::", line)
            search = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
            if not search:
                return line
            classname = search.group(1)
            method = search.group(2)
            args = search.group(3)
            match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
            if match_uid_and_args:
                uid = match_uid_and_args.group(1)
                attr_or_dict = match_uid_and_args.group(2)
            else:
                uid = args
                attr_or_dict = False

            attr_and_value = ""
            if method == "update" and attr_or_dict:
                match_dict = re.search('^({.*})$', attr_or_dict)
                if match_dict:
                    self.update_dict(classname, uid, match_dict.group(1))
                    return ""
                match_attr_and_value = re.search(
                    '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
                if match_attr_and_value:
                    attr_and_value = (match_attr_and_value.group(
                        1) or "") + " " + (match_attr_and_value.group(2) or "")
            command = method + " " + classname + " " + uid + " " + attr_and_value
            self.onecmd(command)
            return command
        
        def update_dict(self, class_name, uid, sup_dict):
            """Assisting method for update() also with dict."""
            i = sup_dict.replace("'", '"')
            j = json.loads(i)
            if not class_name:
                print("** class name missing **")
            elif class_name not in storage.classes():
                print("** class doesn't exist **")
            elif uid is None:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(class_name, uid)
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    attributes = storage.attributes()[class_name]
                    for attribute, value in j.items():
                        if attribute in attributes:
                            value = attributes[attribute](value)
                        setattr(storage.all()[key], attribute, value)
                    storage.all()[key].save()

if __name__ == "__main__":
    HBNB_command().cmdloop()