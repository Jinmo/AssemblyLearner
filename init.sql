CREATE TABLE IF NOT EXISTS user (
  id CHAR(20) PRIMARY KEY,
  password CHAR(40),
  role CHAR(10) DEFAULT 'member'
);

CREATE TABLE IF NOT EXISTS problem (
  id INTEGER PRIMARY Key AUTOINCREMENT ,
  name CHAR(200) UNIQUE,
  instruction TEXT,
  answer_regex TEXT,
  suffix TEXT,
  example TEXT,
  status CHAR(10),
  category CHAR(50),
  input TEXT,
  createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS solved (
  id INTEGER PRIMARY Key AUTOINCREMENT,
  problem INTEGER,
  status CHAR(10),
  answer TEXT,
  errmsg TEXT,
  time TIMESTAMP
);

CREATE TABLE IF NOT EXISTS snippets (
    id INTEGER PRIMARY Key AUTOINCREMENT ,
    filename TEXT UNIQUE,
    code TEXT,
    owner CHAR(200)
);
