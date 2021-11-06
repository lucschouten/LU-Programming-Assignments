CREATE TABLE Account(
username VARCHAR(30),
score_easy INT DEFAULT 0,
score_medium INT DEFAULT 0,
score_hard INT DEFAULT 0,
score_extreme INT DEFAULT 0,
PRIMARY KEY (username));
-- DROP TABLE Account;
CREATE Table Password(
username VARCHAR(30),
hash_key VARCHAR(256), #hexed hash key of 128bytes
salt VARCHAR(64), #hexed bytarrary of 32bytes
FOREIGN KEY (username) REFERENCES Account(username) ON DELETE CASCADE);
-- DROP TABLE Password;
-- SHOW PROCESSLIST;
-- SELECT * FROM Account;
-- SELECT * From Password;