Projet Blockchain (en python)
=============================

Ce repertoire contient du code pour créer sa blockchain. Il a un
objectif pédagogique et il est donc très commenté. Le code originale
peut être trouvé en anglais sur
`python\ :sub:`blockchainapp` <https://github.com/satwikkansal/python_blockchain_app/tree/ibm_blockchain_post>`__
ou chez
[[https://developer.ibm.com/technologies/blockchain/tutorials/develop-a-blockchain-application-from-scratch-in-python/
][IBM]].

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

    python --vesrion
    virtualenv --version

Créer un environnement virtuel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Linux

.. code:: bash

    virtualenv monEnv
    cd monEnv
    source bin/activate

Windows

.. code:: bash

    virtualenv monEnv
    cd MonEnv
    source Scripts/activate

Télécharger le code
~~~~~~~~~~~~~~~~~~~

Assurez-vous d'avoir `git <https://git-scm.com/download/win>`__ installé
et exécutez:

.. code:: bash

    git clone https://github.com/maliky/blockchain.git
    cd blockchain

\_\ :sub:`bash`

Installer les bibliothèques nécessaires

.. code:: bash

    pip install -r requirements.txt

Vous être prêt à lancer le programme

Lancement
---------

Variable d'environements
~~~~~~~~~~~~~~~~~~~~~~~~

Linux

.. code:: bash

    export FLASK_APP=noeud_serveur

Windows (cmd.exe) faire

.. code:: bash

    set FLASK_APP=noeud_serveur

pour Windows Powerhsell voir `la doc du projet
Flask <https://flask.palletsprojects.com/en/1.1.x/cli/#application-discovery>`__.

En local
~~~~~~~~

#. Lancer le serveur

   .. code:: bash

       flask run --port 8000

   Le noeud serveur est maintenant accessible en local à
   http://127.0.0.1:8000 Vous pouvez changer cette adresse la variable
   ADRESSE\ :sub:`NOEUDSERVEUR` dans
   `file:app/client.py <app/client.py>`__

#. Lancer le client

   Dans un autre terminal faites

   .. code:: bash

       python lance_client.py

   puis visiter http://localhost:5000 avec votre navigateur

template
--------

https://jinja.palletsprojects.com/en/2.11.x/templates/#list-of-control-structures
