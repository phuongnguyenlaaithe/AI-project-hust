# read n3.csv, convert osmid to lat, lon
import time
import pandas as pd
# temp path includes time of execution
temp_path = "data/tmp/path_"+str(time.time())+".csv"

# ndf = pd.read_csv("data/n3.csv")

def convert_id(id):
    ndf = pd.read_csv("data/n3.csv")
    ndf = ndf.set_index('osmid')
    lat = ndf.loc[id]['y']
    lon = ndf.loc[id]['x']
    return [lat, lon, id]

def convert_id_list(id_list: list[str]):
    ndf = pd.read_csv("data/n3.csv")
    ndf = ndf.set_index('osmid')
    # write to csv
    df = pd.DataFrame(columns=['osmid', 'y', 'x'])
    for id in id_list:
        lat = ndf.loc[id]['y']
        lon = ndf.loc[id]['x']
        df = df._append({'osmid': id, 'y': lat, 'x': lon}, ignore_index=True)
    df.to_csv(temp_path, index=False)

def get_lat_lon(id):
    ndf = pd.read_csv("data/n3.csv")
    ndf = ndf.set_index('osmid')
    lat = ndf.loc[id]['y']
    lon = ndf.loc[id]['x']
    return {"lat": lat, "lng": lon}

def convert_path(path: list[str]):
    finalPath = []
    for node in path:
        finalPath.append(get_lat_lon(node))
    return finalPath
