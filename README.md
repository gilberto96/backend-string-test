# Foobar

API for backend development evaluation with Python and Flask for Sting.

## Installation

1. Clone repository from:
```
https://github.com/gilberto96/backend-string-test.git
```

2. Open the project folder in terminal

3. Start the enviroment in venv folder 
```bash
venv\Scripts\activate.bat
```

4. Install python libraries:

```bash
pip install -r requirements.txt
```

5. Set enviroment variables:
```bash
Linux/Mac
export FLASK_APP=flaskr
export FLASK_ENV=development

Windows cmd
set FLASK_APP=flaskr
set FLASK_ENV=development

Windows PowerShell
$env:FLASK_APP = "flaskr"
$env:FLASK_ENV = "development"
```

6. Configure database connection string in config.py file:
```
config.py
DATABASE = {
    "SQLALCHEMY_DATABASE_URI":"mysql://dbuser:dbpassword@localhost/databasename",
}
```

7. Run Flask
```bash
flask run
```

## Usage

To view the documentation and test the API go to:

```browser
http://127.0.0.1:5000/api/docs
```
## Tests

To run pytest just execute this command form terminal in the project folder:

```
pytest
```