import numpy as np
from igakit.nurbs import NURBS
from numpy.linalg import inv as matrix_inverse

# ...
try:
    import f90nml
    F90NML=True
except ImportError:
    F90NML=False
# ...

__all__ = ['XML', 'formatter', 'TXT', 'BZR','NML', "geopdes"]

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
                print(("Exception _get_data, invalid tag : ", TAG))
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
                                raise NotImplementedError("Operator not yet implemented")

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
        for TAG, txt in list(geo.attributs.items()):
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
            print(("Warning: wrong or bad values for ", TAG))
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
            for TAG, txt in list(nrb.attributs.items()):
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
                for key, data in list(dic.items()):
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
def remove_duplicates( lst ):
    no_dups = []
    for i in lst:
        if i not in no_dups:
            no_dups.append(i)
    return no_dups

class NML(object):

    def __init__(self):
        pass

    def read(self, filename, geo):
        if not F90NML:
            raise ImportError("f90nml not installed. Please use another input/output driver.")

        nml = f90nml.read(filename)
        d_dim = nml['d_dimension']['d_dim']
        p_dim = len(nml['degree'])

        if p_dim >=1:
            p_u = nml['degree']['spline_deg1']
        if p_dim >=2:
            p_v = nml['degree']['spline_deg2']
        if p_dim >=3:
            p_w = nml['degree']['spline_deg3']

        if p_dim >=1:
            n_u = nml['shape']['num_pts1']
        if p_dim >=2:
            n_v = nml['shape']['num_pts2']
        if p_dim >=3:
            n_w = nml['shape']['num_pts3']

        if p_dim >=1:
            knots_u = nml['knots_1']['knots1']
        if p_dim >=2:
            knots_v = nml['knots_2']['knots2']
        if p_dim >=3:
            knots_w = nml['knots_3']['knots3']

        knots = []
        if p_dim >=1:
            knots_u = np.array(knots_u)
            knots.append(knots_u)
        if p_dim >=2:
            knots_v = np.array(knots_v)
            knots.append(knots_v)
        if p_dim >=3:
            knots_w = np.array(knots_w)
            knots.append(knots_w)

        if d_dim >=1:
            ctrl_pts_x = nml['control_points_1']['control_pts1']
            ctrl_pts_x = np.array(ctrl_pts_x)
        if d_dim >=2:
            ctrl_pts_y = nml['control_points_2']['control_pts2']
            ctrl_pts_y = np.array(ctrl_pts_y)
        if d_dim >=3:
            ctrl_pts_z = nml['control_points_3']['control_pts3']
            ctrl_pts_z = np.array(ctrl_pts_z)

        _weights = None
        try:
            _weights = nml['control_weights']['weights']
            _weights = np.array(_weights)
        except:
            if p_dim ==1:
                weights = np.ones(n_u)
            if p_dim ==2:
                weights = np.ones((n_u,n_v))
            if p_dim ==3:
                weights = np.ones((n_u,n_v,n_w))

        if p_dim ==1:
            control_points = np.zeros((n_u, 3))
            control_points[:,0] = ctrl_pts_x
            if d_dim > 1:
                control_points[:,1] = ctrl_pts_y
            if d_dim > 2:
                control_points[:,2] = ctrl_pts_z

            if _weights is not None:
                weights = _weights

        if p_dim ==2:
            control_points = np.zeros((n_u, n_v, 3))
            I = 0
            for j in range(0, n_v):
                for i in range(0, n_u):
                    control_points[i,j,0] = ctrl_pts_x[I]
                    I += 1
            if d_dim > 1:
                I = 0
                for j in range(0, n_v):
                    for i in range(0, n_u):
                        control_points[i,j,1] = ctrl_pts_y[I]
                        I += 1
            if d_dim > 2:
                I = 0
                for j in range(0, n_v):
                    for i in range(0, n_u):
                        control_points[i,j,2] = ctrl_pts_z[I]
                        I += 1

            if _weights is not None:
                weights = np.zeros((n_u, n_v))
                I = 0
                for j in range(0, n_v):
                    for i in range(0, n_u):
                        weights[i,j] = _weights[I]
                        I += 1

            weights = np.array(weights).reshape((n_u,n_v))

        if p_dim ==3:
            control_points = np.zeros((n_u, n_v, n_w, 3))
            I = 0
            for k in range(0, n_w):
                for j in range(0, n_v):
                    for i in range(0, n_u):
                        control_points[i,j,k,0] = ctrl_pts_x[I]
                        I += 1
            if d_dim > 1:
                I = 0
                for k in range(0, n_w):
                    for j in range(0, n_v):
                        for i in range(0, n_u):
                            control_points[i,j,k,1] = ctrl_pts_y[I]
                            I += 1
            if d_dim > 2:
                I = 0
                for k in range(0, n_w):
                    for j in range(0, n_v):
                        for i in range(0, n_u):
                            control_points[i,j,k,2] = ctrl_pts_z[I]
                            I += 1

            if _weights is not None:
                weights = np.zeros((n_u, n_v, n_w))
                I = 0
                for k in range(0, n_w):
                    for j in range(0, n_v):
                        for i in range(0, n_u):
                            weights[i,j,k] = _weights[I]
                            I += 1

        from caid.cad_geometry import cad_nurbs

#        print "knots : ", knots
#        print "points : ", control_point
        nrb = cad_nurbs(knots, control=control_points, weights=weights)
        geo.append(nrb)

    def write(self, name, geo):
        # ...
        d_dim = geo.Rd
        def exportPatch(nrb, filename):
            fo = open(filename, "w")

            # ...
            fo.write("&transf_label\n")
            fo.write("    label = "+"\""+filename+"\""+"\n")
            fo.write("/" + "\n\n")
            # ...

            # ...
            fo.write("&d_dimension\n")
            fo.write("    d_dim = "+str(d_dim)+"\n")
            fo.write("/" + "\n\n")
            # ...

            # ... write degree
            fo.write("&degree\n")
            fo.write("    spline_deg1 = " +str(nrb.degree[0])  +"\n")
            if nrb.dim >= 2:
                fo.write("    spline_deg2 = " + str(nrb.degree[1]) +"\n")
            if nrb.dim == 3:
                fo.write("    spline_deg3 = " + str(nrb.degree[2]) +"\n")
            fo.write("/" + "\n\n")
            # ...

            # ... write shape
            fo.write("&shape\n")
            fo.write("    num_pts1 = " + str(nrb.shape[0]) +"\n")
            if nrb.dim >= 2:
                fo.write("    num_pts2 = " + str(nrb.shape[1])+"\n")
            if nrb.dim == 3:
                fo.write("    num_pts3 = " + str(nrb.shape[2])+"\n")
            fo.write("/" + "\n\n")
            # ...

            # ... write rational
            fo.write("&rational\n")
            if nrb.rational:
                txt = "1"
            else:
                txt = "0"
            fo.write("    is_rational = "+txt+"\n")
            fo.write("/" + "\n\n")
            # ...

            # ... write knots
            txt = str(nrb.knots[0])[1:-1]

            cartesian_mesh_locations1=remove_duplicates(nrb.knots[0])

            fo.write("&knots_1\n")
            fo.write("    knots1"" = "+txt+"\n")
            fo.write("/" + "\n\n")

            if nrb.dim >= 2:
                txt = str(nrb.knots[1])[1:-1]
                cartesian_mesh_locations2=remove_duplicates(nrb.knots[1])
                fo.write("&knots_2\n")
                fo.write("    knots2 = "+txt+"\n")
                fo.write("/" + "\n\n")
            if nrb.dim == 3 :
                txt = str(nrb.knots[2])[1:-1]
                cartesian_mesh_locations3=remove_duplicates(nrb.knots[2])
                fo.write("&knots_3\n")
                fo.write("    knots3 = "+txt+"\n")
                fo.write("/" + "\n\n")
            # ...

            # ... write Control Points
            n = nrb.shape
            x1 = []
            x2 = []
            x3 = []

            if nrb.dim == 1:
                for i in range(0, n[0]):
                    x1.append(str(nrb.points[i,0])+' ')
                fo.write("&control_points_1\n")
                fo.write("\n")
                fo.write("    control_pts1 = "+" ".join(x1)+"\n")
                fo.write("/" + "\n\n")

                if d_dim > 1:
                    for i in range(0, n[0]):
                        x2.append(str(nrb.points[i,1])+' ')
                    fo.write("&control_points_2\n")
                    fo.write("\n")
                    fo.write("    control_pts2 = "+" ".join(x2)+"\n")
                    fo.write("/" + "\n\n")

                if d_dim > 2:
                    for i in range(0, n[0]):
                        x3.append(str(nrb.points[i,2])+' ')
                    fo.write("&control_points_3\n")
                    fo.write("\n")
                    fo.write("    control_pts3 = "+" ".join(x3)+"\n")
                    fo.write("/" + "\n\n")


            if nrb.dim == 2:
                for j in range(0, n[1]):
                    for i in range(0, n[0]):
                        x1.append(str(nrb.points[i,j,0])+' ')
                fo.write("&control_points_1\n")
                fo.write("\n")
                fo.write("    control_pts1 = "+" ".join(x1)+"\n")
                fo.write("/" + "\n\n")

                if d_dim > 1:
                    for j in range(0, n[1]):
                        for i in range(0, n[0]):
                            x2.append(str(nrb.points[i,j,1])+' ')
                    fo.write("&control_points_2\n")
                    fo.write("\n")
                    fo.write("    control_pts2 = "+" ".join(x2)+"\n")
                    fo.write("/" + "\n\n")

                if d_dim > 2:
                    for j in range(0, n[1]):
                        for i in range(0, n[0]):
                            x3.append(str(nrb.points[i,j,1])+' ')
                    fo.write("&control_points_3\n")
                    fo.write("\n")
                    fo.write("    control_pts3 = "+" ".join(x3)+"\n")
                    fo.write("/" + "\n\n")

            if nrb.dim == 3:
                for k in range(0, n[2]):
                    for j in range(0, n[1]):
                        for i in range(0, n[0]):
                            txt = str(nrb.points[i,j,k,:])[1:-1]
                            x1.append(str(nrb.points[i,j,k,0])+' ')
                fo.write("&control_points_1\n")
                fo.write("\n")
                fo.write("    control_pts1 = "+" ".join(x1)+"\n")
                fo.write("/" + "\n\n")

                if d_dim > 1:
                    for k in range(0, n[2]):
                        for j in range(0, n[1]):
                            for i in range(0, n[0]):
                                txt = str(nrb.points[i,j,k,:])[1:-1]
                                x2.append(str(nrb.points[i,j,k,1])+' ')
                    fo.write("&control_points_2\n")
                    fo.write("\n")
                    fo.write("    control_pts2 = "+" ".join(x2)+"\n")
                    fo.write("/" + "\n\n")

                if d_dim > 2:
                    for k in range(0, n[2]):
                        for j in range(0, n[1]):
                            for i in range(0, n[0]):
                                txt = str(nrb.points[i,j,k,:])[1:-1]
                                x3.append(str(nrb.points[i,j,k,2])+' ')
                    fo.write("&control_points_3\n")
                    fo.write("\n")
                    fo.write("    control_pts3 = "+" ".join(x3)+"\n")
                    fo.write("/" + "\n\n")
            # ...

            # ... write weights
            n = nrb.shape
            wgts = []
            if nrb.dim == 1:
                for i in range(0, n[0]):
                    txt = str(nrb.weights[i])
                    wgts.append(txt)
            if nrb.dim == 2:
                for j in range(0, n[1]):
                    for i in range(0, n[0]):
                        txt = str(nrb.weights[i,j])
                        wgts.append(txt)
            if nrb.dim == 3:
                for k in range(0, n[2]):
                    for j in range(0, n[1]):
                        for i in range(0, n[0]):
                            txt = str(nrb.weights[i,j,k])
                            wgts.append(txt)

            fo.write("&control_weights\n")
            fo.write("\n")
            fo.write("    weights = "+" ".join(wgts)+"\n")
            fo.write("/" + "\n\n")
            # ...

            # ...
            # add information relevant to the construction of the logical mesh.
            if nrb.dim == 1:
                fo.write("&cartesian_mesh_1d\n")
            if nrb.dim == 2:
                fo.write("&cartesian_mesh_2d\n")
            if nrb.dim == 3:
                fo.write("&cartesian_mesh_3d\n")

            nc1 = len(cartesian_mesh_locations1) - 1
            fo.write("    number_cells1 = " + str(nc1) + "\n")
            if nrb.dim >= 2:
                nc2 = len(cartesian_mesh_locations2) - 1
                fo.write("    number_cells2 = " + str(nc2) + "\n")
            if nrb.dim == 3:
                nc3 = len(cartesian_mesh_locations3) - 1
                fo.write("    number_cells3 = " + str(nc3) + "\n")
            fo.write("/" + "\n\n")

            fo.close()


        # ...
        _name = name.split('.')[0]
        for i in range(0, geo.npatchs):
            nrb = geo[i]
            filename = _name + "_" + "patch"+str(i)+".nml"
            exportPatch(nrb, filename)

        # ...

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
                # TODO ARA bc in case of periodic splines or duplication
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

def save_nodes_2d(geo, basename=None, dirname=None):
    filename = "nodes.txt"
    if basename is not None:
        filename = basename + "_" + filename
    if dirname is not None:
        filename = dirname + "/" + filename

    list_nodeData = get_nodes_2d(geo)

    # .................................................
    # ... exporting files
    fmt_nodes = '%d, %.15f, %.15f, %d'
    # .................................................

    # .................................................
    a = open(filename, "w")
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
                # TODO ARA bc in case of periodic splines or duplication
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

def save_nodes_bezier_2d(geo, basename=None, dirname=None):
    filename = "nodes_bezier.txt"
    if basename is not None:
        filename = basename + "_" + filename
    if dirname is not None:
        filename = dirname + "/" + filename

    list_nodeData = get_nodes_bezier_2d(geo)

    # .................................................
    # ... exporting files
    fmt_nodes = '%d, %.15f, %.15f, %d'
    # .................................................

    # .................................................
    a = open(filename, "w")
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

        nx_elt = len(nrb.breaks(0)) - 1
        ny_elt = len(nrb.breaks(1)) - 1
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

                elementData = [[i_elt+1], index_vertices, neighbours, lpi_p]

                lineElementData = []
                for data in elementData:
                    for d in data:
                        lineElementData.append(d)

                list_elementData.append(lineElementData)
    # ...
    return list_elementData
    # .................................................

def save_elements_2d(geo, basename=None, dirname=None):
    filename = "elements.txt"
    if basename is not None:
        filename = basename + "_" + filename
    if dirname is not None:
        filename = dirname + "/" + filename

    list_elementData = get_elements_2d(geo)

    # .................................................
    # ... exporting files
    fmt_int = '%d'
    # .................................................

    # .................................................
    a = open(filename, "w")
    # ... write size of list_elementData and number of vertex per element
    a.write(str(len(list_elementData)) + " , 4 " +' \n')

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

def save_elements_bezier_2d(geo, basename=None, dirname=None):
    filename = "elements_bezier.txt"
    if basename is not None:
        filename = basename + "_" + filename
    if dirname is not None:
        filename = dirname + "/" + filename

    list_elementData = get_elements_bezier_2d(geo)

    # .................................................
    # ... exporting files
    fmt_int = '%d'
    # .................................................

    # .................................................
    a = open(filename, "w")
    # ... write size of list_elementData and number of vertices per element
    a.write(str(len(list_elementData)) + " , 4 "+' \n')

    for L in list_elementData:
        line = ''.join(str(fmt_int % e)+', ' for e in L[0:])[:-2]+' \n'
        a.write(line)
    a.close()
    # .................................................

def get_sons_2d(geo):
    # ... sets the list of Nodes
    geo_ref, list_lmatrices = geo.bezier_extract()

    list_elementData = []

    max_n_elements = -1
    max_n_vertices = -1

    element_index = 0
    for nrb_ref, nrb in zip(geo_ref, geo):
        # ...
        # we loop over each element and generate the P,
        # ...
        # we start by matching the 1D index with the 2D one
        lpi_n = nrb_ref.shape
        lpi_p = nrb_ref.degree

        # .................................................
        nx_elt = len(nrb.breaks(0)) - 1
        ny_elt = len(nrb.breaks(1)) - 1
        list_i = list(range(0,nx_elt))
        list_j = list(range(0,ny_elt))
#        print "nxny ", nx_elt, ny_elt
        for elt_j in list_j:
            for elt_i in list_i:
                element_index += 1

                # compute index element index
                i_elt = elt_i + elt_j * len(list_i)

                # ... elements indices
                list_indices = []
                for _j in range(0, lpi_p[1]):
                    j = _j + lpi_p[1] * elt_j
                    for _i in range(0, lpi_p[0]):
                        i = _i + lpi_p[0] * elt_i

                        I = i + j * nx_elt * lpi_p[0]
#                        print element_index, I, _i,_j, i,j
                        list_indices.append(I+1)
                # ...

                # ... number of elements
                n_elements = len(list_indices)

                if (max_n_elements < n_elements):
                    max_n_elements = n_elements

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

                if (max_n_vertices < n_vertices):
                    max_n_vertices = n_vertices

                elementData = [[i_elt+1, n_elements, n_vertices], list_indices, list_nodes_indices]
                list_elementData.append(elementData)
        # ...
    return max_n_elements, max_n_vertices, list_elementData
    # .................................................

def save_sons_2d(geo, basename=None, dirname=None):
    filename = "sons.txt"
    if basename is not None:
        filename = basename + "_" + filename
    if dirname is not None:
        filename = dirname + "/" + filename

    max_n_elements, max_n_vertices, list_elementData = get_sons_2d(geo)

    # .................................................
    # ... exporting files
    fmt_int = '%d'
    # .................................................

    # .................................................
    a = open(filename, "w")
    # ... write size of list_nodeData
    nData        = len(list_elementData)
    line = str(nData) + ", "+ str(max_n_elements) + ", "+ str(max_n_vertices) +  ' \n'
    a.write(line)
    # ...

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

def get_bernstein_span_2d(geo):
    # .................................................
    from caid.numbering.connectivity import connectivity
    from caid.numbering.boundary_conditions import boundary_conditions

    # ... without bc
    con = connectivity(geo)
    con.init_data_structure()
    geo_ref, list_lmatrices = geo.bezier_extract()
    # ...

    # ... sets the list of Dirichlet Basis functions for each Element
    #     All external faces are set to Dirichlet
    list_DirFaces = []
    for i in range(0, geo.npatchs):
        list_DirFaces.append([])

    list_extFaces = geo.external_faces
    for extFaces in list_extFaces:
        patch_id    = extFaces[0]
        face_id     = extFaces[1]
        list_DirFaces[patch_id].append(face_id)
    # ...

    # ... with dirichlet bc
    con_dir = connectivity(geo)
    bc = boundary_conditions(geo)
    bc.dirichlet(geo, list_DirFaces)
    con_dir.init_data_structure(bc)
    # ...

    # ... max nen
    maxnen = -1
    for patch_id in range(0, geo.npatchs):
        nrb = geo[patch_id]
        lpi_p = nrb.degree
        nen = (lpi_p[0] + 1) * (lpi_p[1] + 1)
        if (nen > maxnen):
            maxnen = nen
    # ...

    # ... space dim
    dim_space = np.max(asarray((con.ID)))
    # ...

    # ... sets the list of connectivities
    list_bernstein_spanData = [[maxnen, dim_space]]

    for patch_id in range(0, geo.npatchs):
        nrb = geo[patch_id]
        lmatrices    = list_lmatrices[patch_id]
        local_LM     = con.LM[patch_id]
        local_LM_dir = con_dir.LM[patch_id]

        lpi_n = nrb.shape
        lpi_p = nrb.degree
        nx_elt = len(nrb.breaks(0)) - 1
        ny_elt = len(nrb.breaks(1)) - 1
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
                Mat_Bform = Mat_Bform.todense()
                Mat_Bform = np.ravel(Mat_Bform, order='F')
                # ...

                # ...
                Mat_LM_dir = local_LM_dir[:,i_elt]
                list_Dirichlet = np.zeros(nen, dtype=np.int)
                for enum_lm, lm in enumerate(Mat_LM_dir):
                    if lm == 0:
                        list_Dirichlet[enum_lm] = 1
                # ...


                bernstein_spanData = [[i_elt+1, nen], Mat_LM, Mat_Bform, list_Dirichlet]
                list_bernstein_spanData.append(bernstein_spanData)
    # ...
    return list_bernstein_spanData
    # .................................................

def save_bernstein_span_2d(geo, basename=None, dirname=None):
    filename = "bernstein_span.txt"
    if basename is not None:
        filename = basename + "_" + filename
    if dirname is not None:
        filename = dirname + "/" + filename

    list_bernstein_spanData = get_bernstein_span_2d(geo)

    # .................................................
    # ... exporting files
    fmt_int   = '%d'
    fmt_float = '%.15f'
    # .................................................

    # .................................................
    a = open(filename, "w")
    # ... write size of list_bernstein_spanData
    multiL    = list_bernstein_spanData[0]
    nData     = len(list_bernstein_spanData[1:])
    nen       = multiL[0]
    dim_space = multiL[1]
    line = str(nData) + ", "+ str(nen) + ", "+ str(dim_space) +  ' \n'
    a.write(line)
    # ...
    for multiL in list_bernstein_spanData[1:]:
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
        # ... dirichlet basis functions id
        L = multiL[3]
        line = ''.join(str(fmt_int % e)+', ' for e in L[:])[:-2]+' \n'
        a.write(line)
    a.close()
    # ...
    # .................................................

# ...
def save_bernstein_basis_2d(geo, quad_rule="legendre", nderiv=1, dirname=None):
    # .................................................
    # ... exporting files
    fmt_int   = '%d'
    fmt_float = '%.15f'
    # .................................................
    filename_quad   = "quadrature.txt"
    filename_values = "bernstein_values.txt"
    if dirname is not None:
        filename_quad   = dirname + "/" + "quadrature.txt"
        filename_values = dirname + "/" + "bernstein_values.txt"

    nrb = geo[0]
    px = nrb.degree[0] ; py = nrb.degree[1]

    # ... create a Bezier patch of the given polynomial degrees
    nderiv_x = min(nderiv+1, px)
    nderiv_y = min(nderiv+1, py)

    Bx = bernstein(px)
    By = bernstein(py)
    qd = quadratures()
    xint = np.asarray([0.,1.])
    yint = np.asarray([0.,1.])
    qx = px ; qy = py
    [x,wx] = qd.generate(xint, qx, quad_rule)
    [y,wy] = qd.generate(yint, qy, quad_rule)
    x = x[0] ; wx = wx[0]
    y = y[0] ; wy = wy[0]
    Batx = Bx.evaluate(x, der=nderiv_x)
    Baty = By.evaluate(y, der=nderiv_y)

    lpi_p = np.asarray([px,py])

    # .................................................
    a = open(filename_quad, "w")
    # ... write spline degrees
    npts = (qx+1) * (qy+1)
    line = str(npts) + ' \n'
    a.write(line)
    # ... write gauss points and their weights
    for _y,_wy in zip(y,wy):
        for _x,_wx in zip(x,wx):
            _wxy = _wx * _wy
            line = str(fmt_float % _x) + ', ' + str(fmt_float % _y) + ', ' + str(fmt_float % _wxy)
            line = line + ' \n'
            a.write(line)
    a.close()
    # .................................................

    # .................................................
    a = open(filename_values, "w")
    # ... write spline degrees    and     n derivaties
    nen = (lpi_p[0]+1) * (lpi_p[1]+1)
    line = str(nen) + ', ' + str(nderiv_x) + ' \n'
    a.write(line)
    # ... write gauss points and their weights
    # loop over Bernstein polynomials
    for j in range(0, py+1):
        for i in range(0, px+1):
            # loop over quadrature points
            for jy in range(0,py+1):
                for ix in range(0,px+1):
                    line = " "
                    # loop over derivatives
                    # B_0_0
                    dx = 0 ; dy = 0
                    B = Batx[i,ix,dx] * Baty[j,jy,dy]
                    line += str(fmt_float % B) + ', '
                    # B_x_0
                    dx = 1 ; dy = 0
                    B = Batx[i,ix,dx] * Baty[j,jy,dy]
                    line += str(fmt_float % B) + ', '
                    # B_0_y
                    dx = 0 ; dy = 1
                    B = Batx[i,ix,dx] * Baty[j,jy,dy]
                    line += str(fmt_float % B) + ', '
                    # B_x_y
                    dx = 1 ; dy = 1
                    B = Batx[i,ix,dx] * Baty[j,jy,dy]
                    line += str(fmt_float % B) + ', '
                    if (nderiv_x > 1) and (nderiv_y > 1):
                        # B_xx_0
                        dx = 2 ; dy = 0
                        B = Batx[i,ix,dx] * Baty[j,jy,dy]
                        line += str(fmt_float % B) + ', '
                        # B_0_yy
                        dx = 0 ; dy = 2
                        B = Batx[i,ix,dx] * Baty[j,jy,dy]
                        line += str(fmt_float % B) + ', '

#                    for dy in range(0,nderiv+2):
#                        for dx in range(0,nderiv+2):
#                            B = Batx[i,ix,dx] * Baty[j,jy,dy]
#                            line += str(B) + ', '
                    line = line[:-2] + ' \n'
                    a.write(line)
    a.close()
    # .................................................
# ...

########################################################################

class BZR(object):
    def __init__(self):
        pass

    def write(self, geo, fmt="txt", basename=None, dirname=None, basis_only=False):
        # ...
        print("xxxxx degree " , geo[0].degree)
        if geo.dim == 1:
            raise NotImplementedError("Not yet implemented")

        if geo.dim == 2:
            if not basis_only:
                save_nodes_2d(geo, basename=basename, dirname=dirname)
                save_nodes_bezier_2d(geo, basename=basename, dirname=dirname)
                save_elements_2d(geo, basename=basename, dirname=dirname)
                save_elements_bezier_2d(geo, basename=basename, dirname=dirname)
                save_sons_2d(geo, basename=basename, dirname=dirname)
            save_bernstein_span_2d(geo, basename=basename, dirname=dirname)
            save_bernstein_basis_2d(geo, dirname=dirname)

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
                for key, data in list(dic.items()):
                    label = key
                    fo.write(label)
                    fo.write("\n")
                    txt   = str(data)[1:-1]
                    fo.write(txt)
                    fo.write("\n")
            # ...

            fo.close()
        # ...

        if not basis_only:
            # ...
            if fmt == "zip":
                import os
                os.system("mkdir " + dirname)

            if fmt == "zip":
                _filename = "info.txt"
                if basename is not None:
                    _filename = basename + "_" + _filename
                if dirname is not None:
                    _filename = dirname + "/" + _filename
            if fmt == "txt":
                _filename = "info.txt"
                if basename is not None:
                    _filename = basename + "_" + _filename
                if dirname is not None:
                    _filename = dirname + "/" + _filename
            exportAdditionalInfo(geo, _filename)
            # ...

            # ...
            if fmt == "zip":
                if dirname is None:
                    raise ValueError("Error: dirname must be given.")

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
                basedir = dirname
                archivename = dirname
                zipdir(basedir, archivename)
                os.system("rm -R " + _name)
            # ...
















# ...
def geopdes_to_caid_faces_2d(value):
    i_face = None
    if value == 0:
        i_face = 1
    if value == 1:
        i_face = 3
    if value == 2:
        i_face = 2
    if value == 3:
        i_face = 4

    return i_face
# ...

# ...
class Writer(object):

    def __init__(self, filename=None):
        self._lines = []
        self._filename = filename
        self._f = None

    @property
    def filename(self):
        return self._filename

    def add_line(self, data, dtype='i', top=False):
        # .................................................
        # ... exporting files
        fmt_int   = '%d'
        fmt_float = '%.15f'
        # .................................................
        line = None
        if dtype == 'i':
            line = ''.join(str(fmt_int % e)+' ' for e in data[:])+' \n'
        elif dtype == 'd':
            line = ''.join(str(fmt_float % e)+' ' for e in data[:])+' \n'
        elif dtype == 's':
            line = data

        if line is not None:
            if top:
                self._lines.reverse()
                self._lines.append(line)
                self._lines.reverse()
            else:
                self._lines.append(line)

    def open(self):
        self._f = open(self.filename, "w")

    def close(self):
        self._f.close()

    def write(self, line=None):
        if line is None:
            for L in self._lines:
                self._f.write(L)
        else:
            self._f.write(line)
# ...

# ...
class Writer_geopdes(object):
    def __init__(self, filename, geo):
        self._geometry = geo
        writer = Writer(filename)
        self._writer = writer

    @property
    def geometry(self):
        return self._geometry

    @property
    def writer(self):
        return self._writer

    def open(self):
        self.writer.open()

    def close(self):
        self.writer.close()

    def write(self):
        self.writer.write()

    def add_patch(self, i_patch):
        geo = self.geometry
        writer = self.writer

        nrb = geo[i_patch]
        line = "PATCH " + str(i_patch+1)+'\n'
        writer.add_line(line, dtype='s')
        # p(i): the degree in each Cartesian direction (ndim integers)
        writer.add_line(nrb.degree, dtype='i')
        # ncp(i): the number of control points in each direction (ndim integers)
        writer.add_line(nrb.shape, dtype='i')
        # knots{i}: knot sequence in the Cartesian direction (ncp(i)+p(i)+1 floats)
        for axis in range(0, geo.dim):
            writer.add_line(nrb.knots[axis], dtype='d')
        total_size = np.asarray(nrb.shape).prod()
        # cp_x, cp_y, cp_z: coordinates of the weighted control points
        #   (see Section 4.2 of The NURBS Book, L. Piegl & W. Tiller)
        #   (rdim rows, each one with prod_{i=1}^{N} ncp(i) float values)
        #
        # The control points are numbered in a reverse lexicographic order: starting
        #  from the origin, we first increase the parametric coordinate x_1 and then
        #  the parametric coordinate x_2 (and for 3D cases, then the coordinate x_3).
        for d in range(0, geo.Rd):
            points = nrb.points[...,d].reshape(total_size)
            writer.add_line(points, dtype='d')
        # weights: weight associated to each basis function (or control point)
        #          (prod(ncp ) float values)
        weights = nrb.weights[...].reshape(total_size)
        writer.add_line(weights, dtype='d')

    def add_patchs(self):
        geo = self.geometry
        for i_patch in range(0, geo.npatchs):
            self.add_patch(i_patch)

    def add_interfaces(self):
        geo = self.geometry
        writer = self.writer

        for enum, interface in enumerate(geo.connectivity):
            line = "INTERFACE " + str(enum+1) + "\n"
            writer.add_line(line, dtype='s')
            for key, value in interface.items():
                i_patch = value[0]+1
                i_face = geopdes_to_caid_faces_2d(value[1])
                data = [i_patch, i_face]
                writer.add_line(data, dtype='i')
            # ... TODO add orientation, for the moment it is supposed to be the same
            data = [1]
            writer.add_line(data, dtype='i')
            # ...

    def add_subdomains(self):
        geo = self.geometry
        writer = self.writer

        # TODO : add color/subdomain notion
        enum = 0
        line = "SUBDOMAIN " + str(enum+1) + "\n"
        writer.add_line(line, dtype='s')
        list_patchs = list(range(1, geo.npatchs+1))
        writer.add_line(list_patchs, dtype='i')

    def add_boundaries(self, tol=1.e-7):
        geo = self.geometry
        writer = self.writer

        # ...
        n_ext_bnd = len(geo.external_faces)
        list_parent = list(range(0,n_ext_bnd))
        list_is_master = np.ones(n_ext_bnd, dtype=np.int)
        list_global_bnd = []
        for i in range(0, n_ext_bnd):
            list_global_bnd.append([])
        for i_m in range(0, n_ext_bnd-1):
            i_patch_m = geo.external_faces[i_m][0]
            i_face_m  = geo.external_faces[i_m][1]

            nrb_m = geo[i_patch_m]
            bnd_m = nrb_m.extract_face(i_face_m).clone()

            u_m = np.linspace(bnd_m.knots[0][0],bnd_m.knots[0][-1], 2)
            P_m = bnd_m(u_m)
            D_m = bnd_m.gradient(u=u_m)

            i_face = geopdes_to_caid_faces_2d(i_face_m)
            list_i_bnd = [[i_patch_m+1, i_face]]
            for i_s in range(i_m+1, n_ext_bnd):
                i_patch_s = geo.external_faces[i_s][0]
                i_face_s  = geo.external_faces[i_s][1]

                nrb_s = geo[i_patch_s]
                bnd_s = nrb_s.extract_face(i_face_s).clone()

                u_s = np.linspace(bnd_s.knots[0][0],bnd_s.knots[0][-1], 2)
                P_s = bnd_s(u_s)
                D_s = bnd_s.gradient(u=u_s)

                i_bnd_m = None
                i_bnd_s = None
                if np.allclose(P_m[0], P_s[0], rtol=0, atol=tol) :
                    i_bnd_m = 0
                    i_bnd_s = 0
                if np.allclose(P_m[0], P_s[1], rtol=0, atol=tol) :
                    i_bnd_m = 0
                    i_bnd_s = 1
                if np.allclose(P_m[1], P_s[0], rtol=0, atol=tol) :
                    i_bnd_m = 1
                    i_bnd_s = 0
                if np.allclose(P_m[1], P_s[1], rtol=0, atol=tol) :
                    i_bnd_m = 1
                    i_bnd_s = 1

                if (i_bnd_m is not None) and (i_bnd_s is not None):
                    # ... TODO test alignement instead of the equality of the gradient
                    condition = np.allclose(D_m[i_bnd_m].reshape(3)[:geo.Rd], \
                                            D_s[i_bnd_s].reshape(3)[:geo.Rd], \
                                            rtol=0., atol=tol)
                    condition = condition or np.allclose(D_m[i_bnd_m].reshape(3)[:geo.Rd], \
                                            -D_s[i_bnd_s].reshape(3)[:geo.Rd], \
                                            rtol=0., atol=tol)

                    if condition:
                        i_face = geopdes_to_caid_faces_2d(i_face_s)
                        list_i_bnd.append([i_patch_s+1, i_face])
                        list_parent[i_s] = i_m
                        list_is_master[i_s] = 0

            i_parent = list_parent[i_m]
            for pf in list_i_bnd:
                if not (pf in list_global_bnd[i_parent]):
                    list_global_bnd[i_parent].append(pf)
        # ...

        # ...
        enum = 0
        for G, is_master in zip(list_global_bnd, list_is_master):
            if is_master == 1:
                enum += 1
                line = "BOUNDARY " + str(enum) + "\n"
                writer.add_line(line, dtype='s')
                line = str(len(G)) + "\n"
                writer.add_line(line, dtype='s')
                for data in G:
                    writer.add_line(data, dtype='i')
        # ...

    def add_info(self):
        #  ndim : dimension of the parametric domain
        #  rdim : dimension of the physical domain
        #  Np: number of patches to construct the geometry
        #  Ni: total number of interfaces, each one connecting two patches
        #  Ns: total number of subdomains, formed by the union of patches

        geo = self.geometry
        writer = self.writer

        data = np.zeros(5, dtype=np.int)
        data[0] = geo.dim
        data[1] = geo.Rd
        data[2] = geo.npatchs
        data[3] = len(geo.connectivity)
        data[4] = 1 # TODO must use the number of colors

        writer.add_line(data, dtype='i', top=True)

    def add_header(self):
        geo = self.geometry
        writer = self.writer

        header  = "# this geometry has been automaticaly generated by CAID \n"
        header += "# to report bugs please contact : ratnaniahmed@gmail.com \n"
        writer.add_line(header, dtype='s', top=True)
# ...


class geopdes(object):
    def __init__(self):
        self._list_begin_line = []

        self._n_lines_per_patch = 0

    def read(self, filename, geo=None):
        from caid.cad_geometry import cad_geometry, cad_nurbs
        if geo is None:
            geo = cad_geometry()

        f = open(filename)
        lines = f.readlines()
        f.close()

        _lines = []
        for line in lines:
            if line[0].strip() != "#":
                _lines.append(line)
        lines = _lines
        data = self._read_header(lines[0])
        n_dim = data[0]
        r_dim = data[1]
        n_patchs = data[2]

        geo.set_r_dim(r_dim)

        if n_dim == 2:
            self._n_lines_per_patch = 2 + 2 + 3
        else:
            raise ValueError("Only 2d patchs are used for the moment")

        self._list_begin_line = self._get_begin_line(lines, n_patchs)

        for i_patch in range(0, n_patchs):
            cad_nrb = self._read_patch(lines, i_patch+1)
            geo.append(cad_nrb)

        return geo

    def write(self, filename, geo):
        writer_geopdes = Writer_geopdes(filename, geo)
        writer_geopdes.open()
        writer_geopdes.add_patchs()
        writer_geopdes.add_interfaces()
        writer_geopdes.add_subdomains()
        writer_geopdes.add_boundaries()
        writer_geopdes.add_info()
        writer_geopdes.add_header()
        writer_geopdes.write()
        writer_geopdes.close()

    # ...
    def _read_header(self, line):
        chars = line.split(" ")
        data  = []
        for c in chars:
            try:
                data.append(int(c))
            except:
                pass
        return data
    # ...

    # ...
    def _extract_patch_line(self, lines, i_patch):
        text = "PATCH " + str(i_patch)
        for i_line,line in enumerate(lines):
            r = line.find(text)
            if r != -1:
                print(">> find patch ", i_patch, " at the line number ", i_line)
                return i_line
        return None
    # ...

    # ...
    def _get_begin_line(self, lines, n_patchs):
        list_begin_line = []
        for i_patch in range(0, n_patchs):
            r = self._extract_patch_line(lines, i_patch+1)
            if r is not None:
                list_begin_line.append(r)
            else:
                raise ValueError("Seriours error while parsing the input file")
        return list_begin_line
    # ...

    # ...
    def _read_line(self, line):
        chars = line.split(" ")
        data  = []
        for c in chars:
            try:
                data.append(int(c))
            except:
                try:
                    data.append(float(c))
                except:
                    pass
        return data
    # ...

    # ...
    def _read_patch(self, lines, i_patch):
        from caid.cad_geometry import cad_nurbs

        i_begin_line = self._list_begin_line[i_patch-1]
        data_patch = []
        for i in range(i_begin_line+1, i_begin_line+self._n_lines_per_patch+1):
            data_patch.append(self._read_line(lines[i]))
        degree = data_patch[0]
        shape  = data_patch[1]
        u      = np.array(data_patch[2])
        v      = np.array(data_patch[3])
        x      = np.array(data_patch[4])
        y      = np.array(data_patch[5])
        w      = np.array(data_patch[6])

        X = x.reshape(shape)
        Y = y.reshape(shape)
        W = w.reshape(shape)

        points = np.zeros((shape[0], shape[1], 3))
        points[:,:,0] = X
        points[:,:,1] = Y

        knots = [u,v]

        cad_nrb = cad_nurbs(knots, points, weights=W)
        return cad_nrb
    # ...


