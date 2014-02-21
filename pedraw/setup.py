# $File: setup.py $
# $LastChangedDate:  $
# $Rev:  $
# Copyright (c) 2014, Gao Wang <ewanggao@gmail.com>
# GNU General Public License (http://www.gnu.org/licenses/gpl.html)

# python setup.py install
import sys, imp, os
from distutils.core import setup
try:
   from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
   from distutils.command.build_py import build_py

from src import VERSION, NAME, LOCAL

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
'Pedigree/ChildlessNode.pm',
]
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
