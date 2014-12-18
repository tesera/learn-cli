'''
The purpose of this module is to store standard stand and stock table
management subroutines.

Created March 3, 2008.
'''

import math

def getHeaderMinusKeyNames(ssHeader, ssTabKeynames):
    '''
    This subroutine gets a list of variables names
    that are in the header but not in ssTabKeynames
    '''
    newList = []
    for item in ssHeader:
        newList.append(item)
    for varName in ssTabKeynames:
        location = newList.index(varName)
        del newList[location]
    return newList


def initialize_ssPlotDict(ssHeader, ssTabKeynames, PNO, cldefKeys, spList, LDSTATlist):
    '''
    This subroutine initializes the stand and stock table attributes - setting each one
    to equal 0. ssHeader contains the header variables. ssTableKeynames contains the dictionary keys.
    PNO is plot number. cldefKeys are the eligible diameter class labels.  LDSTATlist provides a list of the eligible
    live and dead trees - this may be extended to include other kinds of trees.
    '''
    NewDict = {PNO:{}}
    for dclass in cldefKeys:
        NewDict[PNO].update({dclass:{}})
        for species in spList:
            NewDict[PNO][dclass].update({species:{}})
            for ldstat in LDSTATlist:
                NewDict[PNO][dclass][species].update({ldstat:{}})
                for attribute in ssHeader:
                    flag = 'False'
                    for key in ssTabKeynames:
                        if key == attribute:
                            flag = 'True'
                    if flag == 'False':
                        NewDict[PNO][dclass][species][ldstat].update({attribute:0})                                     
    return NewDict

def GetBasalAreaPerHectare(dbh,sph):
    bph = float(sph) * 3.141592654 * (float(dbh)/float(200))**2
    return bph

def GetQmd(bph,sph):
    if sph <= 0:
        qmd = 0
    else:
        bpt = bph/float(sph)
        qmd = 200 * (bpt/math.pi)**0.5
    return qmd

def GetBasalAreaPerTreeInCm(dbh):
    bpt = 3.141592654 * (float(dbh)/float(2))**2
    return bpt

def GetBasalAreaPerTreeInM2(dbh):
    bpt = 3.141592654 * (float(dbh)/float(200))**2
    return bpt

def GetTreeDiameterInCm(bpt):
    diam = 2 * (bpt/3.141592654)**0.5
    return diam

def GetPhfFromPrismBAF(dbh, baf):
    newPhf = 0
    if baf > 0 and dbh > 0:
        bpt = GetBasalAreaPerTreeInM2(dbh)
        newPhf = baf/bpt   
    return newPhf
