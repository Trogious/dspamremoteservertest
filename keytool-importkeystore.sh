#!/bin/sh

keytool -importkeystore -deststorepass storepass1 -destkeypass storepass1 -destkeystore $2 -deststoretype BKS -srckeystore $1 -srcstoretype PKCS12 -srcstorepass storepass1 -alias dspamremoteserver.herokuapp.com -provider org.bouncycastle.jce.provider.BouncyCastleProvider -providerpath bcprov-jdk15on-158.jar
