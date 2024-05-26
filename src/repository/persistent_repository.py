"""
@Author: Bianca Popu (bia1708)
@Date: 12/03/2024
@Links: https://github.com/bia1708/cimple.git
"""
import os
import pickle

from src.repository.repository import Repository


class PersistentRepository(Repository):
    """
    Persistent repository class.
    :param filename: `str` filename to save the repository to. By default, saved in the artifacts folder.
    :ivar __items: `list` of items stored in the repository.
    """
    def __init__(self, filename):
        super().__init__()
        if not os.path.exists("artifacts/"):
            os.makedirs("artifacts/")
        self.__filename = filename
        if not os.path.isfile(self.__filename):
            open(self.__filename, 'wb')
        if os.stat(self.__filename).st_size == 0:
            self.__items = []
        else:
            self.__items = self.read_from_file()

    def add(self, item):
        """
        Add an item to the repository.
        :param item: `AnyType` Item to add.
        """
        self.__items.append(item)
        self.write_to_file()

    def delete(self, item):
        """
        Delete an item from the repository.
        :param item: `AnyType` Item to delete.
        """
        self.__items.remove(item)
        self.write_to_file()

    def update(self, old_item, item):
        """
        Update an item from the repository.
        :param old_item: `AnyType` Old item to update.
        :param item: `AnyType` New item to update.
        """
        self.__items.remove(old_item)
        self.__items.append(item)
        self.write_to_file()

    def update_current(self, item):
        """
        Move an item from the repository to the front of the list.
        :param item: `AnyType` Item to move.
        """
        self.__items.remove(item)
        self.__items.insert(0, item)

    def get_current(self):
        """
        Get the current item from the repository (the one at the front of the list).
        :return: `AnyType` First item in the list or None if no item was found.
        """
        return self.__items[0] if len(self.__items) > 0 else None

    def read_from_file(self):
        """
        Read the items from the given file.
        :return: `List` File contents, deserialized into a list.
        """
        with open(self.__filename, 'rb') as file:
            return pickle.load(file)

    def write_to_file(self):
        """
        Write the items to the given file.
        """
        with open(self.__filename, 'wb') as file:
            pickle.dump(self.__items, file)

    def get_all(self):
        """
        Get all items from the repository.
        :return: `List` All items from the repository.
        """
        return self.__items

    def close(self):
        """
        Close the repository by writing the items to the given file.
        """
        self.write_to_file()

    def get_server_by_url(self, url):
        """
        Get an item with the given url from the repository.
        :param url: `str` Url of the item to fetch.
        :return: `Server` Item with the given url.
        """
        for server in self.__items:
            if server.get_url() == url:
                return server
        return None
