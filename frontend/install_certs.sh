#!/usr/bin/env bash
#export D=/usr/share/nginx/html
#export SITE=test
#export DOMAIN=myplaymkr.co
openssl dhparam -dsaparam -out dhparams.pem 4096
cd /root/.acme.sh && ./acme.sh --issue -w $D -d ${SITE}.${DOMAIN} -k 4096
cd /root/.acme.sh && ./acme.sh --installcert -d ${SITE}.${DOMAIN} \
--keypath /etc/nginx/ssl/letsencrypt/${DOMAIN}/${DOMAIN}.key \
--fullchainpath /etc/nginx/ssl/letsencrypt/${DOMAIN}/${DOMAIN}.crt