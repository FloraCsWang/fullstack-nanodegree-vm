-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE game ( id SERIAL,
                    name TEXT,
                    wins Integer DEFAULT 0,
                    matches Integer DEFAULT 0);
