#!/usr/bin/env bash
#export D=/usr/share/nginx/html
#export SITE=test.myplaymkr.co
openssl dhparam -dsaparam -out dhparams.pem 4096
cd /root/.acme.sh && ./acme.sh --issue -w $D -d ${SITE} -k 4096
cd /root/.acme.sh && ./acme.sh --installcert -d ${SITE} \
--keypath /etc/nginx/ssl/letsencrypt/${SITE}/${SITE}.key \
--fullchainpath /etc/nginx/ssl/letsencrypt/${SITE}/${SITE}.crt