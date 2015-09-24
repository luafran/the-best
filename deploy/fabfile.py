import glob

from fabenvs import *
from fabric.api import *


ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
INSTALL_DIR = "/opt/the-best"

DIST_DIR = os.path.join(ROOT_DIR, "dist")
CONTINUOUS_INTEGRATION_DIR = os.path.join(ROOT_DIR, "ci")
DEPLOY_DIR = os.path.join(ROOT_DIR, "deploy")
SYSCONFIG_DIR = os.path.join(DEPLOY_DIR, "sysconfig")


@task
def make_and_deploy():

    make_packages()
    target_roles = ['application']
    # fabric.api.execute(deploy, roles=target_roles)
    fabric.api.execute(deploy)


@task
def make_packages():

    build_packages_script = os.path.join(CONTINUOUS_INTEGRATION_DIR, "build_packages.sh")
    local('rm -rf ' + DIST_DIR)
    local(build_packages_script + ' ' + ROOT_DIR + ' 000 cdlg2015')


@task
@parallel
def deploy():

    nginx_service = 'nginx'
    supervisor_service = 'supervisor'

    with settings(warn_only=True):
        sudo('service ' + nginx_service + ' stop')
        sudo('service ' + supervisor_service + ' stop')
        sudo("pkill -f thebest-runservice")
        sudo("rm -rf " + INSTALL_DIR)
        sudo("virtualenv " + INSTALL_DIR)

    package_name = 'thebest'
    package_file_path = glob.glob(os.path.join(DIST_DIR, package_name+"*.tar.gz"))[0]
    put(package_file_path, "/tmp/")
    sudo(". " + INSTALL_DIR + "/bin/activate; " + INSTALL_DIR + "/bin/pip install " + "/tmp/" +
         os.path.basename(package_file_path))

    sudo("service supervisor start")
    sudo("service nginx start")

    print("Service(s) successfully deployed!!!")


@task
def upload_deploy_scripts(deploy_scripts_file, target_dir):

    with lcd('/tmp'):
        local('tar cvzf ' + deploy_scripts_file + ' ' + DEPLOY_DIR)
        put(deploy_scripts_file, target_dir)

@task
def install_env_stack():

    fabric.api.execute(install_app_server)
    fabric.api.execute(install_elasticsearch)


@task
@fabric.api.roles(['application'])
@parallel
def install_app_server():
    deploy_scripts_file = 'deploy.tgz'
    target_dir = '/tmp'
    upload_deploy_scripts(deploy_scripts_file, target_dir)

    with cd(target_dir):
        sudo('rm -rf deploy/')
        run('tar xvzf ' + deploy_scripts_file)
        with cd('deploy'):
            sudo('./install_appserver.sh')

@task
@fabric.api.roles(['application'])
@parallel
def install_elasticsearch():
    deploy_scripts_file = 'deploy.tgz'
    target_dir = '/tmp'
    upload_deploy_scripts(deploy_scripts_file, target_dir)

    with cd(target_dir):
        sudo('rm -rf deploy/')
        run('tar xvzf ' + deploy_scripts_file)
        with cd('deploy'):
            sudo('./install_elasticsearch.sh')


@task
@fabric.api.roles(['application'])
@parallel
def service_status():
    run('ps -ef | grep thebest-runservice')
