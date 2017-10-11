It's a Swiss Tournament planner using [PostgreSQL](https://www.postgresql.org/docs/9.4/static/datatype-numeric.html) database. This project is a part of Udacity class.

Swiss system tournament: It is a non-emilinating tournament format. The players in games are not eliminated, and each player are paired with another player with the similar running score.

## File structure
- `tournament_test.py`: Test cases for `tournament.py`
- `tournament.py`: Contains functions to match up players in the tournament and to access the database
- `tournament.sql`: Databese schema

## VM Usage
1. Power up the VM and log in to the VM.

Navigate to `swiss-tournament` directory in terminal(if Mac), then run the following.
```
vagrant up 
vagrant ssh
```

2. launch psql in `/vagrant/swiss-tournament` directory
```
vagrant@vagrant:~$ cd /vagrant/tournament
vagrant@vagrant:~$ psql
```

3. Import `tournament.sql`, which creates related database and tables 
```
vagrant=> \i tournament.sql
```
Other psql command can be found [here](#psql-command-line)

## Test code
Run `tournament_test.py`.
```
vagrant@vagrant:/vagrant/tournament$ python tournament_test.py
```

## psql command line
- `psql` Launches psql command line
- `psql tournament` Launches and connects to tournament database 
- `\c tournament` Connects to the tournament database, dropping the previous connection
- `\i tournament.sql` Imports the file and executes the sql commands within the file
- `\d matches` Describe the table (matches) structure
- `\dt` List tables in the database
- `\q` Quit the psql

## Further description
Further description can be found [here](https://docs.google.com/document/d/16IgOm4XprTaKxAa8w02y028oBECOoB1EI1ReddADEeY/pub?embedded=true)
