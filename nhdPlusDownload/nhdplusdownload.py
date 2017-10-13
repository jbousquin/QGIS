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
import util

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
        # Set user database folder to save downloads into
        db_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path()+'0.0.3/'
        
        # Create the dialog (after translation) and keep reference
        self.dlg = nhdPlusDownloadDialog()
        # Layers loaded in QGIS legend
        layer_list = []
        for layer in self.iface.legendInterface().layers():
            layer_list.append(layer.name())
        # Set dropdown in GUI to list those layers
        self.dlg.ui.comboBox1.addItems(layer_list)
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # Selection from GUI (layer legend)
            index = self.dlg.ui.comboBox1.currentIndex()
            #nhdPlus dataset
            data_source = db_dir + "data/BoundaryUnit.shp"
            # Get layer objects
            lyrB = util.getVectorLayerByFile(data_source)
            lyrA = util.getVectorLayerByName(layer_list[index])
            # Select Layer A where it intersects Layer B
            util.SelectLayerByLocation(lyrB, lyrA, "ADD")
            # Get needed attributes from selection
            ID_List = util.fieldToList(lyrB, 1, True)
            d_List = util.fieldToList(lyrB, 0, True)
            # Get requests
            requests = util.getNHDrequest(ID_List, d_List)
            # Download requests
            # requests = [(request1, [file1, file2]), (request2, [file1, file2])]
            for request in requests:
                for f in request[1]:
                    QMessageBox.information(self.iface.mainWindow(), "Request:", "Request: {}; loc: {}; file: {}".format(request[0], db_dir, f))
                    util.HTTP_download(request[0], db_dir, f)
                    # Unzip dowloads
                    util.WinZip_unzip(db_dir, f)
                    # Pull unzipped file into database?

            #QMessageBox.information(self.iface.mainWindow(), "Lists:", "{}; {}; ".format(ID_List, drainList))
