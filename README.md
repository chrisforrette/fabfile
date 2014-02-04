# fabfile

Handy Fabric tools for building environments and deploying Django projects. Uses Apache/mod_wsgi and Nginx for static file serving, Git for deployment, and follows the project structure of my `django-project-template` repo: https://github.com/chrisforrette/django-project-template

## Requirements

* Ubuntu
* Apache
* Nginx
* Python
* Pip
* Django

## Getting Started

Install this into the same directory as your Django project. Create a settings file for each environment you want to work with under the `settings` directory with a matching settings file in your Django project. For example, if your project is called 'radtown', you should create `fabfile/settings/radtown.py` and `your_django_project/settings/radtown.py`. Fill in your settings as documented below and use the Fabric environment bootstrapping command, `e`, before all of your command calls like so:

```
fab e:radtown deploy
```

## Settings

### Project-Wide

* `env.repo_url` Git repository clone URL, used for deployment.
* `env.static_dir` Path relative to the project root where static files live.
* `env.project_name` Name of the Django project, should be equal to the project directory in the root of the project.

### Environment

* `env.name` Should be the name of the environment file as well as the settings file in Django. For example if the project is called "radtown", create `settings/radtown.py`, and `my_django_project/settings/radtown.py`.
* `env.python` Python path prefix used for Python calls. This defaults to 'python' and is handy for installing virtualenv and running the Python directly from it.
* `env.url` Base URL for environment (no `http://` or `www`, see `env.www_prefix` for including `www`), used in Apache and Nginx configuration. Example: 'mysite.com'
* `env.server_ip` The IP address for this server, used in Apache and Nginx config.
* `env.apache_root` Absolute path to directory of Apache virtual hosts. Example: '/etc/apache2/sites-enabled/''
* `env.nginx_root` Absolute path to directory of Nginx virtual hosts. Example: '/etc/nginx/sites-enabled/'
* * `env.server_admin` Server admin email address used in Apache config.
* `env.repo_branch` The Git branch name to use for this environment. Example: 'master'
* `env.project_root` Absolute path to the root of the project. Git will checkout and serve the project from this location. Example: '/home/mysite.com/''
* `env.virtualenv_dir` Directory path relative to `env.project_root` where virtualenv should be installed.
* `env.www_prefix` Whether or not to prefix 'www' to `env.url`.