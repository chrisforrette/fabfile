import os

from fabric.api import env, cd, run
from fabric.contrib.files import exists, upload_template
from fabric.operations import require


__all__ = ['upload_apache_conf', 'upload_nginx_conf', 'install_virtualenv', 'install_requirements', \
    'pull', 'clean', 'compile_css', 'collect_static', 'compress', 'restart_apache', 'restart_nginx', \
    'deploy']

here = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(here, 'templates')
apache_template_dir = os.path.join(template_dir, 'apache')
nginx_template_dir = os.path.join(template_dir, 'nginx')


def upload_apache_conf():
    require('server_apache_root', 'site_url', 'site_root', 'project_name')
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


def pull():
    require('site_root', 'repo_url', 'repo_branch', provided_by='e')
    if not exists(env.site_root):
        with cd(os.path.dirname(env.site_root.rstrip('/'))):
            run('git clone %s %s' % (env.repo_url, os.path.basename(env.site_root.rstrip('/'))))
    
    with cd(env.site_root):
        run('git fetch')
        run('git checkout %s' % env.repo_branch)
        run('git pull origin %s' % env.repo_branch)


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


def deploy():
    pull()
    upload_apache_conf()
    upload_nginx_conf()
    install_virtualenv()
    install_requirements()
    clean()
    compile_css()
    collect_static()
    # compress()
    restart_apache()
    restart_nginx()
