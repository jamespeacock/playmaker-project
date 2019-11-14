#!/usr/bin/env bash
export D=/usr/share/nginx/html
export DOMAIN=test.myplaymkr.co
mkdir -p /etc/nginx/ssl/letsencrypt/${DOMAIN}
cd /etc/nginx/ssl/letsencrypt/${DOMAIN} && openssl dhparam -dsaparam -out dhparams.pem 4096
cd /root/.acme.sh && ./acme.sh --issue -w $D -d ${DOMAIN} -k 4096
cd /root/.acme.sh && ./acme.sh --installcert -d ${DOMAIN} \
--keypath /etc/nginx/ssl/letsencrypt/${DOMAIN}/${DOMAIN}.key \
--fullchainpath /etc/nginx/ssl/letsencrypt/${DOMAIN}/${DOMAIN}.crt