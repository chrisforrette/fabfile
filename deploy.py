import os

from fabric.api import env, cd, run
from fabric.contrib.files import exists, upload_template
from fabric.context_managers import settings
from fabric.operations import require


__all__ = ['upload_apache_conf', 'upload_nginx_conf', 'install_virtualenv', 'install_requirements', \
    'pull', 'clean', 'compile_css', 'collect_static', 'compress', 'restart_apache', 'restart_nginx', \
    'deploy']

here = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(here, 'templates')
apache_template_dir = os.path.join(template_dir, 'apache')
nginx_template_dir = os.path.join(template_dir, 'nginx')


def _setup():
    require('site_root', 'site_logs_dir', provided_by='e')
    env.site_log_path = os.path.join(env.site_root, env.site_logs_dir)
    env.site_apache_log_path = os.path.join(env.site_log_path, 'apache')
    env.site_nginx_log_path = os.path.join(env.site_log_path, 'nginx')
    env.site_dumps_path = os.path.join(env.site_root, env.site_db_dump_dir)


def install_ubuntu_packages():
    require('project_use_node', provided_by='e')
    with settings(user='root'):
        run('apt-get update')
        run('apt-get -y install python-software-properties apache2 nginx libapache2-mod-wsgi memcached python-pip postgresql postgresql-client')
        run('pip install virtualenv')
        if env.project_use_node:
            run('apt-get install npm')


def make_directories():
    _setup()
    run('mkdir -p %s' % env.site_log_path)
    run('mkdir -p %s' % env.site_apache_log_path)
    run('mkdir -p %s' % env.site_nginx_log_path)
    run('mkdir -p %s' % env.site_dumps_path)


def set_owner():
    pass


def upload_apache_conf():
    require('server_apache_root', 'site_url', 'site_root', 'project_name', provided_by='e')
    conf_path = os.path.join(env.server_apache_root, '%s.conf' % env.site_url)
    wsgi_path = os.path.join(env.site_root, 'dist/apache/%s.wsgi' % env.site_url)

    upload_template('django.conf', conf_path, context=env, use_jinja=True, template_dir=apache_template_dir, \
        backup=False, mode=0755)
    upload_template('django.wsgi', wsgi_path, context=env, use_jinja=True, template_dir=apache_template_dir, \
        backup=False, mode=0755)


def upload_nginx_conf():
    require('server_nginx_root', 'site_url', 'site_root', 'project_name')
    path = os.path.join(env.server_nginx_root, '%s.conf' % env.site_url)
    upload_template('django.conf', path, context=env, use_jinja=True, template_dir=nginx_template_dir, \
        backup=False, mode=0755)


def install_virtualenv():
    require('site_root', 'site_virtualenv_dir', provided_by='e')
    with cd(env.site_root):
        if not exists(os.path.join(env.site_root, env.site_virtualenv_dir)):
            run('virtualenv %s --no-site-packages' % env.site_virtualenv_dir)


def install_requirements():
    require('site_root', 'site_virtualenv_dir', provided_by='e')
    with cd(env.site_root):
        run('./%s/bin/pip install -r ./requirements.txt' % env.site_virtualenv_dir)
        if env.project_use_node:
            run('npm install')

        if env.project_use_bower:
            run('bower install')


def checkout_repo():
    require('site_root', 'project_repo_url', provided_by='e')
    if not exists(env.site_root):
        with cd(os.path.dirname(env.site_root.rstrip('/'))):
            run('git clone %s %s' % (env.project_repo_url, os.path.basename(env.site_root.rstrip('/'))))


def pull():
    require('site_root', 'site_repo_branch', provided_by='e')
    with cd(env.site_root):
        run('git fetch')
        run('git checkout %s' % env.site_repo_branch)
        run('git pull origin %s' % env.site_repo_branch)


def clean():
    require('site_root', provided_by='e')
    with cd(env.site_root):
        run('find . -name \*.pyc -print -delete')


def compile_css():
    require('site_root', provided_by='e')
    with cd(env.site_root):
        run('compass compile')


def collect_static():
    require('site_root', 'name', provided_by='e')
    with cd(env.site_root):
        run('%s manage.py collectstatic --settings=%s.settings.%s' % (env.python, env.project_name, env.name))


def compress():
    require('site_root', 'name', provided_by='e')
    with cd(env.site_root):
        run('%s manage.py compress --settings=%s.settings.%s' % (env.python, env.project_name, env.name))


def restart_apache():
    run('service apache2 restart')


def restart_nginx():
    run('service nginx restart')


def install():
    install_ubuntu_packages()
    checkout_repo()
    make_directories()
    install_virtualenv()
    set_owner()
    upload_apache_conf()
    upload_nginx_conf()
    restart_apache()
    restart_nginx()

def deploy():
    pull()
    upload_apache_conf()
    upload_nginx_conf()
    install_requirements()
    clean()
    compile_css()
    collect_static()
    # compress()
    restart_apache()
    restart_nginx()
