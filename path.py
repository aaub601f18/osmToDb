class Path:
    id = ""
    name = ""
    speed = ""
    oneway = ""
    type = ""
    start_node = ""
    end_node = ""

    def __init__(self, entity, start_node, end_node):

        try:
            self.id = entity.id
        except KeyError:
            id = "-"
        try:
            self.name = entity.tags['name']
        except KeyError:
            self.name = "-"
        try:
            if entity.tags['oneway'] == 'yes':
                self.oneway = 'N'
            else:
                self.oneway = 'Y'
        except KeyError:
            self.oneway = 'N'
        try:
           self.speed = entity.tags['maxspeed']
        except KeyError:
            self.speed = "0"

            self.type = entity.tags['highway']

        self.start_node = start_node
        self.end_node = end_node

    def __str__(self):
        return "id: {}, name: {}, speed: {}, oneway: {}, startnode: {}, endnode: {}".\
            format(self.id, self.name, self.speed, self.oneway, self.start_node, self.end_node)
