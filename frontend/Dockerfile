# base image
FROM node:14.2.0-slim

# set working directory
WORKDIR /app
RUN mkdir /app/node_modules

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /app/package.json
RUN npm update
RUN npm install react-scripts@3.4.1 -g
RUN npm install node-sass@4.14.1
#RUN yarn add react-scripts

# start app
CMD npm start