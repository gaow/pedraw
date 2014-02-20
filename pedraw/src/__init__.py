import sys, os, re, tempfile
from distutils.dir_util import mkpath, remove_tree

NAME = 'pedraw'
VERSION = '0.0.1'
LOCAL = '~/{}'.format(NAME)

class Environment:
    def __init__(self):
        self.__width_cache = 1
        # About the program 
        self.proj = "Pedigree Drawing Tool"
        self.prog = NAME
        self.version = VERSION 
        # Runtime support
        self.resource_dir = os.path.expanduser(LOCAL)
        self.tmp_dir = self.__mktmpdir()
        self.debug = False

    def __mktmpdir(self):
        pattern = re.compile(r'{}_tmp_*(.*)'.format(self.prog))
        for fn in os.listdir(tempfile.gettempdir()):
            if pattern.match(fn):
                remove_tree(os.path.join(tempfile.gettempdir(), fn))
        return tempfile.mkdtemp(prefix='{}_tmp_'.format(self.prog))
            
    def error(self, msg = None, show_help = False, exit = False):
        if msg is None:
            sys.stderr.write('\n')
            return
        if type(msg) is list:
            msg = ' '.join(map(str, msg))
        else:
            msg = str(msg)
        start = '\n' if msg.startswith('\n') else ''
        end = '\n' if msg.endswith('\n') else ''
        msg = msg.strip()
        sys.stderr.write(start + "\033[1;40;33mERROR: {}\033[0m\n".format(msg) + end)
        if show_help:
            self.log("Type '{} -h' for help message".format(env.prog))
            remove_tree(self.tmp_dir)
            sys.exit()
        if exit:
            remove_tree(self.tmp_dir)
            sys.exit()
        
    def log(self, msg = None, flush=False):
        if msg is None:
            sys.stderr.write('\n')
            return
        if type(msg) is list:
            msg = ' '.join(map(str, msg))
        else:
            msg = str(msg)
        start = "{0:{width}}".format('\r', width = self.__width_cache + 10) + "\r" if flush else ''
        end = '' if flush else '\n'
        start = '\n' + start if msg.startswith('\n') else start
        end = end + '\n' if msg.endswith('\n') else end
        msg = msg.strip()
        if flush:
            self.__width_cache = len(msg)
        sys.stderr.write(start + "\033[1;40;32mMESSAGE: {}\033[0m".format(msg) + end)

env = Environment()
