CREATE TABLE IF NOT EXISTS user (
  id CHAR(20) PRIMARY KEY,
  password CHAR(40),
  solved TEXT
);

CREATE TABLE IF NOT EXISTS problem (
  name CHAR(200) PRIMARY KEY,
  title TEXT,
  instruction TEXT,
  answer_regex TEXT
);

CREATE TABLE IF NOT EXISTS category (
  name CHAR(200) PRIMARY KEY,
  title TEXT,
  order_no INT
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
