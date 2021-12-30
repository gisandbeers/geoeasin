from qgis.core import QgsProcessingProvider

from PyQt5.QtGui import QIcon
from os import path


from .union import UnirInformacionPas
from .Prueba import CalculateWildlifeCorridor   # TEXTO INCLUIDO
from .prueba2 import SetStudyAreaExtractLandCover    # TEXTO INCLUIDO  

class ProcessingToolsProvider(QgsProcessingProvider):

    def loadAlgorithms(self, *args, **kwargs):
        # self.addAlgorithm(ExampleProcessingAlgorithm())
        self.addAlgorithm(UnirInformacionPas())
        self.addAlgorithm(CalculateWildlifeCorridor())   # TEXTO INCLUIDO
        self.addAlgorithm(SetStudyAreaExtractLandCover())  #TEXTO INCLUIDO

    def id(self, *args, **kwargs):
        """The ID of your plugin, used for identifying the provider.

        This string should be a unique, short, character only string,
        eg "qgis" or "gdal". This string should not be localised.
        """
        return 'GeoEASIN'

    def name(self, *args, **kwargs):
        """The human friendly name of your plugin in Processing.

        This string should be as short as possible (e.g. "Lastools", not
        "Lastools version 1.0.1 64-bit") and localised.
        """
        return self.tr('GeoEASIN')

    def icon(self):
        """Should return a QIcon which is used for your provider inside
        the Processing toolbox.
        """
        return QgsProcessingProvider.icon(self)

    def icon(self):
        """Should return a QIcon which is used for your provider inside
        the Processing toolbox.
        """
        return QIcon(path.dirname(__file__) + '/img/icon.png')
