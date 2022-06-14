import os
import sys
import time

import secret

FLAGS = _ = None
DEBUG = False
STIME = time.time()


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    try:
        conn = mariadb.connect(
                 user=secret.dbuser,
                 password=secret.dbpassword,
                 host=secret.dbhost,
                 port=secret.dbport,
                 database=secret.dbname)
    except mariadb.Error as e:
        print(f'[{int(time.time()-STIME)}] Error connecting to MariaDB: {e}')
        sys.exit(0)
    cur = conn.cursor()

    if FLAGS.reset:
        print(f'[{int(time.time()-STIME)}] Dropped all tables of {secret.dbname}')


    cur.execute('''SHOW TABLES;''')
    res = cur.fetchall()
    print(f'[{int(time.time()-STIME)}] Created Tables: {res}')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    root_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(root_path)
    os.chdir(root_dir)

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--reset', action='store_true',
                        help='Clear exists tables before creation')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()

