import filecmp
import json

from py2neo import Graph
from py2neo import Database

graph = Graph("bolt://35.224.32.106:8000", auth=("neo4j", "yelpme"))

def main():
    print("--- test 1: checking if the restaurants returned is ordered by stars ---")
    hold = get_buss("Champlain", "Burgers")
    with open('tests/out/out1.json', 'w') as filehandle:
        json.dump(hold, filehandle)
    #problematic because it's a dictionary thingy that changes order
    #cmp = filecmp.cmp("tests/out/out1.json", "tests/actual/actual1.json")
    #print(cmp)


def get_buss(city, cruisine):
    store = graph.run("MATCH (m:Business)-[:IN_CATEGORY]->(n:Category) WHERE m.city=\""+city+"\" AND n.id=\""+cruisine+"\" RETURN m,n ORDER BY m.stars DESC, m.review_count DESC").data()
    return store

if __name__ == "__main__":
    main()