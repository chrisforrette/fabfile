import datetime
import os

from fabric.api import env, get, run, abort, local
from fabric.colors import green
from fabric.contrib.files import exists


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DUMP_DIR_NAME = 'dumps'
DUMP_PATH = os.path.join(PROJECT_ROOT, DUMP_DIR_NAME)


__all__ = ['fetch_dump', 'load_dump']


def fetch_dump():
    now = datetime.datetime.now()

    if not os.path.exists(DUMP_PATH):
        os.mkdir(DUMP_PATH, 0777)

    remote_dump_path = os.path.join(env.project_root, DUMP_DIR_NAME)

    if not exists(remote_dump_path):
        run('mkdir 0755 %s' % remote_dump_path)

    filename = '%s_%s.sql.gz' % (env.db_name, now.strftime('%Y-%m-%d_%H-%M-%S'))
    remote_file_path = os.path.join(remote_dump_path, filename)
    command = 'pg_dump %s -U %s|gzip > %s'  % (env.db_name, env.db_user, remote_file_path)
    run(command)
    get(remote_file_path, DUMP_PATH)


def load_dump(filename=None):
    if not filename:
        filename = sorted([fl for fl in os.listdir(DUMP_PATH) if not fl.startswith('.')]).pop()

    filepath = os.path.join(DUMP_PATH, filename)

    if filepath[-3] == '.gz':
        local('gunzip -f %s' % filepath)
        sqlfile = filepath[:-3]
    else:
        sqlfile = filepath

    if os.path.isfile(sqlfile):
        print(green('Dropping database and loading: %s' % sqlfile))
        local('dropdb %s -U %s' % (env.db_name, env.db_user))
        local('createdb %s -U %s' % (env.db_name, env.db_user))
        local('psql %s < %s' % (env.db_name, sqlfile))
    else:
        abort('%s does not exist' % sqlfile)

