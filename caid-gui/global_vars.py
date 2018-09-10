from os      import environ
from os.path import abspath, dirname

CAIDwildcard = "CAID file (*.xml; *.txt; *.zip)|*.xml;*.txt;*.zip"
CAIDWorkGroupwildcard = "CAID WorkGroup file (*.wkl)|*.wkl"
CAIDViewerWildcard = "Image (*.png; *.jpeg)|*.png;*.jpeg"
CAIDConnectivityWildcard = "Connectivity (*.zip)|*.zip"
CAIDFieldWildcard = "Field (*.pfl)|*.pfl"
CAIDMarkerswildcard = "Markers (*.txt)|*.txt"
CAIDThemewildcard = "CAID Theme file (*.xml)|*.xml"

DIM_PROJECT = 0

#ALPHA = 1.0
#BETA  = 1.0
#
## RGB colors
#COLOR_GEOMETRY_MESH     = [1.,1.,1.]
#COLOR_GEOMETRY_NURBS    = [0.45, 0.45, 0.45] #[0.,0.,1.]
#COLOR_GEOMETRY_POINTS   = [0.1,0.1,0.1]
#
#SIZE_GEOMETRY_POINTS    = 6.
#
#COLOR_PATCH_MESH        = [0.8,0.8,0.8]
#COLOR_PATCH_NURBS       = None
#COLOR_PATCH_POINTS      = None
#
#SIZE_PATCH_POINTS       = 6.
#
#COLOR_SELECTIONRECTANGLE = [0.65,0.65,0.65]

try:
    CAID_DIR = environ['CAID_DIR']
except:
    CAID_DIR = dirname( dirname( abspath( __file__ ) ) )
    print ("WARNING: Environmental variable CAID_DIR not set... Falling back to parent directory '{}'.".format( CAID_DIR ) )

DATA_DIRECTORY       = CAID_DIR+"/data"
MODELS_DIRECTORY     = CAID_DIR+"/models"
MACROS_DIRECTORY     = CAID_DIR+"/macros"
TEMP_DIRECTORY       = CAID_DIR+"/macros"
MACROS_METRIC_SCRIPT = MACROS_DIRECTORY+"/macroMetric.py"

N_RECENT_FILES = 5

#MESH_RESOLUTION_VALUE = 5
#BOUNDARY_RESOLUTION_VALUE = 50
#INTERSECTION_RESOLUTION_VALUE = 50
#REMOVE_KNOT_TOLERANCE_VALUE = 1.0e-3

def strtoArray(txt):
#    print ">> strtoArray. Input :" + txt
    if txt == "None":
        return None
    if txt is None:
        return None

    # remove '(' and ')'
    if len(txt.split(',')) > 1:
        _txt = txt[1:-1]
        tab = _txt.split(',')
    # remove '(' and ')'
    elif len(txt.split(' ')) > 1:
        _txt = txt[1:-1]
        tab = _txt.split(' ')
    else:
        print(("Erro with " + str(tab)))
        raise
    _tab = [x for x in tab if len(x)>=1]
    tab = [float(x) for x in _tab]
    return tab
