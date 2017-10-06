# -*- coding: utf-8 -*-
"""
/***************************************************************************
 nhdPlusDownload
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
# Import the PyQt and QGIS libraries
import os, sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from nhdplusdownloaddialog import nhdPlusDownloadDialog
# Set up current path, so that we know where to look for modules
currentPath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.dirname(__file__) + os.sep + 'tools'))
#import the custom functions
import byBoundaryUnit

class nhdPlusDownload:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        
        # initialize plugin directory
        fld = "{0}python{0}plugins{0}nhdplusdownload".format(os.sep) #qgis py plugins folder
        plug_dir = os.path.dirname(os.path.realpath(__file__))
        #self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + fld
        self.plugin_dir = QFileInfo(plug_dir)
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale").toString()[0:2]

        if QFileInfo(self.plugin_dir).exists():
            i18n_fld = "{0}i18n{0}nhdplusdownload_".format(os.sep)
            localePath = plug_dir + i18n_fld + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":{0}plugins{0}nhdplusdownload{0}icon.png".format(os.sep)), \
            "Download NHD Plus", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&NHD PLus Downloader", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&NHD PLus Downloader", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        #set user database folder to save downloads into
        dbFldr = QFileInfo(QgsApplication.qgisUserDbFilePath()).path()+'/0.0.3/'
        
        # Create the dialog (after translation) and keep reference
        self.dlg = nhdPlusDownloadDialog()
        # Layers loaded in QGIS legend
        layer_list = []
        for layer in self.iface.legendInterface().layers():
            layer_list.append(layer.name())
            #QMessageBox.information(self.iface.mainWindow(), "Layer: ",layer.name())
            #self.dlg.comboBox.Items.Insert(layer_list)
        self.dlg.ui.comboBox1.addItems(layer_list)
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # disply selection
            index = self.dlg.ui.comboBox1.currentIndex()
            layerB = byBoundaryUnit.doIntersect(self.iface.legendInterface().layers()[index], str(dbFldr))
            #layerA = self.iface.legendInterface().layers()[index]
            #layer = self.dlg.ui.comboBox1.itemData(index)
            #lyr = self.iface.addVectorLayer(layerB, "BU", "ogr")
            if layerB.isValid():
                QgsMapLayerRegistry.instance().addMapLayer(layerB)
            layer2 = str(layer_list[index])
            QMessageBox.information(self.iface.mainWindow(), "Layer: ","{}; ".format(layer2))
