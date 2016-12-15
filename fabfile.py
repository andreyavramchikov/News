from fabric.api import env, run
from fabric.operations import sudo

env.user = 'ubuntu'
env.hosts = [
    'ec2-54-165-162-6.compute-1.amazonaws.com'
]


env.key_filename = '/home/andrey/News.pem'
env.project_name = 'News'
env.path = '/home/ubuntu/projects/%(project_name)s' % env
env.env_path = '%(path)s/env' % env
env.repo_path = '%(path)s/repository' % env
env.supervisor_log_path = '%(path)s/repository/logs' % env


# deploy site with nginx-uwsgi conjunction
def deploy():
    clean_repositories()
    setup_directories()
    setup_virtualenv()
    clone_repo()
    install_requirements()
    # run('source %(env_path)s/bin/activate; %(env_path)s/bin/python %(repo_path)s/manage.py collectstatic' % env)
    sudo(
        'ln -s /home/ubuntu/projects/News/repository/mysite_nginx.conf /etc/nginx/sites-enabled/')
    sudo('/etc/init.d/nginx restart')
    run('source %(env_path)s/bin/activate; %(env_path)s/bin/python %(repo_path)s/manage.py migrate' % env)
    run('source %(env_path)s/bin/activate; pip install uwsgi' % env)
    run('source %(env_path)s/bin/activate; uwsgi --ini %(repo_path)s/mysite_uwsgi.ini' % env)


def clean_repositories():
    sudo('rm -rf projects')
    sudo('rm -rf /etc/nginx/sites-enabled/mysite_nginx.conf')


def install_requirements():
    """
    Install the required packages using pip.
    """
    run('source %(env_path)s/bin/activate; pip install -r %(repo_path)s/requirements.txt' % env)


def clone_repo():
    """
    Do initial clone of the git repository.
    """
    run('git clone https://github.com/andreyavramchikov/%(project_name)s.git %(repo_path)s' % env)


def setup_directories():
    """
    Create directories necessary for deployment.
    """
    run('mkdir -p %(path)s' % env)
    run('mkdir -p %(env_path)s' % env)


def activate_virtualenv():
    run('source %(env_path)s/bin/activate;' % env)


def setup_virtualenv():
    """
    Setup a fresh virtualenv.
    """
    run('virtualenv %(env_path)s --no-site-packages;' % env)
    run('source %(env_path)s/bin/activate;' % env)


def setup():
    sudo('apt-get -y update')
    sudo('apt-get -y upgrade')
    sudo('apt-get -y install python-dev')
    sudo('apt-get -y install python-virtualenv')
    sudo('apt-get -y install libmysqlclient-dev')
    sudo('apt-get install -y git')
    sudo('apt-get install -y nginx')
    sudo('apt-get install -y build-essential python')
    sudo('apt-get install -y python-dev')