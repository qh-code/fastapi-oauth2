# Setup Development Environment

## Install Python Dependencies

This project uses https://github.com/pypa/pipenv for dependencies
management, so you must install it on your system:

```bash
$ sudo apt install pipenv
```

Then, install requirements (both windows and other OS):

```bash
$ pipenv install
```

## OAuth configuration

(see [here](OAUTH-README.md))


## Starting app

```bash
$ pipenv run uvicorn main:app --reload
```
