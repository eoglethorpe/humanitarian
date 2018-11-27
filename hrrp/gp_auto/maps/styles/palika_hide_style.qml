<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyAlgorithm="0" labelsEnabled="0" version="3.4.1-Madeira" minScale="1e+8" simplifyDrawingHints="1" simplifyMaxScale="1" maxScale="0" simplifyDrawingTol="1" simplifyLocal="1" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" readOnly="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" preprocessing="0" forceraster="0" type="invertedPolygonRenderer">
    <renderer-v2 symbollevels="0" enableorderby="0" forceraster="0" type="RuleRenderer">
      <rules key="{d983cff8-54c5-4015-ab53-918fde039d55}">
        <rule symbol="0" key="{3df8d7f7-c301-4a36-a594-c229d13c2dba}" filter="$id =  @atlas_featureid"/>
      </rules>
      <symbols>
        <symbol alpha="1" clip_to_extent="1" type="fill" name="0">
          <layer enabled="1" class="SimpleFill" pass="0" locked="0">
            <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="color" v="255,255,255,255"/>
            <prop k="joinstyle" v="bevel"/>
            <prop k="offset" v="0,0"/>
            <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="offset_unit" v="MM"/>
            <prop k="outline_color" v="35,35,35,255"/>
            <prop k="outline_style" v="dot"/>
            <prop k="outline_width" v="0.46"/>
            <prop k="outline_width_unit" v="MM"/>
            <prop k="style" v="solid"/>
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </symbols>
    </renderer-v2>
  </renderer-v2>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory enabled="0" penWidth="0" minScaleDenominator="0" lineSizeScale="3x:0,0,0,0,0,0" opacity="1" penColor="#000000" sizeScale="3x:0,0,0,0,0,0" backgroundColor="#ffffff" penAlpha="255" width="15" labelPlacementMethod="XHeight" sizeType="MM" height="15" rotationOffset="270" backgroundAlpha="255" scaleBasedVisibility="0" scaleDependency="Area" diagramOrientation="Up" minimumSize="0" lineSizeType="MM" barWidth="5" maxScaleDenominator="1e+8">
      <fontProperties description=".SF NS Text,13,-1,5,50,0,0,0,0,0" style=""/>
      <attribute label="" color="#000000" field=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings showAll="1" obstacle="0" dist="0" placement="1" zIndex="0" priority="0" linePlacementFlags="18">
    <properties>
      <Option type="Map">
        <Option value="" type="QString" name="name"/>
        <Option name="properties"/>
        <Option value="collection" type="QString" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="FIRST_DIST">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="FIRST_GaPa">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="FIRST_Type">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="PalikaCode">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="dist_cod">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" field="FIRST_DIST" name=""/>
    <alias index="1" field="FIRST_GaPa" name=""/>
    <alias index="2" field="FIRST_Type" name=""/>
    <alias index="3" field="PalikaCode" name=""/>
    <alias index="4" field="dist_cod" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="FIRST_DIST"/>
    <default expression="" applyOnUpdate="0" field="FIRST_GaPa"/>
    <default expression="" applyOnUpdate="0" field="FIRST_Type"/>
    <default expression="" applyOnUpdate="0" field="PalikaCode"/>
    <default expression="" applyOnUpdate="0" field="dist_cod"/>
  </defaults>
  <constraints>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="FIRST_DIST" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="FIRST_GaPa" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="FIRST_Type" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="PalikaCode" unique_strength="0"/>
    <constraint constraints="0" notnull_strength="0" exp_strength="0" field="dist_cod" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="FIRST_DIST"/>
    <constraint exp="" desc="" field="FIRST_GaPa"/>
    <constraint exp="" desc="" field="FIRST_Type"/>
    <constraint exp="" desc="" field="PalikaCode"/>
    <constraint exp="" desc="" field="dist_cod"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column width="-1" hidden="0" type="field" name="FIRST_DIST"/>
      <column width="-1" hidden="0" type="field" name="FIRST_GaPa"/>
      <column width="-1" hidden="0" type="field" name="FIRST_Type"/>
      <column width="-1" hidden="0" type="field" name="PalikaCode"/>
      <column width="-1" hidden="0" type="field" name="dist_cod"/>
      <column width="-1" hidden="1" type="actions"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="1" name="FIRST_DIST"/>
    <field editable="1" name="FIRST_GaPa"/>
    <field editable="1" name="FIRST_Type"/>
    <field editable="1" name="PalikaCode"/>
    <field editable="1" name="dist_cod"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="FIRST_DIST"/>
    <field labelOnTop="0" name="FIRST_GaPa"/>
    <field labelOnTop="0" name="FIRST_Type"/>
    <field labelOnTop="0" name="PalikaCode"/>
    <field labelOnTop="0" name="dist_cod"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>FIRST_DIST</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
