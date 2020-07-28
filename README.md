broken-links:t \^:{}

Projet Blockchain (en python)
=============================

Ce repertoire contient du code pour créer sa blockchain. Il a un
objectif pédagogique et il est donc très commenté. Il s'inspire d'un
[tutoriel
d'IBM](https://developer.ibm.com/technologies/blockchain/tutorials/develop-a-blockchain-application-from-scratch-in-python/)
en anglais, dont le code est aussi sur [ce répertoire
git](https://github.com/satwikkansal/python_blockchain_app/tree/master).

Le code crée une application web avec le framework python
[Flask](https://palletsprojects.com/p/flask/) pour écrire, lire et
partager des données sur une blockchain. Il s'agit d'un serveur et un
client blockchain.

Il n'y a pas de meilleure manière d'apprendre ce qu'est la blockchain
que d'en construire une.

Le code peut être copié et testé localement, puis sur différentes
machines distantes à l'aide d'un service comme
[ngrok](https://ngrok.com) qui permet de rendre une adresse réseau
locale visible depuis sur internet.

Pré-requis
----------

Assurez-vous d'avoir une version récente de python (par exemple 3.8) et
que virtualenv est installé. Executant dans un terminal.

``` {.bash}
$ python --vesrion
Python 3.8.2

$ virtualenv --version
virtualenv 20.0.23 from ...
```

Notez que je distingue ici l'invite de commande Linux et windows avec
respectivement '\$' et '&gt;'. Si rien n'est spécifié c'est probablement
exactement les même commandes.

### Créer un environnement virtuel

Linux

``` {.bash}
$ virtualenv <VosInitiales>Envs
$ cd <VosInitiales>Envs
$ source bin/activate
```

Windows

``` {.bash}
> virtualenv <VosInitiales>Envs
> cd <VosInitiales>Envs
> Scripts\activate
```

### Télécharger le code

Assurez-vous d'avoir [git](https://git-scm.com/download/win) installé

``` {.bash}
$ git --version
git version 2.17.1
```

puis exécutez

``` {.bash}
$ git clone https://github.com/maliky/blockchain.git
$ cd blockchain  # ou pour windows, dir blockchain
```

Vous pourez ensuite mettre à jour le code simplement avec

``` {.bash}
$ git pull 
# ou, $ git pull origin master
```

Installer les bibliothèques nécessaires

``` {.bash}
$ pip install -r requirements.txt
```

Vous être prêt à lancer le programme

Lancement
---------

### Variable d'environements

N'oubliez pas cette étape. Elle est importante. Linux

``` {.bash}
$ export FLASK_APP=noeud_serveur
```

Windows (cmd.exe) faire

``` {.bash}
> set FLASK_APP=noeud_serveur
```

pour Windows Powerhsell voir [la doc du projet
Flask](https://flask.palletsprojects.com/en/1.1.x/cli/#application-discovery).

### En local

#### Lancer le serveur

``` {.bash}
$ flask run --port 8000
```

Le noeud serveur est maintenant accessible en local à
<http://127.0.0.1:8000> Vous pouvez changer cette adresse la variable
ADRESSE~NOEUDSERVEUR~ dans [file:app/client.py](app/client.py)

#### Lancer le client

Ouvrez un autre terminal puism aller dans le dossier
'&lt;VosInitiales&gt;Envs'

``` {.bash}
> cd \votre\chemin\pour\<VosInitiales>Envs
```

activez l'environnement virtuel

``` {.bash}
> Scripts\activate
```

aller dans le dossier blockchain

``` {.bash}
> cd blockchain
```

puis lancer l'application cliente avec

``` {.bash}
> python lance_client.py
```

L'interface est accessible a <http://localhost:5000>

### Avec un adresse accessible depuis l'internet

#### Créer un accès (temporaire) à notre serveur local depuis internet

S'inscrire sur [ngrok.com](https://ngrok.com) et suivre les instructions
du site

#### Utiliser curl pour ajouter les autres noeuds serveur

``` {.bash}
curl -X POST \
  <address.ngrok.de.votre.partenair>/senregistrer_aupres \
  -H 'Content-Type: application/json' \
  -d '{"adresse": "http://votre.adresse.ngrok ou http://127.0.0.1:8000"}'
```

### Exercices

Décommenter les codes dans client.py et essayer d'ajouter une interface
pour s'enregistrer aurpès des autres noeuds. via l'interface cliente
