#!/usr/bin/env python 
#  
#    There is currently no simple and easily documented way to query
#   if a *specific* Portable Executable has TypeLib (TLB) information
#   in it. It turns out, this technique LoadTypeLib(filename) checks
#   the file for TYPELIB PE section and parses it....This tool will walk
#   a directory tree and print out files that contain TypeLib data.
#
# EXAMPLE USAGE:
#
#  C:\WINDOWS\msagent>z:\data\work\Matasano\LogMeIn\helpers\who_has_tlb.py
#  Checking the directory: C:\WINDOWS\msagent
#  Recursing into directory C:\WINDOWS\msagent
#  !!! TLB INFO FOUND IN C:\WINDOWS\msagent\agentctl.dll !!!
#  !!! TLB INFO FOUND IN C:\WINDOWS\msagent\agentsvr.exe !!!
#  !!! TLB INFO FOUND IN C:\WINDOWS\msagent\agtctl15.tlb !!!
#  Recursing into directory C:\WINDOWS\msagent\chars
#  Recursing into directory C:\WINDOWS\msagent\intl


import pythoncom
import os
import sys
import code

def _checkdir(adir):
    print "Recursing into directory %s" % os.path.abspath(adir)
    for root, dirs, files in os.walk(adir, topdown=False):
        for file in files:
            #print "Checking %s for TLB info." % os.path.abspath(file)
            try:
                tlb = pythoncom.LoadTypeLib(os.path.abspath(file))
            except:
                pass
            else:
                print "!!! TLB INFO FOUND IN %s !!!" % os.path.abspath(file)
                tlbattr = tlb.GetLibAttr()
                print "\t",repr(tlbattr),"\n"
                mycmd = code.InteractiveConsole(locals())
                mycmd.interact()
        for a in dirs:
            _checkdir(a)

pythoncom.CoInitialize()         
if len(sys.argv) > 1:
    checkdir = sys.argv[1]
else:
    checkdir = os.path.abspath(os.curdir)
print("Checking the directory: %s" % checkdir)
if not os.path.exists(checkdir):
    print "Directory %s does not exist. Quitting" % checkdir
    sys.exit(1)
else:
    os.chdir(checkdir)

_checkdir(checkdir)

pythoncom.CoUninitialize()



