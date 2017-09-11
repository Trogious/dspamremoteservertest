#Generating Client/Server certificates with a local CA
#*make sure openssl points to the correct instillation (%which openssl).  Mine is aliased to /usr/local/openssl/bin/openssl

#Generate a CA
echo "Generating CA"
#openssl req -days 36500 -out ca.pem -new -x509
#        -generates CA file "ca.pem" and CA key "privkey.pem" pass: capass1

#Generate server certificate/key pair 
#        - no password required.
echo "Generating server key"
openssl genrsa -out server.key 2048
echo "Generating server CSR"
openssl req -key server.key -new -out server.csr
echo "Generating and signing server cert"
openssl x509 -req -days 3650 -in server.csr -CA ca.pem -CAkey privkey.pem -CAserial file.srl -out server.pem
#        -contents of "file.srl" is a two digit number.  eg. "00"

#Generate client certificate/key pair

#5    Either choose to encrypt the key(a) or not(b)
#        a. Encrypt the client key with a passphrase
#            openssl genrsa -des3 -out client.key 2048
#        b. Don't encrypt the client key
echo "generating client key"
openssl genrsa -out client.key 2048
echo "generating client CSR"
openssl req -key client.key -new -out client.csr
echo "generating and signing client cert"
openssl x509 -req -days 365 -in client.csr -CA ca.pem -CAkey privkey.pem -CAserial file.srl -out client.pem
#        -contents of "file.srl" is a two digit number.  eg. "00"

#8)    DONE
