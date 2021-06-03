#!/usr/bin/env python3

# Author Roelof Rietbroek (r.rietbroek@utwente.nl,2021)

# Initialize a RISE presentation with jupylecture goodies
import sys
import argparse
import pkg_resources
import os
import re

def copyResource(resource,outfile,link=False):
    if os.path.exists(outfile):
        print("%s already exists, not reextracting"%outfile)
        return
    if link:
        frompath=pkg_resources.resource_filename('jupylecture',resource)
        os.symlink(frompath,outfile) 
    else:
        with pkg_resources.resource_stream('jupylecture',resource) as fid:
            with open(outfile,'wb') as fout:
                fout.write(fid.read())

def listTemplates():
    templates=[]
    for f in pkg_resources.resource_listdir('jupylecture','templates'):
        if re.match('.*ipynb',f):
            templates.append(f)
    return templates

def main(argv):
    # Possibly add arguments to the program
    usage="Initialize a jupylecture in the current directory"
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument('-d','--develop',action='store_true',
                            help="Development mode, link to rise.cssi, and original image files instead of copying them (this option only makes sense when jupylecture is installed as editable)")
    parser.add_argument('fileout',type=str,default='Lecture1.ipynb',help='Output name (*ipynb) where the template is copied to',nargs='?')
    templates=listTemplates() 
    helpmessage="Select one of the currently supported templates (default=0):\n%s"%("".join([" %d: %s"%(i,f) for i,f in enumerate(templates)]))
    parser.add_argument('-t','--template',type=int,default=0,help=helpmessage,nargs=1,metavar="N")
    args = parser.parse_args(argv[1:])
    
    template='templates/ITCTemplateBlack.ipynb' #Note currently only one template available
    # copy or link the css file
    copyResource('templates/rise.css','rise.css',args.develop)
    copyResource(template,args.fileout)
    os.mkdir('images') 
    for f in pkg_resources.resource_listdir('jupylecture','templates/images'):
        copyResource(os.path.join('templates/images',f),os.path.join('images',f),args.develop)
   
if __name__ == "__main__":
    main(sys.argv)
