Toutes les commandes à exécuter dans l'ordre pour décompresser les fichiers et faire fonctionner votre API conteneurisée avec bentoml.
Les commandes à exécuter pour lancer les tests unitaires sur votre API qui devront tous retourner le status PASSED.

# Prérequis

- Docker installé
- Python 3 installé.

Ci-dessous, remplacer FOLDER par le chemin absolu du dossier contenant les 3 livrables dont ce README.

# Terminal 1

cd FOLDER
docker load -i bento_image.tar
docker run --rm -p 3001:3000 marie_admission_service:67s23ghrisru2bqk

# Terminal 2

cd FOLDER
python -m venv .venv
pip install PyJWT==2.10.1 pytest==9.0.2 requests==2.32.5
python -m pytest service_test.py
