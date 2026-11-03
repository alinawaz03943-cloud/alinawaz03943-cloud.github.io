import os
from qgis.core import QgsProject, QgsVectorLayer

# === SET THIS TO THE SAME PATH AS YOUR EXPORT SCRIPT ===
INPUT_FOLDER = r"path/to/your/shapefile/folder"

def load_shapefiles_recursive(folder_path):
    """
    Recursively finds all .shp files in folder_path and loads them into QGIS.
    """
    if not os.path.exists(folder_path):
        print(f"❌ Error: The folder '{folder_path}' does not exist.")
        return

    project = QgsProject.instance()
    # Get list of currently loaded layer names to avoid duplicates (optional check)
    existing_names = [l.name() for l in project.mapLayers().values()]
    
    count = 0
    print(f"📂 Scanning: {folder_path} ...")

    # os.walk traverses the directory tree (root, directories, files)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # We only care about .shp files (ignore .shx, .dbf, etc.)
            if file.lower().endswith(".shp"):
                full_path = os.path.join(root, file)
                base_name = os.path.splitext(file)[0]
                
                # Check if a valid layer
                layer = QgsVectorLayer(full_path, base_name, "ogr")
                
                if not layer.isValid():
                    print(f"⚠️  Invalid layer, skipping: {base_name}")
                    continue
                
                # (Optional) Skip if already loaded to prevent duplicates
                # Uncomment the next 2 lines if you don't want duplicates:
                # if base_name in existing_names:
                #     print(f"⏭️  Already loaded: {base_name}")
                #     continue

                # Add to project
                project.addMapLayer(layer)
                print(f"✅ Loaded: {base_name}")
                count += 1

    print("-" * 30)
    print(f"🎉 Process Complete. Loaded {count} shapefiles.")

# Run the function
load_shapefiles_recursive(INPUT_FOLDER)