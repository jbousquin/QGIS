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

from PyQt4 import QtCore, QtGui
from ui_nhdplusdownload import Ui_nhdPlusDownload
# create the dialog
class nhdPlusDownloadDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_nhdPlusDownload()
        self.ui.setupUi(self)
