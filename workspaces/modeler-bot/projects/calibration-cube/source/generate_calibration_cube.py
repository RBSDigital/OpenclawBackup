import bpy

ROOT = "/home/vin/.openclaw/workspaces/modeler-bot/projects/calibration-cube"
BLEND_PATH = ROOT + "/source/calibration_cube_version_0.1.0.blend"
STL_PATH = ROOT + "/exports/calibration_cube_version_0.1.0.stl"

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

scene = bpy.context.scene
scene.unit_settings.system = "METRIC"
scene.unit_settings.length_unit = "MILLIMETERS"
scene.unit_settings.scale_length = 0.001

bpy.ops.mesh.primitive_cube_add(size=20, location=(0, 0, 10))
cube = bpy.context.object
cube.name = "calibration_cube_20mm"

bpy.ops.object.text_add(location=(-7.4, -4.2, 20.0), rotation=(0, 0, 0))
text = bpy.context.object
text.name = "embossed_20mm_label"
text.data.body = "20MM"
text.data.align_x = "LEFT"
text.data.align_y = "CENTER"
text.data.size = 4.5
text.data.extrude = 0.8

bpy.ops.object.convert(target="MESH")
label = bpy.context.object
label.name = "embossed_20mm_label_mesh"

bpy.ops.object.select_all(action="DESELECT")
cube.select_set(True)
label.select_set(True)
bpy.context.view_layer.objects.active = cube
bpy.ops.object.join()
model = bpy.context.object
model.name = "calibration_cube_version_0.1.0"

bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.mesh.remove_doubles(threshold=0.0001)
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.object.mode_set(mode="OBJECT")

bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)

bpy.ops.object.select_all(action="DESELECT")
model.select_set(True)
bpy.context.view_layer.objects.active = model
bpy.ops.wm.stl_export(filepath=STL_PATH, export_selected_objects=True, apply_modifiers=True)

print("saved_blend=" + BLEND_PATH)
print("saved_stl=" + STL_PATH)

