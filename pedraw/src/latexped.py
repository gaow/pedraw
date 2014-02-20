# $File: latexped.py $
# $LastChangedDate:  $
# $Rev:  $
# Copyright (c) 2014, Gao Wang <ewanggao@gmail.com>
# GNU General Public License (http://www.gnu.org/licenses/gpl.html)
import sys, os, subprocess, re
from . import env
from latexmake import LatexMaker

_TEXTBGN_ = '''
\usepackage{ifpdf}
\ifpdf
  \usepackage{auto-pst-pdf}
\else
  \usepackage{pstricks}
\fi
\usepackage{pst-pdgr}
\begin{document}
'''
_TEXTEND_ = "\end{document}"

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

class PedigreeDrawer:
    def __init__(self, fout):
        self.output = fout
        self.tmpfile = os.path.join(env.tmp_dir, output)
        self.input = self.tmpfile + '.txt'
        self.cfg = self.tmpfile + '.cfg'
        self.tex = self.tmpfile + '.tex'
        
    def WriteInput(self, data):
        '''convert data to pedigree.pl input'''
        # data: dictionary with ped information and output filename
        # FIXME
        with open(self.input, 'w') as f:
            f.write('\n'.join([]))

    def WriteConfig(self, belowtextfont, abovetextfont,
                    descarmA, xdist, ydist, maxW, maxH, auto_rotate):
        '''write cfg file'''
        res = ['$fulldoc=0', '$printlegend=0', '$language="english"',
               '$belowtextfont="\\{}"'.format(belowtextfont), '$abovetextfont="\\{}"'.format(abovetextfont),
               '$descarmA = {}'.format(descarmA), '$xdist = {}'.format(xdist), '$ydist = {}'.format(ydist), 
               '$maxW = {}'.format(maxW), '$maxH = {}'.format(maxH),
               '$rotate = "{}"'.format("maybe" if auto_rotate else "no"), "1;"]
        with open(self.cfg + ".cfg", 'w') as f:
            f.write('\n'.join(res))

    def GenerateTex(self, genotypes = None, marker_names = None):
        '''perl pedigree.pl -c config.cfg -o - data.txt'''
        error, out = subprocess.Popen(['perl', os.path.join(env.resource_dir, 'pedigree.pl'),
                                       '-c', self.cfg, '-o', '-', self.input],
                                       stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE,
                                       env = {'PERL5LIB': os.path.join(env.resource_dir, 'Pedigree')}).communicate()
        if sys.version_info.major == 3:
            out = out.decode(sys.getdefaultencoding())
        if genotypes is not None:
            out += '\n' + self.__TrackGenotypes(genotypes, marker_names, out)
        with open(self.tex, 'w') as f:
           f.write('\n'.join(_TEXBGN_, out, _TEXEND_))

    def GeneratePDF(self, verbose = False):
        opts = Struct(**{'clean':True, 'verbose':verbose, 'exit_on_error':True,
                         'preview':False, 'pdf':True, 'check_cite':False})
        LatexMaker(self.tex, opts).run()

    def __TrackGenotypes(self, genotypes, marker_names, out):
        #FIXME
        return ''
