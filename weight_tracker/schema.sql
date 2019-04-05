DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS weight_record;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE weight_record (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  recorded TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  weight REAL NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);