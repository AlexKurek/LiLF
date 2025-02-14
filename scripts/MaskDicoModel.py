#!/usr/bin/env python3

import optparse
import pickle
import numpy as np

try:
    from DDFacet.Imager.ModModelMachine import GiveModelMachine as ClassModModelMachine
except:
    from DDFacet.Imager.ModModelMachine import ClassModModelMachine

#from DDFacet.Imager import ClassCasaImage

SaveName="last_MaskDicoModel.obj"

def read_options():
    desc="""Questions and suggestions: cyril.tasse@obspm.fr"""
    global options
    opt = optparse.OptionParser(usage='Usage: %prog <options>',version='%prog version 1.0',description=desc)

    group = optparse.OptionGroup(opt, "* Data-related options", "Won't work if not specified.")
    group.add_option('--InDicoModel',help='Input DicoModel name [no default]',default='')
    group.add_option('--OutDicoModel',help='Output DicoModel name, default is %default',default=None)
    group.add_option('--MaskName',help='Name of the fits mask, default is %default',default=None)
    group.add_option('--NPixOut',help='Change pixel size of the output image, default is %default',default=None)
#    group.add_option('--InvertMask',help='Invert the mask, default is False',action="store_true")
    group.add_option('--FilterNegComp',help='Remove negative components, default is False',action="store_true")
    opt.add_option_group(group)

    options, arguments = opt.parse_args()
    f = open(SaveName,"wb")
    pickle.dump(options,f)

def main(options=None):
    if options==None:
        f = open(SaveName,'rb')
        options = pickle.load(f)


    if options.OutDicoModel is None:
        raise ValueError("--OutDicoModel should be specified")
    ModConstructor = ClassModModelMachine()
    MM=ModConstructor.GiveInitialisedMMFromFile(options.InDicoModel)
    if options.MaskName:
        MM.CleanMaskedComponants(options.MaskName)#,InvertMask=options.InvertMask)

    if options.FilterNegComp:
        MM.RemoveNegComponants()

    if options.NPixOut:
        MM.ChangeNPix(int(options.NPixOut))

    MM.ToFile(options.OutDicoModel)


if __name__=="__main__":
    read_options()
    f = open(SaveName,'rb')
    options = pickle.load(f)

    main(options=options)
