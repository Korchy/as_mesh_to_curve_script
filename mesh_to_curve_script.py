import bpy
from mathutils import Vector

merge_threshold = 0.05
scene_origin_point = Vector((0.0, 0.0, 0.0))

bpy.ops.object.mode_set(mode='OBJECT')

# separate by loose parts
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.select_set(True)
        bpy.ops.mesh.separate(type='LOOSE')

# merge vertices by distance
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=merge_threshold)
        bpy.ops.object.mode_set(mode='OBJECT')

# to curves
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        if len(obj.data.vertices) <= 1:
            bpy.data.objects.remove(obj, do_unlink=True)
        else:
            # to curve
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.object.convert(target='CURVE')

# tune curve direction
for obj in bpy.data.objects:
    if obj.type == 'CURVE':
        for spline in obj.data.splines:
            p_first_world = obj.matrix_world @ spline.points[0].co.to_3d()
            p_last_world = obj.matrix_world @ spline.points[-1].co.to_3d()
            if (scene_origin_point - p_first_world).length > (scene_origin_point - p_last_world).length:
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.curve.switch_direction()
                bpy.ops.object.mode_set(mode='OBJECT')
