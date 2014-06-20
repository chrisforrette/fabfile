import os, sys
sys.path.append('{{ site_root }}')
sys.path.append('{{ site_root }}{{ project_name }}')
os.environ['DJANGO_SETTINGS_MODULE'] = '{{ project_name }}.settings.{{ name }}'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
