"""
Model exported as python.
Name : 4. Calculate wildlife corridor
Group : SCOAM
With QGIS : 31200
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterPoint
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorDestination
import processing


class CalculateWildlifeCorridor(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterPoint('pointa', 'Point A', defaultValue=''))
        self.addParameter(QgsProcessingParameterPoint('pointb', 'Point B', defaultValue=''))
        self.addParameter(QgsProcessingParameterRasterLayer('resistanceraster', 'Resistance', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('Corridor', 'Corridor', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=''))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(3, model_feedback)
        results = {}
        outputs = {}

        # r.cost
        alg_params = {
            '-k': False,
            '-n': True,
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_RASTER_FORMAT_META': '',
            'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_REGION_CELLSIZE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'input': parameters['resistanceraster'],
            'max_cost': 0,
            'memory': 300,
            'null_cost': None,
            'start_coordinates': parameters['pointa'],
            'start_points': None,
            'start_raster': None,
            'stop_coordinates': parameters['pointb'],
            'stop_points': None,
            'outdir': QgsProcessing.TEMPORARY_OUTPUT,
            'output': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Rcost'] = processing.run('grass7:r.cost', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # r.drain
        alg_params = {
            '-a': False,
            '-c': False,
            '-d': True,
            '-n': False,
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,
            'GRASS_RASTER_FORMAT_META': '',
            'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_REGION_CELLSIZE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False,
            'GRASS_VECTOR_LCO': '',
            'direction': outputs['Rcost']['outdir'],
            'input': outputs['Rcost']['output'],
            'start_coordinates': parameters['pointb'],
            'start_points': None,
            'drain': QgsProcessing.TEMPORARY_OUTPUT,
            'output': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Rdrain'] = processing.run('grass7:r.drain', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # r.to.vect
        alg_params = {
            '-b': False,
            '-s': False,
            '-t': False,
            '-v': False,
            '-z': False,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,
            'GRASS_REGION_CELLSIZE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False,
            'GRASS_VECTOR_LCO': '',
            'column': 'value',
            'input': outputs['Rdrain']['output'],
            'type': 0,
            'output': parameters['Corridor']
        }
        outputs['Rtovect'] = processing.run('grass7:r.to.vect', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Corridor'] = outputs['Rtovect']['output']
        return results

    def name(self):
        return '4. Calculate wildlife corridor'

    def displayName(self):
        return '4. Calculate wildlife corridor'

    def group(self):
        return 'SCOAM'

    def groupId(self):
        return 'SCOAM'

    def createInstance(self):
        return CalculateWildlifeCorridor()
