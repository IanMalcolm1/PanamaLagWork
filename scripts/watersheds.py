"""
Automation for making watershed polygons. Parameter layer names are hardcoded.
"""

import arcpy
from arcpy.sa import *
from arcpy.management import *
from arcpy.da import SearchCursor
from arcpy.conversion import RasterToPolygon

def Model():  # Model

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("spatial")

    flowacc_30m = arcpy.Raster("flowacc_30m")
    flowdir_30m = arcpy.Raster("flowdir_30m")

    acp_stations = MakeFeatureLayer("https://services.arcgis.com/o6oETlrWetREI1A2/arcgis/rest/services/ACP_CHCP_Estaciones_Hidrometeorol%C3%B3gicas/FeatureServer/0")
    
    watershed_polys = []
    with SearchCursor(acp_stations, ['ID', 'On_Major_River']) as stations_cursor:
        for station_row in stations_cursor:
            on_major_river = station_row[1]
            if not on_major_river:
                continue

            station_id = station_row[0]

            station_selection = SelectLayerByAttribute(
                acp_stations,
                selection_type='NEW_SELECTION',
                where_clause=f"ID = '{station_id}'"
            )

            snap_pour_point = SnapPourPoint(
                in_pour_point_data=station_selection,
                in_accumulation_raster=flowacc_30m,
                snap_distance=75,
                pour_point_field="Code"
                )
            
            watershed_raster = Watershed(
                in_flow_direction_raster=flowdir_30m,
                in_pour_point_data=snap_pour_point,
                pour_point_field="Value"
            )


            watershed_poly = f"memory/{station_id}"
            
            RasterToPolygon(watershed_raster, watershed_poly, simplify=True)

            AddField(watershed_poly, "Station_Id", "TEXT", field_length=3)
            CalculateField(watershed_poly, "Station_Id", f'"{station_id}"', "PYTHON3")

            watershed_polys.append(watershed_poly)

            del snap_pour_point
            del watershed_raster
            
    Merge(watershed_polys, "acp_station_watersheds")
    
    del acp_stations


if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace="C:\\Users\\ianma\\OneDrive - University of Redlands\\GisCapstone\\AlajuelaProject\\AlajuelaProject.gdb", workspace="C:\\Users\\ianma\\OneDrive - University of Redlands\\GisCapstone\\AlajuelaProject\\AlajuelaProject.gdb"):
        Model()
