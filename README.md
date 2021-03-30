# Keep me on rails

## Implemented features
- [x] Application factory
- [x] Flask Blueprints
- [x] Unitary test classes with pytest
- [ ] ???

## Run the app

### Requirements

To run the app, you'll need:

* an SQL database engine (like sqlite, postgres, etc)
* an API key for SNCF API

The app requires a *.env* file in the /app folder. 
This environment variables file must contain those variables: 

* PROD_DATABASE_URI: uri of the database for the production environment (eg 'sqlite:////home/user/prod_app.db')
* DEV_DATABASE_URI: uri of the database for dev purpose (eg 'sqlite:////home/user/dev_app.db')
* TEST_DATABASE_URI: uri of the database for pytest (eg 'sqlite:////home/user/test_app.db')
* SNCF_TOKEN: token provided by the SNCF API


### Locally
The following commands are run at the root of the repo folder. 

First, install required Python packages: 

```bash
pipenv install
```

Then activate the virtual: 

```bash
pipenv shell
```

After the virtual environment is activated, export the following environment variables:

```bash
export FLASK_APP=app/wsgi.py
export FLASK_ENV=development
```

The app configuration is different according to **FLASK_ENV** definition: *testing*, *development* and *production* options are handled. 

### With a docker container
More to come...
