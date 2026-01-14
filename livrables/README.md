# Prérequis

- Docker (28.3.3, build 980b856) installé
- Python 3.12.3 installé.

Ci-dessous, remplacer FOLDER par le chemin absolu du dossier contenant les 3 livrables dont ce README.

# Terminal 1

cd FOLDER
docker load -i bento_image.tar
docker run --rm -p 3001:3000 marie_admission_service:67s23ghrisru2bqk

Le terminal 1 se bloque. Le laisser ouvert et passer au terminal 2.

# Terminal 2

cd FOLDER
python3 -m venv .venv
source .venv/bin/activate
pip install PyJWT==2.10.1 pytest==9.0.2 requests==2.32.5
python3 -m pytest service_test.py
