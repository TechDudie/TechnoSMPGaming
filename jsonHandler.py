from json import load, dump
from os.path import exists
import time
template = {
    "guildIds": {"type": "list", "store": []},
    "OnJoinRolesID": {"type": "list", "store": []},
    "WelcomeChannelID": {"type": "int", "store": None},
    "Url": {"type": "str", "store": None},
    "Port": {"type": "int", "store": None},
}


def __createConfig():
    if not exists("settings.json"):
        with open("settings.json", "w") as configHandler:
            dump(template, configHandler, indent=4)


def writeConfig(key: str, value):
    """no idea what it does too sleepy to document it... lol"""
    __createConfig()
    if key in template.keys():
        template_type, value_type = template.get(key).get("type"), type(value).__name__
        if template_type == value_type:
            with open("settings.json", "r") as configHandler:
                data = load(configHandler)
                if template_type == "list":
                    data.get(key).get("store").extend(value)
                elif template_type == "str":
                    data[key]["store"] = value
                elif template_type == "int":
                    data[key]["store"] = value
                with open("settings.json", "w") as configHandler:
                    dump(data, configHandler, indent=4)

        else:
            raise Exception(
                f'{key} has type "{template_type}" but type "{value_type}" was provided'
            )
    else:
        raise Exception(f'"{key}" not found in the settings')


def createConfig(key: str, default_value=None):
    """creates a new entry in the config supported datatypes are int, str, list throws exceptions if keys already exists or when provided datatype isnt supported"""
    __createConfig()
    if not readConfig(key):
        if type(default_value).__name__ in ["int", "str", "list"]:
            data = {key: {"type": type(default_value).__name__, "store": default_value}}
            with open("settings.json", "r") as configHandler:
                loaded_data: dict = load(configHandler)
                data.update(loaded_data)
            with open("settings.json", "w") as configHandler:
                dump(data, configHandler, indent=4)
                
        else:
            raise Exception(
                f'Type "{type(default_value).__name__}" is Invalid Must be int, str, list"'
            )
    elif readConfig(key):
        raise Exception(f'Key "{key}" already Exists')

def deleteConfig(key: str):
    """deletes a key from config if exists else throws an exception"""
    __createConfig()
    loaded_data: dict = {}
    if readConfig(key):
        with open("settings.json", "r") as configHandler:
            loaded_data = load(configHandler)
            loaded_data.pop(key)
        with open("settings.json", "w") as configHandler:
            dump(loaded_data, configHandler, indent=4)
    else:
        raise Exception(f'Key "{key}" does\'nt Exists')

def readConfig(key: str):
    """Reads a key from the config if it exists return's the value else returns None"""
    __createConfig()
    with open("settings.json", "r") as configHandler:
        loaded_data: dict = load(configHandler)
        if key in loaded_data.keys():
            
            return loaded_data[key]["store"]
        return None

def updateConfig(key: str, value):
    """Updates/Replace the value of the given key if exists else throws an exception
       If datatype of the given value doesn't equal to that in the config its
       throws an exception
    """
    __createConfig()
    with open("settings.json", "r") as configHandler:
        loaded_data: dict = load(configHandler)
        if key in loaded_data.keys():
            loaded_data_type, value_type = loaded_data[key]['type'], type(value).__name__
            if  loaded_data_type == value_type:
                loaded_data[key]['store'] = value
                with open("settings.json", "w") as configHandler:
                    dump(loaded_data, configHandler, indent=4)
            else:
                raise Exception(f'value "{value}" has type "{value_type}" while it requires "{loaded_data_type}" type')
        else:
            raise Exception(f'Key "{key}" does\'nt Exists')




