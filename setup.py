import sys
import os

from ez_setup import use_setuptools
use_setuptools('0.6c3')

from setuptools import setup, find_packages, Extension
from distutils.sysconfig import get_python_inc
from glob import glob
import commands


dist = setup( name='shr-today',
    version='0.0.1',
    author='Slyon',
    author_email='lukasmaerdian@googlemail.com',
    description='python-elementary and opimd based lock and today screen for the SHR distribution',
    url='http://wiki.github.com/slyon/today',
    download_url='git://github.com/slyon/today.git',
    license='GNU GPL',
    scripts=['shr-today'],
    data_files=[('/etc', ['data/shr-today.conf']),
        ('/usr/share/shr-today', ['data/wallpaper.png'])]
)

installCmd = dist.get_command_obj(command="install_data")
installdir = installCmd.install_dir
installroot = installCmd.root

if not installroot:
    installroot = ""

if installdir:
    installdir = os.path.join(os.path.sep,
        installdir.replace(installroot, ""))

