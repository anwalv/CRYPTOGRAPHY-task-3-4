#!/bin/bash

echo -n "give my friend 2 bitcoins for a pizza" > message.txt

echo "Message encryption via OpenSSL..."
openssl pkeyutl -encrypt -pubin -inkey key.pub -in message.txt -out message.enc

echo "Resulted encypted message:"
echo "--------------------------------------------------"
base64 -i message.enc
echo "--------------------------------------------------"

echo "File of encrypted message located in Task06/message.enc"
