import copy

import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        self._nodes = []
        self._edges = []
        self.G = nx.Graph()
        self._idMap = {}
        self.soluzione_best=[]


    def build_graph(self, durata: int):

        self.G.clear()

        all_albums=DAO.get_album(durata)

        for a in all_albums:
            self._idMap[a.id] = a


        archi=DAO.get_connessioni()


        for arco in archi:

            a1=arco[0]
            a2=arco[1]

            if a1 in self._idMap and a2 in self._idMap:
                nodo_obj_1 = self._idMap[a1]
                nodo_obj_2 = self._idMap[a2]

                self.G.add_edge(nodo_obj_1, nodo_obj_2)

        self._nodes = list(self.G.nodes())

        return self.G

    def get_component(self, album):
        if album not in self.G:
            return []
        return list(nx.node_connected_component(self.G, album))


    def get_set_album_best(self, start_album, max_duration):
        componente = self.get_component(start_album)
        self.soluzione_best = []
        self.ricorsione(componente, [start_album], start_album.duration, max_duration)
        return self.soluzione_best


    def ricorsione(self, albums, current_set, current_duration, max_duration):
        if len(current_set)> len(self.soluzione_best):
            self.soluzione_best = copy.deepcopy(current_set)

        for album in albums:
            if album in current_set:
                continue
            new_duration = album.duration + current_duration
            if new_duration <= max_duration:
                current_set.append(album)
                self.ricorsione(albums, current_set, new_duration, max_duration)
                current_set.pop()







