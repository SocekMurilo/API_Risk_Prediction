# DESCRICAO

- Configuracao do software renault_ml

## CRIACAO DO REPO

- Caso seja uma maquina de desenvolvimento, realize o clone do repo, caso ele nao exista em /home/jornada/renault_ml

```bash

cd /home/jornada
git clone https://senai-journey@dev.azure.com/senai-journey/renault-risk-manager/_git/renault_ml
cd renault_ml
git remote rename origin devops

git config --local git.email "<SEU_EMAIL_DA_AZURE>"
git config --local git.name "<SEU_NOME>"

git checkout -b $SIGLA_DO_DEV(ex: rf)
git push -u devops $SIGLA_DO_DEV(ex: rf)


```

## CONFIGURACAO DO DOCKER

### CRIACAO DA IMAGEM

- O procedimento abaixo e necessario apenas para a criacao da imagem

```bash

cd /home/jornada/renault_ml

# Ajuste o start_app.csh para executar o loop...
docker-compose up --build --detach

# Importante: utilizar o id do container nos comandos commit
docker commit --message='Install packages' $(docker ps -aqf "name=renault_ml") renault_ml:latest

# Caso seja uma maquina de desenvolvimento linux padrão faça isso:
docker save renault_ml:latest | gzip > /home/jornada/images/renault_ml.tar.gz


```

### CRIACAO DO CONTAINER

- A imagem deve existir em /home/jornada/images/ caso nao exista, transfira uma imagem de uma maquina ja existente, para entao realizar o procedimento abaixo

```bash

cd /home/jornada/renault_ml
docker load < /home/jornada/images/renault_ml.tar.gz
make run_dev

```

## CONFIGURACAO DO HOST

```bash

# Liberar portas (Debian)
sudo ufw allow 5020/tcp
sudo ufw allow 5023/tcp

```