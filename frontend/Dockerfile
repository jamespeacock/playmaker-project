# base image
FROM node:12.2.0-alpine

# set working directory
WORKDIR /app
RUN mkdir /app/node_modules

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /app/package.json
RUN npm install
RUN npm install react-scripts@3.4.0 -g
RUN npm install -g --unsafe-perm node-sass@4.14.1
RUN npm update

# start app
CMD npm start --debug