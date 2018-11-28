import os
import sys

sys.path.append('/Applications/QGis3.app/Contents/Resources/python/')
# sys.path.append('/Applications/QGis3.app/Contents/Resources/python/plugins') # if you want to use the processing module, for example
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/Applications/QGIS3.app/Contents/Plugins'

from qgis.core import *
from qgis.PyQt.QtXml import QDomDocument


# from PyQt5.QtGui import *

class at(object):
    def __init__(self):
        self.app = QgsApplication([], False)
        self.app.setPrefixPath('/Applications/QGIS3.app/Contents/MacOS', True)
        self.app.initQgis()

        self.project = QgsProject.instance()
        self.project.setCrs(QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId))

    def add_layer(self, *args):
        # can also add with QgsPr   oject.instance().addMapLayer()
        self.project.addMapLayer(QgsVectorLayer(*args))

    def get_layer(self, nm):
        # return layer object based on its given name, not Qs internal identifier
        return {v.name(): v for k, v in self.project.layerStore().mapLayers().items()}[nm]

    def join_lays(self, parent, parent_code, to_join, to_join_code):
        joinObject = QgsVectorLayerJoinInfo()
        joinObject.setJoinFieldName(to_join_code)
        joinObject.setTargetFieldName(parent_code)
        joinObject.setJoinLayerId(self.get_layer(to_join).id())
        joinObject.setUsingMemoryCache(True)
        joinObject.setJoinLayer(self.get_layer(to_join))
        self.get_layer(parent).addJoin(joinObject)

    def write_proj(self, loc):
        self.project.write(loc)

    def set_col_type(self):
        pass
        ##dunno

        # dat.fields()[2].setTypeName('Integer')
        # provider = dat.dataProvider()
        # updateMap = {}
        # fieldIdx = dat.fields().indexFromName('val')
        # # features = provider.getFeatures()
        # # for feature in features:
        # updateMap[feature.id()] = {fieldIdx: 'a'}
        # provider.changeAttributeValues(updateMap)

    def get_layers(self):
        return self.project.layerStore().mapLayers()

    def apply_styling(self, lay, style):
        self.get_layer(lay).loadNamedStyle(style)

    def _open_atlas_styling(self):
        with open('./styles/atlas_layout.qpt', 'r') as templateFile:
            self.templateContent = templateFile.read()

        self.document = QDomDocument()
        self.document.setContent(self.templateContent)

    def make_atlas(self, at_lay, type, list=None):
        # https: // github.com / carey136 / Standalone - Export - Atlas - QGIS3 / blob / master / AtlasExport.py
        self._open_atlas_styling()

        self.layout = QgsPrintLayout(self.project)
        self.layout.loadFromTemplate(self.document, QgsReadWriteContext(), True)

        self.myLayout = self.layout
        self.myAtlas = self.myLayout.atlas()
        self.myAtlasMap = self.myAtlas.layout()

        #### atlas query ####
        self.myAtlas.setCoverageLayer(self.get_layer(at_lay))
        self.myAtlas.setEnabled(True)
        self.myAtlas.beginRender()
        self.myAtlas.setFilterFeatures(True)

        if list:
            # list = tuple([i for i in range(51001, 51003)])
            self.myAtlas.setFilterExpression('"PalikaCode" IN %s' % str(list))

        #### image output name ####
        self.myAtlas.setFilenameExpression('PalikaCode')

        print("Starting output")

        #### image and pdf settings ####
        if type == 'svg':
            image_settings = QgsLayoutExporter(self.myAtlasMap).SvgExportSettings()
            image_settings.dpi = -1
            image_settings.exportMetadata = False

            result, error = QgsLayoutExporter.exportToSvg(self.myAtlas,
                                                          baseFilePath='./atlas_out/',
                                                          settings=image_settings)
            if not result == QgsLayoutExporter.Success:
                print(error)

        elif type == 'img':
            image_settings = QgsLayoutExporter(self.myAtlasMap).ImageExportSettings()
            imageExtension = '.png'

            result, error = QgsLayoutExporter.exportToImage(self.myAtlas,
                                                            baseFilePath='./atlas_out/',
                                                            extension=imageExtension, settings=image_settings)
            if not result == QgsLayoutExporter.Success:
                print(error)

        print("Script done")

    def make_atlas_old(self, at_lay):
        # code that doesn't really work

        # Load template from file

        # grab template file
        with open('', 'r') as templateFile:
            self.templateContent = templateFile.read()

        self.document = QDomDocument()
        self.document.setContent(self.templateContent)

        self.layout = QgsPrintLayout(self.project)
        self.layout.loadFromTemplate(self.document, QgsReadWriteContext(), False)
        self.layout.initializeDefaults()

        # the atlas map
        self.atlas_map = QgsLayoutItemMap(self.layout)
        # self.atlas_map.attemptSetSceneRect(QRectF(20, 20, 130, 130))
        self.atlas_map.setFrameEnabled(True)
        self.atlas_map.setLayers([self.get_layer(at_lay)])
        self.layout.addLayoutItem(self.atlas_map)

        # the atlas
        self.atlas = self.layout.atlas()
        self.atlas.setCoverageLayer(self.get_layer(at_lay))
        self.atlas.setEnabled(True)

        # an overview
        self.overview = QgsLayoutItemMap(self.layout)
        # self.overview.attemptSetSceneRect(QRectF(180, 20, 50, 50))
        self.overview.setFrameEnabled(True)
        self.overview.overview().setLinkedMap(self.atlas_map)
        self.overview.setLayers([self.get_layer(at_lay)])
        self.layout.addLayoutItem(self.overview)
        nextent = QgsRectangle(49670.718, 6415139.086, 699672.519, 7065140.887)
        self.overview.setExtent(nextent)



        # https://gis.stackexchange.com/questions/272774/using-qgis-3-0-api-for-layout

        # for comp in self.projectLayoutManager.printLayouts():
        #     print(comp)
        #     result, error = QgsLayoutExporter.exportToImage(atlas,
        #                                                     baseFilePath='./atlas_out/', extension='.png',
        #                                                     settings=image_settings)
        #     if not result == QgsLayoutExporter.Success:
        #         print(error)

        # # Generate atlas
        # self.atlas.beginRender()
        # self.projectLayoutManager = self.project.layoutManager()
        #
        # self.image_settings = exporter.ImageExportSettings()
        # self.image_settings.dpi = 300  # or whatever you want
        #
        # while self.atlas.next():
        #     self.atlas.prepareForFeature(i)
        #     print(self.atlas.currentFeatureNumber())

        # for i in range(0, self.atlas.numFeatures()):
        #     self.atlas.prepareForFeature(i)
        #     output_jpeg = os.path.join('/.atlas_out/', '% i out.jpeg' % i)
        #     image = self.layout.printPageAsRaster(0)
        #     image.save(output_jpeg)
        #     self.layout.endRender()


        # #grab template file
        # with open('/Users/ewanog/Documents/work/code/repos/humanitarian/hrrp/gp_auto/maps/map_out.qpt', 'r') as templateFile:
        #     self.templateContent = templateFile.read()
        #
        # self.document = QDomDocument()
        # self.document.setContent(self.templateContent)
        #
        # self.composition = QgsLayout(self.project)
        # self.composition.loadFromTemplate(self.document, QgsReadWriteContext(), False)
        #
        # # Get map composition and define scale
        # self.atlasMap = QgsLayoutItemMap(self.composition)
        # self.composition.initializeDefaults()
        # # atlasMap.setNewScale(int(scale))


        # # Setup Atlas
        # atlas = QgsAtlasComposition(composition)
        # atlas.setCoverageLayer(self.get_layer(at_lay))  # Atlas run from desktop_search
        # # atlas.setComposerMap(atlasMap)
        # atlas.setFixedScale(True)
        # atlas.fixedScale()
        # atlas.setHideCoverage(False)
        # atlas.setFilterFeatures(True)
        # atlas.setFeatureFilter("reference = '%s'" % (str(ref)))
        # atlas.setFilterFeatures(True)
        #

    def exit(self):
        self.app.exitQgis()


def go():
    atlas = at()

    atlas.add_layer('./hrrp_shapes/wards/merge.shp', 'wards', 'ogr')
    # for hiding other palikas while atlasing
    atlas.add_layer('./hrrp_shapes/palika/GaPaNaPa_hrrp.shp', 'palika_hide', 'ogr')
    atlas.add_layer('./hrrp_shapes/palika/GaPaNaPa_hrrp.shp', 'palikas', 'ogr')
    atlas.add_layer('./hrrp_shapes/districts/Districts_hrrp.shp', 'dists', 'ogr')
    atlas.add_layer('./data/data.csv', 'data', 'ogr')

    atlas.join_lays(parent='wards', parent_code='N_WCode', to_join='data', to_join_code='N_WCode')

    atlas.apply_styling('dists', './styles/dist_style.qml')
    atlas.apply_styling('palikas', './styles/palika_style.qml')
    atlas.apply_styling('palika_hide', './styles/palika_hide_style.qml')
    atlas.apply_styling('wards', './styles/ward_style.qml')

    list = (29004,
            10001,
            39001,
            36001,
            13001,
            36002,
            38001,
            40001,
            43001,
            39002,
            10002,
            45001)
    atlas.make_atlas('palikas', 'svg')

    # atlas.make_atlas('palikas', 'svg', list)

    atlas.write_proj('./inprog.qgs')

    atlas.exit()


go()

# #show joins:
# lay.vectorJoins()
#
# #good way to do joins:
# import processing
# result = processing.runandload('qgis:joinattributestable', lay, csv, 'HLCIT_CODE', 'HLCIT_CODE', None)
#
# #apply styling to layers:
# l.loadNamedStyle()
#


