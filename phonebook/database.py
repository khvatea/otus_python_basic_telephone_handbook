import json
import difflib
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

    def compare(self) -> list:
        """
        Comparison of the handbook before and after the change
        :return: List of changes
        """
        # Read the original handbook file
        with open(self.file, "r", encoding='utf8') as origin:
            source_json = json.load(origin)

        # Saving intermediate changes to a handbook buffer
        with open(self.file_buff, "w", encoding='utf8') as buffer:
            json.dump(self.contacts, buffer, ensure_ascii=False, indent=4)
        # Reread the stream from the beginning of the file
        with open(self.file_buff, "r", encoding='utf8') as buffer:
            source_buffer = json.load(buffer)

        ret = []
        before = [str(row) for row in source_json]
        after = [str(row) for row in source_buffer]
        difflist = difflib.ndiff(before, after)

        for line in difflist:
            if line.startswith(u'+'):
                ret.append("\033[3m\033[32m{}\033[0m\n".format(line))
            elif line.startswith(u'-'):
                ret.append("\033[3m\033[31m{}\033[0m\n".format(line))
            elif line.startswith(u'?'):
                ret.append("{}".format(line))
        return ret

    def close(self):
        # if os.path.exists(self.file_buff):
        if pathlib.Path(self.file_buff).exists():
            pathlib.Path(self.file_buff).unlink()
        print("Выход...")