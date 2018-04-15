from handle import *

h = Handle('denmark-latest.osm.pbf')

result = h.import_osm()
print(result)
h.cursor.close()
h.cnx.close()


