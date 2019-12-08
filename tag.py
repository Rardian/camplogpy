class Tag:
    def __init__(self, id):
        self.id = id
        self.name = id[1:len(id)]
        self.type = TagSwitcher().switch(id[0])
        self.count = 1
    
    def increaseCount(self):
        self.count += 1
        return self

    def __str__(self):
        return self.id + "-" + self.name + "(" + self.type + "): " + str(self.count)
    
class TagSwitcher:

    def switch(self, arg):
        options = {'@' : "Charakter",
                    '#' : "Region",
                    '*' : "Monster",
                    '^' : "Gruppe",
                    '$' : "Schatz",
                    '!' : "Ort",
                    '~' : "Plot",
                    '§' : "Abschnitt",
                    '+' : "Aspekt",
                    '%' : "Datum",
        }

        return options.get(arg, "unbekannt-" + arg)
