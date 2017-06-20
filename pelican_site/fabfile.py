# from fabric.api import *
from fabric.api import local, hosts, env
import fabric.contrib.project as project
from lib import constants
import os
from datetime import datetime

today = datetime.today()

HOME = os.path.expanduser('~')
# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = '/tmp/ryanmoco/'
env.HOME = HOME

env.dest_path = '/var/www/ryanssite/'
env.dropbox_path = constants.dropbox_path
env.staging_path = constants.staging_path
env.log_file = constants.log_file

env.roledefs['remote'] = [constants.production_server]
env.roledefs['local'] = ['localhost']

if os.path.exists('{HOME}/.virtualenvs/blog/bin/pelican'.format(**env)):
    env.pelican = '{HOME}/.virtualenvs/blog/bin/pelican'.format(**env)
else:
    env.pelican = '{HOME}/dev/pelican/bin/pelican'.format(**env)

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
