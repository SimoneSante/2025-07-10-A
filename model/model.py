import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph =nx.DiGraph()
        self._idMap={}

    def build_graph(self,a1,a2,cat):
        self._graph.clear()
        self._idMap.clear()

        nodi=DAO.get_nodi(int(cat))
        self._graph.add_nodes_from(nodi)
        for n in nodi:
            self._idMap[n.product_id]=n


        edges=DAO.get_archi(a1,a2,int(cat))


        for a in edges:
            if int(a[1]) == int(a[3]):
                self._graph.add_edge(self._idMap[a[0]], self._idMap[a[2]],
                                     weight=int(int(a[1])+int(a[3])))
                self._graph.add_edge(self._idMap[a[2]], self._idMap[a[0]],
                                     weight=int(int(a[1])+int(a[3])))
            if int(a[1]) > int(a[3]):
                self._graph.add_edge(self._idMap[a[0]], self._idMap[a[2]],
                                     weight=int(int(a[1]) + int(a[3])))
            if int(a[1]) < int(a[3]):
                self._graph.add_edge(self._idMap[a[2]], self._idMap[a[0]],
                                     weight=int(int(a[1]) + int(a[3])))


    def getDateCategory(self):
        return DAO.getCategories()

    def get_stats(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getDateRange(self):
        return DAO.getDateRange()

    def topprod(self):
        nodi=self._graph.nodes()
        li=[]
        for n in nodi:
            peso_in=0.0
            peso_out=0.0

            archi_out=list(self._graph.out_edges(n, data=True))

            for k in archi_out:
                peso_out=peso_out+float(k[2]["weight"])

            archi_in = list(self._graph.in_edges(n, data=True))
            for k in archi_in:
                peso_in=peso_in+float(k[2]["weight"])
            li.append((n,(peso_out-peso_in)))
        li = sorted(li, key=lambda x: x[1], reverse=True)
        aa=[]
        for t in range(5):
            aa.append(li[t])
        return aa