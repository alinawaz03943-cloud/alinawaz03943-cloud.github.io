from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsField

# Get the active (selected) layer
layer = iface.activeLayer()

if layer is None:
    print("No layer selected!")
else:
    provider = layer.dataProvider()

    # Check existing fields
    existing_fields = [field.name() for field in layer.fields()]

    new_fields = []

    # Add zone_code field if it doesn't exist
    if "zone_code" not in existing_fields:
        new_fields.append(QgsField("zone_code", QVariant.String, len=50))

    # Add zone_name field if it doesn't exist
    if "zone_name" not in existing_fields:
        new_fields.append(QgsField("zone_name", QVariant.String, len=255))

    if new_fields:
        provider.addAttributes(new_fields)
        layer.updateFields()
        print("Fields added successfully.")
    else:
        print("Fields already exist.")