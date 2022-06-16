import bpy
import bmesh
import math

from Scripts.materials import Materials


def deleteAll():
    # delete old everything
    # clear all materials
    for material in bpy.data.materials:
        material.user_clear()
        bpy.data.materials.remove(material)

    bpy.ops.object.select_all(action='SELECT')  # selektiert alle Objekte
    # löscht selektierte objekte
    bpy.ops.object.delete(use_global=False, confirm=False)
    bpy.ops.outliner.orphans_purge()  # löscht überbleibende Meshdaten etc.


def parenting(elements, parent):
    bpy.ops.object.select_all(action='DESELECT')  # deselect all object
    for element in elements:
        element.select_set(True)  # select the object for the 'parenting'
    # the active object will be the parent of all selected object
    bpy.context.view_layer.objects.active = parent
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

def prepare_mesh(meshname: str, object_name: str):
        mesh = bpy.data.meshes.new(meshname)  # add a new mesh
        # add a new object using the mesh
        obj = bpy.data.objects.new(object_name, mesh)
        scene = bpy.context.scene
        # put the object into the scene (link)
        scene.collection.objects.link(obj)
        # set as the active object in the scene
        bpy.context.view_layer.objects.active = obj
        obj.select_set(state=True)  # select object

        mesh = bpy.context.object.data
        return mesh

class Door:

    @staticmethod
    def __generate_normal_door(width: float, height: float, strength: float, cutout_frame: float):
        width = width / 100
        height = height / 100
        strength = strength / 100
        cutout_frame = cutout_frame / 100

        mesh_name = "normal_door"
        mesh: bpy.types.Mesh = prepare_mesh(mesh_name, mesh_name)
        bm = bmesh.new()

        # verticies
        verts = [
            (-width/2, strength/2, 0), (width/2, strength/2, 0), (width/2, -strength/2+cutout_frame, 0), (width/2-cutout_frame, -strength/2+cutout_frame, 0), (width/2 -
                                                                                                                                                               cutout_frame, -strength/2, 0), (-width/2+cutout_frame, -strength/2, 0), (-width/2+cutout_frame, -strength/2+cutout_frame, 0), (-width/2, -strength/2+cutout_frame, 0),
            (-width/2, strength/2, height), (width/2, strength/2, height), (width/2, -strength/2+cutout_frame, height), (width/2-cutout_frame, -strength/2+cutout_frame, height-cutout_frame), (width/2-cutout_frame, -
                                                                                                                                                                                                strength/2, height-cutout_frame), (-width/2+cutout_frame, -strength/2, height-cutout_frame), (-width/2+cutout_frame, -strength/2+cutout_frame, height-cutout_frame), (-width/2, -strength/2+cutout_frame, height)
        ]
        for v in verts:
            bm.verts.new(v)  # add all verts from array

        bm.verts.ensure_lookup_table()  # add [index] functionality
        # No edges, because should be defined through faces

        # faces
        faces = [
            (bm.verts[0], bm.verts[1], bm.verts[2], bm.verts[3],
             bm.verts[4], bm.verts[5], bm.verts[6], bm.verts[7]),
            (bm.verts[8], bm.verts[9], bm.verts[10], bm.verts[15]),
            (bm.verts[10], bm.verts[11], bm.verts[14], bm.verts[15]),
            (bm.verts[11], bm.verts[12], bm.verts[13], bm.verts[14]),
            (bm.verts[0], bm.verts[8], bm.verts[15], bm.verts[7]),
            (bm.verts[0], bm.verts[8], bm.verts[9], bm.verts[1]),
            (bm.verts[1], bm.verts[9], bm.verts[10], bm.verts[2]),
            (bm.verts[2], bm.verts[10], bm.verts[11], bm.verts[3]),
            (bm.verts[3], bm.verts[11], bm.verts[12], bm.verts[4]),
            (bm.verts[4], bm.verts[12], bm.verts[13], bm.verts[5]),
            (bm.verts[5], bm.verts[13], bm.verts[14], bm.verts[6]),
            (bm.verts[6], bm.verts[14], bm.verts[15], bm.verts[7])
        ]
        for f in range(len(faces)):
            bm.faces.new(faces[f])  # add all faces from array

        # make the bmesh the object's mesh
        bm.to_mesh(mesh)
        bm.free()  # always do this when finished
        obj: bpy.types.object = bpy.context.object
        return obj

    @staticmethod
    def __generate_frame(width_door: float, height_door: float, cutout_door: float, width: float, strength: float, height: float):

        width_door = width_door/100
        height_door = height_door/100
        cutout_door = cutout_door/100
        width = width / 100
        strength = strength / 100
        height = height / 100

        cutout_2 = 3/100

        mesh_name = "normal_door_frame"
        mesh: bpy.types.Mesh = prepare_mesh(mesh_name, mesh_name)
        bm = bmesh.new()

        verts = [
            # unten 1
            (width_door/2 + width-cutout_door, 0, 0), (width_door/2-cutout_door, 0, 0), (width_door/2-cutout_door, -cutout_door, 0), (width_door/2-cutout_door - cutout_door, -cutout_door,
                                                                                                                                      0), (width_door/2-cutout_door*2, -cutout_door - strength/2, 0), (width_door/2 + width-cutout_door, -cutout_door - strength/2, 0),
            # oben 1
            (width_door/2 + width-cutout_door, -cutout_door - strength/2, height_door+height), (width_door/2 + \
                                                                                                width-cutout_door, 0, height_door + height), (width_door/2-cutout_door, 0, height_door - cutout_door),
            (width_door/2-cutout_door, -cutout_door, height_door-cutout_door), (width_door/2-cutout_door-cutout_door, -cutout_door, height_door - \
                                                                                cutout_door - cutout_2), (width_door/2-cutout_door-cutout_door, -cutout_door - strength/2, height_door-cutout_door - cutout_2),
            # oben mitte
            (0, -cutout_door - strength/2, height_door+height), (0, 0,
                                                                 height_door + height), (0, 0, height_door - cutout_door),
            (0, -cutout_door, height_door-cutout_door), (0, -cutout_door, height_door-cutout_door - \
                                                         cutout_2), (0, -cutout_door - strength/2, height_door-cutout_door - cutout_2),

        ]
        for v in verts:
            bm.verts.new(v)  # add all verts from array
        # bm.verts.new(verts[0])
        bm.verts.ensure_lookup_table()  # add [index] functionality

        faces = [
            (bm.verts[5], bm.verts[0], bm.verts[7], bm.verts[6]),
            (bm.verts[0], bm.verts[1],  bm.verts[8], bm.verts[7]),
            (bm.verts[1],  bm.verts[8], bm.verts[9], bm.verts[2]),
            (bm.verts[2],  bm.verts[3], bm.verts[10], bm.verts[9]),
            (bm.verts[3],  bm.verts[4], bm.verts[11], bm.verts[10]),
            (bm.verts[0], bm.verts[1], bm.verts[2],
             bm.verts[3], bm.verts[4], bm.verts[5]),
            (bm.verts[6],  bm.verts[7], bm.verts[13], bm.verts[12]),
            (bm.verts[7],  bm.verts[13], bm.verts[14], bm.verts[8]),
            (bm.verts[8],  bm.verts[14], bm.verts[15], bm.verts[9]),
            (bm.verts[9],  bm.verts[15], bm.verts[16], bm.verts[10]),
            (bm.verts[10],  bm.verts[16], bm.verts[17], bm.verts[11]),
        ]
        for f in range(len(faces)):
            bm.faces.new(faces[f])  # add all faces from array

        # make the bmesh the object's mesh
        bm.to_mesh(mesh)
        bm.free()  # always do this when finished
        obj: bpy.types.object = bpy.context.object
        mod = obj.modifiers.new('MirrorX', 'MIRROR')
        mod.use_axis[0] = True
        bpy.ops.object.modifier_apply(modifier='MirrorX')

        obj.matrix_world.translation = (0.0, strength/2+cutout_door, 0.0)
        bpy.ops.object.transform_apply(
            location=True, scale=False, rotation=False)

        mod = obj.modifiers.new('MirrorY', 'MIRROR')
        mod.use_axis[0] = False
        mod.use_axis[1] = True
        bpy.ops.object.modifier_apply(modifier='MirrorY')
        obj.matrix_world.translation = (0.0, -strength/2-cutout_door, 0.0)
        return obj

    @staticmethod
    def __generate_keyhole(door: bpy.types.Object, height_door: float, width_door: float, fspace: float, radius: float, depth: float, under_hold: float, rad_hole: float):
        posx = width_door/2-fspace-radius
        posy = 0
        posz = height_door/2 - under_hold

        posx = posx/100
        posy = posy/100
        posz = posz/100
        radius = radius / 100
        depth = depth / 100
        rad_hole = rad_hole / 100
        under_hold = under_hold / 100

        bpy.types.Mesh = bpy.ops.mesh.primitive_cylinder_add(
            radius=radius,
            depth=depth,
            location=(posx, posy, posz)
        )

        keyhole = bpy.context.object

        bpy.types.Mesh = bpy.ops.mesh.primitive_cylinder_add(
            radius=rad_hole,
            depth=depth+0.1,
            location=(posx, posy, posz)
        )

        hole = bpy.context.object

        boolean = keyhole.modifiers.new(name="keyhole_bool", type="BOOLEAN")
        boolean.object = hole
        boolean.operation = "DIFFERENCE"

        keyhole.rotation_euler[0] = math.radians(90)

        hole.rotation_euler[0] = math.radians(90)

        boolean2 = door.modifiers.new(name="keyhole_bool2", type="BOOLEAN")
        boolean2.object = hole
        boolean2.operation = "DIFFERENCE"

        parenting([hole, keyhole], keyhole)
        hole.hide_set(True)
        return keyhole

    @staticmethod
    def __generate_doorhandle(height_door: float, width_door: float, fspace: float, radius: float, length_x: float, length_y: float):

        posx = width_door/2-fspace-radius
        posy = 0
        posz = height_door/2

        posx = posx/100
        posy = posy/100
        posz = posz/100
        radius = radius / 100
        length_x = length_x/100
        length_y = length_y/100

        mesh_name = "door_handle"
        mesh: bpy.types.Mesh = prepare_mesh(mesh_name, mesh_name)
        bm = bmesh.new()
        # verticies
        verts = [
            (posx, posy, posz), (posx, posy+length_y,
                                 posz), (posx-length_x, posy+length_y, posz)
        ]
        for v in verts:
            bm.verts.new(v)  # add all verts from array
        bm.verts.ensure_lookup_table()  # add [index] functionality
        edges = [(bm.verts[0], bm.verts[1]), (bm.verts[1], bm.verts[2])]
        for e in range(len(edges)):
            bm.edges.new(edges[e])
        # make the bmesh the object's mesh
        bm.to_mesh(mesh)
        bm.free()  # always do this when finished
        doorhandle: bpy.types.object = bpy.context.object
        # Modifiers
        mod_skin = doorhandle.modifiers.new(
            name="door_handle_skin", type="SKIN")
        mod_skin.use_smooth_shade = True
        for v in doorhandle.data.skin_vertices[0].data:
            v.radius = radius, radius
        mod_subdiv = doorhandle.modifiers.new(
            name="door_handle_subdiv", type="SUBSURF")
        mod_subdiv.levels = 1
        mod_subdiv.render_levels = 2
        mod_subdiv.quality = 3
        return doorhandle

    @staticmethod
    def generate_door(door_width: float = 120, door_height: float = 210, cutout_frame: float = 2, door_material: bpy.types.Material = None, door_strength: float = 4,
                      keyhole_space_from_doorside: float = 3, keyhole_radius: float = 2, keyhole_under_hold: float = 10, keyhole_hole_radius: float = 0.5, keyhole_material: bpy.types.Material = None,
                      handle_space_from_doorside: float = 5, handle_radius: float = 1.5, handle_away_from_door_length: float = 8, handle_length : float = 10, handle_material: bpy.types.Material = None,
                      frame_width: float = 25, frame_strength: float = 10, frame_height: float = 25, frame_material: bpy.types.Material = None,
                      handle_side_right: bool = False, inside: bool = True, double_doors: bool = False, sliding_door: bool = False):
        print("Generate Door")

        # TODO weitere Parameter programmieren

        if door_material == None:
            door_material = Materials.create_wood_material()
        if handle_material == None:
            handle_material = Materials.create_metal_material()
        if frame_material == None:
            frame_material = Materials.create_wood_material()
        if keyhole_material == None:
            keyhole_material = Materials.create_metal_material()
        
        normal_door: bpy.types.object = Door.__generate_normal_door(
            door_width, door_height, door_strength, cutout_frame)

        keyhole = Door.__generate_keyhole(
            normal_door, door_height, door_width, keyhole_space_from_doorside, keyhole_radius, door_strength+1, keyhole_under_hold, keyhole_hole_radius)
        door_handle = Door.__generate_doorhandle(door_height, door_width, handle_space_from_doorside, handle_radius, handle_away_from_door_length, handle_length)
        frame = Door.__generate_frame(door_width, door_height, cutout_frame, frame_width, frame_strength, frame_height)
        # parenting und Materialien
        normal_door.data.materials.append(door_material)
        frame.data.materials.append(frame_material)
        keyhole.data.materials.append(keyhole_material)
        door_handle.data.materials.append(handle_material)

        # parenting
        parenting([normal_door, frame, keyhole, door_handle], normal_door)
        return normal_door


# TODO deleteAll entfernen
deleteAll()

bpy.data.scenes["Scene"].eevee.use_ssr = True

door = Door.generate_door()  # Masse in cm