CREATE TABLE IF NOT EXISTS user (
  id CHAR(20) PRIMARY KEY,
  password CHAR(40),
  role CHAR(10) DEFAULT 'member'
);

CREATE TABLE IF NOT EXISTS problem (
  name CHAR(200) PRIMARY KEY,
  title TEXT,
  instruction TEXT,
  answer_regex TEXT,
  suffix TEXT,
  example TEXT,
  status CHAR(10),
  createdAt TIMESTAMP,
  updatedAt TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tag (
  name CHAR(200),
  problem_name CHAR(200)
);

CREATE TABLE IF NOT EXISTS solved (
  id CHAR(20),
  problem CHAR(200),
  status CHAR(10),
  answer 
  time TIMESTAMP
);
