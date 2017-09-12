#!/bin/sh

openssl pkcs12 -export -in client.pem -inkey client.key -out $1 -name dspamremoteserver.herokuapp.com -CAfile ca.pem
