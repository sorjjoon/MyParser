class char():
    def __init__(self, id:int, name:str, char_class="-", server="-" ):
        self.id = id
        self.name = name
        if char_class is None:
            self.char_class = " - "
        else:
            self.char_class = char_class
        if server is None:
            self.server = " - "
        else:
            self.server=server