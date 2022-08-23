# Federated Learning Hub Service

## Prerequirements

- [Docker](https://docs.docker.com/engine/install/ubuntu/)

- Requirements

```bash
apt install libmariadb-dev
pip3 install --upgrade -r requirements.txt
```

## Prepare database

### Run MariaDB on Docker

```bash
docker pull mariadb
docker run --name flhubdb -p 3306:3306 -v ABSOLUTEPATH/var/lib/mysql:/var/lib/mysql -e MARIADB_ROOT_PASSWORD=my-secret-pw -d mariadb:latest
```

### Create user and database

```bash
docker exec -it flhubdb bash
mariadb -uroot -p
```

```sql
CREATE DATABASE flhubdb;
CREATE USER IF NOT EXISTS flhub@flhubdb IDENTIFIED BY 'user-secret-pw';
SHOW WARNINGS;
GRANT ALL PRIVILEGES ON flhubdb.* TO 'flhub'@'%' IDENTIFIED BY 'user-secret-pw';
FLUSH PRIVILEGES;
```

### Create secret file

```python
dbname = 'flhub'
dbhost = '127.0.0.1'
dbport = 3306
dbuser = 'fluser'
dbpassword = 'user-secret-pw'
```
