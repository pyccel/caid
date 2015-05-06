import numpy as np
from igakit.nurbs import NURBS

__all__ = ['XML', 'formatter', 'TXT', 'BZR']

class formatter(object):
    """
    this class is needed as multi-arrays are stored as 1D-arrays in the XML
    description
    """
    def __init__(self):
        pass

    def to_nparray(self, list_points, dim, list_n, Rd=3):
        try:
            if dim == 1:
                return self.to_nparray_crv(list_points, list_n, Rd)
            if dim == 2:
                return self.to_nparray_srf(list_points, list_n, Rd)
            if dim == 3:
                return self.to_nparray_vol(list_points, list_n, Rd)
        except:
            print("Problem occurs while converting the numpy array to xml-list")
            return None

    def to_nparray_crv(self, list_points, list_n, Rd):
        C = None
        if Rd == 1:
            C = np.zeros(list_n[0])
            C[:] = np.asarray(list_points).reshape(list_n)

        if Rd > 1:
            list_C = list(zip(* list_points))
            C = np.zeros((list_n[0],Rd))
            for i in range(0,Rd):
                C[:,i] = np.asarray(list_C[i]).reshape(list_n)

        return C

    def to_nparray_srf(self, list_points, list_n, Rd):
        C = None
        if Rd == 1:
            C = np.zeros((list_n[0], list_n[1]))
            C[:,:] = np.asarray(list_points).reshape(list_n[::-1]).transpose()

        if Rd > 1:
            list_C = list(zip(* list_points))
            C = np.zeros((list_n[0], list_n[1],Rd))
            for i in range(0,Rd):
                C[:,:,i] = np.asarray(list_C[i]).reshape(list_n[::-1]).transpose()

        return C

    def to_nparray_vol(self, list_points, list_n, Rd):
        print("to_nparray_vol: TODO transpose()")
        C = None
        if Rd == 1:
            C = np.zeros((list_n[0], list_n[1], list_n[2]))
            C[:,:,:] = np.asarray(list_points).reshape(list_n)

        if Rd > 1:
            list_C = list(zip(* list_points))
            C = np.zeros((list_n[0], list_n[1], list_n[2],Rd))
            for i in range(0,Rd):
                C[:,:,:,i] = np.asarray(list_C[i]).reshape(list_n)

        return C

    def to_list(self, C, dim, list_n, Rd=3):
        if dim == 1:
            return self.to_list_crv(C, list_n, Rd)
        if dim == 2:
            return self.to_list_srf(C, list_n, Rd)
        if dim == 3:
            return self.to_list_vol(C, list_n, Rd)

    def to_list_crv(self, C, list_n, Rd):
        n = np.asarray(list_n).prod()
        if Rd == 1:
            return C[:].reshape(n)
        if Rd == 2:
            return list(zip(  C[:,0].reshape(n) \
                       , C[:,1].reshape(n)))
        if Rd == 3:
            return list(zip(  C[:,0].reshape(n) \
                       , C[:,1].reshape(n) \
                       , C[:,2].reshape(n)))

    def to_list_srf(self, C, list_n, Rd):
        n = np.asarray(list_n).prod()
        if Rd == 1:
            return C[:,:].transpose().reshape(n)
        if Rd == 2:
            return list(zip(  C[:,:,0].transpose().reshape(n) \
                       , C[:,:,1].transpose().reshape(n)))
        if Rd == 3:
            return list(zip(  C[:,:,0].transpose().reshape(n) \
                       , C[:,:,1].transpose().reshape(n) \
                       , C[:,:,2].transpose().reshape(n)))

    def to_list_vol(self, C, list_n, Rd):
        print("to_list_vol: TODO transpose()")
        n = np.asarray(list_n).prod()
        if Rd == 1:
            return C[:,:,:].reshape(n)
        if Rd == 2:
            return list(zip(  C[:,:,:,0].reshape(n) \
                       , C[:,:,:,1].reshape(n)))
        if Rd == 3:
            return list(zip(  C[:,:,:,0].reshape(n) \
                       , C[:,:,:,1].reshape(n) \
                       , C[:,:,:,2].reshape(n)))


class XML(object):
    __currentNode__ = None
    __patchList__   = None


    RATIONAL_TAG        = "rational"
    DIM_TAG             = "dimension"
    SHAPE_TAG           = "shape"
    DEGREE_TAG          = "degree"
    KNOTS_TAG           = "knots"
    POINTS_TAG          = "points"
    WEIGHTS_TAG         = "weights"
    FACE_TAG            = "face"
    ORIGINAL_TAG        = "original"
    CLONE_TAG           = "clone"
    ORIENTATION_TAG     = "orientation"

    GEOMETRY_TAG        = "geometry"
    PATCH_TAG           = "patch"
    CONNECTIVITY_TAG    = "connectivity"
    INTERNALFACES_TAG   = "internal_faces"
    EXTERNALFACES_TAG   = "external_faces"

    SEP_TAG         = ','
    PSEP_TAG        = ';'

    dim = None
    def __init__( self ):
        self.doc = None

    def getRootElement(self):
        if self.__currentNode__ == None:
            self.__currentNode__ = self.doc.documentElement

        return self.__currentNode__

    def getText(self, node):
        return node.childNodes[0].nodeValue

    def _array_to_str(self, array):
        txt = ""
        for x in array[:-1]:
            txt += ' ' + str(x) + self.SEP_TAG
        txt += ' ' + str(array[-1]) + ' '
        return txt

    def _str_to_array(self, txt, fmt):
        data = None
        lps_data = txt.split(self.SEP_TAG)
#        print "lps_data : ", lps_data
        if fmt=="int":
            data = [int(x) for x in lps_data]
#            print "int-data -> ", data
        if fmt=="float":
#            print "float-data -> ", data
            data = [float(x) for x in lps_data]
        if fmt=="string":
            data = lps_data
        return data

    def _get_attribut(self, TAG, datas, id=0):
        try:
            #.... reading data
            attr = datas.getAttribute(TAG)
            if attr == "":
                return None
            else:
                return attr
#            print "attr : ", attr
            return attr
        except:
            return None

    def _get_data(self, TAG, datas, fmt, id=0):
        try:
            #.... reading data
            node = datas.getElementsByTagName(TAG)[id]
            txt = self.getText(node)
            data = self._str_to_array(txt, fmt=fmt)
#            print "data : ", data
            return data
        except:
            if TAG not in ["orientation"]:
                print("Exception _get_data, invalid tag : ", TAG)
            return None

    def read(self, filename, geo):
        from xml.dom.minidom import parse
        doc = parse(filename)
        self.doc = doc
        rootElt = self.getRootElement()
        self.xmltogeo(geo, doc, rootElt)

    def xmltogeo(self, geo, doc, rootElt):
        from caid.cad_geometry import cad_nurbs, cad_op_nurbs, cad_grad_nurbs
        from caid.op_nurbs import grad

        geo_attributs       = {}
        # ... geometry attributs
        for TAG in list(rootElt.attributes.keys()):
            txt = rootElt.attributes[TAG].value
            if txt == "True":
                txt = True
            if txt == "False":
                txt = False

            if txt is not None:
                geo_attributs[TAG]   = txt
        # ...

        for datas in rootElt.getElementsByTagName(self.PATCH_TAG):

            attributs       = {}
            # ... patch attributs
            for TAG in list(datas.attributes.keys()):
                txt = datas.attributes[TAG].value
                if txt is not None:
                    attributs[TAG]   = txt
            # ...

            if datas.nodeType == datas.ELEMENT_NODE:
                try:
                    # ... reading dim
                    list_dim = self._get_data(self.DIM_TAG, datas, fmt="int")
                    li_dim = list_dim[0]
                    # ...

                    # ... reading the shape
                    list_n = self._get_data(self.SHAPE_TAG, datas, fmt="int")
                    # ...

                    # ... reading the degree
                    list_p = self._get_data(self.DEGREE_TAG, datas, fmt="int")
                    # ...

                    # ... reading the knots
                    list_knots = []
                    for axis in range(0, li_dim):
                        knots = self._get_data(self.KNOTS_TAG, datas, fmt="float", id=axis)
                        list_knots.append(knots)
                    # ...

                    # ... reading the points
                    list_points = self._get_data(self.POINTS_TAG, datas, fmt="float")
                    C = np.asarray(list_points)
                    C = C.reshape(list_n+[3]) # we need to add the Rd dimension
                    # ...

                    # ... reading the weights
                    list_weights = self._get_data(self.WEIGHTS_TAG, datas, fmt="float")
                    W = np.asarray(list_weights)
                    W = W.reshape(list_n)
                    # ...

                    # ... reading rational
                    try:
                        list_rational = self._get_data(self.RATIONAL_TAG, datas, fmt="string")
                        rational = list_rational[0]
                        if rational.lower() == "yes":
                            rational = True
                        else:
                            rational = False
                    except:
                        print("XML.read: Exception while reading rational arg")
                        rational = False
                    # ...

                    # ... reading faces orientation
                    list_sgn = self._get_data(self.ORIENTATION_TAG, datas, fmt="int")
                    # ...

                    try:
                        nrb_type = attributs["type"]
                    except:
                        nrb_type = "cad_nurbs"

                    try:
                        nrb_operator = attributs["operator"]
                    except:
                        nrb_operator = None

                    try:
                        if nrb_type == "cad_nurbs":
                            nrb = cad_nurbs(list_knots, C, weights=W)
                        elif nrb_type == "cad_grad_nurbs":
                            _nrb = NURBS(list_knots, C, weights=W)
                            grad_nrb = grad(_nrb)
                            nrb = cad_grad_nurbs(grad_nrb)
                        elif nrb_type == "cad_op_nurbs":
                            if nrb_operator == "grad":
                                _nrb = NURBS(list_knots, C, weights=W)
                                grad_nrb = grad(_nrb)
                                nrb = cad_op_nurbs(grad_nrb)
                                print("Warning: creates a cad_op_nurbs instead of cad_grad_nurbs")
                            else:
                                print("Operator not yet implemented")
                                raise

                        nrb.set_attributs(attributs)
                        nrb.set_orientation(list_sgn)
                        nrb.set_rational(rational)
                    except:
                        print("XML.read: Exception while creating the corresponding cad_nurbs")

                except:
                    nrb = None
                    print('Un des TAGS suivant est manquants')

                geo.append(nrb)

        # ... read connectivity
        list_connectivity = []
        for Elt in rootElt.getElementsByTagName(self.CONNECTIVITY_TAG):
            original = self._get_data(self.ORIGINAL_TAG, Elt, fmt="int")
            clone    = self._get_data(self.CLONE_TAG, Elt, fmt="int")
            connectivity = {}
            connectivity['original']  = original
            connectivity['clone']     = clone
            list_connectivity.append(connectivity)
        # ...

        # ... read internal_faces
        list_intFaces = []
        try:
            Elt = rootElt.getElementsByTagName(self.INTERNALFACES_TAG)[0]
            nFaces = len(Elt.getElementsByTagName(self.FACE_TAG))
            for id in range(0, nFaces):
                face = self._get_data(self.FACE_TAG, Elt, fmt="int", id=id)
                list_intFaces.append(face)
        except:
            pass
        # ...

        # ... read external_faces
        list_extFaces = []
        try:
            Elt = rootElt.getElementsByTagName(self.EXTERNALFACES_TAG)[0]
            nFaces = len(Elt.getElementsByTagName(self.FACE_TAG))
            for id in range(0, nFaces):
                face = self._get_data(self.FACE_TAG, Elt, fmt="int", id=id)
                list_extFaces.append(face)
        except:
            pass
        # ...

        geo.set_internal_faces(list_intFaces)
        geo.set_external_faces(list_extFaces)
        geo.set_connectivity(list_connectivity)

        geo.set_attributs(geo_attributs)

        return geo

    def geotoxml(self, geo, doc, rootElt):
        """
        generates xml doc from cad_geometry object
        """
        # ... sets geometry attributs
        for TAG, txt in geo.attributs.items():
            if txt is not None:
                rootElt.setAttribute(TAG, str(txt))
        # ...

        self._patchs_to_xml(geo, doc, rootElt)
        self._internal_faces_to_xml(geo, doc, rootElt)
        self._external_faces_to_xml(geo, doc, rootElt)
        self._connectivity_to_xml(geo, doc, rootElt)

        return doc

    def write(self, filename, geo):
        from xml.dom.minidom import Document
        # Create the minidom document
        doc = Document()
        # Create the <geometry> base element
        rootElt = doc.createElement(self.GEOMETRY_TAG)
        doc.appendChild(rootElt)

        f = open(filename, 'w')
        doc = self.geotoxml(geo, doc, rootElt)
        s = doc.toprettyxml()
        f.write(s)
        f.close()

    def _internal_faces_to_xml(self, geo, doc, rootElt):
        """
        Args:
            geo : is a cad_geometry
        """
        faces  = geo.internal_faces
        nFaces          = len(faces)
        if nFaces > 0:
            # Create the main <card> element
            maincard = doc.createElement(self.INTERNALFACES_TAG)
            rootElt.appendChild(maincard)
            # ... write dimension
            for id in range(0,nFaces):
                F = faces[id]
                self._update_xml(self.FACE_TAG, F, doc, maincard)
            # ...

    def _external_faces_to_xml(self, geo, doc, rootElt):
        """
        Args:
            geo : is a cad_geometry
        """
        faces  = geo.external_faces
        nFaces          = len(faces)
        if nFaces > 0:
            # Create the main <card> element
            maincard = doc.createElement(self.EXTERNALFACES_TAG)
            rootElt.appendChild(maincard)
            # ... write dimension
            for id in range(0,nFaces):
                F = faces[id]
                self._update_xml(self.FACE_TAG, F, doc, maincard)
            # ...

    def _connectivity_to_xml(self, geo, doc, rootElt):
        """
        Args:
            geo : is a cad_geometry
        """

        # Create the main <card> element
        list_connectivity  = geo.connectivity
        n             = len(list_connectivity)
        # ... write dimension
        for id in range(0,n):
            connectivity = list_connectivity[id]
            original        = connectivity['original']
            clone           = connectivity['clone']

            maincard = doc.createElement(self.CONNECTIVITY_TAG)
            rootElt.appendChild(maincard)

            self._update_xml(self.ORIGINAL_TAG, original, doc, maincard)
            self._update_xml(self.CLONE_TAG   , clone   , doc, maincard)
        # ...

    def _update_xml(self, TAG, data, doc, maincard):
        try:
            # ... write data
            Elt = doc.createElement(TAG)
            maincard.appendChild(Elt)
            if type(data) == str:
                txt = data
            else:
                txt = self._array_to_str(data)
            Text = doc.createTextNode(txt)
            Elt.appendChild(Text)
        except:
            print("Warning: wrong or bad values for ", TAG)
#        print TAG, txt
        # ...

    def _patchs_to_xml(self, geo, doc, rootElt):
        """
        Args:
            geo : is a cad_geometry
        """
        list_nrb = geo.list_all
        for nrb in list_nrb:
            # Create the main <card> element
            maincard = doc.createElement(self.PATCH_TAG)
            rootElt.appendChild(maincard)

            # ... patch attributs
            for TAG, txt in nrb.attributs.items():
                if txt is not None:
                    maincard.setAttribute(TAG, txt)
            # ...

            # ... write rational
            if nrb.rational:
                str_rational = "yes"
            else:
                str_rational = "no"
            self._update_xml(self.RATIONAL_TAG, str_rational, doc, maincard)
            # ...

            # ... write dimension
            self._update_xml(self.DIM_TAG, np.asarray([nrb.dim]), doc, maincard)
            # ...

            # ... write shape
            self._update_xml(self.SHAPE_TAG, np.asarray(list(nrb.shape)), doc, maincard)
            # ...

            # ... write degree
            self._update_xml(self.DEGREE_TAG, np.asarray(list(nrb.degree)), doc, maincard)
            # ...

            # ... write knots
            for axis in range (0,nrb.dim):
                self._update_xml(self.KNOTS_TAG, nrb.knots[axis], doc, maincard)
            # ...

            # ... write points
            self._update_xml(self.POINTS_TAG, nrb.points.reshape(nrb.points.size), doc, maincard)
            # ...

            # ... write weights
            self._update_xml(self.WEIGHTS_TAG, nrb.weights.reshape(nrb.weights.size), doc, maincard)
            # ...

            # ... write orientation
            try:
                self._update_xml(self.ORIENTATION_TAG, np.asarray(list(nrb.orientation)), doc, maincard)
            except:
#                print "Warning: wrong or bad values for orientation. Please do not forget to specify it."
                pass
            # ...

class TXT(object):
    def __init__(self):
        pass

    def write(self, name, geo, fmt="zip"):
        # ...
        def exportPatch(nrb, filename):
            fo = open(filename, "w")
            # ... write degree
            fo.write("# degree")
            fo.write("\n")
            txt = str(nrb.degree)[1:-1]
            fo.write(txt)
            fo.write("\n")
            # ...

            # ... write shape
            fo.write("# shape")
            fo.write("\n")
            txt = str(nrb.shape)[1:-1]
            fo.write(txt)
            fo.write("\n")
            # ...

            # ... write rational
            fo.write("# rational")
            fo.write("\n")
            if nrb.rational:
                txt = "1"
            else:
                txt = "0"
            fo.write(txt)
            fo.write("\n")
            # ...

            # ... write knots
            for axis in range (0, nrb.dim):
                fo.write("# knots")
                fo.write("\n")
                txt = str(nrb.knots[axis])[1:-1]
                fo.write(txt)
                fo.write("\n")
            # ...

            # ... write Control Points
            fo.write("# points")
            fo.write("\n")
            n = nrb.shape
            if nrb.dim == 1:
                for i in range(0, n[0]):
                    txt = str(nrb.points[i,:])[1:-1]
                    fo.write(txt)
                    fo.write("\n")
            if nrb.dim == 2:
                for i in range(0, n[0]):
                    for j in range(0, n[1]):
                        txt = str(nrb.points[i,j,:])[1:-1]
                        fo.write(txt)
                        fo.write("\n")
            if nrb.dim == 3:
                for i in range(0, n[0]):
                    for j in range(0, n[1]):
                        for k in range(0, n[2]):
                            txt = str(nrb.points[i,j,k,:])[1:-1]
                            fo.write(txt)
                            fo.write("\n")
            # ...

            # ... write weights
            fo.write("# weights")
            fo.write("\n")
            n = nrb.shape
            if nrb.dim == 1:
                for i in range(0, n[0]):
                    txt = str(nrb.weights[i])
                    fo.write(txt)
                    fo.write("\n")
            if nrb.dim == 2:
                for i in range(0, n[0]):
                    for j in range(0, n[1]):
                        txt = str(nrb.weights[i,j])
                        fo.write(txt)
                        fo.write("\n")
            if nrb.dim == 3:
                for i in range(0, n[0]):
                    for j in range(0, n[1]):
                        for k in range(0, n[2]):
                            txt = str(nrb.weights[i,j,k])
                            fo.write(txt)
                            fo.write("\n")
            # ...

            fo.close()
        # ...

        # ...
        def exportAdditionalInfo(geo, filename):
            fo = open(filename, "w")

            # ... Rd
            fo.write("# Rd")
            fo.write("\n")
            txt = str(geo.Rd)
            fo.write(txt)
            fo.write("\n")
            # ...

            # ... dim
            fo.write("# dim")
            fo.write("\n")
            txt = str(geo.dim)
            fo.write(txt)
            fo.write("\n")
            # ...

            # ... number of patchs
            fo.write("# npatchs")
            fo.write("\n")
            txt = str(geo.npatchs)
            fo.write(txt)
            fo.write("\n")
            # ...

            # ... external_faces
            fo.write("# external_faces")
            fo.write("\n")
            for data in geo.external_faces:
                txt = str(data)[1:-1]
                fo.write(txt)
                fo.write("\n")
            # ...

            # ... internal_faces
            fo.write("# internal_faces")
            fo.write("\n")
            for data in geo.internal_faces:
                txt = str(data)[1:-1]
                fo.write(txt)
                fo.write("\n")
            # ...

            # ... connectivity
            fo.write("# connectivity")
            fo.write("\n")
            for dic in geo.connectivity:
                for key, data in dic.items():
                    label = key
                    fo.write(label)
                    fo.write("\n")
                    txt   = str(data)[1:-1]
                    fo.write(txt)
                    fo.write("\n")
            # ...

            fo.close()
        # ...

        # ...
        _name = name.split('.')[0]
        if fmt == "zip":
            import os
            os.system("mkdir " + _name)

        for i in range(0, geo.npatchs):
            nrb = geo[i]
            if fmt == "zip":
                filename = _name + "/" + "patch"+str(i)+".txt"
            if fmt == "txt":
                filename = _name + "_" + "patch"+str(i)+".txt"

            exportPatch(nrb, filename)

        if fmt == "zip":
            filename = _name + "/" + "info.txt"
        if fmt == "txt":
            filename = _name + "_" + "info.txt"
        exportAdditionalInfo(geo, filename)
        # ...

        # ...
        if fmt == "zip":
            from contextlib import closing
            from zipfile import ZipFile, ZIP_DEFLATED
            import os

            # ...
            def zipdir(basedir, archivename):
                assert os.path.isdir(basedir)
                with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
                    for root, dirs, files in os.walk(basedir):
                        #NOTE: ignore empty directories
                        for fn in files:
                            absfn = os.path.join(root, fn)
                            zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
                            z.write(absfn, zfn)
            # ...
            basedir = _name
            archivename = name
            zipdir(basedir, archivename)
            os.system("rm -R " + _name)
        # ...

#    def read_geometries_hdf5(as_hdf5_file):
#        import h5py as h5
#        lo_file = h5.File(as_hdf5_file,'r')
#        __list_domains__ = []
#        lo_domain=patch()
#        li_npatchs = len(list(lo_file))
#        for li_id in range(0, li_npatchs):
#            lo_domain.read_hdf5(lo_file, li_id)
#            __list_domains__.append(lo_domain)
#        lo_file.close()
#        return __list_domains__

########################################################################
# TODO to move to a directory io, in a file bezier

from caid.numbering.connectivity import connectivity
from caid.utils.quadratures import *
from caid.utils.bernstein import *
def get_nodes_2d(geo):
    # ... sets the list of Nodes
    geo_ref, list_lmatrices = geo.bezier_extract()

    list_nodeData = []

    node_index = 0
    for nrb in geo_ref:
        # ...
        # we loop over each element and generate the P,
        # ...
        # we start by matching the 1D index with the 2D one
        lpi_n = nrb.shape
        lpi_p = nrb.degree

        # .................................................
        list_i = list(range(0,lpi_n[0],lpi_p[0]))
        list_j = list(range(0,lpi_n[1],lpi_p[1]))
        for enum_j, j in enumerate(list_j):
            for enum_i, i in enumerate(list_i):
                node_index += 1

                # compute index element index
                i_elt = enum_i + enum_j * len(list_i)

                pts_x = nrb.points[i,j,0]
                pts_y = nrb.points[i,j,1]

                # ...
                # compute the boundary code, for dirichlet
                # ...
                boundaryCode = 0
                if j in  [0,lpi_n[1] - 1]:
                    boundaryCode = 1
                if i in  [0,lpi_n[0] - 1]:
                    boundaryCode = 1
                # ...

                nodeData = [[node_index], [pts_x, pts_y], [boundaryCode]]

                lineNodeData = []
                for data in nodeData:
                    for d in data:
                        lineNodeData.append(d)

                list_nodeData.append(lineNodeData)
        # ...
    return list_nodeData
    # .................................................

def save_nodes_2d(geo, filename):
    list_nodeData = get_nodes_2d(geo)

    # .................................................
    # ... exporting files
    fmt_nodes = '%d, %.15f, %.15f, %d'
    # .................................................

    # .................................................
    a = open(filename+"_nodes.txt", "w")
    # ... write size of list_nodeData
    a.write(str(len(list_nodeData))+' \n')

    for L in list_nodeData:
        line = fmt_nodes % tuple(L) +' \n'
        a.write(line)
    a.close()
    # .................................................

def get_nodes_bezier_2d(geo):
    # ... sets the list of Nodes
    geo_ref, list_lmatrices = geo.bezier_extract()

    list_nodeData = []
    node_index = 0

    for nrb in geo_ref:
        # ...
        # we loop over each element and generate the P,
        # ...
        # we start by matching the 1D index with the 2D one
        lpi_n = nrb.shape
        lpi_p = nrb.degree

        # .................................................
        list_i = list(range(0,lpi_n[0]))
        list_j = list(range(0,lpi_n[1]))
        for enum_j, j in enumerate(list_j):
            for enum_i, i in enumerate(list_i):
                node_index += 1

                # compute index element index
                i_elt = enum_i + enum_j * len(list_i)

                pts_x = nrb.points[i,j,0]
                pts_y = nrb.points[i,j,1]

                # ...
                # compute the boundary code, for dirichlet
                # ...
                boundaryCode = 0
                if j in  [0,lpi_n[1] - 1]:
                    boundaryCode = 1
                if i in  [0,lpi_n[0] - 1]:
                    boundaryCode = 1
                # ...

                nodeData = [[node_index], [pts_x, pts_y], [boundaryCode]]

                lineNodeData = []
                for data in nodeData:
                    for d in data:
                        lineNodeData.append(d)

                list_nodeData.append(lineNodeData)
        # ...
    return list_nodeData
    # .................................................

def save_nodes_bezier_2d(geo, filename):
    list_nodeData = get_nodes_bezier_2d(geo)

    # .................................................
    # ... exporting files
    fmt_nodes = '%d, %.15f, %.15f, %d'
    # .................................................

    # .................................................
    a = open(filename+"_nodes_bezier.txt", "w")
    # ... write size of list_nodeData
    a.write(str(len(list_nodeData))+' \n')

    for L in list_nodeData:
        line = fmt_nodes % tuple(L) +' \n'
        a.write(line)
    a.close()
    # .................................................

def get_elements_2d(geo):
    # TODO ancestor and sons
    list_elementData = []

    # .................................................
    for nrb in geo:
        lpi_n = nrb.shape
        lpi_p = nrb.degree

        nx_elt = len(np.unique(nrb.knots[0])) - 1
        ny_elt = len(np.unique(nrb.knots[1])) - 1
        list_i = list(range(0,nx_elt))
        list_j = list(range(0,ny_elt))
        for enum_j, j in enumerate(list_j):
            for enum_i, i in enumerate(list_i):
                # compute index element index
                i_elt = enum_i + enum_j * len(list_i)

                # TODO for each element, we must compute its neighbours
                neighbours  = [-1, -1, -1, -1]

                # ... vertex indices
                index_vertices = []

                _i = i ; _j = j
                ind = _i + _j * lpi_n[0]
                index_vertices.append(ind+1)

                _i = i+lpi_p[0]; _j = j
                ind = _i + _j * lpi_n[0]
                index_vertices.append(ind+1)

                _i = i+lpi_p[0]; _j = j+lpi_p[1]
                ind = _i + _j * lpi_n[0]
                index_vertices.append(ind+1)

                _i = i; _j = j+lpi_p[1]
                ind = _i + _j * lpi_n[0]
                index_vertices.append(ind+1)
                # ...

                elementData = [[i_elt+1], index_vertices, neighbours]

                lineElementData = []
                for data in elementData:
                    for d in data:
                        lineElementData.append(d)

                list_elementData.append(lineElementData)
    # ...
    return list_elementData
    # .................................................

def save_elements_2d(geo, filename):
    list_elementData = get_elements_2d(geo)

    # .................................................
    # ... exporting files
    fmt_int = '%d'
    # .................................................

    # .................................................
    a = open(filename+"_elements.txt", "w")
    # ... write size of list_elementData
    a.write(str(len(list_elementData))+' \n')

    for L in list_elementData:
        line = ''.join(str(fmt_int % e)+', ' for e in L[0:])[:-2]+' \n'
        a.write(line)
    a.close()
    # .................................................

def get_elements_bezier_2d(geo):
    geo_ref, list_lmatrices = geo.bezier_extract()
    list_elementData = []

    # .................................................
    for nrb in geo_ref:
        lpi_n = nrb.shape
        lpi_p = nrb.degree

        nx_elt = lpi_n[0]-1
        ny_elt = lpi_n[1]-1
        list_i = list(range(0,nx_elt))
        list_j = list(range(0,ny_elt))
        for enum_j, j in enumerate(list_j):
            for enum_i, i in enumerate(list_i):
                # compute index element index
                i_elt = enum_i + enum_j * len(list_i)

                # TODO for each element, we must compute its neighbours
                neighbours  = [-1, -1, -1, -1]

                # ... vertex indices
                index_vertices = []

                _i = i ; _j = j
                ind = _i + _j * lpi_n[0]
                index_vertices.append(ind+1)

                _i = i+1; _j = j
                ind = _i + _j * lpi_n[0]
                index_vertices.append(ind+1)

                _i = i+1; _j = j+1
                ind = _i + _j * lpi_n[0]
                index_vertices.append(ind+1)

                _i = i; _j = j+1
                ind = _i + _j * lpi_n[0]
                index_vertices.append(ind+1)
                # ...

                elementData = [[i_elt+1], index_vertices, neighbours]

                lineElementData = []
                for data in elementData:
                    for d in data:
                        lineElementData.append(d)

                list_elementData.append(lineElementData)
    # ...
    return list_elementData
    # .................................................

def save_elements_bezier_2d(geo, filename):
    list_elementData = get_elements_bezier_2d(geo)

    # .................................................
    # ... exporting files
    fmt_int = '%d'
    # .................................................

    # .................................................
    a = open(filename+"_elements_bezier.txt", "w")
    # ... write size of list_elementData
    a.write(str(len(list_elementData))+' \n')

    for L in list_elementData:
        line = ''.join(str(fmt_int % e)+', ' for e in L[0:])[:-2]+' \n'
        a.write(line)
    a.close()
    # .................................................

def get_nodes_sons_2d(geo):
    # ... sets the list of Nodes
    geo_ref, list_lmatrices = geo.bezier_extract()

    list_nodeData = []

    node_index = 0
    for nrb_ref, nrb in zip(geo_ref, geo):
        # ...
        # we loop over each element and generate the P,
        # ...
        # we start by matching the 1D index with the 2D one
        lpi_n = nrb_ref.shape
        lpi_p = nrb_ref.degree

        # .................................................
        nx_elt = len(np.unique(nrb.knots[0])) - 1
        ny_elt = len(np.unique(nrb.knots[1])) - 1
        list_i = list(range(0,nx_elt))
        list_j = list(range(0,ny_elt))
        for elt_j in list_j:
            for elt_i in list_i:
                node_index += 1

                # compute index element index
                i_elt = elt_i + elt_j * len(list_i)

                # ... vertex indices
                list_indices = []
                for _j in range(0, lpi_p[1]+1):
                    j = _j + lpi_p[1] * elt_j
                    for _i in range(0, lpi_p[0]+1):
                        i = _i + lpi_p[0] * elt_i

                        I = i + j * lpi_n[0]
                        list_indices.append(I+1)
                # ...

                # ... number of nodes
                n_nodes = len(list_indices)

                nodeData = [[i_elt+1, n_nodes], list_indices]
                list_nodeData.append(nodeData)
        # ...
    return list_nodeData
    # .................................................

def save_nodes_sons_2d(geo, filename):
    list_nodeData = get_nodes_sons_2d(geo)

    # .................................................
    # ... exporting files
    fmt_int = '%d'
    # .................................................

    # .................................................
    a = open(filename+"_nodes_sons.txt", "w")
    # ... write size of list_nodeData
    a.write(str(len(list_nodeData))+' \n')

    for multiL in list_nodeData:
        # ... element id  and  number of sons nodes
        L = multiL[0]
        line = str(L[0]) + ", "+ str(L[1]) +  ' \n'
        a.write(line)
        # ... sons nodes indices
        L = multiL[1]
        line = ''.join(str(fmt_int % e)+', ' for e in L[0:])[:-2]+' \n'
        a.write(line)
    a.close()
    # .................................................


def get_elements_sons_2d(geo):
    # ... sets the list of Nodes
    geo_ref, list_lmatrices = geo.bezier_extract()

    list_elementData = []

    element_index = 0
    for nrb_ref, nrb in zip(geo_ref, geo):
        # ...
        # we loop over each element and generate the P,
        # ...
        # we start by matching the 1D index with the 2D one
        lpi_n = nrb_ref.shape
        lpi_p = nrb_ref.degree

        # .................................................
        nx_elt = len(np.unique(nrb.knots[0])) - 1
        ny_elt = len(np.unique(nrb.knots[1])) - 1
        list_i = list(range(0,nx_elt))
        list_j = list(range(0,ny_elt))
        for elt_j in list_j:
            for elt_i in list_i:
                element_index += 1

                # compute index element index
                i_elt = elt_i + elt_j * len(list_i)

                # ... vertex indices
                list_indices = []
                for _j in range(0, lpi_p[1]):
                    j = _j + lpi_p[1] * elt_j
                    for _i in range(0, lpi_p[0]):
                        i = _i + lpi_p[0] * elt_i

                        I = i + j * (lpi_n[0]-1)
                        list_indices.append(I+1)
                # ...

                # ... number of elements
                n_elements = len(list_indices)

                # ... vertex indices
                list_nodes_indices= []
                for _j in range(0, lpi_p[1]+1):
                    j = _j + lpi_p[1] * elt_j
                    for _i in range(0, lpi_p[0]+1):
                        i = _i + lpi_p[0] * elt_i

                        I = i + j * lpi_n[0]
                        list_nodes_indices.append(I+1)
                # ...

                # ... number of vertices
                n_vertices = len(list_nodes_indices)

                elementData = [[i_elt+1, n_elements, n_vertices], list_indices, list_nodes_indices]
                list_elementData.append(elementData)
        # ...
    return list_elementData
    # .................................................

def save_elements_sons_2d(geo, filename):
    list_elementData = get_elements_sons_2d(geo)

    # .................................................
    # ... exporting files
    fmt_int = '%d'
    # .................................................

    # .................................................
    a = open(filename+"_elements_sons.txt", "w")
    # ... write size of list_nodeData
    a.write(str(len(list_elementData))+' \n')

    for multiL in list_elementData:
        # ... element id, number of sons elements and vertices
        L = multiL[0]
        line = str(L[0]) + ", "+ str(L[1]) + ", "+ str(L[2]) +  ' \n'
        a.write(line)
        # ... sons elements indices
        L = multiL[1]
        line = ''.join(str(fmt_int % e)+', ' for e in L[0:])[:-2]+' \n'
        a.write(line)
        # ... sons vertices indices
        L = multiL[2]
        line = ''.join(str(fmt_int % e)+', ' for e in L[0:])[:-2]+' \n'
        a.write(line)
    a.close()
    # .................................................

def get_bernstein_representation_2d(geo):
    # .................................................
    from caid.numbering.connectivity import connectivity
    con = connectivity(geo)
    con.init_data_structure()

    geo_ref, list_lmatrices = geo.bezier_extract()

    # ... sets the list of connectivities
    list_bernstein_representationData = []

    for patch_id in range(0, geo.npatchs):
        nrb = geo[patch_id]
        lmatrices = list_lmatrices[patch_id]
        local_LM = con.LM[patch_id]

        lpi_n = nrb.shape
        lpi_p = nrb.degree
        nx_elt = len(np.unique(nrb.knots[0])) - 1
        ny_elt = len(np.unique(nrb.knots[1])) - 1
        list_i = list(range(0,nx_elt))
        list_j = list(range(0,ny_elt))
        for enum_j, j in enumerate(list_j):
            for enum_i, i in enumerate(list_i):
                # compute index element index
                i_elt = enum_i + enum_j * len(list_i)

                # ... number of non vanishing basis per element
                nen = (lpi_p[0] + 1) * (lpi_p[1] + 1)
                # ...

                # ... global index for each local basis function
                Mat_LM = local_LM[:,i_elt]
                Mat_LM = np.ravel(Mat_LM, order='F')
                # ...

                # ... local Bezier-extraction matrix
                Mat_Bform = lmatrices[i_elt]
                Mat_Bform = np.ravel(Mat_Bform, order='F')
                # ...

                bernstein_representationData = [[i_elt+1, nen], Mat_LM, Mat_Bform]
                list_bernstein_representationData.append(bernstein_representationData)
    # ...
    return list_bernstein_representationData
    # .................................................

def save_bernstein_representation_2d(geo, filename):
    list_bernstein_representationData = get_bernstein_representation_2d(geo)

    # .................................................
    # ... exporting files
    fmt_int   = '%d'
    fmt_float = '%.15f'
    # .................................................

    # .................................................
    a = open(filename+"_bernstein_representation.txt", "w")
    # ... write size of list_bernstein_representationData
    a.write(str(len(list_bernstein_representationData))+' \n')
    for multiL in list_bernstein_representationData:
        # ... element id  and  number of non vanishing basis per element
        L = multiL[0]
        line = str(L[0]) + ", "+ str(L[1]) +  ' \n'
        a.write(line)
        # ... local LM
        L = multiL[1]
        line = ''.join(str(fmt_int % e)+', ' for e in L[:])[:-2]+' \n'
        a.write(line)
        # ... local B-form
        L = multiL[2]
        line = ''.join(str(fmt_float % e)+', ' for e in L[:])[:-2]+' \n'
        a.write(line)
    a.close()
    # ...
    # .................................................

# ...
def save_bernstein_basis_2d(geo, basename=None, quad_rule="legendre", nderiv=1):
    filename_quad   = "quadrature.txt"
    filename_values = "bernstein_values.txt"
    if basename is not None:
        filename_quad   = basename + "_" + "quadrature.txt"
        filename_values = basename + "_" + "bernstein_values.txt"

    nrb = geo[0]
    px = nrb.degree[0] ; py = nrb.degree[1]

    # ... create a Bezier patch of the given polynomial degrees
    Bx = bernstein(px)
    By = bernstein(px)
    qd = quadratures()
    xint = np.asarray([0.,1.])
    yint = np.asarray([0.,1.])
    [x,wx] = qd.generate(xint, px, quad_rule)
    [y,wy] = qd.generate(yint, py, quad_rule)
    x = x[0] ; wx = wx[0]
    y = y[0] ; wy = wy[0]
    Batx = Bx.evaluate(x, der=nderiv)
    Baty = By.evaluate(y, der=nderiv)

    lpi_p = np.asarray([px,py])

    # .................................................
    a = open(filename_quad, "w")
    # ... write spline degrees
    line = str(lpi_p[0]) + ', ' + str(lpi_p[1]) + ' \n'
    a.write(line)
    # ... write gauss points and their weights
    for _y,_wy in zip(y,wy):
        for _x,_wx in zip(x,wx):
            line = str(_x) + ', ' + str(_y) + ', ' + str(_wx*_wy)
            line = line + ' \n'
            a.write(line)
    a.close()
    # .................................................

    # .................................................
    a = open(filename_values, "w")
    # ... write spline degrees    and     n derivaties
    line = str(lpi_p[0]) + ', ' + str(lpi_p[1]) + ', ' + str(nderiv) + ' \n'
    a.write(line)
    # ... write gauss points and their weights
    for j in range(0, py+1):
        for i in range(0, px+1):
            for jy in range(0,py+1):
                for ix in range(0,px+1):
                    line = " "
                    for dy in range(0,nderiv+1):
                        for dx in range(0,nderiv+1):
                            B = Batx[i,ix,dx] * Baty[j,jy,dy]
                            line += str(B) + ', '
                    line = line[:-2] + ' \n'
                    a.write(line)
    a.close()
    # .................................................
# ...


########################################################################

class BZR(object):
    def __init__(self):
        pass

    def write(self, name, geo, fmt="txt"):
        # ...
        if geo.dim == 2:
            save_nodes_2d(geo, name)
            save_nodes_bezier_2d(geo, name)
            save_nodes_sons_2d(geo, name)
            save_elements_2d(geo, name)
            save_elements_bezier_2d(geo, name)
            save_elements_sons_2d(geo, name)
            save_bernstein_representation_2d(geo, name)
            save_bernstein_basis_2d(geo, basename=name)

        # ...
        def exportAdditionalInfo(geo, filename):
            fo = open(filename, "w")
            # ... Rd
            fo.write("# Rd")
            fo.write("\n")
            txt = str(geo.Rd)
            fo.write(txt)
            fo.write("\n")
            # ...

            # ... dim
            fo.write("# dim")
            fo.write("\n")
            txt = str(geo.dim)
            fo.write(txt)
            fo.write("\n")
            # ...

            # ... number of patchs
            fo.write("# npatchs")
            fo.write("\n")
            txt = str(geo.npatchs)
            fo.write(txt)
            fo.write("\n")
            # ...

            # ... external_faces
            fo.write("# external_faces")
            fo.write("\n")
            for data in geo.external_faces:
                txt = str(data)[1:-1]
                fo.write(txt)
                fo.write("\n")
            # ...

            # ... internal_faces
            fo.write("# internal_faces")
            fo.write("\n")
            for data in geo.internal_faces:
                txt = str(data)[1:-1]
                fo.write(txt)
                fo.write("\n")
            # ...

            # ... connectivity
            fo.write("# connectivity")
            fo.write("\n")
            for dic in geo.connectivity:
                for key, data in dic.items():
                    label = key
                    fo.write(label)
                    fo.write("\n")
                    txt   = str(data)[1:-1]
                    fo.write(txt)
                    fo.write("\n")
            # ...

            fo.close()
        # ...

        # ...
        _name = name.split('.')[0]
        if fmt == "zip":
            import os
            os.system("mkdir " + _name)

        if fmt == "zip":
            filename = _name + "/" + "info.txt"
        if fmt == "txt":
            filename = _name + "_" + "info.txt"
        exportAdditionalInfo(geo, filename)
        # ...

        # ...
        if fmt == "zip":
            from contextlib import closing
            from zipfile import ZipFile, ZIP_DEFLATED
            import os

            # ...
            def zipdir(basedir, archivename):
                assert os.path.isdir(basedir)
                with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
                    for root, dirs, files in os.walk(basedir):
                        #NOTE: ignore empty directories
                        for fn in files:
                            absfn = os.path.join(root, fn)
                            zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
                            z.write(absfn, zfn)
            # ...
            basedir = _name
            archivename = name
            zipdir(basedir, archivename)
            os.system("rm -R " + _name)
        # ...

