from fabric.contrib.files import append, exists, sed, cd
from fabric.api import env, local, run, put, sudo
import random

# the user to use for the remote commands
env.user = 'ubuntu'
env.password = '!ubuntu#12'
# the servers where the commands are executed
env.hosts = [ '192.168.56.110' ]
env.port = 4222

remote_path = '/usr/java'
bin_filename = 'jdk-8u102-linux-x64.tar.gz'
# remote_path = env.remote_path
# bin_filename = env.bin_filename

def prepare_directory_if_necessary():
    if not exists(remote_path, verbose=True):
        sudo('mkdir -p %s' % remote_path)

def deploy():
    # prepare directory for jdk
    prepare_directory_if_necessary()
    
    if not exists('%s/%s' % (remote_path, bin_filename), verbose=False):
        # put binary file to remote_path
        print 'put %s to %s' % (bin_filename, remote_path)
        put(bin_filename, remote_path, use_sudo=True)

    print 'extract jdk-8u102-linux-x64.tar.gz'
    with cd(remote_path):
        sudo('tar xvzf jdk-8u102-linux-x64.tar.gz')
        if exists('jdk1.8.0', verbose=True):
            print 'symbolic link exists for jdk1.8.0 so unlink that'
            sudo('unlink jdk1.8.0')
        sudo ('ln -s ./jdk1.8.0_102 jdk1.8.0')
        sudo('rm -rfv jdk-8u102-linux-x64.tar.gz')

    print 'check java version that was installed...'
    with cd('%s/%s' % (remote_path, 'jdk1.8.0/bin')):
        run('./java -version')
