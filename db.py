import datetime
import os

from fabric.api import env, get, run, abort, local
from fabric.colors import green, yellow
from fabric.contrib.files import exists
from fabric.operations import require
from fabric.utils import warn


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))


__all__ = ['fetch_dump', 'load_dump', 'clear_dumps', 'create_database']


def fetch_dump():
    require('site_db_name', provided_by='e')
    require('site_db_user', provided_by='e')
    require('site_db_password', provided_by='e')
    require('site_db_dump_dir', provided_by='e')

    now = datetime.datetime.now()
    dump_path = os.path.join(PROJECT_ROOT, env.site_db_dump_dir)

    if not os.path.exists(dump_path):
        os.mkdir(dump_path, 0777)

    remote_dump_path = os.path.join(env.site_root, env.site_db_dump_dir)

    if not exists(remote_dump_path):
        run('mkdir 0755 %s' % remote_dump_path)

    filename = '%s_%s.sql.gz' % (env.site_db_name, now.strftime('%Y-%m-%d_%H-%M-%S'))
    remote_file_path = os.path.join(remote_dump_path, filename)
    command = 'pg_dump %s -U %s -W %s|gzip > %s'  % (env.site_db_name, env.site_db_user, env.site_db_password, remote_file_path)

    run(command)
    get(remote_file_path, dump_path)


def load_dump(filename=None):
    require('site_db_name', provided_by='e')
    require('site_db_user', provided_by='e')
    require('site_db_password', provided_by='e')
    require('site_db_dump_dir', provided_by='e')

    dump_path = os.path.join(PROJECT_ROOT, env.site_db_dump_dir)

    if not filename:
        filename = sorted([fl for fl in os.listdir(dump_path) if fl.endswith('.gz')]).pop()

    if filename is None:
        raise Exception("No dump found.")

    filepath = os.path.join(dump_path, filename)
    filepath_sql = filepath[:-3]

    if os.path.exists(filepath) and not os.path.exists(filepath_sql):
        local("gunzip -f %s" % filepath)

    create_database()

    local('pv %s | psql %s  -U %s -W %s < %s' % (filepath_sql, env.site_db_name, env.site_db_user, env.site_db_password, filepath_sql))


def clear_dumps():
    require('site_db_dump_dir', provided_by='e')
    dump_path = os.path.join(PROJECT_ROOT, env.site_db_dump_dir)
    local("rm -fr %s/*" % dump_path.rstrip('/'))


def create_database():
    require('site_db_name', provided_by='e')
    require('site_db_user', provided_by='e')
    require('site_db_password', provided_by='e')

    try:
        local('createdb %s -U %s -W %s' % (env.site_db_name, env.site_db_user, env.site_db_password))
        warn(magenta('Created Database = %s' % env.site_db_name))
    except Exception, e:
        warn(yellow('%s' % e))
