"""Render a seamless Blender/Eevee holographic AI-core loop for the profile hero."""
from pathlib import Path
import math
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
FRAMES = ROOT / "assets" / "jarvis-frames"
FRAMES.mkdir(parents=True, exist_ok=True)
FPS, FRAME_END = 15, 60

for block in bpy.data.objects:
    bpy.data.objects.remove(block, do_unlink=True)
for collection in (bpy.data.materials, bpy.data.cameras, bpy.data.lights):
    pass

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 578
scene.render.resolution_y = 620
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.fps = FPS
scene.frame_start, scene.frame_end = 1, FRAME_END
scene.render.film_transparent = False
scene.world.color = (0.002, 0.006, 0.015)
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.001, 0.005, 0.018, 1)
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = .08
scene.view_settings.look = "AgX - Medium High Contrast"

def material(name, color, metallic=0, roughness=.35, emission=None, strength=0, transmission=0, alpha=1):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, alpha)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if emission:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1)
        bsdf.inputs["Emission Strength"].default_value = strength
    if transmission:
        bsdf.inputs["Transmission Weight"].default_value = transmission
        bsdf.inputs["Alpha"].default_value = alpha
        mat.surface_render_method = "DITHERED"
    return mat

metal = material("Titanium alloy", (0.025, .07, .11), .92, .19)
metal_lit = material("Blue anodized metal", (.015, .13, .22), .8, .22, (.02, .18, .35), .35)
glass = material("Ionized glass", (.02, .23, .36), .22, .09, (.01, .20, .38), .4, .58, .22)
cyan = material("Cyan energy", (.01, .35, .6), .1, .16, (.02, .65, 1), 8)
blue = material("Blue energy", (.015, .08, .7), .05, .22, (.04, .15, 1), 5)
dark = material("Panel black", (.002, .008, .018), .2, .28)

def smooth(obj):
    if hasattr(obj.data, "polygons"):
        for p in obj.data.polygons:
            p.use_smooth = True

def torus(name, major, minor, mat, rotation=(0,0,0), segments=96, minor_segments=16):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=segments, minor_segments=minor_segments, location=(0,0,0), rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    smooth(obj)
    return obj

def cylinder(name, radius, depth, mat, z=0, vertices=96):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=(0,0,z))
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    bevel = obj.modifiers.new("machined bevel", "BEVEL")
    bevel.width, bevel.segments = .035, 3
    return obj

def key_rotate(obj, axis, turns, phase=0):
    obj.rotation_euler[axis] = phase
    obj.keyframe_insert("rotation_euler", index=axis, frame=1)
    obj.rotation_euler[axis] = phase + math.tau * turns
    obj.keyframe_insert("rotation_euler", index=axis, frame=FRAME_END)

def orbit_marker(radius, angle, z, size, mat):
    bpy.ops.mesh.primitive_cube_add(location=(radius * math.cos(angle), radius * math.sin(angle), z))
    obj = bpy.context.object
    obj.name = "rotor tick"
    obj.scale = (.035, .14, .055)
    obj.rotation_euler = (0, 0, angle + math.pi / 2)
    obj.data.materials.append(mat)
    bevel = obj.modifiers.new("micro bevel", "BEVEL")
    bevel.width, bevel.segments = .025, 2
    return obj

# Back panel and emission halo form the lab-projected volume behind the physical assembly.
panel = cylinder("recessed holo chamber", 4.7, .16, dark, z=-.58)
panel.scale.y = .88
halo = torus("volumetric halo", 3.48, .045, blue, rotation=(0,0,0), segments=128, minor_segments=10)
halo.scale.y = .84
halo.location.z = -.42

outer = torus("outer gimbal", 3.05, .105, metal_lit, rotation=(math.radians(68), 0, math.radians(8)))
inner = torus("inner gimbal", 2.42, .075, metal, rotation=(math.radians(22), math.radians(64), 0))
glass_ring = torus("transparent data ring", 2.73, .034, glass, rotation=(math.radians(86), math.radians(6), 0))
scan_ring = torus("scanning ring", 1.72, .035, cyan, rotation=(math.radians(76), math.radians(12), 0))
key_rotate(outer, 2, 1.0)
key_rotate(inner, 1, -1.55, .3)
key_rotate(glass_ring, 2, -2.2)
key_rotate(scan_ring, 0, 2.8, .5)

# Mechanical tick arrays create readable depth at small GIF sizes.
tick_group = bpy.data.objects.new("outer rotating indicators", None)
bpy.context.collection.objects.link(tick_group)
for i in range(28):
    tick = orbit_marker(3.05, i * math.tau / 28, .05, .035, metal_lit if i % 4 else cyan)
    tick.parent = tick_group
key_rotate(tick_group, 2, 1.0)

inner_ticks = bpy.data.objects.new("inner rotating indicators", None)
bpy.context.collection.objects.link(inner_ticks)
for i in range(18):
    tick = orbit_marker(1.7, i * math.tau / 18, .12, .03, cyan if i % 3 else blue)
    tick.parent = inner_ticks
key_rotate(inner_ticks, 2, -2.5)

# Central energy assembly: glass shell, metallic cage and emissive core.
bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, location=(0,0,.15), scale=(.82,.82,.82))
shell = bpy.context.object
shell.name = "refractive holographic shell"
shell.data.materials.append(glass)
smooth(shell)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=.43, location=(0,0,.15))
core = bpy.context.object
core.name = "pulsing energy core"
core.data.materials.append(cyan)
smooth(core)
core.scale = (.78,.78,.78)
core.keyframe_insert("scale", frame=1)
core.scale = (1.05,1.05,1.05)
core.keyframe_insert("scale", frame=31)
core.scale = (.78,.78,.78)
core.keyframe_insert("scale", frame=FRAME_END)

cage = torus("core cage A", .93, .035, metal_lit, rotation=(math.radians(70), 0, 0))
cage_b = torus("core cage B", .93, .035, metal_lit, rotation=(math.radians(12), math.radians(72), 0))
key_rotate(cage, 2, 3)
key_rotate(cage_b, 1, -2)

# Light columns and particles use true 3D emissive mesh elements.
for angle in (0, math.pi/2, math.pi, 3*math.pi/2):
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=.022, depth=4.8, location=(0,0,.28), rotation=(math.pi/2,0,angle))
    beam = bpy.context.object
    beam.name = "volumetric scan beam"
    beam.data.materials.append(blue)
    beam.keyframe_insert("rotation_euler", index=2, frame=1)
    beam.rotation_euler.z += math.tau
    beam.keyframe_insert("rotation_euler", index=2, frame=FRAME_END)

for i in range(70):
    angle = i * 2.399963229728653
    radius = 1.05 + (i % 10) * .23
    z = -1.0 + (i % 11) * .19
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=.014 + (i % 3)*.007, location=(radius*math.cos(angle), radius*math.sin(angle), z))
    particle = bpy.context.object
    particle.name = "floating data particle"
    particle.data.materials.append(cyan if i % 4 else blue)
    original_z = particle.location.z
    particle.keyframe_insert("location", frame=1)
    particle.location.z += .18 + (i % 5)*.05
    particle.rotation_euler.z += .2
    particle.keyframe_insert("location", frame=31)
    particle.location.z = original_z
    particle.keyframe_insert("location", frame=FRAME_END)

# Cinematic lighting with cyan rim lights, a cool key, and a soft back glow.
def point(name, location, energy, color, radius):
    bpy.ops.object.light_add(type="POINT", location=location)
    light = bpy.context.object
    light.name = name
    light.data.energy, light.data.color, light.data.shadow_soft_size = energy, color, radius
    return light
point("cyan key", (2.8,-3.2,4.8), 920, (.10,.68,1), 2.2)
point("blue rim", (-3.5,1.8,2.2), 760, (.04,.18,1), 2.0)
point("white core bounce", (0,-.8,1.8), 420, (.55,.95,1), 1.4)

bpy.ops.object.camera_add(location=(0,-11.8,2.6))
camera = bpy.context.object
camera.data.lens = 52
scene.camera = camera
target = Vector((0,0,.1))
camera.rotation_euler = (target - camera.location).to_track_quat('-Z','Y').to_euler()

for frame in range(1, FRAME_END + 1):
    scene.frame_set(frame)
    scene.render.filepath = str(FRAMES / f"core_{frame:03d}.png")
    bpy.ops.render.render(write_still=True)
print(f"Rendered {FRAME_END} Blender frames to {FRAMES}")
