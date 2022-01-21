![Screenshot](logo.png)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Build Status](https://app.travis-ci.com/vyahello/complainer.svg?branch=main)](https://app.travis-ci.com/github/vyahello/complainer)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with pylint](https://img.shields.io/badge/pylint-checked-blue)](https://www.pylint.org)
[![Checked with flake8](https://img.shields.io/badge/flake8-checked-blue)](http://flake8.pycqa.org/)
[![Checked with interrogate](https://img.shields.io/badge/interrogate-checked-yellowgreen)](https://interrogate.readthedocs.io/en/latest/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)
[![EO principles respected here](https://www.elegantobjects.org/badge.svg)](https://www.elegantobjects.org)
[![CodeFactor](https://www.codefactor.io/repository/github/vyahello/complainer/badge)](https://www.codefactor.io/repository/github/vyahello/complainer)

# Complainer

> Web app to display users product complaints based on fastapi and sqlalchemy.

## Tools

### Production
- python 3.7, 3.8, 3.9
- [fastapi](https://fastapi.tiangolo.com/)
- [sqlalchemy](https://www.sqlalchemy.org) (postgreSQL)
- [pydantic](https://pydantic-docs.helpmanual.io/)

### Development

- [travis](https://travis-ci.org/)
- [pytest](https://pypi.org/project/pytest/)
- [black](https://black.readthedocs.io/en/stable/)
- [mypy](http://mypy.readthedocs.io/en/latest)
- [pylint](https://www.pylint.org/)
- [flake8](http://flake8.pycqa.org/en/latest/)
- [interrogate](https://interrogate.readthedocs.io/en/latest)

## Usage

### Quick start

```bash
git clone git@github.com:vyahello/complainer.git
cd complainer
python3 -m venv venv 
. venv/bin/activate
pip install -r requirements.txt
python app.py
```

**[⬆ back to top](#complainer)**

## Development notes

### REST API 

Please follow `/docs` endpoint to see all API endpoints.

- `/register` to register user:
  - Request sample:
    ```bash
    curl -X 'POST' \
      'http://127.0.0.1:8000/register' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "email": "aa@gmail.com",
      "password": "string",
      "phone": "string",
      "first_name": "string",
      "last_name": "string",
      "iban": "string"
    }'
    ```
  - Response body sample (201 code):
    ```bash 
    {"token": "XXXXX"}
    ```

- `/login` to login user:
  - Request sample:
    ```bash
    curl -X 'POST' \
      'http://127.0.0.1:8000/login' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "email": "aa@gmail.com",
     "password": "string"
    }'
    ```
  - Response body sample (200 code):
    ```bash 
    {"token": "XXXXX"}
    ```

- `/complaints` (user should be authorized via bearer token):
  - Get all complaints (`GET` request sample):
    ```bash
    curl -X 'GET' \
      'http://127.0.0.1:8000/complaints' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer XXXX'
    ```
  - Response body sample (200 code):
    ```bash
    [
      {
        "title": "aa@gmail.com",
        "description": "string",
        "photo_url": "string",
        "amount": 20,
        "id": 1,
        "created_at": "2022-01-20T11:53:34.532277",
        "status": "Pending"
      }
    ]
    ```
  - Create complaint (`POST` request sample):
    ```bash
    curl -X 'POST' \
      'http://127.0.0.1:8000/complaints' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer XXXX' \
      -H 'Content-Type: application/json' \
      -d '{
       "title": "aa@gmail.com",
       "description": "string",
       "photo_url": "string",
       "amount": 20
    }'
    ```
  - Response body sample (200 code):
    ```bash
    {
      "title": "aa@gmail.com",
      "description": "string",
      "photo_url": "string",
      "amount": 20,
      "id": 1,
      "created_at": "2022-01-20T11:53:34.532277",
      "status": "Pending"
    }
    ```

- `/delete` to delete complaint (only `admin` user role can delete complaints): 
  - Request sample:
    ```bash
    curl -X 'DELETE' \
      'http://127.0.0.1:8000/complaint/2' \
      -H 'accept: */*' \
      -H 'Authorization: Bearer XXXX'
    ```
  - Response sample (empty with 204 code)

- `/users` to get all users (user should be authorized via bearer token): 
  - Request sample:
    ```bash
    curl -X 'GET' \
      'http://127.0.0.1:8000/users' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer XXXX'
    ```
  - Response sample (200 code):
    ```bash
    [
      {
        "id": 1,
        "email": "aa@gmail.com",
        "password": "$2b$12$DiSLHYj54aVrGfQ6BADrAu4/RvJRaiO.eyQsJy08WHuV2HynOKsRe",
        "first_name": "string",
        "last_name": "string",
        "phone": "string",
        "role": "complainer",
        "iban": "string"
      }
    ]
    ```

- `/users/{user_id}/make-admin` change role to admin (user should be authorized via bearer token): 
  - Request sample:
    ```bash
    curl -X 'PUT' \
      'http://127.0.0.1:8000/users/2/make-admin' \
      -H 'accept: */*' \
      -H 'Authorization: Bearer XXXX'
    ```
  - Response sample (empty with 204 code)

    
- `/users/{user_id}/make-approver` change role to approver (user should be authorized via bearer token): 
  - Request sample:
    ```bash
    curl -X 'PUT' \
      'http://127.0.0.1:8000/users/2/make-approver' \
      -H 'accept: */*' \
      -H 'Authorization: Bearer XXXX'
    ```
  - Response sample (empty with 204 code)

- `/complaints/{complaint_id}/approve` approve complaint (user should be authorized via bearer token): 
  - Request sample:
    ```bash
    curl -X 'PUT' \
      'http://127.0.0.1:8000/complaints/3/approve' \
      -H 'accept: */*' \
      -H 'Authorization: Bearer XXXX'
    ```
  - Response sample (empty with 204 code)

- `/complaints/{complaint_id}/reject` reject complaint (user should be authorized via bearer token): 
  - Request sample:
    ```bash
    curl -X 'PUT' \
      'http://127.0.0.1:8000/complaints/3/reject' \
      -H 'accept: */*' \
      -H 'Authorization: Bearer XXXX'
    ```
  - Response sample (empty with 204 code)

### S3 integration

[AWS S3](https://s3.console.aws.amazon.com/s3) is used to store user complaint photos and get access from the repo.
In order to use S3, please fill in the following env vars in your .env file:
```text
AWS_ACCESS_KEY=XXXX
AWS_SECRET_KEY=XXXX
AWS_BUCKET_NAME=XXXX
AWS_REGION=XXXX
```

### Custom scripts 

[create_super_user](complainer/commands/create_super_user.py) script is used to create new admin user.

Please make sure that `PYTHONPATH` is set to current working directory:
```bash
export PYTHONPATH=./
```

### DB migration

`alembic` is used for database migrations (let's say you have added new column to your table).

Init migrations:
```bash
alembic init migrations
```

Generate revision:
```bash
alembic revision --autogenerate -m 'Initial'
```

Set latest db revision:
```bash
alembic upgrade head
```

### Testing

Generally, `pytest` tool is used to organize testing procedure.

Please follow next command to run unittests:
```bash
pytest
```

### CI

Project has Travis CI integration using [.travis.yml](.travis.yml) file thus code analysis (`black`, `pylint`, `flake8`, `mypy` and `interrogate`) and unittests (`pytest`) will be run automatically after every made change to the repository.

To be able to run code analysis, please execute command below:
```bash
./analyse-source-code.sh
```

---
**Note:** It is possible to set `analyse-source-code.sh` as a pre-commit hook. Please copy shell file to `.git/hooks/pre-commit` path.

---

### Release notes

Please check [changelog](CHANGELOG.md) file to get more details about actual versions and it's release notes.

### Meta

Author – _Volodymyr Yahello_. Please check [authors](AUTHORS.md) file for more details.

Distributed under the `MIT` license. See [license](LICENSE.md) for more information.

You can reach out me at:
* [vyahello@gmail.com](vyahello@gmail.com)
* [https://github.com/vyahello](https://github.com/vyahello)
* [https://www.linkedin.com/in/volodymyr-yahello](https://www.linkedin.com/in/volodymyr-yahello)

### Contributing

I would highly appreciate any contribution and support. If you are interested to add your ideas into project please follow next simple steps:

1. Clone the repository
2. Configure `git` for the first time after cloning with your `name` and `email`
3. `pip install -r requirements.txt` to install all project dependencies
4. `pip install -r requirements-dev.txt` to install all development project dependencies
5. Create your feature branch (git checkout -b feature/fooBar)
6. Commit your changes (git commit -am 'Add some fooBar')
7. Push to the branch (git push origin feature/fooBar)
8. Create a new Pull Request

### What's next

All recent activities and ideas are described at project [issues](https://github.com/vyahello/complainer/issues) page. 
If you have ideas you want to change/implement please do not hesitate and create an issue.

**[⬆ back to top](#complainer)**
