# ObitBase
Obit software build package
This distribution contains the higher level structures for building the Obit environment for processing astronomy data, especially data from radio interferometer arrays.
The source code for several of the more troublesome third packages are included and built as part of the installation.  Obit code is obtained from the github repository as part of the build/update.  See the README file in the top level directory for build instructions, some of which is reproduced below:
             Obit Installation Kit

   This directory contains the Obit source installation kit.  After
untarring the contents where you would like it installed, the software
can be built using one of the scripts in subdirectory scripts.
  scripts/build_with_SSE     Use only SSE vector instructions
  scripts/build_with_AVX     Use also AVX vector instructions
  scripts/build_with_AVX2    Use also AVX2 vector instructions
  scripts/build_with_AVX512  Use also AVX512f vector instructions
These control which vector instruction set is used in the build.
These depend on the hardware in the target machine and you would like
to use the most advanced version that the machine supports.
Attempting to use an unsupported instruction causes the program to
crash.  If your machine has a /proc/cpuinfo file, you can test the
various options (sse, avx, avx2, avx512) by
% grep avx2 /proc/cpuinfo
If this produces a blank string, that option is not available.  Every
interesting computer should have sse and most will have avx.
