#!/bin/sh

keytool -import -deststorepass storepass1 -destkeypass storepass1 -destkeystore $1 -deststoretype BKS -alias dspamremoteserver.herokuapp.com_CA -file ca.pem -srcstorepass storepass1 -alias dspamremoteserver.herokuapp.com -provider org.bouncycastle.jce.provider.BouncyCastleProvider -providerpath bcprov-jdk15on-158.jar
