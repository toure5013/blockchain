import json
import time
from blockchain import Blockchain
from bloc import Bloc

from flask import Flask, request
import requests

from typing import Set

app = Flask(__name__)
print(__name__)
blockchain = Blockchain()
blockchain.creer_bloc_genese()

pairs: Set[str] = set()


@app.route("/nvl_tx", methods=["POST"])
def nvl_tx():
    donnees_tx_recues = request.get_json()

    # pour chacun des champs obligatoires ["author", "content"]
    # Nous vérifions que le champ est bien renseigné
    if not all([c for c in ["author", "content"] if donnees_tx_recues.get(c, False)]):
        return "Donnée de transaction invalide", 404

    # nous ajoutons l'heure
    donnees_tx_recues["timestamp"] = time.time()

    # et ajoutons le bloc dans notre blockchain
    blockchain.ajoute_nvl_tx(tx=donnees_tx_recues)

    # Nous Renvoyons un message si tous c'est bien passé
    return "Succès", 201


@app.route("/chaine", methods=["GET"])
def recupe_chaine():
    # Quand le noeud serveur est appelé sur cette url
    # Nous sauvegardons la chaine dans une variable
    donnee_chaine = [bloc.__dict__ for bloc in blockchain.chaine]

    # et Renvoyons un dictionnaire au format JSON (pour une communication
    # via internet)
    # ce dictionnaire contient la longueur de la chaine,
    # la chaine comme une liste  de bloc au format dictionnaire
    # la liste des adresses des pairs
    return json.dumps(
        {"longueur": len(donnee_chaine), "chaine": donnee_chaine, "pairs": list(pairs)}
    )


@app.route("/miner", methods=["GET"])
def miner_txs_non_confirmees():

    # Nous minons les transactions en attente si il y en a.
    validation_minage = blockchain.miner()

    if not validation_minage:
        return "Pas de transaction à Miner"
    else:
        # Nous sauvegardons la longeur de notre chaine
        longueur_chaine = len(blockchain.chaine)
        # avant d'effectuer l'aglorithme de consensus pour voir
        # si tous les noeuds sont en accord sur la 'meilleure' chaine.
        # la meilleur chaine étant la plus longue blockchain valide
        consensus()
        # si la longueur de notre chaine est plus égale à la longueur
        # de la blockchaine après le consensus, c'est qu'il y a consensus
        if longueur_chaine == len(blockchain.chaine):
            # et nous pouvons annoncer l'acceptation de notre nouveau bloc
            # qui est le dernier à avoir été miné et ajouté à notre blockchain
            announce_nv_bloc(blockchain.dernier_bloc)

        # Nous renvoyons un message d'information
        return f"Le Bloc #{blockchain.dernier_bloc.hauteur} est miné."


@app.route("/enregistrer_noeud", methods=["POST"])
def enregistrer_nvx_pairs():
    adresse_noeud = request.get_json()["adresse_noeud"]
    if not adresse_noeud:
        return "Données invalides.", 400

    pairs.add(adresse_noeud)

    return recupe_chaine()


@app.route("/senregistrer_aupres", methods=["POST"])
def senregistrer_aupres_noeud_existant():
    adresse_noeud = request.get_json()["adresse_noeud"]
    if not adresse_noeud:
        return "Données invalides.", 400

    # voir comment récupére l'adress ngrok
    data = {"adresse_noeud": request.host_url}
    entetes = {"Content-Type": "application/json"}

    reponse = requests.post(
        url=adresse_noeud + "/enregistrer_noeud", data=json.dumps(data), headers=entetes
    )

    if reponse.status_code == 200:
        global blockchain
        global pairs
        chaine_brute = reponse.json()["chaine"]
        blockchain = recupe_chaine_brute(chaine_brute)
        pairs.update(reponse.json()["pairs"])
        return "Enregistrement Réussit", 200
    else:
        return reponse.content, reponse.status_code


def recupe_chaine_brute(chaine_brute):
    blockchain_generee = Blockchain()
    blockchain_generee.creer_bloc_genese()
    for idx, donnees_bloc in enumerate(chaine_brute):
        if idx == 0:
            continue  # skip genesis bloc
        bloc = Bloc(
            donnees_bloc["hauteur"],
            donnees_bloc["txs"],
            donnees_bloc["timestamp"],
            donnees_bloc["hachage_precedent"],
            donnees_bloc["nonce"],
        )
        preuve = donnees_bloc["hachage"]
        bloc_ajoute = blockchain_generee.ajouter_bloc(bloc, preuve)
        if not bloc_ajoute:
            raise Exception("Le contenu de la chaine a été modifié.")
    return blockchain_generee


@app.route("/ajouter_bloc", methods=["POST"])
def verifier_ajouter_bloc():
    # Ce point d'entré permet d'ajouter un bloc à la blockchain
    # du noeud serveur

    # Nous récupérons les données associées avec l'url 'ajouter_bloc'
    donnes_recues = request.get_json()

    # Nous instantions un objet bloc avec mais
    bloc = Bloc(
        donnes_recues["hauteur"],
        donnes_recues["txs"],
        donnes_recues["timestamp"],
        donnes_recues["hachage_precedent"],
        donnes_recues["nonce"],
    )
    # Nous stockons séparément la preuve (hachage)
    preuve = donnes_recues["hachage"]
    # pour la vérifier au moment de l'ajout
    validation_ajout = blockchain.ajouter_bloc(bloc, preuve)

    # Nous renvoyons des messages de validations si tous c'est bien passé.
    return (
        ("Le Bloc a été ajouter à la chaine", 201)
        if validation_ajout
        else ("Le bloc a été ignoré par le noeud.", 400)
    )


@app.route("/tx_en_attente")
def recupe_tx_en_attente():
    return json.dumps(blockchain.txs_non_confirmees)


def consensus():
    global blockchain

    # Nous initialisons la variable qui contiendra
    # la plus longue blockchain, celle du consensus
    plus_lg_blockchain = None
    # Nous sauvegardons la longueur de la chaine du noeud courant
    lg_courante = len(blockchain.chaine)

    # Pour chaque autre noeud (un noeud est une adresse IP)
    for noeud in pairs:
        # Nous appelons la fonction du noeud qui
        # renvois la chaine
        reponse = requests.get(f"{noeud}chaine")
        # Nous récupérons les données de la chaine (longueur et blocs)
        longueur = reponse.json()["longueur"]
        chaine = reponse.json()["chaine"]

        # et nous comparons la longueur de la chaine récupérée avec la longueur de
        # notre chaine.  Nous vérifions aussi la validité de la chaine récupérée
        if longueur > lg_courante and blockchain.verifier_validite_chaine(chaine):
            # si elle est valide et que sa longueur est plus grande que la notre,
            # alors nous l'enregistrons comme la plus longue chaine
            # avant de vérifier les chaines des autres noeuds serveurs
            lg_courante = longueur
            plus_lg_blockchain = chaine

    # Finalement, si nous avons trouver une chaine plus longue que celle
    # du noeud courant,
    if plus_lg_blockchain:
        # Nous remplaçons notre blockchain avec la plus longue chaine
        blockchain = plus_lg_blockchain

        # et renvoyons Vrai
        return True

    # Sinon nous renvoyons Faux
    return False


def announce_nv_bloc(bloc):
    # Lorsque qu'un noeud serveur a miné un nouveau bloc et que le consensus
    # peut être respecter pour ajouter ce bloc à la chaine, alors il faut
    # annoncer la création du bloc pour que les autres noeuds l'ajoute à leur
    # copie de la blockchain

    # pour chaque autre noeud serveur
    for noeud in pairs:
        # nous postons à l'url ajouter_bloc les données du bloc (en __dict__)
        requests.post(
            url=f"{noeud}ajouter_bloc",
            data=json.dumps(bloc.__dict__, sort_keys=True),
            headers={"Content-Type": "application/json"},
        )
