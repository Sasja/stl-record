#!/usr/bin/env python

from stl import mesh
import math
import numpy as np

height = 2.0
diameter = 300.0
holediam = 5.0


nAngles = 40000

def getSide( diam, nAngles = nAngles, height = height):
    print "getSide()"
    thetaStep = 2.0 * math.pi / nAngles
    allThetas = thetaStep * np.arange(0, nAngles)
    data = np.zeros(nAngles * 2, dtype=mesh.Mesh.dtype)
    for n, theta in enumerate(allThetas):
        if n%10000 == 0: print n
        sint = math.sin(theta)
        sintp = math.sin(theta + thetaStep)
        cost = math.cos(theta)
        costp = math.cos(theta + thetaStep)
        data['vectors'][2 * n] = np.array([
            [cost  * diam   , sint  * diam, -height  ],
            [cost  * diam   , sint  * diam, 0        ], 
            [costp * diam   , sintp * diam, -height  ]
        ])
        data['vectors'][2 * n + 1] = np.array([
            [costp * diam   , sintp * diam, 0        ],
            [cost  * diam   , sint  * diam, 0        ], 
            [costp * diam   , sintp * diam, -height  ]
        ])
    return data

def getDonut(outerD, innerD, nAngles = nAngles, height = 0):
    print "getDonut()"
    thetaStep = 2.0 * math.pi / nAngles
    allThetas = thetaStep * np.arange(0, nAngles)
    data = np.zeros(nAngles * 2, dtype=mesh.Mesh.dtype)
    for n, theta in enumerate(allThetas):
        if n%10000 == 0: print n
        sint = math.sin(theta)
        sintp = math.sin(theta + thetaStep)
        cost = math.cos(theta)
        costp = math.cos(theta + thetaStep)
        data['vectors'][2 * n] = np.array([
            [costp * outerD     , sintp * outerD  , height    ],
            [cost  * outerD     , sint  * outerD  , height    ], 
            [cost  * innerD     , sint  * innerD  , height    ]
        ])
        data['vectors'][2 * n + 1] = np.array([
            [costp * outerD     , sintp * outerD  , height    ],
            [costp * innerD     , sintp * innerD  , height    ], 
            [cost  * innerD     , sint  * innerD  , height    ]
        ])
    return data

def getCircularGroove( getDepth, getDisp, radius, space, angle = math.pi/2, height = 0):
    print "getCircularGroove()"
    thetaStep = 2.0 * math.pi / nAngles
    allThetas = thetaStep * np.arange(0, nAngles)
    data = np.zeros(nAngles * 8, dtype=mesh.Mesh.dtype)
    outerD = radius + space
    innerD = radius - space
    sinangle = math.sin(angle / 2.0)
    ra  = radius + space
    rap = radius + space
    re  = radius - space
    rep = radius - space
    for n, theta in enumerate(allThetas):
        if n%10000 == 0: print n
        sint = math.sin(theta)
        sintp = math.sin(theta + thetaStep)
        cost = math.cos(theta)
        costp = math.cos(theta + thetaStep)
        depth = getDepth(theta)
        depthp = getDepth(theta + thetaStep)
        disp = getDisp(theta)
        dispp = getDisp(theta + thetaStep)

        rb  = radius + depth  * sinangle + disp
        rbp = radius + depthp * sinangle + dispp
        rc  = radius + disp
        rcp = radius + dispp
        rd  = radius - depth  * sinangle + disp
        rdp = radius - depthp * sinangle + dispp

        
        #outer flat
        data['vectors'][8 * n + 0] = np.array([
            [cost  * ra     , sint  * ra  , height    ],
            [cost  * rb     , sint  * rb  , height    ], 
            [costp * rap    , sintp * rap , height    ]
        ])
        data['vectors'][8 * n + 1] = np.array([
            [costp * rbp    , sintp * rbp , height    ],
            [cost  * rb     , sint  * rb  , height    ], 
            [costp * rap    , sintp * rap , height    ]
        ])
        
        #inner flat
        data['vectors'][8 * n + 2] = np.array([
            [cost  * rd     , sint  * rd  , height    ],
            [cost  * re     , sint  * re  , height    ], 
            [costp * rdp    , sintp * rdp , height    ]
        ])
        data['vectors'][8 * n + 3] = np.array([
            [costp * rep    , sintp * rep , height    ],
            [cost  * re     , sint  * re  , height    ], 
            [costp * rdp    , sintp * rdp , height    ]
        ])

        #outer slope 
        data['vectors'][8 * n + 4] = np.array([
            [cost  * rb     , sint  * rb  , height          ],
            [cost  * rc     , sint  * rc  , height - depth  ], 
            [costp * rbp    , sintp * rbp , height          ]
        ])
        data['vectors'][8 * n + 5] = np.array([
            [costp * rcp    , sintp * rcp , height - depthp ],
            [cost  * rc     , sint  * rc  , height - depth  ], 
            [costp * rbp    , sintp * rbp , height          ]
        ])

        #inner slope 
        data['vectors'][8 * n + 6] = np.array([
            [cost  * rd     , sint  * rd  , height          ],
            [cost  * rc     , sint  * rc  , height - depth  ], 
            [costp * rdp    , sintp * rdp , height          ]
        ])
        data['vectors'][8 * n + 7] = np.array([
            [costp * rcp    , sintp * rcp , height - depthp ],
            [cost  * rc     , sint  * rc  , height - depth  ], 
            [costp * rdp    , sintp * rdp , height          ]
        ])
    return data

if __name__=="__main__":
    def mydepth(theta):
        return .6 + .3 * math.sin(theta*2708.53)

    def mydisp(theta):
        return .3 * math.cos(theta*503.134)

    outside= getSide( diameter )
    inside= getSide( holediam )

    underside= getDonut( diameter, holediam, height = -height )

    grLoc = 250
    grSpace = 1.5

    top1= getDonut( diameter, grLoc + grSpace )
    mygroove= getCircularGroove(mydepth, mydisp, radius = grLoc, space = grSpace)
    top2= getDonut( grLoc - grSpace, holediam )


    record = np.concatenate([outside, inside, underside, top1, mygroove, top2])
    recordMesh = mesh.Mesh(record)

    recordMesh.save('record.stl')
