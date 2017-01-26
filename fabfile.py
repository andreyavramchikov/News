from fabric.api import run, env, local, sudo, prefix
from contextlib import contextmanager


def live():
    env.hosts = ['54.202.179.222']
    env.user = 'ubuntu'
    env.cwd = '/var/www/project/buildout'
    env.project = 'News'


def deploy():
    # sudo("git pull")
    pass


def initial():
    # setup_directories()
    # run("git pull")
    # clone_repo()
    # install_virtualenv()
    # install_requirements()
    # create_nginx_config_symblink()
    activate_uwsgi_ini()


def create_nginx_config_symblink():
    sudo('ln -s %s/%s/mysite_nginx.conf /etc/nginx/sites-enabled/' %(env.cwd, env.project))


def activate_uwsgi_ini():
    sudo('uwsgi --ini %s/%s/mysite_uwsgi.ini' % (env.cwd, env.project))

# not working
def setup_directories():
    sudo('mkdir %s' % env.cwd)


def clone_repo():
    sudo('git clone https://github.com/andreyavramchikov/News.git')


@contextmanager
def source_env():
    """Actives embedded virtual env"""
    with prefix('source env/bin/activate'):
        yield


def install_requirements():
    """Installs requirements.txt packages using pip"""
    with source_env():
        sudo('pip install -r News/requirements.txt')


def install_virtualenv():
    """
    Setup a fresh virtualenv.
    """
    sudo('virtualenv %s/env --no-site-packages;' % env.cwd)


def setup():
    sudo('apt-get -y update')
    sudo('apt-get -y upgrade')
    sudo('apt-get -y install python-dev')
    sudo('apt-get -y install python-virtualenv')
    sudo('apt-get -y install libmysqlclient-dev')
    sudo('apt-get install -y git')
    sudo('apt-get install -y nginx')
    sudo('apt-get install -y build-essential python')
    sudo('apt install -y uwsgi')