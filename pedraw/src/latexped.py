## $File: latexped.py $
# $LastChangedDate:  $
# $Rev:  $
# Copyright (c) 2014, Gao Wang <ewanggao@gmail.com>
# GNU General Public License (http://www.gnu.org/licenses/gpl.html)
import sys, os, subprocess, re
from shutil import copyfile
from . import env
from latexmake import LatexMaker

_TEXBGN_ = r'''
\documentclass{article}
\usepackage{ifpdf}
\ifpdf
  \usepackage{auto-pst-pdf}
\else
  \usepackage{pstricks}
\fi
\usepackage{pst-pdgr}
\usepackage[multidot]{grffile}  
\thispagestyle{empty}
\begin{document}
'''
_TEXEND_ = r'\end{document}'
# FIXME: missing data not properly handled
_SEX_ = {'1':'male', '2':'female', '0':'male'}
_CONDITION_ = {'1':'normal', '2':'affected', '0':'normal'}


class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

class PedigreeDrawer:
    def __init__(self, fname, fid):
        self.output = '{}.{}'.format(fname, fid)
        self.id = fid
        self.tmpfile = os.path.join(env.tmp_dir, self.output)
        self.input = self.tmpfile + '.txt'
        self.cfg = self.tmpfile + '.cfg'
        self.tex = self.tmpfile + '.tex'
        
    def WriteInput(self, data):
        '''convert data to pedigree.pl input'''
        def adjustPid(x, y):
            return 'F{}P{}'.format(x, y) if y != '0' else ''
        # data: dictionary with ped information and output filename
        with open (self.input, 'w') as csv_file:
            csv_file.write('Id'+'|'+'Name'+'|'+'Sex'+'|'+'Mother'+'|'+'Father'+'|'+'Condition'+'\n')
            for k in data:
                new_line = '|'.join(['F{}P{}'.format(self.id, k), k,
                                   _SEX_[data[k]['sex']],
                                   adjustPid(self.id, data[k]['motherID']),
                                   adjustPid(self.id, data[k]['fatherID']),
                                   _CONDITION_[data[k]['trait']]]) + '\n'
                csv_file.write(new_line)

    def WriteConfig(self, belowtextfont, abovetextfont,
                    descarmA, xdist, ydist, maxW, maxH, auto_rotate = True):
        '''write cfg file'''
        res = ['$fulldoc=0', '$printlegend=0', '$language="english"',
               "$belowtextfont='\\{}'".format(belowtextfont), "$abovetextfont='\\{}'".format(abovetextfont),
               '$descarmA = {}'.format(descarmA), '$xdist = {}'.format(xdist), '$ydist = {}'.format(ydist), 
               '$maxW = {}'.format(maxW), '$maxH = {}'.format(maxH),
               "$rotate = '{}'".format("maybe" if auto_rotate else "no"), "1"]
        with open(self.cfg, 'w') as f:
            f.write('\n'.join(["{};".format(x) for x in res]))

    def GenerateTex(self, start, genotypes = None, marker_names = None):
        '''perl pedigree.pl -c config.cfg -o - data.txt'''
        out, error = subprocess.Popen(
            ['perl', os.path.join(env.resource_dir, 'pedigree.pl'),
             '-c', self.cfg, '-o', '-', '-s', 'F{}P{}'.format(self.id, start), self.input],
             stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE,
             env = {'PERL5LIB': "{}:{}".format(os.path.join(env.resource_dir, 'Pedigree'), env.resource_dir),
                    'PATH':os.getenv('PATH')}).communicate()
        if sys.version_info.major == 3:
            out = out.decode(sys.getdefaultencoding())
        if genotypes is not None:
            out += '\n' + self.__TrackGenotypes(genotypes, marker_names, out)
        with open(self.tex, 'w') as f:
           f.write('\n'.join([_TEXBGN_, out, _TEXEND_]))

    def GeneratePDF(self, verbose = False):
        opts = Struct(**{'clean':False, 'verbose':verbose, 'exit_on_error':True,
                         'preview':False, 'pdf':True, 'check_cite':False})
        current_dir = os.getcwd()
        os.chdir(env.tmp_dir)
        LatexMaker(os.path.split(self.tex)[-1], opts).run()
        os.chdir(current_dir)
        copyfile(self.tmpfile + '-pics.pdf', self.output + '.pdf')

    def __TrackGenotypes(self, genotypes, marker_names, out):
        #FIXME
        return ''
