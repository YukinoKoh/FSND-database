It's a web server application project using [vagrant](https://www.vagrantup.com/), [sqlalchemy](https://github.com/zzzeek/sqlalchemy/), and [BaseHTTPServer](https://docs.python.org/2/library/basehttpserver.html).

## File Structure
- `database_setup.py`: It will set up database using sqlalchemy
- `restaurantmenu.db`: This file is generated by running database_setup.py
- `session.py`: Session objects to updata the database