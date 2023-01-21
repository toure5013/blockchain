from bloc import Bloc
import time


class Blockchain:
    # difficulte pour notre algorithm de preuve par le travail
    difficulte = 3  # controle le nombre de zéro au début de hachage des blocs

    def __init__(self):
        self.txs_non_confirmees = []  # [] pour des listes
        self.chaine = []

    def creer_bloc_genese(self):
        # créer un objet bloc
        bloc_genese = Bloc(0, [], 0, "0")
        # associer un hachage quelconque pour le premier bloc
        setattr(bloc_genese, "hachage", bloc_genese.calculer_hachage())
        self.chaine.append(bloc_genese)

    @property
    def dernier_bloc(self):
        return self.chaine[-1]

    def ajouter_bloc(self, bloc, preuve):
        # ajoute un bloc à la chaine après avoir vérifié la preuve

        # Vérif. 1: le hachage précédent contenu dans le bloc à ajouter
        # doit être le hachage du dernier bloc de notre chaine
        if bloc.hachage_precedent != self.dernier_bloc.hachage:
            return False

        # Vérif. 2: La preuve doit être valide
        # c'est à dire elle doit commencer par un certain nombre de 0
        # et correspondre au hachage du bloc
        if not Blockchain.preuve_validee(bloc, preuve):
            return False

        # Si ces conditions sont réunies, nous pouvons valider la preuve
        # en l'ajoutant au champ hachage du bloc à ajouter
        bloc.hachage = preuve
        # et nous ajoutons le bloc à la fin de notre chaine
        self.chaine.append(bloc)
        # Nous renvoyons Vraie
        return True

    @staticmethod
    def preuve_de_travail(bloc):
        bloc.nonce = 0
        hachage_calcule = bloc.calculer_hachage()
        # vérifier que le hachage à le bon nombre de zéro
        while not hachage_calcule.startswith("0" * Blockchain.difficulte):
            bloc.nonce += 1
            hachage_calcule = bloc.calculer_hachage()

        return hachage_calcule

    def ajoute_nvl_tx(self, tx):
        # ajouter à notre liste de transactions non confirmée la transaction tx
        self.txs_non_confirmees.append(tx)

    @classmethod
    def preuve_validee(cls, bloc, preuve):
        # Une preuve valide commence par un certain nombre de 0
        # et elle correspond au hachage du bloc
        return (
            preuve.startswith("0" * Blockchain.difficulte)
            and preuve == bloc.calculer_hachage()
        )

    @classmethod
    def verifier_validite_chaine(cls, chaine):
        # Vérifie tout les bloc d'une blockchain
        # Nous supposons que le chaine est correcte
        validation_minage = True
        # et nous commençons avec le premier bloc
        hachage_precedent = "0"

        # pour chaque bloc de la chaine
        for bloc in chaine:
            # nous sauvegardons le hachage du bloc
            hachage_preuve = bloc.hachage
            # avant de le supprimer
            delattr(bloc, "hachage")

            # pour le recalculer en vérifiant qu'il est correcte
            if (
                # si ce n'est pas le cas
                not cls.preuve_validee(bloc, hachage_preuve)
                # ou si le hachage du précédent bloc inspecté ne correspond pas
                # a ce que nous avons enregistré pour le bloc courament inspecté
                or hachage_precedent != bloc.hachage_precedent
            ):
                # nous invalidons la chaine
                validation_minage = False
                # et sortons
                break
            # quand la vérification du bloc est correcte
            # nous rétablissons le champ hachage du bloc avec la valeur que nous avions sauvegardé
            # et nous mettons assignons à la variable hachage précédent le hachage du bloc courant.
            bloc.hachage, hachage_precedent = hachage_preuve, hachage_preuve
            # puis nous vérifions le bloc suivant de la chaine jusqu'à épuisement.

        return validation_minage

    def miner(self):
        # S'il n'y a pas de tx non confirmées on renvoie False
        if not self.txs_non_confirmees:
            return False

        # Nous créons un nouveau bloc
        # la hauteur est incrémentée
        # les transactions sont celles non confirmées
        # le timestamp c'est l'heure actuelle
        # le hachage_précédent c'est le hachage du dernier bloc
        # de la chaine
        nv_bloc = Bloc(
            hauteur=self.dernier_bloc.hauteur + 1,
            txs=self.txs_non_confirmees,
            timestamp=time.time(),
            hachage_precedent=self.dernier_bloc.hachage,
        )

        # Nous ajoutons le nouveau bloc avec la preuve du travail à notre chaine.
        self.ajouter_bloc(nv_bloc, preuve=self.preuve_de_travail(nv_bloc))

        # Nous vidons la liste de transaction non confirmées
        self.txs_non_confirmees = []

        # et nous renvoyons Vrai si tout c'est bien passé.
        return True
