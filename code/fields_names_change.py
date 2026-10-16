from qgis.PyQt.QtWidgets import QMessageBox

layer = iface.activeLayer()

if not layer:
    QMessageBox.warning(None, "No Layer Selected", "Please select a layer first.")
else:
    field_names = [field.name() for field in layer.fields()]

    changes = {}

    # Rename zone_code → overlay_code
    if "zone_code" in field_names:
        changes[layer.fields().indexOf("zone_code")] = "overlay_code"

    # Rename zone_name → overlay_name
    if "zone_name" in field_names:
        changes[layer.fields().indexOf("zone_name")] = "overlay_name"

    if not changes:
        QMessageBox.warning(
            None,
            "Fields Not Found",
            "The fields 'zone_code' and 'zone_name' were not found."
        )
    else:
        layer.startEditing()

        if layer.dataProvider().renameAttributes(changes):
            layer.updateFields()
            layer.commitChanges()

            QMessageBox.information(
                None,
                "Success",
                "Fields renamed successfully:\n"
                "zone_code → overlay_code\n"
                "zone_name → overlay_name"
            )
        else:
            layer.rollBack()
            QMessageBox.critical(
                None,
                "Error",
                "Could not rename the fields."
            )