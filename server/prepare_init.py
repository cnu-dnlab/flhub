import os
import sys
import time
import subprocess
import shlex

import secret

FLAGS = _ = None
DEBUG = False
STIME = time.time()


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    # docker clear
    script_path = os.path.join(os.getcwd(), 'clean.sh')
    with open(script_path, 'w') as f:
        f.write(f'''#!/bin/bash\n''')
        f.write(f'''\n''')
        f.write(f'''if [ "$1" != "yes" ] && [ "$1" != "YES" ];\n''')
        f.write(f'''then\n''')
        f.write(f'''    echo "CAUTION SCRIPT"\n''')
        f.write(f'''    echo "Execute $0 yes"\n''')
        f.write(f'''    exit 0\n''')
        f.write(f'''fi\n''')
        f.write(f'''\n''')
        f.write(f'''docker container stop {secret.ctname}\n''')
        f.write(f'''docker container rm {secret.ctname}\n''')
    command = f'chmod +x {script_path}'
    subprocess.run(shlex.split(command))
    print(f'Created {script_path}')

    # docker preparing
    script_path = os.path.join(os.getcwd(), 'initialize.sh')
    with open(script_path, 'w') as f:
        f.write(f'''#!/bin/bash\n''')
        f.write(f'''\n''')
        f.write(f'''if [ "$1" != "yes" ] && [ "$1" != "YES" ];\n''')
        f.write(f'''then\n''')
        f.write(f'''    echo "CAUTION SCRIPT"\n''')
        f.write(f'''    echo "Execute $0 yes"\n''')
        f.write(f'''    exit 0\n''')
        f.write(f'''fi\n''')
        f.write(f'''\n''')
        f.write(f'''python3 -m grpc_tools.protoc -I./ --python_out . --grpc_python_out . flhub.proto\n''')
        f.write(f'''docker pull mariadb\n''')
        f.write(f'''docker run --name {secret.ctname} -p {secret.dbport}:3306 -v {os.path.join(os.getcwd(), 'var/lib/mysql')}:/var/lib/mysql -v {os.path.join(os.getcwd(), FLAGS.init)}:/docker-entrypoint-initdb.d -e MARIADB_ROOT_PASSWORD={secret.dbrootpassword} -d mariadb:latest''')
    command = f'chmod +x {script_path}'
    subprocess.run(shlex.split(command))
    print(f'Created {script_path}')
    
    # initializing instance
    os.makedirs(FLAGS.init, exist_ok=True)
    script_path = os.path.join(FLAGS.init, '00-create_user.sql')
    with open(script_path, 'w') as f:
        f.write(f'''CREATE DATABASE {secret.dbname};\n''')
        f.write(f'''CREATE USER IF NOT EXISTS {secret.dbuser}@{secret.dbname} IDENTIFIED BY '{secret.dbpassword}';\n''')
        f.write(f'''SHOW WARNINGS;\n''')
        f.write(f'''GRANT ALL PRIVILEGES ON {secret.dbname}.* TO '{secret.dbuser}'@'%' IDENTIFIED By '{secret.dbpassword}';\n''')
        f.write(f'''FLUSH PRIVILEDGES;\n''')
    print(f'Created {script_path}')


if __name__ == '__main__':
    import argparse

    root_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(root_path)
    os.chdir(root_dir)

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--init', default='docker-entrypoint-initdb.d',
                        help='The path for entrypoint')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug
    FLAGS.init = os.path.abspath(os.path.expanduser(FLAGS.init))

    main()

