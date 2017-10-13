# -*- coding: utf-8 -*-
"""
/***************************************************************************
 util module for
 "nhdPlusDownloadDialog"
 A QGIS plugin that will download NHD Plus Data for EPA H2O tool
                             -------------------
        begin                : 2017-10-03
        copyright            : (C) 2017 by Justin Bousquin
        email                : bousquin.justin@epa.gov
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import os

import subprocess
from urllib import urlretrieve

def getVectorLayerByFile(shp_name):
    file_info = QFileInfo(shp_name)
    if file_info.exists():
        lyr_name = file_info.completeBaseName()
    else:
        return False
    layer = QgsVectorLayer(shp_name, lyr_name, "ogr")
    if layer.type() == QgsMapLayer.VectorLayer:
        if layer.isValid():
            return layer
        else:
            return None

#SelectLayerByLocation_management(in_layer, {overlap_type}, {select_features}, {search_distance}, {selection_type}, {invert_spatial_relationship})
def SelectLayerByLocation(in_layer, selectLayer, selection_type):
    #inputLayer = getVectorLayerByFile(lyrB)
    #selectLayer = getVectorLayerByName(lyrA)
    inputLayer = in_layer
    
    inputProvider = inputLayer.dataProvider()
    allAttrs = inputProvider.attributeIndexes()
    inputProvider.select(allAttrs, QgsRectangle())

    selectProvider = selectLayer.dataProvider()
    allAttrs = selectProvider.attributeIndexes()
    selectProvider.select(allAttrs, QgsRectangle())

    feat = QgsFeature()
    infeat = QgsFeature()
    geom = QgsGeometry()
    selectedSet = []
    index = createIndex(inputProvider)
    inputProvider.rewind()
    inputProvider.select(inputProvider.attributeIndexes())

    if inputLayer.isValid():
        QgsMapLayerRegistry.instance().addMapLayer(inputLayer)

    if selectLayer.selectedFeatureCount() > 0:
        features = selectLayer.selectedFeatures()
        for feat in features:
            geom = QgsGeometry(feat.geometry())
            intersects = index.intersects(geom.boundingBox())
            for id in intersects:
                inputProvider.featureAtId(int(id), infeat, True)
                tmpGeom = QgsGeometry(infeat.geometry())
                if geom.intersects(tmpGeom):
                    selectedSet.append(infeat.id())

    else:
        while selectProvider.nextFeature(feat):
            geom = QgsGeometry(feat.geometry())
            intersects = index.intersects(geom.boundingBox())
            for id in intersects:
                inputProvider.featureAtId(int(id), infeat, True)
                tmpGeom = QgsGeometry( infeat.geometry() )
                if geom.intersects(tmpGeom):
                    selectedSet.append(infeat.id())

    if selection_type == "REMOVE_FROM_SELECTION":
        #removing from current selection
        selectedSet = list(set(inputLayer.selectedFeaturesIds()).difference(selectedSet))
    else:
        #adding to current selection
        selectedSet = list(set(inputLayer.selectedFeaturesIds()).union(selectedSet))
    
    #QMessageBox.information(self.iface.mainWindow(), "Layer: ","{}".format(lyrB.name()))
    
    inputLayer.setSelectedFeatures(selectedSet)   

def fieldToList(lyr, ind, slct):
    selection = lyr.selectedFeatures()
    lst = []
    if slct == True: # Subset to selection
        for f in selection:
            lst.append(str(f.attributeMap()[ind].toString()))
    elif slct == False: # No selection
        vprovider = lyr.dataProvider()
        allAttrs = vprovider.attributeIndexes()
        vprovider.select(allAttrs)
        feat = QgsFeature()
        while vprovider.nextFeature(feat):
            lst.append(str(feat.attributeMap()[ind].toString()))
    return lst

def getNHDrequest(ID_list, d_list):
    # http://www.horizon-systems.com/NHDPlusData/NHDPlusV21/Data/NHDPlus
    sub_link = "/{0}Data/{0}V21/Data/{0}".format("NHDPlus")
    NHD_http = "http://www.horizon-systems.com" + sub_link

    # Component name is the name of the NHDPlusV2 component file
    f_comp = "NHDPlusCatchment"
    f2_comp = "NHDPlusAttributes"
    f3_comp = "NHDSnapshot"
    f4_comp = "NHDPlusBurnComponents"

    # Version dictionary, [f_comp, f2_comp, f3_comp, f4_comp]
    vv_dict = {'10U': ["02", "09", "01", "01"],
           '13': ["02", "05", "01", "01"],
           '17': ["02", "08", "01", "01"],
           "06": ["05", "09", "01", "01"],
           "20": ["01", "02", "01", "01"],
           "21": ["01", "02", "01", "01"],
           "22AS": ["01", "02", "01", "01"],
           "22GU": ["01", "02", "01", "01"],
           "22MP": ["01", "02", "01", "01"],
           "03N": ["01", "05", "01", "01"],
           "03S": ["01", "06", "06", "02"],
           "03W": ["01", "05", "01", "01"],
           "16": ["01", "05", "01", "01"],
           "02": ["01", "06", "01", "01"],
           "09": ["01", "06", "01", "01"],
           "11": ["01", "06", "01", "01"],
           "18": ["01", "06", "01", "01"],
           "01": ["01", "07", "01", "01"],
           "08": ["01", "07", "01", "01"],
           "12": ["01", "07", "01", "01"],
           "05": ["01", "08", "01", "01"],
           "15": ["01", "08", "01", "01"],
           "07": ["01", "09", "01", "01"],
           "14": ["01", "09", "01", "01"],
           "10L": ["01", "11", "01", "01"],
           "04": ["01", "12", "01", "01"]
           }
    rows = []
    for i, DA in enumerate(d_list):
        ID = ID_list[i]
        ext = ".7z"

        # Set versions
        f_vv = vv_dict[ID][0]
        f2_vv = vv_dict[ID][1]
        f3_vv = vv_dict[ID][2]
        f4_vv = vv_dict[ID][3]

        # Set http zipfile is requested from
        if DA in ["SA", "MS", "CO", "PI"]:  # regions with sub-regions
            request = NHD_http + DA + "/" + "NHDPlus" + ID + "/"
        else:
            request = NHD_http + DA + "/"

        # Assign catchment filenames
        f = "NHDPlusV21_{}_{}_{}_{}{}".format(DA, ID, f_comp, f_vv, ext)
        # Assign attribute filenames
        f2 = "NHDPlusV21_{}_{}_{}_{}{}".format(DA, ID, f2_comp, f2_vv, ext)
        f3 = "NHDPlusV21_{}_{}_{}_{}{}".format(DA, ID, f3_comp, f3_vv, ext)
        f4 = "NHDPlusV21_{}_{}_{}_{}{}".format(DA, ID, f4_comp, f4_vv, ext)
        row = (request, [f, f2, f3, f4])
        rows.append(row)
    return rows


def HTTP_download(request, directory, filename):
    """Download HTTP request to filename
    Param request: HTTP request link ending in "/"
    Param directory: Directory where downloaded file will be saved
    Param filename: Name of file for download request and saving
    """
    host = "http://www.horizon-systems.com/NHDPlus/NHDPlusV2_data.php"
    # Add dir to var zipfile is saved as
    f = directory + "/" + filename # was os.sep
    r = request + filename
    try:
        urlretrieve(r, f)
        #message("HTTP downloaded successfully as:\n" + str(f))
    except:
        e = error
        #message("Error downloading from: " + '\n' + str(r))
        #message("Try manually downloading from: " + host)

def WinZip_unzip(directory, zipfile):
    """Use program WinZip in C:\Program Files\WinZip to unzip .7z"""
    #message("Unzipping download...")
    #message("Winzip may open. If file already exists you will be prompted...")
    d = directory
    z = directory + os.sep + zipfile
    try:
        zipExe = r"C:\Program Files\WinZip\WINZIP64.EXE"
        args = zipExe + ' -e ' + z + ' ' + d
        subprocess.call(args, stdout=subprocess.PIPE)
        #message("Successfully extracted NHDPlus data to:\n" + d)
        os.remove(z)
        #message("Deleted zipped NHDPlus file")
    except:
        #message("Unable to extract NHDPlus files. " +
        #        "Try manually extracting the files from:\n" + z)
        #message("Software to extract '.7z' files can be found at: " +
        #        "http://www.7-zip.org/download.html")
        print("error")


        
### Stolen directly from fTools_utils

# Convinience function to add a vector layer to canvas based on input shapefile path ( as string )
def addShapeToCanvas( shapefile_path ):
    file_info = QFileInfo( shapefile_path )
    if file_info.exists():
        layer_name = file_info.completeBaseName()
    else:
        return False
    vlayer_new = QgsVectorLayer( shapefile_path, layer_name, "ogr" )
    print layer_name
    if vlayer_new.isValid():
        QgsMapLayerRegistry.instance().addMapLayer( vlayer_new )
        return True
    else:
        return False

# Return QgsVectorLayer from a layer name ( as string )
def getVectorLayerByName( myName ):
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layermap.iteritems():
        if layer.type() == QgsMapLayer.VectorLayer and layer.name() == myName:
            if layer.isValid():
                return layer
            else:
                return None
            
# Check if two input CRSs are identical
def checkCRSCompatibility( crsA, crsB ):
    if crsA == crsB:
        return True
    else:
        return False
        
# Return list of names of all fields from input QgsVectorLayer
def getFieldNames( vlayer ):
    fieldmap = getFieldList( vlayer )
    fieldlist = []
    for name, field in fieldmap.iteritems():
        if not field.name() in fieldlist:
            fieldlist.append( unicode( field.name() ) )
    return sorted( fieldlist, cmp=locale.strcoll )


# Return the field list of a vector layer
def getFieldList( vlayer ):
    vprovider = vlayer.dataProvider()
    feat = QgsFeature()
    allAttrs = vprovider.attributeIndexes()
    vprovider.select( allAttrs )
    myFields = vprovider.fields()
    return myFields


# Convinience function to create a spatial index for input QgsVectorDataProvider
def createIndex( provider ):
    feat = QgsFeature()
    index = QgsSpatialIndex()
    provider.rewind()
    provider.select()
    while provider.nextFeature( feat ):
        index.insertFeature( feat )
    return index
