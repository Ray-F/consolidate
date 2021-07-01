# Consolidate

![logo](https://raw.githubusercontent.com/Ray-F/consolidate/master/docs/assets/consolidate_logo_64.png)

PWA for consolidating and reporting on personal finances across different asset categories.



## Software Architecture and prerequisites

Development for this application mainly requires knowledge of:
- JavaScript (TypeScript optional) - React, Material UI, styled-components 
- Python 3 - This uses Flask as a backend API
- GraphQL - API language

Make sure you have the following installed before proceeding:

- Node version 14+ with `yarn` or `npm`
- Python3 and `pip`

## Client Setup

1. Go into the `client` directory and install node dependencies (`yarn install`)

## Server Setup

1. Go into the `server` directory and run `pip install virtualenv`

2. Go into this virtual environment by running `python3 -m venv env`. This will create a new `venv` folder in the 
   root directory (this is ignored by Git).
   
3. To activate the virtual environment, run `source venv/bin/activate` on macOS and `.\venv\Scripts\activate` on Windows
   
4. Install all required pip packages by running `pip install -r requirements.txt` 
   (this installs all packages listed in `requirements.txt` file). IMPORTANT: Make sure this is run inside the virtual
   environment.
   
5. Create an environment file inside the root directory (`.env`) with the following runtime options:

```
PYTHONDONTWRITEBYTECODE=true
FLASK_APP=main
FLASK_ENV=development
```

6. Create another environment file `main/.env` for application secrets:

```
MONGO_URI=<MONGO_KEY_HERE>
```

## Running the Dev Environment

1. To run the application, run `flask run` inside the root directory. This should start a dev server at `localhost:5000`

2. Activate development server by running `yarn run start`. This starts a dev server at `localhost:3000`

