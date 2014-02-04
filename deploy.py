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
    require('apache_root', 'url', 'project_root', 'project_name')
    conf_path = os.path.join(env.apache_root, '%s.conf' % env.url)
    wsgi_path = os.path.join(env.project_root, 'dist/apache/%s.wsgi' % env.url)

    upload_template('django.conf', conf_path, context=env, use_jinja=True, template_dir=apache_template_dir, \
        backup=False, mode=0755)
    upload_template('django.wsgi', wsgi_path, context=env, use_jinja=True, template_dir=apache_template_dir, \
        backup=False, mode=0755)


def upload_nginx_conf():
    require('nginx_root', 'url', 'project_root', 'project_name')
    path = os.path.join(env.nginx_root, '%s.conf' % env.url)
    upload_template('django.conf', path, context=env, use_jinja=True, template_dir=nginx_template_dir, \
        backup=False, mode=0755)


def install_virtualenv():
    require('project_root', 'virtualenv_dir', provided_by='e')
    with cd(env.project_root):
        if not exists(os.path.join(env.project_root, env.virtualenv_dir)):
            run('virtualenv %s --no-site-packages' % env.virtualenv_dir)


def install_requirements():
    require('project_root', 'virtualenv_dir', provided_by='e')
    with cd(env.project_root):
        run('./%s/bin/pip install -r ./requirements.txt' % env.virtualenv_dir)


def pull():
    require('project_root', 'repo_url', 'repo_branch', provided_by='e')
    if not exists(env.project_root):
        with cd(os.path.dirname(env.project_root.rstrip('/'))):
            run('git clone %s %s' % (env.repo_url, os.path.basename(env.project_root.rstrip('/'))))
    
    with cd(env.project_root):
        run('git fetch')
        run('git checkout %s' % env.repo_branch)
        run('git pull origin %s' % env.repo_branch)


def clean():
    require('project_root', provided_by='e')
    with cd(env.project_root):
        run('find . -name \*.pyc -print -delete')


def compile_css():
    require('project_root', 'static_dir', provided_by='e')
    with cd(os.path.join(env.project_root, env.static_dir)):
        run('compass compile')


def collect_static():
    require('project_root', 'name', provided_by='e')
    with cd(env.project_root):
        run('%s manage.py collectstatic --settings=%s.settings.%s' % (env.python, env.project_name, env.name))


def compress():
    require('project_root', 'name', provided_by='e')
    with cd(env.project_root):
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
