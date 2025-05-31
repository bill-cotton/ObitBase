#!/usr/bin/python3
#
#   Copyright (C) 2022,2023
#   Associated Universities, Inc. Washington DC, USA.
#
#   This program is free software; you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by the Free
#   Software Foundation; either version 2 of the License, or (at your option)
#   any later version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT
#   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#   FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#   more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   675 Massachusetts Ave, Cambridge, MA 02139, USA.
#
# Build Obit linux binary distribution
#
# Argument:
# 1: string with version number of release
# 2: Vector type 'SSE', 'AVX', 'AVX2', 'AVX512'
import sys, os, tempfile, shutil
from shutil import copyfile, copytree, copy, copy2
ver   = sys.argv[1]
vtype = sys.argv[2]
base = os.getcwd()+'/'   # Base of installation path
distroName = './distro/Obit.'+vtype+'-distro-1.1.'+ver+'/'

# Build basic structure
if not os.path.isdir(distroName):
    os.mkdir (distroName)
if not os.path.isdir(distroName+'/lib'):
    os.mkdir (distroName+'/lib')
if not os.path.isdir(distroName+'/lib/Obit'):
    os.mkdir (distroName+'/lib/Obit')
if not os.path.isdir(distroName+'/lib/Obit/bin'):
    os.mkdir (distroName+'/lib/Obit/bin')
if not os.path.isdir(distroName+'/share'):
    os.mkdir (distroName+'/share')

# Copy stuff
# Copy executables
oldbin = './src/Obit/bin/'  # Obit
newbin = distroName+'lib/Obit/bin/'
execList = os.listdir(oldbin)
for e in execList:
    #print ('executable ',e)
    # Copy if executable
    if os.access(oldbin+e, os.X_OK):
        #print ('cp -p ',oldbin+e,newbin+e)
        copy2(oldbin+e,newbin+e)

# ObitView, ObitMess
oldbin = './src/ObitView/'  # Obit
for e in ('ObitView','ObitMess'):
    copy2(oldbin+e,newbin+e)

# Zap any perl or python files
z=os.system('rm '+ distroName+'/lib/Obit/bin/*.pl')
z=os.system('rm '+ distroName+'/lib/Obit/bin/*.py')

# Change to runpath
execList = os.listdir(newbin)
newlib = distroName+'lib/'
for e in execList:
    z = os.system('chrpath -c -r '+newlib+' '+newbin+e)
for e in ('ObitView','ObitMess'):
    z = os.system('chrpath -c -r '+newlib+' '+newbin+e)

# Strip executables
z=os.system('strip '+ distroName+'/lib/Obit/bin/*')

# List of libraries to exclude from copy - mostly taken from perl script mkapp 
#Seem to need: "libxml2","libgssapi_krb5","libkrb5support","libkrb5","libk5crypto",
excludeLibs = ["libXrandr","librt","libXi","libatlas","libX11","libexpat","libz","libkeyutils", \
               "libdl","libresolv","libnsl","libXext","libXfixes","libgdbm","libSM","libsqlite3", \
               "libcblas","libfontconfig","libICE","libXinerama","libcom_err", \
               "libbz2","libutil", "libxcb","libfreetype","libgobject-2.0",  \
               "libgthread-2.0","libXcursor","libselinux","libf77blas","libc", \
               "libXau","libpthread","libstdc++","libXrender","libm","libuuid",
               "libglib-2.0","libXft","libfreebl3.so","libdb-4.7.so","libgcc_s","libcrypt","libnuma"
               "linux-vdso"];

# run ldd in an Obit task to get list of libraries
os.environ['LD_LIBRARY_PATH'] =  "./deps/lib/:os.getenv('LD_LIBRARY_PATH')"
print ('LD_LIBRARY_PATH',os.getenv('LD_LIBRARY_PATH'))
tfile = distroName+'/lib/Obit/bin/Template'
(tfd,tfname) = tempfile.mkstemp(text=True)  # Temporary scratch file
z = os.system('ldd '+tfile+' >'+tfname)
# and ObitView 
tfile = distroName+'/lib/Obit/bin/ObitView'
z = os.system('ldd '+tfile+' >>'+tfname)
# Python and python3
tfile = shutil.which('python')
z = os.system('ldd '+tfile+' >>'+tfname)
tfile = shutil.which('python3')
z = os.system('ldd '+tfile+' >>'+tfname)
# parse file
libList = {}
fd=open(tfname,'r')
line = '    '
while len(line)>2:
    line=fd.readline()
    if len(line)<=0:
        break
    #print (line)
    parts= line.split()
    #print (parts[0],parts[0].split('.')[0],parts[0].split('.')[0] not in excludeLibs)
    if (len(parts)>=4) and (parts[1]=='=>') and (parts[2]!='not') and \
       (parts[0].split('.')[0] not in excludeLibs):
        libList[parts[0]]=parts[2]

# end loop
fd.close()
if os.path.exists(tfname):
       os.remove(tfname)  # Delete

# Copy libraries
newlib = distroName+'lib/'
print("libList",libList)
for l in libList:
    #print ("library",l)
    #print('cp -p '+libList[l]+' '+newlib+l)
    copy2(libList[l],newlib+l)

# Strip libraries
z=os.system('chmod a+w '+ distroName+'/lib/*')
z=os.system('strip '+ distroName+'/lib/*.so*')

# ObitTalk scripts
copy2("./src/ObitTalk/bin/ObitTalk", distroName+'/lib/Obit/bin/')
z=os.system('sed -i s#$PWD#\$OBIT_ROOT/#g '+ distroName+'/lib/Obit/bin/ObitTalk')
copy2("./src/ObitTalk/bin/ObitTalk3", distroName+'/lib/Obit/bin/')
z=os.system('sed -i s#$PWD#\$OBIT_ROOT/#g '+ distroName+'/lib/Obit/bin/ObitTalk3')
copy2("./src/ObitTalk/bin/ObitTalkServer", distroName+'/lib/Obit/bin/')
z=os.system('sed -i s#$PWD#\$OBIT_ROOT/#g '+ distroName+'/lib/Obit/bin/ObitTalkServer')
z=os.system('chmod a+w '+ distroName+'/lib/Obit/bin/ObitTalk*')
copy2('./copyFiles/dot.obitrc_bin.py', distroName+'/dot.obitrc.py')
copy2('./copyFiles/readme', distroName)

# TDF files
if not os.path.isdir(distroName+'/lib/Obit/tdf'):
    copytree('./src/Obit/TDF', distroName+'/lib/Obit/tdf')

# Setup bin directory
if not os.path.isdir(distroName+'/bin'):
    copytree('template/bin', distroName+'/bin',symlinks=True)

# Copy share modules, data and scripts
if not os.path.isdir(distroName+'/share'):
    os.mkdir (distroName+'/share')
if not os.path.isdir(distroName+'/share/obit'):
    copytree('./src/Obit/share', distroName+'/share/obit',symlinks=True)
if not os.path.isdir(distroName+'/share/obittalk'):
    copytree('./share/obittalk', distroName+'/share/obittalk',symlinks=True)
if not os.path.isdir(distroName+'/share/python'):
    copytree('./src/Obit/python', distroName+'/share/python',symlinks=True)

# PLPlot runtime stuff for version 5.8.0
if not os.path.isdir(distroName+'/share/plplot'):
    copytree('./deps/share/plplot5.8.0', distroName+'/share/plplot',symlinks=True)
if not os.path.isdir(distroName+'/lib/plplot'):
    copytree('./deps/lib/plplot5.8.0', distroName+'/lib/plplot',symlinks=True)

# Strip libraries
z=os.system('strip '+ distroName+'/share/python/*.so')
# Unneeded
z=os.system('rm -f -r '+ distroName+'/share/python/build')
