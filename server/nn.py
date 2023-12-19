import pandas as pd
from sklearn.neighbors import NearestNeighbors

csv_file_nodes = "data/n3.csv"
csv_file_edges = "data/e3.csv"

def nearest_node(point):
    ndf = pd.read_csv(csv_file_nodes)

    X = ndf[['y', 'x']]
    knn = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(X.values)

    dist, idx = knn.kneighbors([point])
    nearest_node_id = ndf.loc[idx[0][0]]['osmid']
    return nearest_node_id

def k_nearest_nodes(point, k):
    ndf = pd.read_csv(csv_file_nodes)
    edf = pd.read_csv(csv_file_edges)

    X = ndf[['y', 'x']]
    knn = NearestNeighbors(n_neighbors=k, algorithm='auto').fit(X.values)

    dist, idx = knn.kneighbors([point])
    nearest_node_ids = ndf.loc[idx[0]]['osmid'].values.tolist()

    if len(nearest_node_ids) == 1:
        return nearest_node_ids
    return nearest_node_ids[1:]

if __name__ == "__main__":
    lat = 21.0210123
    lon = 105.8613706
    k_nearest_nodes([lat,lon],2)