# sh version
# Setup environment to run Obit software
OBITBASE="/export/home/leopard/bcotton/ObitWork/ObitBase/"; export OBITBASE # EDIT
LD_LIBRARY_PATH="$OBITBASE/deps/lib"; export LD_LIBRARY_PATH
OBIT="$OBITBASE/src/Obit"; export Obit
PYTHONPATH="$OBIT/python:$OBITBASE/share/obittalk/python/"; export PYTHONPATH
PATH="~/bin:$OBITBASE/bin:$OBITBASE/deps/bin:$PATH" ; export PATH
PLPLOT_DRV_DIR="$OBITBASE/deps/lib/plplot5.8.0/drivers/"; export PLPLOT_DRV_DIR
PLPLOT_LIB="$OBITBASE/deps/lib/plplot5.8.0/data/"; export PLPLOT_LIB
#; export
