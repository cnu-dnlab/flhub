-- Why we use file storage not RDBMS file arhive?
-- https://www.brentozar.com/archive/2021/07/store-files-in-a-file-system-not-a-relational-database/

-- For authentication
CREATE TABLE IF NOT EXISTS users (
  id INT UNSIGNED AUTO_INCREMENT,
  username TEXT NOT NULL,
  salt TEXT NOT NULL,
  hpassword TEXT NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (username)
);

-- userid: For model uploader
CREATE TABLE IF NOT EXISTS models (
  id INT UNSIGNED AUTO_INCREMENT,
  userid INT UNSIGNED NOT NULL,
  modelname TEXT NOT NULL,
  detail TEXT NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (userid, modelname)
);

-- modelid: Base model
-- parentid: parent version id
CREATE TABLE IF NOT EXISTS versions (
  id INT UNSIGNED AUTO_INCREMENT,
  modelid INT UNSIGNED NOT NULL,
  parentid INT UNSIGNED DEFAULT 0,
  major INT UNSIGNED NOT NULL,
  minor INT UNSIGNED NOT NULL,
  micro INT UNSIGNED NOT NULL,
  location TEXT NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (modelid, major, minor, micro)
);

-- status: 0: normal, 1: merge waiting, 2: merged
CREATE TABLE IF NOT EXISTS commits (
  id INT UNSIGNED AUTO_INCREMENT,
  userid INT UNSIGNED NOT NULL,
  versionidfrom INT UNSIGNED NOT NULL,
  versionidto INT UNSIGNED DEFAULT 0,
  revision INT UNSIGNED NOT NULL,
  location TEXT NOT NULL,
  status TINYINT(2) UNSIGNED DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE (versionidfrom, userid, revision)
);

