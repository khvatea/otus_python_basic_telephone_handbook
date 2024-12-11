from .database import Database
import difflib
import json


class Handbook(Database):
    """Controller for interacting with the handbook database and user queries"""

    def add_row(self, new_contact: dict):
        """
        Add an entry to the handbook
        :param new_contact: New contact in dict format
        :return:
        """
        self.contacts.append(new_contact)

    def find_rows(self, search_string: str, find_by_field="name") -> list:
        """
        Searching for contacts in the handbook
        :param search_string: Search string
        :param find_by_field: Field to search for
        :return: Search result
        """
        result = [contact for contact in self.contacts if search_string in contact[find_by_field]]
        return result

    def update_row(self, name: str, update_contact: dict) -> dict:
        """
        Update a handbook entry
        :param name: Name of the record that is being updated
        :param update_contact: Data according to handbook fields in dict format
        :return: Updated contact
        """
        for contact in self.contacts:
            if contact["name"] == name:
                contact.update(update_contact)
                return contact

    def delete_row(self, name: str):
        """
        Removing an entry from the handbook
        :param name: Name of the entry to be deleted
        :return: Remove contact in dict format
        """
        for contact in self.contacts:
            if contact["name"] == name:
                self.contacts.remove(contact)
                return contact

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
