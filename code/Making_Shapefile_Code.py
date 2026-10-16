import arcpy
import os

arcpy.env.overwriteOutput = True

# Get raster layer (not just text)
input_layer = arcpy.GetParameter(0)

# Get full path correctly
input_raster = input_layer.dataSource

# Extract name (without .tif)
name = os.path.splitext(os.path.basename(input_raster))[0]

# Get folder
folder = os.path.dirname(input_raster)

# Output shapefile
output_shapefile = os.path.join(folder, name + ".shp")

# Spatial Reference (WGS84)
spatial_ref = arcpy.SpatialReference(4326)

# ✅ Create empty polygon shapefile
arcpy.CreateFeatureclass_management(
    folder,
    name,
    "POLYGON",
    spatial_reference=spatial_ref
)

# ✅ Add fields
arcpy.AddField_management(output_shapefile, "zone_code", "TEXT", field_length=50)
arcpy.AddField_management(output_shapefile, "zone_name", "TEXT", field_length=255)

# ✅ Add to ArcMap
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]
arcpy.mapping.AddLayer(df, arcpy.mapping.Layer(output_shapefile))

arcpy.AddMessage("✅ Shapefile created successfully!")