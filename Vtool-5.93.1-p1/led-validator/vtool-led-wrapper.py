'''
Created on 30-Dec-2019

@author: elango
'''
import sys
import os


__all__ = ["checkversion", "checkpackages", "runfile"]

class Vtool:
    
    def checkversion(self):
        '''
        Check the system whether python installed version 3.XXX (otherwise need to be install 3.XXX)
        '''
        
        if sys.version_info[0] < 3:
            raise Exception("Must be using Python 3.XXX")
        
        
        

    def checkpackages(self):
        
        '''
        Some changes might exist for checking packages
        1. "beautifulsoup4" Beautiful Soup 4's module is bs4 (import bs4)
        2. "rdflib-jsonld" RDFLib plugin providing JSON-LD parsing and serialization (import rdflib)
        3. "pytidylib" (import rdflib)
        '''
        a = []
        pkgs = ['rdflib', 'ipykernel', 'lxml', 'html5lib', 'bs4', 'pyld', 'pyshacl', 'owlrl', 'html5validator', 'rfc3987']
        
        for package in pkgs:
            try:
                __import__(package)
            except ImportError as e:
                a.append(str(e))
        return [print (err, file=sys.stderr) for err in a]
       
    
    def runfile(self):
        '''
        Create the arguments for execute the python
        1. pass the value for python|python3 for ubuntu user or python for windows users
        2. Input document xhtml or html file
        '''
        try:
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, 'tools/validate.py')
            exec(open(filename).read())
        except Exception as e:
            print(str(e), file=sys.stderr)
       
       
if __name__ == '__main__':
    
    v = Vtool()
    v.checkversion()
    if len(v.checkpackages()) == 0:
        v.runfile()
