## Prereqs

##### pyenv and pipenv

pyenv: https://github.com/pyenv/pyenv/blob/master/README.md
```
brew install pyenv
pyenv install 3.6.6
pyenv local 3.6.6
python -V
pip install pipenv

# in ../code_dir/playmaker-project/playmaker
pyenv local 3.6.6
mkirtualenv -a . playmaker
workon playmaker

pipenv install --skip-lock 
```

##### Node.js, React

Install node (downloads mac installer .pkg) : https://nodejs.org/dist/v10.15.3/node-v10.15.3.pkg


##### Docker

Download & install docker for mac: https://docs.docker.com/v17.12/docker-for-mac/install/

`docker-compose up --build -d`

Troubleshooting this command...

