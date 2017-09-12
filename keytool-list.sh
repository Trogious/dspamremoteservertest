#!/bin/sh

keytool -list -storepass storepass1 -keystore $1 -storetype BKS -provider org.bouncycastle.jce.provider.BouncyCastleProvider -providerpath bcprov-jdk15on-158.jar
