import os


def make_open(name, plot):
    make = open(name, 'w')
    make.write(plot)
    make.close()


def create_env(name_project):
    plot = """
FLASK_APP=%s/app.py
FLASK_ENV=development
    """ % name_project
    make_open('.env', plot)


def create_secrets():
    plot = "SECRET_KEY='jadkfbsdkjbfbh'"
    make_open('.secrets.toml', plot)


def create_make_file(name_project):
    plot ="""
install:
	pip install .

dev-install:
	pip install -e ."[dev]"

test:
	flake8 -v %s/
	pytest tests -v --cov=%s
	coverage report
	coverage html


simple-test:
	pytest tests -v

debug-test :
	pytest tests -v --cov=%s --pdb

format:
	isort **/*.py
	black -l 79 **/*.py
    """ % (name_project, name_project, name_project) # noqa
    make_open('Makefile', plot)


def create_requiments():
    plot = """
Flask
dynaconf
wheel
python-dotenv
flask-cors
    """
    make_open('requirements.txt', plot)


def create_requiments_dev():
    plot = """
black
flake8
flask-debugtoolbar
flask-shell-ipython
ipdb
ipython
isort
pytest
pytest-flask
pytest-cov
pytest-sugar
"""
    make_open('requirements-dev.txt', plot)


def create_settings(name_project):
    plot = """
[default]
DEBUG = true
SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
SQLALCHEMY_TRACK_MODIFICATIONS = false
TITLE = "%s"
PASSWORD_SCHEMES = ['pbkdf2_sha512', 'md5_crypt']
EXTENSIONS = [
    "flask_cors:CORS"
]

[development]
TEMPLATES_AUTO_RELOAD = true
DEBUG_TOOLBAR_ENABLED = true
DEBUG_TB_INTERCEPT_REDIRECTS = false
DEBUG_TB_PROFILER_ENABLED = true
DEBUG_TB_TEMPLATE_EDITOR_ENABLED = true

[testing]
SQLALCHEMY_DATABASE_URI = 'sqlite://'

[production]
DEBUG = false
""" % name_project
    make_open('settings.toml', plot)


def create_setup(name_project, description):
    plot = """
from setuptools import setup, find_packages


def read(filename):
    return [
        req.strip() for req in open(filename).readlines()
    ]


setup(
    name="%s",
    version="0.1.0",
    description="%s",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read("requirements.txt"),
    extras_require={
        'dev': read("requirements-dev.txt")
    }

)
""" % (name_project, description)
    make_open('setup.py', plot)


def create_configuration(name_project):
    plot = """
from dynaconf import FlaskDynaconf


def init_app(app, **config):
    FlaskDynaconf(app, **config)
"""
    make_open(f'{name_project}/src/configuration.py', plot)


def create_docs(name_project):
    open('brain.txt', 'w')
    open(f'{name_project}/src/__init__.py', 'w')
    open(f'{name_project}/__init__.py', 'w')


def create_conf_test(name_project):
    plot = """
import pytest
from %s.app import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app(FORCE_ENV_FOR_DYNACONF="testing")
    with app.app_context():
        db.create_all(app=app)
        yield app
        db.drop_all(app=app)
""" % name_project

    make_open('tests/conftest.py', plot)


def create_app(name_project):
    plot = """
from flask import Flask

from .src import configuration


def create_app(**config):
    app = Flask(__name__)
    configuration.init_app(app, **config)
    app.config.load_extensions()

    return app
"""
    make_open(f'{name_project}/app.py', plot)


def create_gitignore():
    plot = """
*~
*.pyc
*.egg-info
.atom.sh
.cache
.pytest_cache
.coverage
.secrets.toml
.idea*
.tox/
.env
env/
Thumbs.db
brain.txt
dist
htmlcov
docs/_build
db.sqlite
start_project_flask.py
"""
    make_open('.gitignore', plot)


def create_the_project(name_project, description):
    if description == '':
        description = f"Default Application {name_project}"
    os.makedirs(name_project)
    os.system(f'cd {name_project} && mkdir src')
    os.makedirs('tests')
    create_docs(name_project)
    create_conf_test(name_project)
    create_app(name_project)

    create_env(name_project)
    create_secrets()
    create_make_file(name_project)
    create_requiments()
    create_requiments_dev()
    create_settings(name_project)
    create_configuration(name_project)
    create_setup(name_project, description)
    create_gitignore()

    os.system("python3 -m venv env")


if __name__ == '__main__':
    name_project = input('Typing the name project: ')
    description = input('Typing the name description: ')
    create_the_project(name_project, description)
    print(name_project + " created successfully")
