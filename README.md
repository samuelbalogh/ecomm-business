# Ecomm analytics endpoint

## Summary

The project uses a `sqlite` database file for storing and querying the data, Flask for handling requests.   
It does basic error handling and some unit testing.  
I've opted for a pure SQL solution as opposed to using an ORM or the SqlAlchemy expression language for the sake of simplicity. A raw SQL solution might seem prone to SQL injection, but if it's used with the `?` placeholder, the DB-API makes sure that the parameters are safe.

## Shortcomings

- I could not include the commission per promotion data in the report due to lack of time and lack of complete understanding about the promotion/commission relationship
- I have not written tests for the SQL query, which is a main shortcoming of the submission - writing a test for it would have involved generating a known dataset in a test DB and making sure that the results of the query match the expected results. This would have been essential in a production environment
- The simplicity of the task made me avoid writing OOP-style code
- Logging is omitted


## Requirements & setup

Create and activate Python virtualenv

```
python3 -m venv env
. ./env/bin/activate
python3 -m pip install -r requirements.txt
```

Run tests

```
make test
```

Run the Flask server:

```
make run
```

Visit http://127.0.0.1:5000/2019-09-26 in a browser/Postman/curl which should return a report for that day.



## DB migration

The repository contains a sqlite database file called `ecomm.db` which has the required tables and data already loaded, so it shouldn't be necessary to do the following steps, but I've included the migration steps for the sake of documentation.


`sqlite3` version `3.34` or higher is required:

```
brew install sqlite3
echo 'export PATH="/usr/local/opt/sqlite/bin:$PATH"' >> /Users/$(whoami)/.bash_profile
```

Create the DB and the tables:

```
make migrate
```

Load the data:

```
make loadfixtures
```
