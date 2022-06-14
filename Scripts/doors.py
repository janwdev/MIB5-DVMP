import bpy
import bmesh
import math
import typing

from Scripts.materials import Materials


class Door:

    def prepare_mesh(self, meshname: str, object_name: str):
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

    def generate_normal_door(self, width: float, height: float, strenght: float, cutout_frame: float):
        mesh_name = "normal_door"
        mesh: bpy.types.Mesh = self.prepare_mesh(mesh_name, mesh_name)
        bm = bmesh.new()

        # verticies
        verts = [
            (-width/2, strenght/2, 0), (width/2, strenght/2, 0), (width/2, -strenght/2+cutout_frame, 0), (width/2-cutout_frame, -strenght/2+cutout_frame, 0), (width/2 -
                                                                                                                                                               cutout_frame, -strenght/2, 0), (-width/2+cutout_frame, -strenght/2, 0), (-width/2+cutout_frame, -strenght/2+cutout_frame, 0), (-width/2, -strenght/2+cutout_frame, 0),
            (-width/2, strenght/2, height), (width/2, strenght/2, height), (width/2, -strenght/2+cutout_frame, height), (width/2-cutout_frame, -strenght/2+cutout_frame, height-cutout_frame), (width/2-cutout_frame, -
                                                                                                                                                                                                strenght/2, height-cutout_frame), (-width/2+cutout_frame, -strenght/2, height-cutout_frame), (-width/2+cutout_frame, -strenght/2+cutout_frame, height-cutout_frame), (-width/2, -strenght/2+cutout_frame, height)
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
        obj:bpy.types.object = bpy.context.object
        return obj

    def generate_door(self, width: float, height: float, cutout_frame: float, material: bpy.types.Material = None, strength: float = 4,
                      handle: bpy.types.Mesh = None, keyhole: bpy.types.Mesh = None, frame: bpy.types.Mesh = None,
                      handle_side_right: bool = False, inside: bool = True, double_doors: bool = False, sliding_door: bool = False):
        print("Generate Door")
        width = width / 100
        height = height / 100
        strength = strength / 100
        cutout_frame = cutout_frame / 100
        normal_door: bpy.types.object = self.generate_normal_door(
            width, height, strength, cutout_frame)
        return normal_door

    def generate_frame(self, width_door: float, height_door: float, cutout_door: float, width: float, strength: float, height: float, material: bpy.types.Material = None):

        width_door = width_door/100
        height_door = height_door/100
        cutout_door = cutout_door/100
        width = width / 100
        strength = strength / 100
        height = height / 100

        cutout_2 = 3/100

        mesh_name = "normal_door_frame"
        mesh: bpy.types.Mesh = self.prepare_mesh(mesh_name, mesh_name)
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
        obj:bpy.types.object = bpy.context.object
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

    def generate_keyhole(self, posx_door: int, posy_door: int, posz_door: int, rot_door: float, height_door: float, width_door: float, strength_door: float, fspace: float, radius: float, depth: float, under_hold: float, rad_hole: float = 0.5):
        door = bpy.context.object
        # TODO xyz ueberpruefen
        # TODO einbauen wenn negativ
        posx = posx_door + width_door/2-fspace-radius
        posy = posy_door
        posz = posz_door + height_door/2 - under_hold

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

        # TODO funktioniert nicht, deshalb verstecken
        # bpy.ops.object.modifier_apply(modifier=boolean.name)
        # bpy.ops.object.delete()
        hole.hide_set(True)

        keyhole.rotation_euler[0] = math.radians(90)
        keyhole.rotation_euler[2] = math.radians(rot_door)

        hole.rotation_euler[0] = math.radians(90)
        hole.rotation_euler[2] = math.radians(rot_door)

        boolean2 = door.modifiers.new(name="keyhole_bool2", type="BOOLEAN")
        boolean2.object = hole
        boolean2.operation = "DIFFERENCE"
        
        # parenting auf Keyhole
        bpy.ops.object.select_all(action='DESELECT') #deselect all object
        hole.select_set(True) #select the object for the 'parenting'
        keyhole.select_set(True)
        bpy.context.view_layer.objects.active = keyhole    #the active object will be the parent of all selected object
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

        return keyhole

    def generate_doorhandle(self, posx_door: float, posy_door: float, posz_door: float, height_door: float, width_door: float, fspace: float, radius: float, radius_handle: float):
        print("Doorhandle")

        posx = posx_door + width_door/2-fspace-radius
        posy = posy_door
        posz = posz_door + height_door/2

        posx = posx/100
        posy = posy/100
        posz = posz/100
        radius = radius / 100
        radius_handle = radius_handle/100
        lengthx = 8/100  # TODO dynamisch
        lengthy = 10/100
        mesh_name = "door_handle"
        mesh: bpy.types.Mesh = self.prepare_mesh(mesh_name, mesh_name)
        bm = bmesh.new()
        # verticies
        verts = [
            (posx, posy, posz), (posx, posy+lengthy,
                                 posz), (posx-lengthx, posy+lengthy, posz)
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
        doorhandle:bpy.types.object = bpy.context.object
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


def deleteAll():
    # delete old everything
    ## clear all materials
    for material in bpy.data.materials:
        material.user_clear()
        bpy.data.materials.remove(material)

    bpy.ops.object.select_all(action='SELECT')  # selektiert alle Objekte
    # löscht selektierte objekte
    bpy.ops.object.delete(use_global=False, confirm=False)
    bpy.ops.outliner.orphans_purge()  # löscht überbleibende Meshdaten etc.


# TODO deleteAll entfernen
deleteAll()

bpy.data.scenes["Scene"].eevee.use_ssr = True

doorFac = Door()
door = doorFac.generate_door(120, 210, 2)  # Masse in cm
frame = doorFac.generate_frame(120, 210, 2, 25, 10, 25)
keyhole = doorFac.generate_keyhole(0, 0, 0, 0, 210, 120, 4, 3, 2, 5, 10)
door_handle = doorFac.generate_doorhandle(0, 0, 0, 210, 120, 5, 1.5, 1)

material = Materials()
door.data.materials.append(material.create_wood_material())
frame.data.materials.append(material.create_wood_material())
keyhole.data.materials.append(material.create_metal_material())
door_handle.data.materials.append(material.create_metal_material())

# parenting
bpy.ops.object.select_all(action='DESELECT') #deselect all object
door.select_set(True) #select the object for the 'parenting'
frame.select_set(True)
keyhole.select_set(True)
door_handle.select_set(True)
bpy.context.view_layer.objects.active = door    #the active object will be the parent of all selected object
bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

# TODO return door