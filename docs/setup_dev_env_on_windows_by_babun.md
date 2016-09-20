## Overviwe

적은 인력이 많은 서버를 관리하기 위해서는 자동화가 필수이다. 다양한 DevOps Tools 이 존재하는데 대표적인 것들을 아래에 소개한다.

  * Puppet - Agent
  * Chef - Agent
  * Ansible - Agentless
  * Fabric - Agentless

위의 툴들을 분류하면 Agent 방식인가 그렇지 않은가로 구분할 수 있다. Agent 방식은 관리할 서버에 해당 툴의 Agent를 설치하여야 한다는 뜻이다. 반대로 Agentless는 관리할 서버에 어떠한 Agent도 설치하지 않아도 된다는 말이다.

여기에서는 Agentless인 Ansible과 Fabric을 사용하여 구성해 보도록 하겠다.

## Environment

Java 기반의 Web Application의 경우, OS Independent 하다고 말을 많이 하지만 그래도 대부분 Linux 기반에서 서비스를 운영하는 경우가 많다. 물론 현재 몇 몇 업체는 Windows 기반의 서버를 제공해 주어서 자동화의 걸림돌이 되고 있다. 이런 것들은 수동으로 한다고 생각하면 된다. 논외로 하자.

여기서 선택한 Ansible과 Fabric은 관리대상 서버에 SSH와 Python만 설치되어 있으면 된다. 대부분의 서버가 SSH로 접근할 수 있고, Linux 배포판의 경우 기본적으로 Python은 설치되어 있다. 그렇다면 관리하는 관리자의 컴퓨터도 Linux 또는 Mac 기반이어야 하는 것이 아닐까?

다행히 Windows에서 Linux 명령어를 사용할 수 있게 해 주는 Cygwin 이라는 툴이 있고 이것에 패키지 관리툴 등을 추가한 Babun이 있다. 여기서는 다음과 같은 구성으로 테스트를 진행하겠다.

Babun + VCS(git or svn) + Ansible or Fabric + Linux (Ubuntu or CentOs on VitualBox)

그럼 환경구성을 진행해 보자.

### Babun

[Homepage](http://babun.github.io/)에서 [다운로드](http://projects.reficio.org/babun/download) 받은 후, 압축을 풀고 Windows의 명령 프롬프트에서 `install.bat`를 실행시키면 된다.

```bat
> cd c:\tmp\babun-1.2.0
> install.bat
```

설치가 완료되면 Windows 바탕화면에 단축아이콘을 생성하고 Babun 창이 자동으로 열립니다.

> 참고로 Babun은 bash가 아닌 zsh가 기본 Shell입니다. 거기에 oh-my-zsh가 적용되어 있습니다.

```sh
Executing daily babun check:
Source consistent [OK]
Prompt speed      [OK]
File permissions  [OK]
Connection check  [OK]
Update check      [OK]
Cygwin check      [OK]
Welcome to babun - the Windows shell you will love!
You have got a lot of things under the hood here!

   pact -> a package manager that handles installation of babun packages
      pact install tar -> will install tar package on your system
      pact remove tar -> will remove tar package from your system

   babun -> a script that manages babun and enables auto-update
      babun check -> will check the configuration (proxy, connection, etc)
      babun update -> will update babun to the newest version
      babun --welcome -> will display this message again

There is a couple of plugins installed by default: oh-my-zsh, pact, cacert, etc.
There is also a lot of dev tools such as git, svn, unix utils, etc
If you would like to contribute, code up a plugin or report an issue just
go to github: https://github.com/babun/babun

If you like the project star it on github and follow me on twitter!
This project is created and maintained by Tom Bujok (@tombujok)

{ ~ }  »                                
```

#### oh-my-zsh theme 바꾸기

Babun은 zsh shell에 oh-my-zsh 가 기본으로 설치되어 있어서 기존에 보던 bash shell과는 전혀 다른 모습입니다. plugin에 따른 shell의 모양이 변경되거나 정보가 추가적으로 나오는 것이 oh-my-zsh의 특징입니다. 그래서 최근 많은 사랑을 받고 있습니다.

기본 theme 를 아래의 theme로 변경하도록 하겠습니다.

![lambda-mod-zsh-theme screenshot](https://raw.githubusercontent.com/halfo/lambda-mod-zsh-theme/master/screenshot.png)

```sh
$ cd ~/.oh-my-zsh/themes
$ wget https://raw.githubusercontent.com/halfo/lambda-mod-zsh-theme/master/lambda-mod.zsh-theme
$ chmod a+x lambda-mod.zsh-theme
$ vi ~/.zshrc
ZSH_THEME="lambda-mod"
$ source ~/.zshrc
```

#### font 바꾸기

글꼴도 변경가능합니다. 여기서는 Naver의 D2Coding으로 변경하도록 하겠습니다.

> Naver의 D2Coding은 이미 설치가 되어 있어야 합니다. 이전 Section의 이미지와 같이 꾸미고 싶은 경우, `c:\Users\${USER_NAME}\.babun\fonts`에 있는 `RegisterFont.exe`를 실행시키면 됩니다. 그러면 다음의 글꼴이 설치가 됩니다.
> * Menlo Bold for Powerline.ttf
> * Menlo Bold Italic for Powerline.ttf
> * Menlo Italic for Powerline.ttf
> * Menlo Regular for Powerline.ttf

```sh
$ vi ~/.minttyrc
Font=D2Coding
# Font=Menlo Bold for Powerline
$ source ~/.zshrc
```

#### update packages

우리는 자동화 환경을 구성하기 위해서 svn 또는 git를 사용하기로 하였습니다. 따라서 Babun에서 svn 또는 git 명령어를 수행할 수 있어야 합니다. 아래의 명령어로 svn과 git의 Version을 확인해 보도록 하겠습니다.

```sh
$ svn --version
svn, version 1.8.11 (r1643975)
   compiled Dec 20 2014, 08:56:57 on i686-pc-cygwin

Copyright (C) 2014 The Apache Software Foundation.
This software consists of contributions made by many people;
see the NOTICE file for more information.
Subversion is open source software, see http://subversion.apache.org/

The following repository access (RA) modules are available:

* ra_svn : Module for accessing a repository using the svn network protocol.
  - with Cyrus SASL authentication
  - handles 'svn' scheme
* ra_local : Module for accessing a repository on local disk.
  - handles 'file' scheme
* ra_serf : Module for accessing a repository via WebDAV protocol using serf.
  - using serf 1.3.8
  - handles 'http' scheme
  - handles 'https' scheme

$ git --version
git version 2.1.4

```

Babun에 설치되어 있는 svn과 git의 Version을 확인해 보았습니다. 이제 Babun의 `pact`라는 Package Manager를 사용하여 git를 update해 보도록 하겠습니다.

> svn은 update가 되지 않아서 하지 않습니다.

```sh
$ pact update git
Removing git
Package git removed
Working directory is /setup
Mirror is http://mirrors.kernel.org/sourceware/cygwin/
--2016-08-16 14:54:18--  http://mirrors.kernel.org/sourceware/cygwin//x86/setup.bz2
Resolving mirrors.kernel.org (mirrors.kernel.org)... 149.20.37.36, 198.145.20.143, 2001:4f8:4:6f:0:1994:3:14, ...
Connecting to mirrors.kernel.org (mirrors.kernel.org)|149.20.37.36|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2276287 (2.2M) [application/octet-stream]
Saving to: ‘setup.bz2’

setup.bz2                100%[====================================>]   2.17M   389KB/s   in 6.0s

2016-08-16 14:54:24 (369 KB/s) - ‘setup.bz2’ saved [2276287/2276287]

Updated setup.ini

Installing git
Found package git
--2016-08-16 14:54:25--  http://mirrors.kernel.org/sourceware/cygwin//x86/release/git/git-2.8.3-1.tar.xz
Resolving mirrors.kernel.org (mirrors.kernel.org)... 149.20.37.36, 198.145.20.143, 2001:4f8:4:6f:0:1994:3:14, ...
Connecting to mirrors.kernel.org (mirrors.kernel.org)|149.20.37.36|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 4998940 (4.8M) [application/octet-stream]
Saving to: ‘git-2.8.3-1.tar.xz’

git-2.8.3-1.tar.xz       100%[====================================>]   4.77M  2.32MB/s   in 2.1s

2016-08-16 14:54:28 (2.32 MB/s) - ‘git-2.8.3-1.tar.xz’ saved [4998940/4998940]

Unpacking...
Package git requires the following packages, installing:
bash cygutils cygwin less libcurl4 libexpat1 libgcc1 libiconv2 libintl8 libopenssl100 libpcre1 openssh perl-Carp perl-Error perl-TermReadKey perl_base python rsync zlib0
Package bash is already installed, skipping
Package cygutils is already installed, skipping
Package cygwin is already installed, skipping
Package less is already installed, skipping
Package libcurl4 is already installed, skipping
Package libexpat1 is already installed, skipping
Package libgcc1 is already installed, skipping
Package libiconv2 is already installed, skipping
Package libintl8 is already installed, skipping
Package libopenssl100 is already installed, skipping
Package libpcre1 is already installed, skipping
Package openssh is already installed, skipping
Package perl-Carp is already installed, skipping
Package perl-Error is already installed, skipping
Package perl-TermReadKey is already installed, skipping
Package perl_base is already installed, skipping
Package python is already installed, skipping
Package rsync is already installed, skipping
Package zlib0 is already installed, skipping
Package git installed

$ git --version
git version 2.8.3

```

#### Python 환경 구성

Ansible과 Fabric을 사용하기 위해서는 Python 환경이 구성되어야 합니다. Babun의 Package Manager 명령어인 `pact`를 사용하여 다음과 같이 설치합니다.

```sh
$ pact install python python-paramiko python-crypto gcc-g++ wget openssh python-setuptools
Working directory is /setup
Mirror is http://mirrors.kernel.org/sourceware/cygwin/
setup.ini taken from the cache
Package python is already installed, skipping

Installing python-paramiko
Found package python-paramiko
--2016-08-16 14:59:11--  http://mirrors.kernel.org/sourceware/cygwin//x86/release/python-paramiko/python-paramiko-1.15.2+20150204+gitbdc60c3-2.tar.xz
Resolving mirrors.kernel.org (mirrors.kernel.org)... 149.20.37.36, 198.145.20.143, 2001:4f8:4:6f:0:1994:3:14, ...
Connecting to mirrors.kernel.org (mirrors.kernel.org)|149.20.37.36|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 592688 (579K) [application/octet-stream]
Saving to: ‘python-paramiko-1.15.2+20150204+gitbdc60c3-2.tar.xz’

python-paramiko-1.15.2+2 100%[====================================>] 578.80K   340KB/s   in 1.7s

2016-08-16 14:59:13 (340 KB/s) - ‘python-paramiko-1.15.2+20150204+gitbdc60c3-2.tar.xz’ saved [592688/592688]

Unpacking...
Package python-paramiko requires the following packages, installing:
cygwin python python-crypto
Package cygwin is already installed, skipping
Package python is already installed, skipping
Working directory is /setup
Mirror is http://mirrors.kernel.org/sourceware/cygwin/

Installing python-crypto
Found package python-crypto
--2016-08-16 14:59:16--  http://mirrors.kernel.org/sourceware/cygwin//x86/release/python-crypto/python-crypto-2.6-3.tar.bz2
Resolving mirrors.kernel.org (mirrors.kernel.org)... 149.20.37.36, 198.145.20.143, 2001:4f8:4:6f:0:1994:3:14, ...
Connecting to mirrors.kernel.org (mirrors.kernel.org)|149.20.37.36|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 462958 (452K) [application/octet-stream]
Saving to: ‘python-crypto-2.6-3.tar.bz2’

python-crypto-2.6-3.tar. 100%[====================================>] 452.11K   347KB/s   in 1.3s

2016-08-16 14:59:17 (347 KB/s) - ‘python-crypto-2.6-3.tar.bz2’ saved [462958/462958]

Unpacking...
Package python-crypto requires the following packages, installing:
cygwin python
Package cygwin is already installed, skipping
Package python is already installed, skipping
Package python-crypto installed
Package python-paramiko installed
Package python-crypto is already installed, skipping

Installing gcc-g++
Found package gcc-g++
--2016-08-16 14:59:19--  http://mirrors.kernel.org/sourceware/cygwin//x86/release/gcc/gcc-g++/gcc-g++-5.4.0-1.tar.xz
Resolving mirrors.kernel.org (mirrors.kernel.org)... 149.20.37.36, 198.145.20.143, 2001:4f8:4:6f:0:1994:3:14, ...
Connecting to mirrors.kernel.org (mirrors.kernel.org)|149.20.37.36|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 9372224 (8.9M) [application/octet-stream]
Saving to: ‘gcc-g++-5.4.0-1.tar.xz’

gcc-g++-5.4.0-1.tar..xz   100%[====================================>]   8.94M   381KB/s   in 25s

2016-08-16 14:59:44 (372 KB/s) - ‘gcc-g++-5.4.0-1.tar.xz’ saved [9372224/9372224]

Unpacking...
Package gcc-g++ requires the following packages, installing:
cygwin gcc-core libgmp10 libiconv2 libintl8 libisl13 libmpc3 libmpfr4 libstdc++6 zlib0
Package cygwin is already installed, skipping
Package gcc-core is already installed, skipping
Package libgmp10 is already installed, skipping
Package libiconv2 is already installed, skipping
Package libintl8 is already installed, skipping
Working directory is /setup
Mirror is http://mirrors.kernel.org/sourceware/cygwin/

Installing libisl13
Found package libisl13
--2016-08-16 14:59:50--  http://mirrors.kernel.org/sourceware/cygwin//x86/release/isl/libisl13/libisl13-0.14.1-1.tar.xz
Resolving mirrors.kernel.org (mirrors.kernel.org)... 149.20.37.36, 198.145.20.143, 2001:4f8:4:6f:0:1994:3:14, ...
Connecting to mirrors.kernel.org (mirrors.kernel.org)|149.20.37.36|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 390024 (381K) [application/octet-stream]
Saving to: ‘libisl13-0.14.1-1.tar.xz’

libisl13-0.14.1-1.tar.xz 100%[====================================>] 380.88K   334KB/s   in 1.1s

2016-08-16 14:59:52 (334 KB/s) - ‘libisl13-0.14.1-1.tar.xz’ saved [390024/390024]

Unpacking...
Package libisl13 requires the following packages, installing:
cygwin libgmp10
Package cygwin is already installed, skipping
Package libgmp10 is already installed, skipping
Package libisl13 installed
Package libmpc3 is already installed, skipping
Package libmpfr4 is already installed, skipping
Package libstdc++6 is already installed, skipping
Package zlib0 is already installed, skipping
Package gcc-g++ installed
Package wget is already installed, skipping
Package openssh is already installed, skipping

Installing python-setuptools
Found package python-setuptools
--2016-08-16 14:59:53--  http://mirrors.kernel.org/sourceware/cygwin//noarch/release/python-setuptools/python-setuptools-15.2-1.tar.xz
Resolving mirrors.kernel.org (mirrors.kernel.org)... 149.20.37.36, 198.145.20.143, 2001:4f8:4:6f:0:1994:3:14, ...
Connecting to mirrors.kernel.org (mirrors.kernel.org)|149.20.37.36|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 321956 (314K) [application/octet-stream]
Saving to: ‘python-setuptools-15.2-1.tar.xz’

python-setuptools-15.2-1 100%[====================================>] 314.41K   323KB/s   in 1.0s

2016-08-16 14:59:55 (323 KB/s) - ‘python-setuptools-15.2-1.tar.xz’ saved [321956/321956]

Unpacking...
Package python-setuptools requires the following packages, installing:
cygwin python
Package cygwin is already installed, skipping
Package python is already installed, skipping
Package python-setuptools installed

$ python -V
Python 2.7.8

```

이제 Python의 Package를 설치할 수 있게 해주는 `pip`를 설치해 줍니다. 아래의 명령어를 실행시키면 됩니다.

```sh
$ python /usr/lib/python2.7/site-packages/easy_install.py pip
Searching for pip
Reading https://pypi.python.org/simple/pip/
Best match: pip 8.1.2
Downloading https://pypi.python.org/packages/e7/a8/7556133689add8d1a54c0b14aeff0acb03c64707ce100ecd53934da1aa13/pip-8.1.2.tar.gz#md5=87083c0b9867963b29f7aba3613e8f4a
Processing pip-8.1.2.tar.gz
Writing /tmp/easy_install-9wgGSm/pip-8.1.2/setup.cfg
Running pip-8.1.2/setup.py -q bdist_egg --dist-dir /tmp/easy_install-9wgGSm/pip-8.1.2/egg-dist-tmp-_Z6cWw
warning: no previously-included files found matching '.coveragerc'
warning: no previously-included files found matching '.mailmap'
warning: no previously-included files found matching '.travis.yml'
warning: no previously-included files found matching '.landscape.yml'
warning: no previously-included files found matching 'pip/_vendor/Makefile'
warning: no previously-included files found matching 'tox.ini'
warning: no previously-included files found matching 'dev-requirements.txt'
warning: no previously-included files found matching 'appveyor.yml'
no previously-included directories found matching '.github'
no previously-included directories found matching '.travis'
no previously-included directories found matching 'docs/_build'
no previously-included directories found matching 'contrib'
no previously-included directories found matching 'tasks'
no previously-included directories found matching 'tests'
creating /usr/lib/python2.7/site-packages/pip-8.1.2-py2.7.egg
Extracting pip-8.1.2-py2.7.egg to /usr/lib/python2.7/site-packages
Adding pip 8.1.2 to easy-install.pth file
Installing pip script to /usr/bin
Installing pip2.7 script to /usr/bin
Installing pip2 script to /usr/bin

Installed /usr/lib/python2.7/site-packages/pip-8.1.2-py2.7.egg
Processing dependencies for pip
Finished processing dependencies for pip

```

#### install Ansible

위에서 우리는 `pip`를 설치했습니다. 가볍게 아래의 명령어를 실행시킵니다.

```sh
$ pip install ansible
Collecting ansible
/usr/lib/python2.7/site-packages/pip-8.1.2-py2.7.egg/pip/_vendor/requests/packages/urllib3/util/ssl_.py:318: SNIMissingWarning: An HTTPS request has been made, but the SNI (Subject Name Indication) extension to TLS is not available on this platform. This may cause the server to present an incorrect TLS certificate, which can cause validation failures. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#snimissingwarning.
  SNIMissingWarning
/usr/lib/python2.7/site-packages/pip-8.1.2-py2.7.egg/pip/_vendor/requests/packages/urllib3/util/ssl_.py:122: InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning.
  InsecurePlatformWarning
  Downloading ansible-2.1.1.0.tar.gz (1.9MB)
    100% |████████████████████████████████| 1.9MB 315kB/s
Requirement already satisfied (use --upgrade to upgrade): paramiko in /usr/lib/python2.7/site-packages/paramiko-1.15.2-py2.7.egg (from ansible)
Collecting jinja2 (from ansible)
  Downloading Jinja2-2.8-py2.py3-none-any.whl (263kB)
    100% |████████████████████████████████| 266kB 660kB/s
Collecting PyYAML (from ansible)
  Downloading PyYAML-3.11.zip (371kB)
    100% |████████████████████████████████| 378kB 815kB/s
Requirement already satisfied (use --upgrade to upgrade): setuptools in /usr/lib/python2.7/site-packages (from ansible)
Requirement already satisfied (use --upgrade to upgrade): pycrypto>=2.6 in /usr/lib/python2.7/site-packages/pycrypto-2.6.1-py2.7-cygwin-1.7.34-i686.egg (from ansible)
Requirement already satisfied (use --upgrade to upgrade): ecdsa>=0.11 in /usr/lib/python2.7/site-packages/ecdsa-0.13-py2.7.egg (from paramiko->ansible)
Collecting MarkupSafe (from jinja2->ansible)
  Downloading MarkupSafe-0.23.tar.gz
Installing collected packages: MarkupSafe, jinja2, PyYAML, ansible
  Running setup.py install for MarkupSafe ... done
  Running setup.py install for PyYAML ... done
  Running setup.py install for ansible ... done
Successfully installed MarkupSafe-0.23 PyYAML-3.11 ansible-2.1.1.0 jinja2-2.8
/usr/lib/python2.7/site-packages/pip-8.1.2-py2.7.egg/pip/_vendor/requests/packages/urllib3/util/ssl_.py:122: InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning.
  InsecurePlatformWarning

```

이로서 Ansible의 설치가 완료되었습니다.

#### install Fabric

이제 Fabric을 설치해 보도록 하겠습니다. 이것도 마찬가지로 `pip` 명령어를 사용하여 간단하게 설치할 수 있습니다.

```sh
$ pip install fabric
Collecting fabric
/usr/lib/python2.7/site-packages/pip-8.1.2-py2.7.egg/pip/_vendor/requests/packages/urllib3/util/ssl_.py:318: SNIMissingWarning: An HTTPS request has been made, but the SNI (Subject Name Indication) extension to TLS is not available on this platform. This may cause the server to present an incorrect TLS certificate, which can cause validation failures. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#snimissingwarning.
  SNIMissingWarning
/usr/lib/python2.7/site-packages/pip-8.1.2-py2.7.egg/pip/_vendor/requests/packages/urllib3/util/ssl_.py:122: InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning.
  InsecurePlatformWarning
  Downloading Fabric-1.12.0-py2-none-any.whl (92kB)
    100% |████████████████████████████████| 102kB 524kB/s
Requirement already satisfied (use --upgrade to upgrade): paramiko<2.0,>=1.10 in /usr/lib/python2.7/site-packages/paramiko-1.15.2-py2.7.egg (from fabric)
Requirement already satisfied (use --upgrade to upgrade): pycrypto!=2.4,>=2.1 in /usr/lib/python2.7/site-packages/pycrypto-2.6.1-py2.7-cygwin-1.7.34-i686.egg (from paramiko<2.0,>=1.10->fabric)
Requirement already satisfied (use --upgrade to upgrade): ecdsa>=0.11 in /usr/lib/python2.7/site-packages/ecdsa-0.13-py2.7.egg (from paramiko<2.0,>=1.10->fabric)
Installing collected packages: fabric
Successfully installed fabric-1.12.0

```

Fabric Homepage의 [설치 문서](http://www.fabfile.org/installing.html)를 살펴보면, 경우에 따라 몇 가지 library가 추가로 필요할 수 있음을 설명하고 있습니다. `pip show` 명령어를 통해 확인해 보고 필요하다면 추가로 설치를 하도록 하겠습니다.

* 만일 Paramiko 1.12 이상을 사용하고 있다면 추가로 [ecdsa](https://pypi.python.org/pypi/ecdsa/) library를 추가로 설치
* 병렬 실행 모드(Parallel Execution Mode)를 사용하려면 [multiprocessing]() library를 설치

```sh
$ pip show paramiko
---
Metadata-Version: 1.1
Name: paramiko
Version: 1.15.2
Summary: SSH2 protocol library
Home-page: https://github.com/paramiko/paramiko/
Author: Jeff Forcier
Author-email: jeff@bitprophet.org
License: LGPL
Location: /usr/lib/python2.7/site-packages/paramiko-1.15.2-py2.7.egg
Requires: pycrypto, ecdsa
Classifiers:
  Development Status :: 5 - Production/Stable
  Intended Audience :: Developers
  License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
  Operating System :: OS Independent
  Topic :: Internet
  Topic :: Security :: Cryptography
  Programming Language :: Python
  Programming Language :: Python :: 2
  Programming Language :: Python :: 2.6
  Programming Language :: Python :: 2.7
  Programming Language :: Python :: 3
  Programming Language :: Python :: 3.2
  Programming Language :: Python :: 3.3
  Programming Language :: Python :: 3.4

$ pip show ecdsa
---
Metadata-Version: 1.1
Name: ecdsa
Version: 0.13
Summary: ECDSA cryptographic signature library (pure python)
Home-page: http://github.com/warner/python-ecdsa
Author: Brian Warner
Author-email: warner-pyecdsa@lothar.com
License: MIT
Location: /usr/lib/python2.7/site-packages/ecdsa-0.13-py2.7.egg
Requires:
Classifiers:
  Programming Language :: Python
  Programming Language :: Python :: 2
  Programming Language :: Python :: 2.6
  Programming Language :: Python :: 2.7
  Programming Language :: Python :: 3
  Programming Language :: Python :: 3.2
  Programming Language :: Python :: 3.3
  Programming Language :: Python :: 3.4

$ pip show multiprocessing

$ pip install multiprocessing
Collecting multiprocessing
/usr/lib/python2.7/site-packages/pip-8.1.2-py2.7.egg/pip/_vendor/requests/packages/urllib3/util/ssl_.py:318: SNIMissingWarning: An HTTPS request has been made, but the SNI (Subject Name Indication) extension to TLS is not available on this platform. This may cause the server to present an incorrect TLS certificate, which can cause validation failures. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#snimissingwarning.
  SNIMissingWarning
/usr/lib/python2.7/site-packages/pip-8.1.2-py2.7.egg/pip/_vendor/requests/packages/urllib3/util/ssl_.py:122: InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning.
  InsecurePlatformWarning
  Downloading multiprocessing-2.6.2.1.tar.gz (108kB)
    100% |████████████████████████████████| 112kB 350kB/s
Installing collected packages: multiprocessing
  Running setup.py install for multiprocessing ... done
Successfully installed multiprocessing-2.6.2.1

```

위의 명령어 실행 결과를 보듯이 Paramiko Version이 1.15.2이고 Ecdsa는 이미 설치되어 있고 Version은 0.13인 것을 확인할 수 있습니다. 병렬 실행 모드를 위한 `multiprocessing` library는 설치가 되어 있지 않았고 그래서 추가로 설치하였습니다.

이로서 Babun을 설치하고 git와 svn을 사용할 수 있는 환경을 구성하고, ansible과 fabric을 설치하여 준비를 완료하였습니다. 이제 VCS를 관리할 수 있는 툴을 설치해 보도록 하겠습니다.