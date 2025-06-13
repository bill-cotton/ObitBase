# $Id$
#-----------------------------------------------------------------------
#;  Copyright (C) 2022-2025
#;  Associated Universities, Inc. Washington DC, USA.
#;
#;  This program is free software; you can redistribute it and/or
#;  modify it under the terms of the GNU General Public License as
#;  published by the Free Software Foundation; either version 2 of
#;  the License, or (at your option) any later version.
#;
#;  This program is distributed in the hope that it will be useful,
#;  but WITHOUT ANY WARRANTY; without even the implied warranty of
#;  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#;  GNU General Public License for more details.
#;
#
#;  You should have received a copy of the GNU General Public
#;  License along with this program; if not, write to the Free
#;  Software Foundation, Inc., 675 Massachusetts Ave, Cambridge,
#;  MA 02139, USA.
#;
#;  Correspondence concerning this software should be addressed as follows:
#;         Internet email: bcotton@nrao.edu
#;         Postal address: W. D. Cotton
#;                         National Radio Astronomy Observatory
#;                         520 Edgemont Road
#;                         Charlottesville, VA 22903-2475 USA
#-----------------------------------------------------------------------
#
#    Obit: Merx mollis mortibus nuper
#
#----------------------------------------------------
# Build linux distribution of Obit
# Svn revision number, also fix readme, dot.obitrc_bin.py and dot.obitrc.py in copyFiles
#set CPPFLAGS to set avx, e.g. setenv CPPFLAGS "-mavx -DHAVE_AVX=1" 
# for distro set VTYPE to SSE, AVX, AVX2, AVX512
ver = 670
vtype = $(VTYPE)
disTarget := "Obit.$(VTYPE)-distro-1.1.$(ver).tar"
all: dodeps target

version:
	echo "ver=$(ver)"
	echo "vector Type = $(vtype)"

dodeps: 
	echo "Build deps"
	./SETUP.deps

target:
	echo "Build options ${CPPFLAGS}"
	# Untar stuff	
	cd template; tar xzf template.tgz
	cd share; tar xzf share.tgz
	rm -rf src/*
	export LD_LIBRARY_PATH="";git clone https://github.com/bill-cotton/Obit src
	mv src/ObitSystem/* src
	rm -rf src/other
	/bin/cp -p fixed/configure.ObitView src/ObitView/configure
	./SETUP.Obit
	export LD_LIBRARY_PATH="";cd src/Obit/python;make Obit
	./SETUP.ObitTalk	
	./SETUP.ObitView

rebuild:
	echo "Rebuild options ${CPPFLAGS}"
	./SETUP.Obit
	export LD_LIBRARY_PATH="";cd src/Obit/python;make Obit
	./SETUP.ObitTalk	
	./SETUP.ObitView

bindistro:
	echo "Make binary distro"
	./doDistro.py $(ver) $(vtype)
	cp -f -p VectorType distro/Obit.$(vtype)-distro-1.1.$(ver)/
	cd distro; tar cf $(disTarget) Obit.$(vtype)-distro-1.1.$(ver)
	cd distro; pigz  $(disTarget)

upload:
	scp -p distro/$(TARGET).gz smeagle.cv.nrao.edu:/users/bcotton/public_html/ObitBin/linux_distro/

update:
	cd src;git pull origin master

backup:
	cd ..; tar czvf ObitBase_backup.tgz ObitBase
clean:
	cd deps/src/plplot/plplot-5.8.0; $(MAKE) clean uninstall
	cd deps/src/plplot/; rm -r -f plplot-5.8.0
	cd deps/src/xmlrpc/; rm -r -f xmlrpc-c
	cd deps/src/cfitsio/; rm -r -f cfitsio-4.1.0
	cd deps/src/xml2/libxml2-2.9.10; $(MAKE) clean uninstall
	cd deps/src/xml2/; rm -r -f libxml2-2.9.10
	cd deps/src/curl/; rm -r -f curl-7.20.1 
	cd deps/share; rm -r -f plplot-5.8.0
	cd deps/share; rm -r -f doc 
	cd deps/share; rm -r -f gtk_doc/html/libxml2/*
	cd deps/lib; rm -r -f *
	cd deps/include; rm -r -f *
	cd bin; rm -r -f Obit*
	cd share/obittalk/python; rm -r -f Obit*
	chmod +w -R src/
	rm -r -f src
	mkdir src
	rm -r -f distro/*
