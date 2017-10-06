# -*- coding: utf-8 -*-
"""
/***************************************************************************
 nhdPlusDownloadDialog
                                 A QGIS plugin
 Download NHD Plus Data for EPA H2O tool
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

#return name (test)
def doIntersect(lyrA, db_dir):
    db_dir = db_dir + os.sep + "data"
    data_source = db_dir + os.sep + "BoundaryUnit.shp"
    file_info = QFileInfo(data_source)
    if file_info.exists():
        lyr_name = file_info.completeBaseName()
    else:
        return False
    lyrB = QgsVectorLayer(data_source, lyr_name, "ogr")

    
    string = str(lyrA.name()) + " junk"
    return lyrB

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

def compute(lyrB, lyrA, modify, selection):
    inputLayer = getVectorLayerByFile(lyrB)
    selectLayer = getVectorLayerByName(lyrA)
    
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
    if selection:
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

    #adding to current selection
    selectedSet = list(set(inputLayer.selectedFeaturesIds()).union(selectedSet))
    #removing from current selection
    #selectedSet = list(set(inputLayer.selectedFeaturesIds()).difference(selectedSet))
    inputLayer.setSelectedFeatures(selectedSet)

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

# Convinience function to create a spatial index for input QgsVectorDataProvider
def createIndex( provider ):
    feat = QgsFeature()
    index = QgsSpatialIndex()
    provider.rewind()
    provider.select()
    while provider.nextFeature( feat ):
        index.insertFeature( feat )
    return index
