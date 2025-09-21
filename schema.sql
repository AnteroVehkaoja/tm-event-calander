CREATE TABLE visits (
    id INTEGER PRIMARY KEY,
    visited_at TEXT
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE tournaments (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description_of_event TEXT,
    host_id REFERENCES users,
    qualifier INTEGER,
    whenevent INTEGER
);