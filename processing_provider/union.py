# -*- coding: utf-8 -*-

"""
Model exported as python.
Name : Unir informacion país
Group : EASIN
With QGIS : 32002
"""

from qgis.PyQt.QtCore import QCoreApplication

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink

from qgis import processing


class UnirInformacionPas(QgsProcessingAlgorithm):

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('EASINGrid', 'EASIN Grid', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('Adminboundaries', 'Admin boundaries', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Grid_boundaries', 'grid_boundaries', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Unir atributos por localización
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': parameters['EASINGrid'],
            'JOIN': parameters['Adminboundaries'],
            'JOIN_FIELDS': [''],
            'METHOD': 1,  # Tomar solo los atributos del primer objeto coincidente (uno a uno)
            'PREDICATE': [0],  # interseca
            'PREFIX': '',
            'OUTPUT': parameters['Grid_boundaries']
        }
        outputs['UnirAtributosPorLocalizacin'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Grid_boundaries'] = outputs['UnirAtributosPorLocalizacin']['OUTPUT']
        return results


    def createInstance(self):
        return UnirInformacionPas()

    def name(self):
        return 'Unir informacion país'

    def displayName(self):
        return 'Unir informacion país'

    def group(self):
        return 'Example scripts'

    def groupId(self):
        return ''

    def shortHelpString(self):
        return """<html><body><h2>Descripción del algoritmo</h2>
            <p>Description</p>
            <h2>Parámetros de entrada</h2>
            <h3>EASIN Grid</h3>
            <p>EASIN Grid layer</p>
            <h3>Admin boundaries</h3>
            <p>Administrative boundaries layer</p>
            <h3>grid_boundaries</h3>
            <p></p>
            <h3>grid_boundaries_no_union</h3>
            <p></p>
            <h2>Salidas</h2>
            <h3>grid_boundaries</h3>
            <p></p>
            <h3>grid_boundaries_no_union</h3>
            <p></p>
            <br></body></html>"""

