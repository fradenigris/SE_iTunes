from dataclasses import dataclass

@dataclass
class Album:
    id : int
    title : str
    artist_id : int
    durata : int

    def __str__(self):
        return f"{self.id}, titolo: {self.title}, artist_id: {self.artist_id}, durata: {self.durata}"

    def __repr__(self):
        return f"{self.id}, titolo: {self.title}, artist_id: {self.artist_id}, durata: {self.durata}"

    def __hash__(self):
        return hash(self.id)