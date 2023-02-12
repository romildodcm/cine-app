#!/bin/bash

# install python
echo "Configurando backend..."
echo "Instalando python..."
pwd
sudo apt-get update
sudo apt-get install python3.6
sudo apt-get install python3-pip
sudo apt-get install python3-venv

cd ./backend
pwd
python3 -m venv venv
source venv/bin/activate
export PYTHONPATH=.
echo "Instalando dependencias backend..."
pip install -r requirements.txt
cd ..

# install node
echo "Configurando frontend..."
pwd
echo "Instalando node..."
cd ./frontend
pwd
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
# nvm list-remote
nvm install v16.19.0
node -v
echo "Instalando dependencias frontend..."
pwd
npm install
cd ..

# https://lcalcagni.medium.com/deploy-your-fastapi-to-aws-ec2-using-nginx-aa8aa0d85ec7
echo "Instalando nginx..."
pwd
sudo apt install nginx

echo "Identificando IP publico..."
pwd
public_ip=$(curl -s checkip.dyndns.org | sed -e 's/.*Current IP Address: //' -e 's/<.*$//')
echo "IP publico: $public_ip"

echo "Criando arquivo .env para o frontend..."
echo "VITE_API_URL=http://$public_ip" > ./frontend/.env

echo "Configurando endereço IP para o NGINX..."
filename="fastapi_nginx"
sed -i "s/server_name.*;/server_name $public_ip;/g" $filename

# https://lcalcagni.medium.com/deploy-your-fastapi-to-aws-ec2-using-nginx-aa8aa0d85ec7
echo "Configurando nginx..."
pwd
sudo cp ./fastapi_nginx /etc/nginx/sites-available/
sudo service nginx restart

# tornando scripts executaveis
echo "Tornando executáveis os scripts start-backend.sh e start-frontend.sh..."
pwd
chmod +x ./start-backend.sh
chmod +x ./start-frontend.sh

echo "Ambiente configurado com sucesso!"
echo "Para iniciar o backend, execute: ./start-backend.sh"
echo "Para iniciar o frontend, execute: ./start-frontend.sh"

# leitura que pode ser interessante
# https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04-pt