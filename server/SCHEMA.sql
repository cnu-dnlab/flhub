-- Why we use file storage not RDBMS file arhive?
-- https://www.brentozar.com/archive/2021/07/store-files-in-a-file-system-not-a-relational-database/

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT,
  username TEXT NOT NULL,
  salt TEXT NOT NULL,
  hpassword TEXT NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (username)
);

CREATE TABLE IF NOT EXISTS models (
  id INT AUTO_INCREMENT,
  userid INT NOT NULL,
  modelname TEXT NOT NULL,
  detail TEXT NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (userid, modelname)
);

CREATE TABLE IF NOT EXISTS versions (
  id INT AUTO_INCREMENT,
  modelid INT NOT NULL,
  major INT NOT NULL,
  minor INT NOT NULL,
  micro INT NOT NULL,
  location TEXT NOT NULL,
  PRIMARY KEY(id),
  UNIQUE (modelid, major, minor, micro)
);

CREATE TABLE IF NOT EXISTS commits (
  id INT AUTO_INCREMENT,
  versionid INT NOT NULL,
  userid INT NOT NULL,
  location TEXT NOT NULL,
  status TINYINT(2) UNSIGNED DEFAULT 0, -- 0: normal, 1: merge waiting, 2: merged
  PRIMARY KEY (id),
  UNIQUE (versionid, userid) -- One commit per one user
);
