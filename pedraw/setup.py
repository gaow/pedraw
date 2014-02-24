# python setup.py install --prefix=/home/usr
import sys, imp, os
from distutils.core import setup
try:
   from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
   from distutils.command.build_py import build_py

from src import VERSION, NAME, LOCAL

#the files needed to run pdgr program
resources = ['pedigree.pl',
'Pedigree.pm',
'Pedigree/Node.pm',
'Pedigree/Parser.pm',
'Pedigree/Area.pm',
'Pedigree/AbortionNode.pm',
'Pedigree/Language.pm',
'Pedigree/MarriageNode.pm',
'Pedigree/PersonNode.pm',
'Pedigree/TwinsNode.pm',
'Pedigree/ChildlessNode.pm']

for item in resources:
    if not os.path.isfile(os.path.join(LOCAL, item)):
        sys.exit('Cannot find file {}'.format(os.path.join(LOCAL, item)))
setup(name = NAME,
    version = VERSION,
    description = " ... ",
    author = "...",
    packages = [NAME],
    scripts = ['src/pedraw'],
    package_dir = {NAME:'src'},
    cmdclass = {'build_py': build_py }
)
