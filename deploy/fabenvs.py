import fabric.api
import os

HOME = os.getenv('HOME')

BASTION_IP = ''


@fabric.api.task
def local_env():
    fabric.api.env.env_name = 'local'
    # Don't use same host in multiples roles since fabfile _get_current_role will get confused!
    # This should be fixed
    fabric.api.env.roledefs = {
        'application': {
            'hosts': ['127.0.0.1'],
            'service_name': 'service1',
            'packages_to_install': ['thebest']
        },
        'db_elasticsearch': {
            'hosts': ['127.0.0.1'],
            'service_name': '',
            'packages_to_install': []
        },
    }

    # fabric.api.env.gateway = 'ubuntu@' + BASTION_IP
    fabric.api.env.user = "ubuntu"
    fabric.api.env.iptables_file = None


@fabric.api.task
def dev():
    fabric.api.env.env_name = 'dev'
    # Don't use same host in multiples roles since fabfile _get_current_role will get confused!
    # This should be fixed
    fabric.api.env.roledefs = {
        'application': {
            'hosts': ['52.88.14.176'],
            'service_name': 'service1',
            'packages_to_install': ['thebest']
        },
        'db_elasticsearch': {
            'hosts': ['52.88.14.176'],
            'service_name': '',
            'packages_to_install': []
        },
    }

    # fabric.api.env.gateway = 'ubuntu@' + BASTION_IP
    fabric.api.env.user = "ubuntu"
    fabric.api.env.iptables_file = None
