# Consolidate

![logo](https://raw.githubusercontent.com/Ray-F/consolidate/master/docs/assets/consolidate_logo_64.png)

PWA for consolidating and reporting on personal finances across different asset categories.



## Software Architecture

Development for this application mainly requires knowledge of:
- JavaScript (TypeScript optional) - React, Material UI, styled-components 
- Python 3 - This uses Flask as a backend API
- GraphQL - API language

## Setup

1. Download Python 3 and `pip`. Run `pip install virtualenv`.

2. Go into this virtual environment by running `python3 -m venv env`. This will create a new `venv` folder in the 
   root directory (this is ignored by Git).
   
3. To activate the virtual environment, run `source venv/bin/activate` on macOS and `.\venv\Scripts\activate` on Windows
   
4. Install all required pip packages by running `pip install -r requirements.txt` 
   (this installs all packages listed in `requirements.txt` file). IMPORTANT: Make sure this is run inside the virtual
   environment.
   
5. Create one is inside the root directory (`.env`) with the following runtime options:

```
PYTHONDONTWRITEBYTECODE=true
FLASK_APP=main
FLASK_ENV=development
```

6. Create another environment file `main/.env` for application secrets:

```
MONGO_URI=<MONGO_KEY_HERE>
```

7. To run the application, run `flask run` inside the root directory.
