#!/usr/bin/env bash

CONTA=danielfs
IMAGEM_BASE=$CONTA/rpc-base
IMAGEM_SERVIDOR=$CONTA/rpc-servidor
IMAGEM_CLIENTE=$CONTA/rpc-cliente

echo "Construindo imagem base $IMAGEM_BASE"
docker build -t $IMAGEM_BASE -f Dockerfile.base .

echo "Contruindo imagem servidor $IMAGEM_SERVIDOR"
docker build -t $IMAGEM_SERVIDOR -f Dockerfile.servidor .

echo "Construindo imagem cliente $IMAGEM_CLIENTE"
docker build -t $IMAGEM_CLIENTE -f Dockerfile.cliente .