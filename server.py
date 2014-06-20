from fabric.api import env, cd, run


def create_user():
    pass

def install_ubuntu_packages():
    run('apt-get update')
    run('apt-get -y install python-software-properties apache2 nginx libapache2-mod-wsgi memcached python-pip postgresql postgresql-client')
