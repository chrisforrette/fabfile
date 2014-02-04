import os

from fabric.api import env


# Project settings

env.python = 'python'
env.project_name = ''
env.repo_url = ''
env.static_dir = os.path.join(env.project_name, 'static')

# Environment settings

env.python = 'python'
# env.name = ''
# env.url = ''
# env.project_root = ''
env.repo_branch = 'master'
env.server_ip = ''
env.apache_root = '/etc/apache2/sites-enabled/'
env.nginx_root = '/etc/nginx/sites-enabled/'
env.virtualenv_dir = 'env'
env.www_prefix = False
env.production = False
env.server_admin = 'chris@chrisforrette.com'
