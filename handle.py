import mysql.connector
from osmread import parse_file, Node, Way
from path import Path
from os import path


class Handle:

    file_path = ''
    cnx = mysql.connector.connect(option_files="./mysql.cnf")
    cursor = cnx.cursor()

    def __init__(self, osm_file):
        if path.isfile(path.dirname(path.abspath(__file__)) + '/' + osm_file):
            self.file_path = osm_file
        else:
            raise FileNotFoundError

    def import_osm(self, debug=False):
        # Mysql prep
        add_node = ("INSERT INTO node "
                    "(id, lat, lng) "
                    "VALUES (%s, %s, %s)")


        add_edge = ("INSERT INTO edge "
                    "(n1id, n2id, oneway, speed, name, type, distance) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)")

        count_nodes = 0
        count_edges = 0

        try:
            for entity in parse_file(self.file_path):

                # Find nodes
                if isinstance(entity, Node):
                    data_node = (str(entity.id), str(entity.lat), str(entity.lon))
                    self.cursor.execute(add_node, data_node)
                    count_nodes += 1
                    if debug: print("Node {} processed.".format(entity.id))

                # Find edges
                if isinstance(entity, Way) and 'highway' in entity.tags:
                    number_of_node_relationships = len(entity.nodes)

                    if number_of_node_relationships > 2:  # Must mean that the road is divided up between multiple nodes
                        for x in range(0, number_of_node_relationships - 1):
                            path = Path(entity, entity.nodes[x], entity.nodes[x + 1])
                            data_edge = (path.start_node, path.end_node, path.oneway, path.speed, path.name, path.type, "0")
                            self.cursor.execute(add_edge, data_edge)
                            count_edges += 1
                            if debug: print("Edge {} processed.".format(path.id))

                    elif number_of_node_relationships == 2:
                        path = Path(entity, entity.nodes[0], entity.nodes[1])
                        data_edge = (path.start_node, path.end_node, path.oneway, path.speed, path.name, path.type, "0")
                        self.cursor.execute(add_edge, data_edge)
                        count_edges += 1
                        if debug: print("Edge {} processed.".format(path.id))

        except mysql.connector.errors.IntegrityError:  # If entity already exists in db then skip
            pass

        self.cnx.commit()
        return "Number of nodes found: {}\nNumber of edges found: {}".format(count_nodes, count_edges)
