-- Table definitions for the tournament project.
--
--
-- Create database, checking if the previous datatable exists. If any has exists, drop before creating new one. 
drop database if exists tournament;
create database tournament;

-- running this file from psql, so can contain psql command
\c tournament

-- create table, players to register. To test multiple times, check and drop the previous tables
drop table if exists players;
create table players (
    id serial primary key not null,
    name text not null
);

-- create table, matches to record matches with match id, player id of the winner and the loser.
drop table if exists matches;
create table matches (
    id serial primary key not null,
    winner_id int REFERENCES players(id),
    loser_id int REFERENCES players(id)
);

