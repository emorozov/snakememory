#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@+leo-ver=4-thin
#@+node:eugene.20041116201512.1:@thin install.py
#@@first
#@@first
#@@language python
#@<< install declarations >>
#@+node:eugene.20041116201512.2:<< install declarations >>
import os
import glob
import shutil
#@nonl
#@-node:eugene.20041116201512.2:<< install declarations >>
#@nl
#@+others
#@+node:eugene.20041116201812:compile_translations
def compile_translations():
    po_files = glob.glob('*.po')
    for po in po_files:
        os.system('msgfmt -o %s.mo %s' % (po[:-3], po))
#@nonl
#@-node:eugene.20041116201812:compile_translations
#@+node:eugene.20041116202532:install_translations
def install_translations():
    shutil.copy('ru.mo', '/usr/share/locale/ru/LC_MESSAGES/snakememory.mo')
            
#@-node:eugene.20041116202532:install_translations
#@+node:eugene.20041116201512.3:main
def main():
    os.chdir('po')    
    compile_translations()
    install_translations()
#@nonl
#@-node:eugene.20041116201512.3:main
#@-others
if __name__ == '__main__':
    main()
#@-node:eugene.20041116201512.1:@thin install.py
#@-leo
