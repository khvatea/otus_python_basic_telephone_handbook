import json
import pathlib

class Database:
    """Adapter for working with handbook database entries in JSON file format"""

    def __init__(self, file: str):
        """
         Init and Open phone book from file.
         Writes a List object with contacts in dict format.
        :param file: JSON file containing phone book contact entries
        """
        self.__file = file
        self.__file_buff = None
        self.contacts = []

    @property
    def file(self):
        """
        Get JSON file name
        :return: a string containing the name of the JSON file
        """
        return self.__file

    @property
    def file_buff(self):
        """
                Get JSON buffer file name
                :return: a string containing the name of the JSON buffer file
                """
        if self.__file_buff is None:
            self.__file_buff = "{}/buff.{}".format(pathlib.Path(self.file).parent.resolve() ,pathlib.Path(self.file).name)
        return self.__file_buff

    def open(self):
        """
        Open a directory from JSON and upload it to a List object
        :return:
        """
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
        """
        Close the directory and delete the buffer
        """
        if pathlib.Path(self.file_buff).exists():
            pathlib.Path(self.file_buff).unlink()
