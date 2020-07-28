
# Table of Contents

1.  [Projet Blockchain (en python)](#org84c53cc)
    1.  [Pré-requis](#orgabdde2f)
        1.  [Créer un environnement virtuel](#orge481111)
        2.  [Télécharger le code](#org61afb9b)
    2.  [Lancement](#org350396e)
        1.  [Variable d'environements](#org38a9c98)
        2.  [En local](#orgb8727ec)
        3.  [Avec un adresse accessible depuis l'internet](#org488b605)
        4.  [Exercices](#orgd090d27)



<a id="org84c53cc"></a>

# Projet Blockchain (en python)

Ce repertoire contient du code pour créer sa blockchain. Il a un objectif pédagogique et il est donc très commenté.  Il s'inspire d'un  [tutoriel d'IBM](https://developer.ibm.com/technologies/blockchain/tutorials/develop-a-blockchain-application-from-scratch-in-python/)  en anglais, dont le code est aussi sur [ce répertoire git](https://github.com/satwikkansal/python_blockchain_app/tree/master).

Le code crée une application web avec le framework python [Flask](https://palletsprojects.com/p/flask/) pour écrire, lire et partager des données sur une blockchain.  Il s'agit d'un serveur et un client blockchain.

Il n'y a pas de meilleure manière d'apprendre ce qu'est la blockchain que d'en construire une.

Le code peut être copié et testé localement, puis sur différentes machines distantes à l'aide d'un service comme [ngrok](https://ngrok.com)  qui permet de rendre une adresse réseau locale visible depuis sur internet.


<a id="orgabdde2f"></a>

## Pré-requis

Assurez-vous d'avoir une version récente de python (par exemple 3.8) et que virtualenv est installé.
Executant dans un terminal.

    $ python --vesrion
    Python 3.8.2
    
    $ virtualenv --version
    virtualenv 20.0.23 from ...

Notez que je distingue ici l'invite de commande Linux et windows et les commentaires avec respectivement '$',  '>' et '#'.  Si rien n'est spécifié c'est probablement exactement les même commandes ou alors c'est qu'il s'agit du retour d'une commande. 


<a id="orge481111"></a>

### Créer un environnement virtuel

Linux

    $ virtualenv <VosInitiales>Envs
    $ cd <VosInitiales>Envs
    $ source bin/activate

Windows

    > virtualenv <VosInitiales>Envs
    > cd <VosInitiales>Envs
    > Scripts\activate


<a id="org61afb9b"></a>

### Télécharger le code

Assurez-vous d'avoir [git](https://git-scm.com/download/win) installé 

    $ git --version
    git version 2.17.1

puis exécutez

    $ git clone https://github.com/maliky/blockchain.git
    $ cd blockchain  # ou pour windows, dir blockchain

Vous pourez ensuite mettre à jour le code simplement avec

    $ git pull 
    # ou, $ git pull origin master

Installer les bibliothèques nécessaires

    $ pip install -r requirements.txt

Vous êtes prêt à lancer le programme


<a id="org350396e"></a>

## Lancement


<a id="org38a9c98"></a>

### Variable d'environements

N'oubliez pas cette étape.  Elle est importante.

Pour Linux

    $ export FLASK_APP=noeud_serveur

Pour Windows (cmd.exe) faire

    > set FLASK_APP=noeud_serveur

pour Windows Powerhsell voir [la doc du projet Flask](https://flask.palletsprojects.com/en/1.1.x/cli/#application-discovery).


<a id="orgb8727ec"></a>

### En local


#### Lancer le serveur

    flask run --port 8000

Le noeud serveur est maintenant accessible en local à <http://127.0.0.1:8000>
Vous pouvez changer cette adresse la variable ADRESSE\_NOEUD\_SERVEUR dans <app/client.py>


#### Lancer le client

Ouvrez un autre terminal puism aller dans le dossier '<VosInitiales>Envs'

    > cd \votre\chemin\pour\<VosInitiales>Envs

activez l'environnement virtuel

    > Scripts\activate

aller dans le dossier blockchain

    > cd blockchain

puis lancer l'application cliente avec

    > python lance_client.py

L'interface est accessible a <http://localhost:5000> 


<a id="org488b605"></a>

### Avec un adresse accessible depuis l'internet


#### Créer un accès (temporaire) à notre serveur local depuis internet

S'inscrire sur [ngrok.com](https://ngrok.com) et suivre les instructions du site


#### Utiliser curl pour ajouter les autres noeuds serveur

    curl -X POST \
      <address.ngrok.de.votre.partenair>/senregistrer_aupres \
      -H 'Content-Type: application/json' \
      -d '{"adresse": "http://votre.adresse.ngrok ou http://127.0.0.1:8000"}'


<a id="orgd090d27"></a>

### Exercices

Décommenter les codes dans client.py et essayer d'ajouter une interface pour s'enregistrer aurpès des autres noeuds.
via l'interface cliente

