import xml.dom.minidom as mn

def reduce_edges(graphml_file_path, output_file_path):
    # Parse the GraphML file using XML DOM
    doc = mn.parse(graphml_file_path)

    # Get the root element
    root = doc.documentElement
    graph_element = root.getElementsByTagName("graph")[0]
    # print(graph_element._get_childNodes())

    edges = root.getElementsByTagName("edge")

    # only retain edges that have key = d6 or d8
    rm = True
    for edge in edges[:]:
        # print(edge.data.__str__())
        # if edge.data.getAttribute("key") not in ["d6", "d8"]:
        #     graph_element.removeChild(edge)
        data_elements = edge.getElementsByTagName('data')
        for data_element in data_elements:
            if data_element.getAttribute("key") in ["d10", "d8"]:
                print(data_element.getAttribute("key"))
                rm = False
                break
        if rm:
            graph_element.removeChild(edge)

        rm = True


    after_edges = root.getElementsByTagName("edge")

    # Filter nodes that are not associated with edges
    nodes_with_edges = set()
    for edge in after_edges:
        nodes_with_edges.add(edge.getAttribute("source"))
        nodes_with_edges.add(edge.getAttribute("target"))
    
    print(len(nodes_with_edges))

    nodes = root.getElementsByTagName("node")
    print(len(nodes))
    for node in nodes[:]:
        node_id = node.getAttribute("id")
        if node_id not in nodes_with_edges:
            graph_element.removeChild(node)

    nodes = root.getElementsByTagName("node")
    print(len(nodes))

    with open(output_file_path, "w") as output_file:
        doc.writexml(output_file)

if __name__ == "__main__":
    reduce_edges("data/map_full.graphml", "data/map.graphml")
