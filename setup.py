# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from distutils.command.build import build as _build
from distutils.command.clean import clean as _clean
import os

class my_build(_build):
    def run(self):
        _build.run(self)

        # compile theme files
        import subprocess
        result = subprocess.call( "cd ./data/slider; edje_cc -v slider.edc; mv slider.edj ../", shell=True )
        if result != 0:
            raise Exception( "Can't build theme files. Built edje_cc?" )

class my_clean(_clean):
    def run(self):
        _clean.run(self)

        if os.path.exists('./data/slider.edj'):
            os.remove('./data/slider.edj')

setup(
    name = "shr-today",
    version = "0.7.0+git",
    author = "Lukas 'Slyon' Märdian",
    author_email = "lukasmaerdian@googlemail.com",
    url = "http://wiki.github.com/slyon/today",
    cmdclass = { 'build'    : my_build ,
                 'clean'    : my_clean },
    scripts = [ "shr-today" ],
    data_files = [
        ( "/etc", ["data/shr-today.conf"] ),
        ( "/usr/share/shr-today", ["data/wallpaper.png", "data/slider.edj"] ),
        ( "/etc/X11/Xsession.d", ["data/89shr-today", "data/slider.edj"] ),
        ]
)
