# -*- coding: UTF-8 -*-
#! /usr/bin/python

import numpy as np
from numpy import asarray, array, zeros, zeros_like
import sys
from scipy.interpolate import splev

class bernstein:
    def __init__(self, degree):
        self._degree = degree
        self._knots  = [0.] * (degree+1) + [1.] * (degree+1)
        self._knots  = asarray(self._knots)

    @property
    def degree(self):
        return self._degree

    @property
    def knots(self):
        return self._knots

    def evaluate(self, x, der=0):
        """evaluate b-spline first derivative starting at node i at x, d is the direction"""
        lpr_t = asarray(self.knots)
        li_k = self.degree
        n = self.degree + 1

        Batx = np.zeros((self.degree+1, len(x), der+1))
        for i in range(0, self.degree+1):
            c = zeros_like(lpr_t)
            if i < 0:
                c[n + i]=1.
            else:
                c[i]=1.
            for d in range(0, der+1):
                Batx[i,:,d] = splev(x,(lpr_t,c,li_k), der=d)
        return Batx

if __name__ == "__main__":
    from caid.cad_geometry import cad_geometry, square
    from caid.utils.quadratures import *

    try:
        px = int(sys.argv[1])
        py = int(sys.argv[2])
        nderiv = int(sys.argv[3])
    except:
        raise "Error: you should run this script as: python bernstein.py px py nderiv."

    # ... create a Bezier patch of the given polynomial degrees
    Bx = bernstein(px)
    By = bernstein(px)
    qd = quadratures()
    xint = np.asarray([0.,1.])
    yint = np.asarray([0.,1.])
    [x,wx] = qd.generate(xint, px, "legendre")
    [y,wy] = qd.generate(yint, py, "legendre")
    x = x[0] ; wx = wx[0]
    y = y[0] ; wy = wy[0]
    Batx = Bx.evaluate(x, der=nderiv)
    Baty = By.evaluate(y, der=nderiv)

    lpi_p = np.asarray([px,py])

    a = open("quadrature.txt", "w")
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
    #

    a = open("basis_values.txt", "w")
    # ... write spline degrees
    line = str(lpi_p[0]) + ', ' + str(lpi_p[1]) + ' \n'
    a.write(line)
    # ... write n derivaties
    a.write(str(nderiv)+' \n')
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
    #
