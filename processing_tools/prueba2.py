"""
Model exported as python.
Name : 1. Set study area & extract land cover
Group : SCOAM
With QGIS : 31200
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterExtent
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterRasterDestination
import processing


class SetStudyAreaExtractLandCover(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterExtent('areaextent', 'Area extent', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('landuse', 'Global Land Use', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('OutputLandUse', 'Output: Land Use', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}

        # Clip raster by extent
        alg_params = {
            'DATA_TYPE': 0,
            'INPUT': parameters['landuse'],
            'NODATA': None,
            'OPTIONS': '',
            'PROJWIN': parameters['areaextent'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ClipRasterByExtent'] = processing.run('gdal:cliprasterbyextent', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # r.reclass
        alg_params = {
            'GRASS_RASTER_FORMAT_META': '',
            'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_REGION_CELLSIZE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': parameters['areaextent'],
            'input': outputs['ClipRasterByExtent']['OUTPUT'],
            'rules': '',
            'txtrules': '0 thru 30 = 1\n31 thru 40 = 2\n41 thru 90 = 3\n100 thru 122 = 2\n130 thru 131 = 1\n150  thru 153 = 2\n160  thru 170 = 6\n180  thru 181 = 2\n190  thru 191 = 4\n200  thru 203 = 7\n210  thru 211 = 5\n220  thru 221 = 8',
            'output': parameters['OutputLandUse']
        }
        outputs['Rreclass'] = processing.run('grass7:r.reclass', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['OutputLandUse'] = outputs['Rreclass']['output']
        return results

    def name(self):
        return '1. Set study area & extract land cover'

    def displayName(self):
        return '1. Set study area & extract land cover'

    def group(self):
        return 'SCOAM'

    def groupId(self):
        return 'SCOAM'

    def createInstance(self):
        return SetStudyAreaExtractLandCover()
