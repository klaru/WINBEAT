#! python3
import os, sys, math
from beatinc import *
from winbeatio import *

#procedure cmult(var c:complex;a,b:complex);
#procedure cdivide(var c:complex;a,b:complex);
#procedure cpolar(var magnitude,phase:real;a:complex);


# Complex multiply : c=ab 
def cmult(a, b):

    c[r] = a[r]*b[r] - a[i]*b[i]
    c[i] = a[r]*b[i] + a[i]*b[r]
    return c
# end cmult

# Complex divide
def cdivide(a, b):

    if (abs(b[r]) > sqrt(BIG)) or (abs(b[i]) > sqrt(BIG)) :
        c[r] = 0.0
        c[i] = 0.0
    #end if
    else :
        denominator = sqr(b[r]) + sqr(b[i])
        if (denominator == 0.0) :
            print('Divide by zero in cdivide')
        c[r] = (a[r]*b[r] + a[i]*b[i]) / denominator
        c[i] = (a[i]*b[r] - a[r]*b[i]) / denominator
    #end else
    return c
#end cdivide

# Complex to polar coordinates 
def cpolar(magnitude, a):
    if (abs(a[r]) > math.sqrt(BIG)) or (abs(a[i]) > math.sqrt(BIG)) :
        print('Overflow in cpolar')
    magnitude = math.sqrt( sqr(a[r]) + sqr(a[i]) )
    if (abs(a[r]) < SMALL) :
        if abs(a[i]) < SMALL :
            phase = 0.0
        else :
            if a[i] > 0.0 :
                phase = pi/2.0
            else :
                phase = -pi/2.0
            #end if
    #end if
    else :
        phase = arctan( a[i] / a[r] )
        if a[r] < 0 :
            if a[i] > 0 :
                phase = pi + phase 
            else :
                phase = phase - pi
    return magnitude, phase
    #end if
#end cpolar
