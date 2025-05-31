# c shell version
# Setup environment to run Obit software
setenv OBITBASE "/export/home/leopard/bcotton/ObitWork/ObitBase/" # EDIT
# Blows build setenv LD_LIBRARY_PATH "$OBITBASE/deps/lib"
setenv OBIT $OBITBASE/src/Obit
setenv PYTHONPATH "$OBIT/python:$OBITBASE/share/obittalk/python/:$PYTHONPATH"
setenv PATH "~/bin:$OBITBASE/bin:$OBITBASE/deps/bin:$PATH" 
setenv PLPLOT_DRV_DIR $OBITBASE/deps/lib/plplot5.8.0/drivers/
setenv PLPLOT_LIB $OBITBASE/deps/share/plplot5.8.0/data/
#
