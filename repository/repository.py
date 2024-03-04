
class Repository:
    def __init__(self):
        self.__items = []

    def add(self, item):
        self.__items.append(item)

    def delete(self, item):
        self.__items.remove(item)

    def update(self, old_item, item):
        self.__items.remove(old_item)
        self.__items.append(item)

    def get_all(self):
        return self.__items
