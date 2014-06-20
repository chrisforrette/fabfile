import os

from fabric.api import env


# Project settings

env.project_name = ''
env.project_repo_url = ''

# Server settings

env.name = ''
env.python = 'python'
env.python_version = '2.7'
env.server_ip = ''
env.server_apache_root = '/etc/apache2/sites-enabled/'
env.server_nginx_root = '/etc/nginx/sites-enabled/'
env.server_site_root = '/opt/' # The path to where sites will be added
env.server_admin_email = 'chris@chrisforrette.com'

# Site

env.site_url = ''
env.site_root = ''
env.site_repo_branch = 'master'
env.site_virtualenv_dir = 'env'
env.site_logs_dir = 'logs'
env.site_www_prefix = False
env.site_production = False
env.site_ssl_cert_path = ''
env.site_ssl_cert_key_path = ''
env.site_gzip_enabled = True
env.site_max_upload_size = '12M'

env.site_db_name = ''
env.site_db_user = ''
env.site_db_password = ''
env.site_db_dump_dir = 'dumps'
