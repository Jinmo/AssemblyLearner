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
  category CHAR(200)
);

CREATE TABLE IF NOT EXISTS category (
  name CHAR(200) PRIMARY KEY,
  title TEXT,
  order_no INT
);

CREATE TABLE IF NOT EXISTS solved (
  id CHAR(20),
  problem CHAR(200),
  time TIMESTAMP
);

REPLACE INTO category VALUES
(
  'tutorial', '튜토리얼', 0
),
(
  'sh', '쉘코드 짜기', 1
),
(
  'func', '손-코딩를 해-봅시다.', 2
);
