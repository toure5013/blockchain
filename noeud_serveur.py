import json
import time
from typing import Set

from flask import Flask, request
import requests

from blockchain import Blockchain
from bloc import Bloc
from app.config_locale import ADRESSE_MON_SERVEUR

app = Flask(__name__)

blockchain = Blockchain()
blockchain.creer_bloc_genese()
adrs_noeuds_serveurs: Set[str] = set()


@app.route("/nvl_tx", methods=["POST"])
def nvl_tx():
    donnees_tx_recues = request.get_json()

    # pour chacun des champs obligatoires ["auteur", "contenu"]
    # Nous vérifions que le champ est bien renseigné
    if not all([c for c in ["auteur", "contenu"] if donnees_tx_recues.get(c, False)]):
        return "Donnée de transaction invalide", 404

    # nous ajoutons l'heure
    donnees_tx_recues["timestamp"] = time.time()

    # et ajoutons le bloc dans notre blockchain
    blockchain.ajoute_nvl_tx(tx=donnees_tx_recues)

    # Nous Renvoyons un message si tous c'est bien passé
    return "Succès", 201


@app.route("/info_chaine", methods=["GET"])
def recupe_info_chaine():
    # Quand le noeud serveur est appelé sur cette url
    # Nous sauvegardons la chaine dans une variable
    blockhain_brute = [bloc.__dict__ for bloc in blockchain.chaine]

    global adrs_noeud_serveurs
    # et Renvoyons un dictionnaire au format JSON (pour une communication via internet)
    # ce dictionnaire contient la longueur de la chaine,
    # la chaine comme une liste  de bloc au format dictionnaire
    # la liste des adrs_noeuds_serveurs
    return json.dumps(
        {"chaine": blockhain_brute,
         "adrs_noeuds_serveurs": list(adrs_noeuds_serveurs)}
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


@app.route("/enregistrer_nv_noeud", methods=["POST"])
def enregistrer_nv_noeud():
    # Nous recupérons l'adresse à ajouter aux adrs_noeuds_serveurs
    adresse_a_ajouter = request.get_json()["adresse_a_ajouter"]

    # Nous vérifions qu'elle est valide
    if not adresse_a_ajouter:
        return "Données invalides.", 400

    # Nous l'ajoutons alors à l'ensemble des adrs_noeuds_serveurs
    adrs_noeuds_serveurs.add(adresse_a_ajouter)

    # et nous renvoyons les informations liées à notre chaine, c'est à dire
    # le nombre de bloc, les blocs, et les adrs_noeuds_serveurs que nous connaissons
    return recupe_info_chaine()


@app.route("/senregistrer_aupres", methods=["POST"])
def senregistrer_aupres_noeud_existant():
    # Nous récupérons l'adresse du noeud serveur auprès duquel nous voulons nous
    # enregistrer.  Cette information est postée avec via le client
    adr_serveur_distant = request.get_json()["adr_serveur_distant"]

    if not adr_serveur_distant:
        return "Données invalides.", 400

    # Nous activons la fonction 'enregistrer_nv_noeud' du serveur auprès duquel
    # nous voulons nous enregistrer.
    # nous lui envoyons notre adresse
    url = f"{adr_serveur_distant}/enregistrer_nv_noeud"
    reponse_info_chaine = requests.post(
        url=url,
        data=json.dumps({"adresse_a_ajouter": request.host_url}),
        headers={"Content-Type": "application/json"},
    )

    assert (
        ADRESSE_MON_SERVEUR == request.host_url
    ), f"{ADRESSE_MON_SERVEUR}, {request.host_url}"

    # Si l'appel c'est bien passé
    if reponse_info_chaine.status_code == 200:
        # nous éditons de façon global la blockchain et les adrs_noeuds_serveurs
        global blockchain
        global adrs_noeuds_serveurs
        # Nous mettons à jour notre blockchain avec la copie renvoyée par le
        # noeud serveur où nous nous sommes enregistré
        # c'est notre blockchain qui se met à jour à partir de celle du noeud
        # où nous enregistrons
        blockchain = regenere_blockchain_avec(reponse_info_chaine.json()["chaine"])
        # Nous mettons à jour les adrs_noeuds_serveurs que nous connaissons avec
        # l'adresse du serveur où nous enregistrons et aussi ses adresses connues mais
        # nous retirons la notre
        adrs_du_serveur_distant = set(
            reponse_info_chaine.json()["adrs_noeuds_serveurs"]
        )
        adrs_noeuds_serveurs.update(
            {adr_serveur_distant}, adrs_du_serveur_distant - {ADRESSE_MON_SERVEUR}
        )
        # et Renvoyons un messsage de succès
        return "Enregistrement Réussit", 200
    else:
        # Sinon nous retournons le contenu de la réponse et le code d'erreur
        return reponse_info_chaine.content, reponse_info_chaine.status_code


def regenere_blockchain_avec(chaine_recue):
    # Nous appelons cette fonction lorsque le notre noeud s'enregistre auprès d'un autre
    # noeud serveur.  Nous reconstruisons alors notre blockchain

    # Nous instantion un nouvelle objet Blockchain
    blockchain_regeneree = Blockchain()
    # Pour lequel nous créeons le bloc de genèse
    blockchain_regeneree.creer_bloc_genese()

    # Ensuite pour chaque bloc 'reçu' ie récupéré dans la chaine reçue
    for idx, bloc_recu in enumerate(chaine_recue):
        # nous créons un objet bloc avec une copie des données reçues
        # hauteur, transaction, timestamp, hachage_précedent nonce
        # mais nous ignorons le premier bloc (bloc de genese) car nous
        # l'avons cree manuellement
        if idx == 0:
            # aussi si idx == 0 au passe au bloc suivant directement
            continue
        bloc = Bloc(
            bloc_recu["hauteur"],
            bloc_recu["txs"],
            bloc_recu["timestamp"],
            bloc_recu["hachage_precedent"],
            bloc_recu["nonce"],
        )
        # pour chaque bloc, nous vérifions bien que le hachage est valide
        bloc_ajoute = blockchain_regeneree.ajouter_bloc(
            bloc, preuve=bloc_recu["hachage"]
        )
        # si l'ajout echoue, c'est qu'il y a une erreur et nous soulevons une
        # exception
        if not bloc_ajoute:
            raise Exception("Le contenu de la chaine a été modifié.")

    # Nous renvoyons la blockchain_regeneree
    return blockchain_regeneree


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
    for adresse_noeud in adrs_noeuds_serveurs:
        # Nous appelons la fonction du adresse_noeud qui
        # renvois la chaine
        reponse = requests.get(f"{adresse_noeud}/info_chaine")
        # Nous récupérons les données de la chaine (longueur et blocs)
        chaine = reponse.json()["chaine"]
        longueur = len(chaine)

        # et nous comparons la longueur de la chaine récupérée avec la longueur de
        # notre chaine.  Nous vérifions aussi la validité de la chaine récupérée
        if longueur > lg_courante and blockchain.verifier_validite_chaine(chaine):
            # si elle est valide et que sa longueur est plus grande que la notre,
            # alors nous l'enregistrons comme la plus longue chaine
            # avant de vérifier les chaines des autres adresse_noeuds serveurs
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
    for adresse_noeud in adrs_noeuds_serveurs:
        # nous postons à l'url ajouter_bloc les données du bloc (en __dict__)
        requests.post(
            url=f"{adresse_noeud}ajouter_bloc",
            data=json.dumps(bloc.__dict__, sort_keys=True),
            headers={"Content-Type": "application/json"},
        )
