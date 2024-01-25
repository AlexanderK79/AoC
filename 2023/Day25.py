import argparse
import matplotlib.pyplot as plt
import networkx as nx
import heapq

class WeatherMachine:
    def __init__(self) -> None:
        self.content = list()
        self.parts = {}
        self.paths = {} # N1 = key, N2 = target, path, pathlength
        self.links = {} # N1 = key, N2 = target, direction: N1 -> N2 = 1, N1 <-> N2, = 0, N1 <- N2 = -1
        pass
    def build(self, fContent):
        self.content = fContent
        for (i, thisLine) in enumerate(fContent):
            thisP, thisPdest = thisLine.split(': ')
            self.parts[thisP] = {'dest': thisPdest.split(' '), 'source': []}
        for thisP in set([item for sublist in [i['dest'] for i in self.parts.values()] for item in sublist]):
            if thisP in self.parts.keys(): continue
            self.parts[thisP] = {'dest': [], 'source': []}
        pass
        [[self.parts[dest]['source'].append(thisP) for dest in self.parts[thisP]['dest']] for thisP in self.parts.keys()]
        self.build_links()

    def build_links(self, ignoreLinks=[]):    # build all links
        self.links = {}
        ignoreLinks = [(i['source'], i['target']) for i in ignoreLinks]
        for thisP, val in self.parts.items():
            self.links[thisP] = {}
            for target in val['dest']:
                if (thisP, target) in ignoreLinks: continue
                thisDirection = 0 if thisP in self.parts[target]['dest'] else 1
                self.links[thisP][target] = {'source': thisP, 'target': target, 'direction': thisDirection, 'weight': 1, 'usage_count': 0}
        pass
    def process_paths(self, include_reverse_links=False, reset=False):
        if reset: self.paths = {}
        for thisP, thisVal in self.parts.items():
            prioQ = []
            nextLen, nextDest, nextPath = 0, thisP, [thisP]
            heapq.heappush(prioQ, (nextLen, nextDest, nextPath))
            self.paths[thisP] = {}
            while len(prioQ) > 0:
                nextLen, nextP, thisPath = heapq.heappop(prioQ)
                nextLen += 1
                possibleDests = self.parts[nextP]['dest'] + self.parts[nextP]['source'] if include_reverse_links else self.parts[nextP]['dest']
                for nextDest in possibleDests:
                    nextPath = thisPath + [nextDest]
                    if self.paths[thisP].get(nextDest, None) == None: self.paths[thisP][nextDest] = {}
                    if nextLen < self.paths[thisP][nextDest].get('nodeDest', 999999): # shorter path found
                        self.paths[thisP][nextDest] = {'nodeDest': nextLen, 'path': nextPath}
                        heapq.heappush(prioQ, (nextLen, nextDest, nextPath))
                
            # update links usage count
            for thisDest, thisVal in self.paths[thisP].items():
                if thisVal == {}: continue
                for i, thisNode in enumerate(thisVal['path'][:-1]):
                    if self.links.get(thisVal['path'][i], {}).get(thisVal['path'][i+1], None) != None:
                        self.links[thisVal['path'][i]][thisVal['path'][i+1]]['usage_count'] += 1
                    elif self.links.get(thisVal['path'][i+1], {}).get(thisVal['path'][i], None) != None:
                        self.links[thisVal['path'][i+1]][thisVal['path'][i]]['usage_count'] += 1
                    else:    
                        pass
                        # this bridge is gone
            pass


    def draw(self):
        G = nx.Graph()
        for s in self.links.values():
            for vals in s.values():
                G.add_edge(vals['source'], vals['target'], weight = vals['weight'])

        elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.5]
        esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 0.5]

        pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

        # nodes
        nx.draw_networkx_nodes(G, pos, node_size=700)

        # edges
        nx.draw_networkx_edges(G, pos, edgelist=elarge, width=3)
        nx.draw_networkx_edges(
            G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="solid"
        )

        # node labels
        nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif")
        # edge weight labels
        # edge_labels = nx.get_edge_attributes(G, "weight")
        # nx.draw_networkx_edge_labels(G, pos, edge_labels)

        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()

def main(stdscr):
    with open(fName, 'r+') as f:
        fContent = f.read().splitlines()
    

    myWM = WeatherMachine()
    result = myWM.build(fContent=fContent)
    if args.draw: myWM.draw()

    # find the shortest path from each node to every other node
    myWM.process_paths(include_reverse_links=True)

    # count how many times each link is used in all paths; the bridges are most used
    # when the first bridge is found, destroy it, and run the paths again, until all 3 are found
    bridges = []
    if args.verbose: print('Find bridges')
    while len(bridges) < 3:
        thisBridge = sorted([item for sublist in [i.values() for i in myWM.links.values()] for item in sublist], key=lambda item: item['usage_count'], reverse=True)[0]
        bridges.append(thisBridge)
        # destroy the bridge
        if args.verbose: print('Destroying bridge', thisBridge)
        myWM.parts[thisBridge['source']]['dest'].remove(thisBridge['target'])
        myWM.parts[thisBridge['target']]['source'].remove(thisBridge['source'])
        if thisBridge['source'] in myWM.parts[thisBridge['target']]['dest']:
            myWM.parts[thisBridge['target']]['dest'].remove(thisBridge['source'])
            myWM.parts[thisBridge['source']]['source'].remove(thisBridge['target'])
        del myWM.links[thisBridge['source']]
        myWM.build_links(ignoreLinks = bridges)
        if args.draw: myWM.draw()
        myWM.process_paths(include_reverse_links=True, reset=True)

    # now calculate the size of each group
    # the nodes of the last bridge are in separate groups
    result = len(myWM.paths[thisBridge['source']]) * len(myWM.paths[thisBridge['target']])

    print(20 * '*')

    result = result

    message = f'The answer to part 1 is (sample should be 54, answer should be 555856): {result}'
    print(message)
    pass



# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '25'
fName = f'2023/input/{day}_sample.txt'
if args.production: fName = f'2023/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)