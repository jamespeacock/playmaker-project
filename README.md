# Getting Started

## Clone repo

git clone https://github.com/jamespeacock/playmaker.git

```
cd ..
mv playmaker playmaker-project
cd playmaker-project
```

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
mkvirtualenv -a . playmaker
workon playmaker

pipenv install --dev
```

##### Node.js, React

Install node (downloads mac installer .pkg) : https://nodejs.org/dist/v10.15.3/node-v10.15.3.pkg


##### pyenv, pipenv, python
```
brew install pyenv
pyenv install 3.6.7
cd /path/to/here
pyenv local 3.6.7
mkvirtualenv -a . playmaker
add2virtualenv /path/to/first/playmaker
workon playmaker
pip install --upgrade pip
pip install pipenv
pipenv install
```

##### Docker

Download & install docker for mac: https://docs.docker.com/v17.12/docker-for-mac/install/

`docker-compose up --build -d`

Troubleshooting this command...

#### Running Tests

```
cd playmaker
pytest --html=report.html
```

Create new RunConfiguration in PyCharm
Python Test --> pytest 
Additional arguments: `-c playmaker/pytest.ini --html=report.html`



## Running & Editing

Spin up intially: `docker-compose up -d`

After making changes: `./refresh.sh && docker-compose logs -f interface`


## API Usage

#### Play a song for a listener
`http://localhost:5000/controller/playsong?listener=1&song_uris=spotify:track:5ewqsgAusPBCyYn2zmMt7k`

## Troubleshooting

#### If no staticfiles/css
`python3.6 manage.py collectstatic`

#### When needing to create an initial user
`python3.6 manage.py createsuperuser`