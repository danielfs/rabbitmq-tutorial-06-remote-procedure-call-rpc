#!/usr/bin/env bash

CONTA=danielfs
IMAGEM_BASE=$CONTA/rpc-base
IMAGEM_SERVIDOR=$CONTA/rpc-servidor
IMAGEM_CLIENTE=$CONTA/rpc-cliente

echo "Construindo imagem base $IMAGEM_BASE"
docker push $IMAGEM_BASE

echo "Contruindo imagem servidor $IMAGEM_SERVIDOR"
docker push $IMAGEM_SERVIDOR

echo "Construindo imagem cliente $IMAGEM_CLIENTE"
docker push $IMAGEM_CLIENTE