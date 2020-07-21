Projet Blockchain (en python)
=============================

Ce repertoire contient du code pour créer sa blockchain. Il a un
objectif pédagogique et il est donc très commenté. Le code original peut
être trouvé en anglais dans ce `tutoriel
d'IBM <https://developer.ibm.com/technologies/blockchain/tutorials/develop-a-blockchain-application-from-scratch-in-python/>`__
et le code sur `ce répertoire
git <https://github.com/satwikkansal/python_blockchain_app/tree/master>`__.

Le code créer une application web avec le framework python Flask pour
écrire, lire et partager des données sur une blockchain.

Il n'y a pas de meilleure manière d'apprendre ce qu'est la blockchain
que d'en construire une.

Le code peut être copié et testé sur différentes machines distantes afin
de tester à l'aide d'un service comme `ngrok <https://ngrok.com>`__. Ce
dernier vous permet de rendre une adresse réseau locale visible depuis
sur internet.

Pré-requis
----------

Assurez-vous d'avoir une version récente de python (par exemple 3.8) et
que virtualenv est installé en executant dans un terminal

.. code:: bash

    $ python --vesrion
    Python 3.8.2

    $ virtualenv --version
    virtualenv 20.0.23 from ...

Créer un environnement virtuel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Linux

.. code:: bash

    $ virtualenv MonEnv
    $ cd MonEnv
    $ source bin/activate

Windows

.. code:: bash

    > virtualenv MonEnv
    > cd MonEnv
    > Scripts\activate

Télécharger le code
~~~~~~~~~~~~~~~~~~~

Assurez-vous d'avoir `git <https://git-scm.com/download/win>`__ installé
et exécutez:

.. code:: bash

    $ git clone https://github.com/maliky/blockchain.git
    $ cd blockchain  # ou pour windows, dir blockchain

Vous pourez ensuite mettre à jour le code simplement avec

.. code:: bash

    $ git pull 
    # ou, $ git pull origin master

Installer les bibliothèques nécessaires

.. code:: bash

    $ pip install -r requirements.txt

Vous être prêt à lancer le programme

Lancement
---------

Variable d'environements
~~~~~~~~~~~~~~~~~~~~~~~~

N'oubliez pas cette étape. Elle est importante. Linux

.. code:: bash

    $ export FLASK_APP=noeud_serveur

Windows (cmd.exe) faire

.. code:: bash

    > set FLASK_APP=noeud_serveur

pour Windows Powerhsell voir `la doc du projet
Flask <https://flask.palletsprojects.com/en/1.1.x/cli/#application-discovery>`__.

En local
~~~~~~~~

#. Lancer le serveur

   .. code:: bash

       $ flask run --port 8000

   Le noeud serveur est maintenant accessible en local à
   http://127.0.0.1:8000 Vous pouvez changer cette adresse la variable
   ADRESSE\ :sub:`NOEUDSERVEUR` dans
   `file:app/client.py <app/client.py>`__

#. Lancer le client

   Ouvrez un autre terminal

   -  aller dans le dossier 'MonEnv'
   -  activez l'environnement virtuel
   -  aller dans le dossier blockchain

   .. code:: bash

       > cd \votre\chemin\pour\MonEnv
       > Scripts\activate
       > cd blockchain

   puis

   .. code:: bash

       > python lance_client.py

   après v puis visiter http://localhost:5000 avec votre navigateur

Avec un adresse accessible depuis l'internet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Créer un accès (temporaire) à notre serveur local depuis internet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

S'inscrire sur `ngrok.com <https://ngrok.com>`__ et suivre les
instructions du site

Utiliser curl pour ajouter les autres noeuds serveur
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    curl -X POST \
      <address.ngrok.de.votre.partenair>/senregistrer_aupres \
      -H 'Content-Type: application/json' \
      -d '{"adresse": "http://votre.adresse.ngrok ou http://127.0.0.1:8000"}'

Exercices
~~~~~~~~~

Décommenter les codes dans client.py et essayer d'ajouter une interface
pour s'enregistrer aurpès des autres noeuds.
