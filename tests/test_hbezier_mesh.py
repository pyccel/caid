# coding: utf-8
from caid.core import hbezier
rgeo = 1.0; zgeo = 1.0; amin = 1.0; acentre=0.0; angle_start = 10.0; nr = 10; np = 5
coord2d, vertices, boundary, scales = hbezier.hbezier_polar.construct_grid(rgeo,zgeo,amin,acentre,angle_start,nr,np)
coord2d
