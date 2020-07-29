import datetime
import json

import requests
from flask import render_template, redirect, request

from app import app
from app.config_locale import ADRESSE_MON_SERVEUR


@app.route("/")
def index():
    reponse = requests.get(f"{ADRESSE_MON_SERVEUR}info_chaine")
    contexte = {}
    if reponse.status_code == 200:
        info_chaine = json.loads(reponse.content)
        blockchain = info_chaine["chaine"]
        blockchain = sorted(blockchain, key=lambda k: k["timestamp"], reverse=True)
        for i, bloc in enumerate(blockchain):
            bloc["timestamp"] = litteral_timestamp(bloc["timestamp"])
            blockchain[i] = bloc

        contexte = {
            "titre": "Blockchain: un réseau décentralisé pour partager du contenu",
            "adresse_noeud": ADRESSE_MON_SERVEUR,
            "temps_litteral": litteral_timestamp,
            "adrs_noeuds_serveurs": info_chaine["adrs_noeuds_serveurs"],
            "lg_chaine": len(info_chaine["chaine"]),
            "blockchain": blockchain,
        }

    return render_template("index.html", **contexte)


@app.route("/soumettre", methods=["POST"])
def soumettre_zone_texte():

    requests.post(
        f"{ADRESSE_MON_SERVEUR}nvl_tx",
        json={"auteur": request.form["auteur"], "contenu": request.form["contenu"],},
        headers={"Content-type": "application/json"},
    )

    return redirect("/")


@app.route("/senregistrer", methods=["POST"])
def envoyer_demande_enregistrement():
    adresse_denregistrement = request.form["adresse_denregistrement"]
    reponse = requests.post(
        f"{ADRESSE_MON_SERVEUR}senregistrer_aupres",
        json={"adr_serveur_distant": adresse_denregistrement},
        headers={"Content-type": "application/json"},
    )

    print(reponse)
    return redirect("/")


def litteral_timestamp(temps_):
    return datetime.datetime.fromtimestamp(temps_).strftime("le %d-%m-%Y à %H:%M")
