# fichier bloc.py
import json
from hashlib import sha256


class Bloc:
    def __init__(self, hauteur, txs, timestamp, hachage_precedent, nonce=0):
        self.hauteur = hauteur # index
        self.txs = txs  # des transactions
        self.timestamp = timestamp  # l'heure où le bloc a été miné ou créé
        self.hachage_precedent = hachage_precedent
        self.nonce = nonce   # un entier qui permet d'avoir un hachage avec le nombre de zéro voulue par la difficulté

    def calculer_hachage(self):
        bloc_litteral = json.dumps(self.__dict__, sort_keys=True)
        return sha256(bloc_litteral.encode()).hexdigest()
