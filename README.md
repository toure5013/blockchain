

# Projet Blockchain (en python)

Ce repertoire contient du code pour créer sa blockchain. Il a un objectif pédagogique et il est donc très commenté.  Le code original peut être trouvé en anglais dans ce [tutoriel d'IBM](https://developer.ibm.com/technologies/blockchain/tutorials/develop-a-blockchain-application-from-scratch-in-python/) et le code sur [ce répertoire git](https://github.com/satwikkansal/python_blockchain_app/tree/master).

Le code créer une application web avec le framework python Flask pour écrire, lire et partager des données sur une blockchain.  

Il n'y a pas de meilleure manière d'apprendre ce qu'est la blockchain que d'en construire une.

Le code peut être copié et testé sur différentes machines distantes afin de tester à l'aide d'un service comme [ngrok](https://ngrok.com).  Ce dernier vous permet de rendre une  adresse réseau locale visible depuis sur internet.


## Pré-requis

Assurez-vous d'avoir une version récente de python (par exemple 3.8) et que virtualenv est installé en executant dans un terminal

    $ python --vesrion
    Python 3.8.2
    
    $ virtualenv --version
    virtualenv 20.0.23 from ...


### Créer un environnement virtuel

Linux

    $ virtualenv MonEnv
    $ cd MonEnv
    $ source bin/activate

Windows

    > virtualenv MonEnv
    > cd MonEnv
    > Scripts\activate


### Télécharger le code

Assurez-vous d'avoir [git](https://git-scm.com/download/win) installé et exécutez:

    $ git clone https://github.com/maliky/blockchain.git
    $ cd blockchain  # ou pour windows, dir blockchain

Vous pourez ensuite mettre à jour le code simplement avec

    $ git pull 
    # ou, $ git pull origin master

Installer les bibliothèques nécessaires

    $ pip install -r requirements.txt

Vous être prêt à lancer le programme


## Lancement


### Variable d'environements

N'oubliez pas cette étape.  Elle est importante.
Linux

    $ export FLASK_APP=noeud_serveur

Windows (cmd.exe) faire

    > set FLASK_APP=noeud_serveur

pour Windows Powerhsell voir [la doc du projet Flask](https://flask.palletsprojects.com/en/1.1.x/cli/#application-discovery).


### En local


#### Lancer le serveur

    $ flask run --port 8000

Le noeud serveur est maintenant accessible en local à <http://127.0.0.1:8000>
Vous pouvez changer cette adresse la variable ADRESSE\\\_NOEUD\\\_SERVEUR dans <app/client.py>


#### Lancer le client

Ouvrez un autre terminal

-   aller dans le dossier 'MonEnv'
-   activez l'environnement virtuel
-   aller dans le dossier blockchain

    > cd \votre\chemin\pour\MonEnv
    > Scripts\activate
    > cd blockchain

puis lancer l'application cliente avec

    > python lance_client.py

L'interface est accessible a <http://localhost:5000> 


### Avec un adresse accessible depuis l'internet


#### Créer un accès (temporaire) à notre serveur local depuis internet

S'inscrire sur [ngrok.com](https://ngrok.com) et suivre les instructions du site


#### Utiliser curl pour ajouter les autres noeuds serveur

    curl -X POST \
      <address.ngrok.de.votre.partenair>/senregistrer_aupres \
      -H 'Content-Type: application/json' \
      -d '{"adresse": "http://votre.adresse.ngrok ou http://127.0.0.1:8000"}'


### Exercices

Décommenter les codes dans client.py et essayer d'ajouter une interface pour s'enregistrer aurpès des autres noeuds.

