import json
import pathlib

class Database:
    def __init__(self, file: str):
        """
         Init and Open phone book from file.
         Writes a List object with contacts in dict format.
        :param file: JSON file containing phone book contact entries
        """
        self.file = file
        self.file_buff = "{}/buff.{}".format(pathlib.Path(file).parent.resolve() ,pathlib.Path(file).name)
        self.contacts = []

    def open(self):
        # Open file, read and pass to list object
        with open(self.file, "r", encoding='utf8') as stream:
            handbook_json = json.load(stream)

        # Create a temporary buffer file
        with open(self.file_buff, "w", encoding='utf8') as stream:
            json.dump(handbook_json, stream, ensure_ascii=False, indent=4)

        self.contacts = handbook_json

    def save(self):
        """
        Save the handbook in JSON format
        """
        with open(self.file, "w", encoding='utf8') as stream:
            json.dump(self.contacts, stream, ensure_ascii=False, indent=4)


    def close(self):
        if pathlib.Path(self.file_buff).exists():
            pathlib.Path(self.file_buff).unlink()
