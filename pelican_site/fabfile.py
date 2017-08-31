# from fabric.api import *
from fabric.api import local, hosts, env
import fabric.contrib.project as project
from lib import constants
import os
from datetime import datetime

HOME = os.path.expanduser('~')
today = datetime.today()


class FabConfig(object):
    deploy_path = '/tmp/ryanmoco'
    dest_path = '/var/www/ryanssite/'
    pelican = '{HOME}/.virtualenvs/blog/bin/pelican'.format(HOME=HOME)

    dropbox_path = constants.dropbox_path
    staging_path = constants.staging_path
    log_file = constants.log_file

    def asdict(self):
        print 'dict'
        return {key: getattr(self, key) for key in dir(self) if not key.startswith('__') and not callable(key)}


class iMacFabConfig(FabConfig):
    pass


class MiniFabConfig(FabConfig):
    pelican = '{HOME}/.virtualenvs/ryanmoco/bin/pelican'.format(HOME=HOME)


env.roledefs['remote'] = [constants.production_server]
env.roledefs['local'] = ['localhost']

if not env.roles:
    config = iMacFabConfig()
elif env.roles[0] == 'local':
    config = MiniFabConfig()
elif env.roles[0] == 'remote':
    config = iMacFabConfig()

env.update(**config.asdict())

DEPLOY_PATH = env.deploy_path

# Remote server configuration
production = constants.production_server
dest_path = env.dest_path
dropbox_path = env.dropbox_path


def clean():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))


def build():
    local('{pelican} -s configs/pelicanconf.py'.format(**env))


def buildprod():
    local('{pelican} -v -s configs/publishconf.py'.format(**env))


def rebuild():
    clean()
    build()


def regenerate():
    local('{pelican} -r -s configs/pelicanconf.py'.format(**env))


def serve():
    local('cd {deploy_path} && python -m SimpleHTTPServer'.format(**env))


def reserve():
    build()
    serve()


def preview():
    local('{pelican} -s configs/publishconf.py'.format(**env))


@hosts(production)
def rpublish():
    project.rsync_project(
        remote_dir=dest_path,
        exclude=[".DS_Store", "s", "ip.php", "pa", "json/top_articles.json"],
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True
    )


def lpublish():
    local('cp -r {deploy_path} {dest_path}'.format(**env))


def git():
    print "Commiting to git..."
    local("""
if git diff-index --quiet HEAD --; then
    git add --all && git commit -am "Updated blog on %s"
fi
""" % today.strftime("%Y-%m-%d %H:%M:%S"))
    print "Pushing to Github"
    local('git push origin master')


def venv(conf='configs/publishconf.py'):
    env.update({'conf': conf})
    local('{pelican} --debug -v -s {conf}>> {log_file}'.format(**env))


def publish():
    venv()
    if env.roles[0] == 'remote':
        rpublish()
    elif env.roles[0] == 'local':
        lpublish()
    else:
        print "No role found"
    # git()


def dropbox():
    venv(conf='configs/dropbox_conf.py')
    local('cp -r {deploy_path} {dropbox_path}'.format(**env))


def staging():
    venv(conf='configs/staging_conf.py')
    local('cp -r {deploy_path} {staging_path}'.format(**env))
