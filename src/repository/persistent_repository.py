import pickle
import os

class PersistentRepository():
    def __init__(self, filename):
        self.__filename = filename
        if not os.path.isfile(self.__filename):
            open(self.__filename, 'wb')
        if os.stat(self.__filename).st_size == 0:
            self.__items = []
        else:
            self.__items = self.read_from_file()

    def add(self, item):
        self.__items.append(item)
        self.write_to_file()

    def delete(self, item):
        self.__items.remove(item)
        self.write_to_file()

    def update(self, old_item, item):
        self.__items.remove(old_item)
        self.__items.append(item)
        self.write_to_file()
        
    def read_from_file(self):
        with open(self.__filename, 'rb') as file:
            return pickle.load(file)

    def write_to_file(self):
        with open(self.__filename, 'wb') as file:
            pickle.dump(self.get_all_serialized(), file)
    
    def get_all(self):
        return self.__items
    
    def get_all_serialized(self):
        return [server.serialize() for server in self.__items]