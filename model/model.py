import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.Graph()
        self._nodes = None
        self._edges = []
        self._map = {}

    def build_grafo(self, durata: int):
        self.G.clear()

        self._nodes = [item for item in DAO.get_album(durata)]
        self.G.add_nodes_from(self._nodes)

        playlist = [item for item in DAO.get_all_playlist()]

        diz = {}
        for album in self._nodes:
            prova = DAO.get_tracks_for_each_album(album.id)
            tracks = [item['id'] for item in prova]
            diz[album] = tracks

        for p in playlist:
            prova1 = DAO.get_tracks_for_each_playlist(p.id)
            pl_tracks = [item['track_id'] for item in prova1]
            for a1 in diz.keys():
                for a2 in diz.keys():
                    if a1 != a2:
                        for t1 in diz[a1]:
                            for t2 in diz[a2]:
                                if t1 in pl_tracks and t2 in pl_tracks:
                                    self.G.add_edge(a1, a2)
                                    self._edges.append((a1, a2))

    def get_nodes(self):
        return self._nodes

    def analisi_componente(self, a1):

        componente = list(nx.node_connected_component(self.G, a1))

        num = 0
        for item in componente:
            num += item.durata

        return num, len(componente)

    def get_set_album(self, a1, d_tot_minuti):

        self._bestSet = []

        if a1 not in self.G:
            return []

        componente = list(nx.node_connected_component(self.G, a1))

        candidati = [item for item in componente if item != a1]

        parziale = [a1]
        durata_iniziale = a1.durata

        if durata_iniziale > d_tot_minuti:
            return [a1]

        self._ricorsione(parziale, candidati, 0, durata_iniziale, d_tot_minuti)

        return self._bestSet

    def _ricorsione(self, parziale, candidati, livello, durata_attuale, limite):

        if len(parziale) > len(self._bestSet):
            self._bestSet = list(parziale)

        if livello == len(candidati):
            return

        curr_album = candidati[livello]

        if durata_attuale + curr_album.durata <= limite:
            parziale.append(curr_album)
            self._ricorsione(parziale, candidati, livello + 1, durata_attuale + curr_album.durata, limite)
            parziale.pop()

        self._ricorsione(parziale, candidati, livello + 1, durata_attuale, limite)



