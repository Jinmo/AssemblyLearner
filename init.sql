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
  createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tag (
  name CHAR(200),
  prob_id INTEGER
);

CREATE TABLE IF NOT EXISTS solved (
  id CHAR(20),
  problem INTEGER,
  status CHAR(10),
  answer TEXT,
  time TIMESTAMP
);
