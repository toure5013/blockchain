import datetime
import json

import requests
from flask import render_template, redirect, request

from app import app

ADRESSE_NOEUD_CONNECTE = "http://127.0.0.1:8000"

publications = []


def recupe_publications():
    reponse = requests.get(f"{ADRESSE_NOEUD_CONNECTE}/chaine")

    if reponse.status_code == 200:
        contenu = []
        chaine = json.loads(reponse.content)
        for bloc in chaine["chaine"]:
            for tx in bloc["txs"]:
                tx["hauteur"] = bloc["hauteur"]
                tx["hachage"] = bloc["hachage_precedent"]
                contenu.append(tx)

        global publications
        publications = sorted(contenu, key=lambda k: k["timestamp"], reverse=True)


@app.route("/")
def index():
    recupe_publications()
    return render_template(
        "index.html",
        titre="Votre Réseau décentralisé, pour partager du contenu",
        publications=publications,
        adresse_noeud=ADRESSE_NOEUD_CONNECTE,
        temps_litteral=litteral_timestamp,
    )


@app.route("/soumettre", methods=["POST"])
def soumettre_zone_texte():

    requests.post(
        f"{ADRESSE_NOEUD_CONNECTE}/nvl_tx",
        json={"auteur": request.form["auteur"], "contenu": request.form["contenu"],},
        headers={"Content-type": "application/json"},
    )

    return redirect("/")


def litteral_timestamp(temps_):
    return datetime.datetime.fromtimestamp(temps_).strftime("%H:%M")
