import preprocessingGraph as pg
import numpy as np
from haversine import haversine
from sklearn.neighbors import KDTree

xmldoc = pg.parseXML("data/map.graphml")

def getOSMId(lat, lon):
    itemlist = xmldoc.getElementsByTagName('node')
    for eachNode in range(len(itemlist)):
        dataPoints = itemlist[eachNode].getElementsByTagName('data')
        if(dataPoints[0].firstChild.data==str(lat)):
            if(dataPoints[1].firstChild.data==str(lon)):
                return (itemlist[eachNode].attributes['id'].value)  

def getLatLon(OSMId):
    ls = []
    itemlist = xmldoc.getElementsByTagName('node')
    for eachNode in range(len(itemlist)):
        dataPoints = itemlist[eachNode].getElementsByTagName('data')
        if(itemlist[eachNode].attributes['id'].value==str(OSMId)):
            ls.append(float(dataPoints[0].firstChild.data))
            ls.append(float(dataPoints[1].firstChild.data))
            break
    return tuple(ls)
    
def calculateHeuristic(curr,destination):
    return (haversine(curr,destination))
    
def getNeighbours(OSMId, destinationLetLon):
    neighbourDict = {}
    tempList = []
    itemList = xmldoc.getElementsByTagName('edge')
    for eachEdge in range(len(itemList)):
        length = 0
        if(itemList[eachEdge].attributes['source'].value==str(OSMId)):
            temp_nbr = {}
            
            dataPoints = itemList[eachEdge].getElementsByTagName('data')
            
            for eachData in range(len(dataPoints)):
                if(dataPoints[eachData].attributes['key'].value=="d10"):
                    length = dataPoints[eachData].firstChild.data
                    
            neighbour = itemList[eachEdge].attributes['target'].value
            curr = getLatLon(neighbour)
            heuristic = calculateHeuristic(curr, destinationLetLon)
            
            temp_nbr[neighbour] = [curr, length, heuristic]
            tempList.append(temp_nbr)
            
    neighbourDict[OSMId] = tempList
    return (neighbourDict)

def getNeighbourInfo(neighbourDict):
    neighbourId = 0
    neighbourHeuristic = 0
    neighbourCost = 0
    for key, value in neighbourDict.items():
        
        neighbourId = key
        neighbourHeuristic = float(value[2])
        neighbourCost = float(value[1])/1000
        neighbourLatLon = value[0]
        
    return neighbourId, neighbourHeuristic, neighbourCost, neighbourLatLon

#Argument should be tuple
def getKNN(pointLocation):
    itemlist = xmldoc.getElementsByTagName('node')
    locations = []
    for eachNode in range(len(itemlist)):
        dataPoints = itemlist[eachNode].getElementsByTagName('data')
        locations.append((dataPoints[0].firstChild.data,dataPoints[1].firstChild.data))

    locations_arr = np.asarray(locations, dtype=np.float32)
    point = np.asarray(pointLocation, dtype=np.float32)

    tree = KDTree(locations_arr, leaf_size=2)
    dist, ind = tree.query(point.reshape(1,-1), k=3) 
    
    nearestNeighbourLoc = (float(locations[ind[0][0]][0]), float(locations[ind[0][0]][1]))
    return nearestNeighbourLoc

def getResponsePathDict(paths, source, destination):
    finalPath = []
    child = destination
    parent = ()
    cost = 0
    while(parent!=source):
        tempDict = {}
        cost = cost + float(paths[str(child)]["cost"])
        parent = paths[str(child)]["parent"]
        parent = tuple(float(x) for x in parent.strip('()').split(','))
        
        tempDict["lat"] = parent[0]
        tempDict["lng"] = parent[1]
        
        finalPath.append(tempDict)
        child = parent
        
    return finalPath, cost