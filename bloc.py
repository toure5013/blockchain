import json
from hashlib import sha256


class Bloc:
    def __init__(self, hauteur, txs, timestamp, hachage_precedent, nonce=0):
        self.hauteur = hauteur
        self.txs = txs
        self.timestamp = timestamp
        self.hachage_precedent = hachage_precedent
        self.nonce = nonce

    def calculer_hachage(self):
        bloc_litteral = json.dumps(self.__dict__, sort_keys=True)
        return sha256(bloc_litteral.encode()).hexdigest()
