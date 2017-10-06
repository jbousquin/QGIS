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
 This script initializes the plugin, making it known to QGIS.
"""


def name():
    return "NHD PLus Downloader"


def description():
    return "Download NHD Plus Data for EPA H2O tool"


def version():
    return "Version 0.1"


def icon():
    return "icon.png"


def qgisMinimumVersion():
    return "1.8"

def author():
    return "Justin Bousquin"

def email():
    return "bousquin.justin@epa.gov"

def classFactory(iface):
    # load nhdPlusDownload class from file nhdPlusDownload
    from nhdplusdownload import nhdPlusDownload
    return nhdPlusDownload(iface)
