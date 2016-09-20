from fabric.contrib.files import append, exists, sed, cd, is_link
from fabric.api import env, local, run, put, sudo, lcd
import random
import datetime, time

# the user to use for the remote commands
env.user = 'devops'
env.password = '!D3vOps#34756'
# the servers where the commands are executed
# env.hosts = [ '211.210.89.74', '211.210.89.72' ]
env.hosts = [ '192.168.56.120' ]
env.port = 4222
env.build_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
env.build_datetime = '20160919153941'

component_name = 'mg'
dist_base_dir = '/data/brainagenet/' + component_name
dist_config_dir = ('%s/config' % dist_base_dir)
dist_deploy_dir = ('%s/deploy' % dist_base_dir)

# print ('#########################################################################')
# print ('# env.build_datetime: %s' % env.build_datetime)
# print ('# --------------------------------------------------------------------- #')
# print ('# dist_base_dir: %s' % dist_base_dir)
# print ('#   - dist_config_dir: %s' % dist_config_dir)
# print ('#   - dist_deploy_dir: %s' % dist_deploy_dir)
# print ('#########################################################################')

def create_checksum():
    print('# create checksums -----------------------------------')
    md5cmd = "md5sum"
    with lcd('./target'):
        local('%s *.war *.tar > checksums.txt' % md5cmd)

def verify_checksums(build_number):
    print('# verify checksums -----------------------------------')
    md5cmd = "md5sum"
    with cd(dist_base_dir + '/dist/' + build_number):
        result = run('%s -c checksums.txt' % md5cmd)
        if not result.return_code == 0:
            print('It\'s not matched with checksums.txt. Something wrong... bad files...')
        else:
            print('verify OK!!')

def prepare_directory_if_necessary(build_number):
    print('# prepare directory if necessary -----------------------------------')
    print('#   - build_number: %s' % build_number)
    if not exists(dist_base_dir, verbose=True):
        run('mkdir -p %s' % dist_base_dir)
        run(('chown -Rf %s:%s %s' % (env.user, env.user, dist_base_dir)))
        print ('build number: %s' % build_number)
    if not exists(dist_base_dir + '/dist/' + build_number, verbose=True):
        # run('mkdir -p %s' % dist_base_dir + '/dist/' + build_number + '/config')
        run('mkdir -p %s' % dist_base_dir + '/dist/' + build_number + '/deploy')

def dist_artifacts(build_number):
    put('./target/message-gateway.war', dist_base_dir + '/dist/' + build_number)
    put('./target/message-gateway-config.tar', dist_base_dir + '/dist/' + build_number)
    put('./target/checksums.txt', dist_base_dir + '/dist/' + build_number)

def extract_config(build_number):
    with cd(dist_base_dir + '/dist/' + build_number):
        run('tar xvf message-gateway-config.tar')

def extract_webapp(build_number):
    with cd(dist_base_dir + '/dist/' + build_number):
        run('unzip message-gateway.war -d ./deploy')

def update_symbolic_links(build_number):
    with cd(dist_base_dir):
        if is_link('config', verbose=True):
            run('unlink config')
        run('ln -s ./dist/%s/config config' % build_number)

        if is_link('deploy', verbose=True):
            run('unlink deploy')
        run('ln -s ./dist/%s/deploy deploy' % build_number)

def deploy(build_number):
    # create md5 checksums for build artifacts
    create_checksum()

    # prepare directory for dist.
    if not build_number:
        build_number = env.build_datetime
    prepare_directory_if_necessary(build_number)

    # dist artifacts
    dist_artifacts(build_number)

    # verify md5 checksum for distributed artifacts
    verify_checksums(build_number)

    # extract config
    extract_config(build_number)

    # extract war
    extract_webapp(build_number)

    # update symbolic link
    update_symbolic_links(build_number)
