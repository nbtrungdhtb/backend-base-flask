# at.backend-base
Base API project with Flask + Python 3.6+


# Setup
### Install pipenv
`pip install pipenv --user`

### Setup env storage per project
Edit .bashrc or .zshrc and add this line

`export PIPENV_VENV_IN_PROJECT=1`

### Create virtual environment for project
cd to your project directory

`cd ~/at.backend-base`

create virtual environment

`pipenv --python 3.6`

### Install package for virtual environment with dev package
`pipenv install --dev`

### Run flask for dev
`pipenv run python run.py`

# Test before pull request or commit

## Check code style
`pipenv run flake8 app` 
