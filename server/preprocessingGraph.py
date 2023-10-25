import osmnx as ox
from xml.dom import minidom

def generateGraphML(osmFile,filePathML):
    multiGraph = ox.graph_from_xml(osmFile,True,True,True)
    ox.save_graphml(multiGraph, filePathML)

def parseXML(graphMLFile):
    print("Called")
    xmldoc = minidom.parse(graphMLFile)
    return xmldoc

osmFile = "data/map.osm"
filePathML = "data/map.graphml"
