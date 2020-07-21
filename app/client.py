import datetime
import json

import requests
from flask import render_template, redirect, request

from app import app

# voir ici pour ngrok
ADRESSE_NOEUD_SERVEUR = "http://b481ee5f4ca8.ngrok.io"


@app.route("/")
def index():
    reponse = requests.get(f"{ADRESSE_NOEUD_SERVEUR}/info_chaine")
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
            "adresse_noeud": ADRESSE_NOEUD_SERVEUR,
            "temps_litteral": litteral_timestamp,
            "pairs": info_chaine["pairs"],
            "lg_chaine": len(info_chaine["chaine"]),
            "blockchain": blockchain,
        }

    return render_template("index.html", **contexte)


@app.route("/soumettre", methods=["POST"])
def soumettre_zone_texte():

    requests.post(
        f"{ADRESSE_NOEUD_SERVEUR}/nvl_tx",
        json={"auteur": request.form["auteur"], "contenu": request.form["contenu"],},
        headers={"Content-type": "application/json"},
    )

    return redirect("/")


# @app.route("/senregistrer", methods=["POST"])
# def envoyer_demande_enregistrement():
#     adresse_noeud_existant = request.form['adresse_denregistrement']
#     requests.post(
#         f"{adresse_noeud_existant}/senregistrer_aupres",
#         json={"adresse": ADRESSE_NOEUD_SERVEUR},
#         headers={"Content-type": "application/json"},
#     )

#     return redirect("/")


def litteral_timestamp(temps_):
    return datetime.datetime.fromtimestamp(temps_).strftime("le %d-%m-%Y à %H:%M")
