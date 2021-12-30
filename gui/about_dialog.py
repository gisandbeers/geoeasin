# -*- coding: utf-8 -*-
"""

"""

import os

from ..tools.tools import getPath

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'about_dialog.ui'))


class AboutDialog(QtWidgets.QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor."""
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)

        self.tbInfo.setHtml(self.get_about_text())
        self.tbLicense.setPlainText(self.get_license_text())

    def get_about_text(self):
        return self.tr(
            '<p>Web services downloader and tools to analyze the European Alien Species Information Network data (EASIN).</p>'
            '<p><strong>Developers:</strong> <a href="https://geoinnova.org/">Geoinnova</a></p>'
            '<p><strong>Issue tracker:</strong> <a href="https://github.com/geoinnova/geoeasin/issues">GitHub</a></p>'
            '<p><strong>Source code:</strong> <a href="https://github.com/geoinnova/geoeasin">GitHub</a></p>')

    def get_license_text(self):
        uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])
        CURR_PATH = uppath(__file__, 2)

        with open(os.path.join(CURR_PATH, 'LICENSE')) as f:
            return f.read()
