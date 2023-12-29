def generatePaths(theGraph, startNode, endNode, allPaths, allPathsB, pathSoFar="", pathSoFarLst=()):
    """
    Recursive function. Finds all paths through the specified
    graph from start node to end node. For cyclical paths, this stops
    at the end of the first cycle.
    """
    pathSoFar = pathSoFar + startNode
    pathSoFarLst = list(pathSoFarLst) + [startNode]

    for node in theGraph[startNode]:
        if node == endNode:
            # pathSoFarLst.append(node)
            allPathsB.append(list(pathSoFarLst) + [node])
            allPaths.append(pathSoFar + node)
            pass
        else:
            generatePaths(theGraph, node, endNode, allPaths, allPathsB, pathSoFar, tuple(pathSoFarLst))
    return (allPaths, allPathsB)

def main():
    graph = {"A":["B", "D", "E"], "B":["C"], "C":["D", "E"], "D":["C", "E"], "E":["B"]}
    paths, pathsB = [], []
    paths, pathsB  = generatePaths(graph, "A", "C", paths, pathsB)
    print (paths)
    print (pathsB)

main()