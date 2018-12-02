import os
import sys
import csv

sys.path.append('/Applications/QGis3.app/Contents/Resources/python/')
# sys.path.append('/Applications/QGis3.app/Contents/Resources/python/plugins') # if you want to use the processing module, for example
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/Applications/QGIS3.app/Contents/Plugins'

from qgis.core import *
from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt.QtCore import QVariant
from openpyxl import load_workbook


# from PyQt5.QtGui import *

class at(object):
    def __init__(self, data_uri, wards_uri, palika_uri, dists_uri, dists_syle, pka_style, pka_hide_style, ward_style,
                        parent_join_cd, to_join_code, pka_list = None):
        self.app = QgsApplication([], False)
        self.app.setPrefixPath('/Applications/QGIS3.app/Contents/MacOS', True)
        self.app.initQgis()

        self.project = QgsProject.instance()
        self.project.setCrs(QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId))

        self.data_uri = data_uri
        self.wards_uri = wards_uri
        self.palika_uri = palika_uri
        self.dists_uri = dists_uri
        self.dists_syle = dists_syle
        self.pka_style = pka_style
        self.pka_hide_style = pka_hide_style
        self.ward_style = ward_style
        self.parent_join_cd = parent_join_cd
        self.to_join_code = to_join_code
        self.pka_list = pka_list

    def make_maps(self):
        self.add_layer(self.get_map_data(self.data_uri, 'Map Data'))
        self.add_layer(self.wards_uri, 'wards', 'ogr')
        self.add_layer(self.palika_uri, 'palika_hide', 'ogr') # for hiding other palikas while atlasing
        self.add_layer(self.palika_uri, 'palikas', 'ogr')
        self.add_layer(self.dists_uri, 'dists', 'ogr')

        self.join_lays(parent='wards', parent_code=self.parent_join_cd, to_join='data', to_join_code=self.to_join_code)

        self.apply_styling('dists', self.dists_syle)
        self.apply_styling('palikas', self.pka_style)
        self.apply_styling('palika_hide', self.pka_hide_style)
        self.apply_styling('wards', self.ward_style)

        self.make_atlas('palikas', 'svg')
        self.write_proj('./inprog.qgs')

        self.exit()

    def add_layer(self, *args):
        """check to see if layer properly added.
            can also add with QgsProject.instance().addMapLayer() """

        #check to see if we're sending an already formed layer to add
        if len(args) == 1 & isinstance(args[0], QgsVectorLayer):
            self.project.addMapLayer(args[0])
            nm = args[0].name()

        else:
            self.project.addMapLayer(QgsVectorLayer(*args))
            nm = args[1]

        self.get_layer(nm)

    def get_layer(self, nm):
        # return layer object based on its given name, not Qs internal identifier
        #if the name isn't there, return none
        layz = {v.name(): v for k, v in self.project.layerStore().mapLayers().items()}
        if nm in layz:
            return layz[nm]

        else:
            raise Exception("%s not in layer listing!" %nm)

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

    def get_layers(self):
        return self.project.layerStore().mapLayers()


    def apply_styling(self, lay, style):
        self.get_layer(lay).loadNamedStyle(style)

    def _open_atlas_styling(self):
        with open('./styles/atlas_layout.qpt', 'r') as templateFile:
            self.templateContent = templateFile.read()

        self.document = QDomDocument()
        self.document.setContent(self.templateContent)

    def make_atlas(self, at_lay, type):
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

        if self.pka_list:
            # list = tuple([i for i in range(51001, 51003)])
            self.myAtlas.setFilterExpression('"PalikaCode" IN %s' % str(self.pka_list))

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

    def _get_xls_row_vals(self, row):
        """get all values from an excel row"""
        return [v.value for v in row]

    def _transform_map_data(self):
        """
        take palika | ward 1 ... | ward n layout to palika-# | val
        returns a list of tuples
        """
        WARD_FMT = '%s-%s'
        self.map_data_trans = []
        lookup = {i.column: ''.join(filter(lambda x: x.isdigit(), i.value)) for i in self.sht[1]}

        #skip over header
        rs = iter(self.sht.rows)
        next(rs)
        next(rs)
        for r in rs:
            pka = r[0].value
            for c in r[1:]:
                if c.value is None:
                    c.value = 0

                self.map_data_trans.append((WARD_FMT%(pka, lookup[c.column]), c.value))

    def get_map_data(self, uri, sht_nm):
        """
        work around for pulling out Map Data sheet and writing to csv then reading as layer
        """
        self.wb = load_workbook(uri, data_only=True)
        self.sht = self.wb.get_sheet_by_name(sht_nm)
        TMP_DATA = 'tmp_data.csv'

        self._transform_map_data()

        with open('./data/%s' % TMP_DATA, 'w', newline="") as f:
            c = csv.writer(f)
            c.writerow(('ward','value'))
            for r in self.map_data_trans:
                c.writerow(r)

        vl = QgsVectorLayer('./data/%s' % TMP_DATA, 'data', 'ogr')

        return vl

    def exit(self):
        self.app.exitQgis()