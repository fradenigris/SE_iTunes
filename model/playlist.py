from dataclasses import dataclass

@dataclass
class Playlist:
    id: int
    name: str

    def __str__(self):
        return f"{self.id}, nome: {self.name}"

    def __repr__(self):
        return f"{self.id}, nome: {self.name}"

    def __hash__(self):
        return hash(self.id)