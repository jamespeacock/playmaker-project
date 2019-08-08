ARG TAG
FROM playmaker-interface:$TAG

RUN mkdir -p /var/www/static
RUN python3.6 /app/manage.py collectstatic --noinput

FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
RUN apt-get update && apt-get install -y iputils-ping vim
ADD nginx.conf /etc/nginx/conf.d/nginx.conf
#RUN mkdir /static/
#COPY --from=builder /app/staticfiles /static