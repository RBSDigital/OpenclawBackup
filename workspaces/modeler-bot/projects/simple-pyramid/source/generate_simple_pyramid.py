from pathlib import Path

import bpy

ROOT = Path("/home/vin/.openclaw/workspaces/modeler-bot/projects/simple-pyramid")
VERSION = "version_0.1.0"
SLUG = "simple_pyramid"
BLEND_PATH = ROOT / "source" / f"{SLUG}_{VERSION}.blend"
STL_PATH = ROOT / "exports" / f"{SLUG}_{VERSION}.stl"

BASE_MM = 60.0
HEIGHT_MM = 60.0


def reset_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def configure_units():
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "MILLIMETERS"
    scene.unit_settings.scale_length = 0.001


def create_pyramid():
    half = BASE_MM / 2.0
    vertices = [
        (-half, -half, 0.0),
        (half, -half, 0.0),
        (half, half, 0.0),
        (-half, half, 0.0),
        (0.0, 0.0, HEIGHT_MM),
    ]
    faces = [
        (3, 2, 1, 0),
        (0, 1, 4),
        (1, 2, 4),
        (2, 3, 4),
        (3, 0, 4),
    ]

    mesh = bpy.data.meshes.new("simple_pyramid_mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    model = bpy.data.objects.new(f"simple_pyramid_{VERSION}", mesh)
    bpy.context.collection.objects.link(model)
    bpy.context.view_layer.objects.active = model
    model.select_set(True)

    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.remove_doubles(threshold=0.0001)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode="OBJECT")
    return model


def add_view_setup(model):
    mat = bpy.data.materials.new("matte_warm_gray")
    mat.diffuse_color = (0.72, 0.69, 0.63, 1.0)
    model.data.materials.append(mat)

    bpy.ops.object.light_add(type="AREA", location=(0, -90, 120))
    light = bpy.context.object
    light.name = "preview_key_light"
    light.data.energy = 350
    light.data.size = 80

    bpy.ops.object.camera_add(location=(85, -105, 75), rotation=(1.1, 0.0, 0.68))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    camera.data.lens = 55

    scene = bpy.context.scene
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 900
    scene.eevee.taa_render_samples = 64
    scene.world.color = (1.0, 1.0, 1.0)


def main():
    reset_scene()
    configure_units()
    model = create_pyramid()
    add_view_setup(model)

    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    bpy.ops.object.select_all(action="DESELECT")
    model.select_set(True)
    bpy.context.view_layer.objects.active = model
    bpy.ops.wm.stl_export(
        filepath=str(STL_PATH),
        export_selected_objects=True,
        apply_modifiers=True,
    )

    print("saved_blend=" + str(BLEND_PATH))
    print("saved_stl=" + str(STL_PATH))


if __name__ == "__main__":
    main()
