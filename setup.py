import sys
import os

from ez_setup import use_setuptools
use_setuptools('0.6c3')

from setuptools import setup, find_packages, Extension
from distutils.sysconfig import get_python_inc
from glob import glob
import commands


dist = setup( name='shr-today',
    version='0.7.0',
    author='Lukas \'Slyon\' Märdian',
    author_email='lukasmaerdian@googlemail.com',
    description='python-edje and opimd based lock and today screen for the SHR distribution',
    url='http://wiki.github.com/slyon/today',
    download_url='git://github.com/slyon/today.git',
    license='GNU GPL',
    scripts=['shr-today'],
    data_files=[('/etc', ['data/shr-today.conf']),
        ('/usr/share/shr-today', glob('data/*/*.edj')),
        ('/usr/share/shr-today', ['data/wallpaper.png']),
        ('/etc/X11/Xsession.d/', ['data/89shr-today'])]
)

installCmd = dist.get_command_obj(command="install_data")
installdir = installCmd.install_dir
installroot = installCmd.root

if not installroot:
    installroot = ""

if installdir:
    installdir = os.path.join(os.path.sep,
        installdir.replace(installroot, ""))

