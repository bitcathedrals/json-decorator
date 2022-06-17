#! /bin/bash

PACKAGE_PYTHON_VERSION="3.10:latest"

case $1 in

#
# tooling
#

    "install-tools")
        brew update

        brew install pyenv
        brew install pyenv-virtualenv
    ;;
    "update-tools")
        brew update

        brew upgrade pyenv
        brew upgrade pyenv-virtualenv
    ;;

#
# virtual environments
#
    "virtual-install")
        pyenv install --skip-existing "$PACKAGE_PYTHON_VERSION"

        LATEST=$(pyenv versions | grep -E '\d+\.\d+\.\d+' | sed 's/ *//g')

        pyenv virtualenv "$LATEST" "release"

        pyenv virtualenv "$LATEST" "dev"
    ;;
    "virtual-destroy")
        pyenv virtualenv-delete "release"
        pyenv virtualenv-delete "dev"

    ;;

    "virtual-list")
        pyenv virtualenvs
    ;;

#
# all environments
#
    "versions")
        pyenv version
        pyenv exec python --version
        pipenv graph
    ;;
    "test")
        pyenv exec python -m pytest tests
    ;;

    "run")
        shift
        pyenv exec $@ 
    ;;

#
#   build
#
    "freeze")
        pipenv lock
    ;;
    "requirements")
        pipenv run python -m pip freeze
    ;;
    "build")
        pyenv local "release"
        pipenv install --ignore-pipfile &&\
        pyenv exec python -m pytest tests &&\
        pyenv exec python -m build
    ;;

#
# dev environment
#
    "dev-pull")
        pipenv install --skip-lock
        pyenv rehash
    ;;
    "dev-all")
        pythion -m pip install -U pip
        python -m pip install -U pipenv
        pipenv install --dev --skip-lock
        pyenv rehash
    ;;
  
#
# release environment
#
    "release-pull")
        pyenv exec python -m pip -U pip
        python -m pip install -U pipenv
        pipenv install --ignore-pipfile
        pyenv rehash
    ;;

    *)
        echo "unknown command."
    ;;
esac
