import bpy
import bmesh


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
        return mesh

    def generate_door(self, width: float, height: float, cutout_frame: float, material: bpy.types.Material = None, strength: float = 4,
                      handle: bpy.types.Mesh = None, keyhole: bpy.types.Mesh = None, frame: bpy.types.Mesh = None,
                      handle_side_right: bool = False, inside: bool = True, double_doors: bool = False, sliding_door: bool = False):
        print("Generate Door")
        width = width / 100
        height = height / 100
        strength = strength / 100
        cutout_frame = cutout_frame / 100
        normal_door_mesh: bpy.types.Mesh = self.generate_normal_door(
            width, height, strength, cutout_frame)

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

        #TODO
        verts = [
            # unten 1
            (width_door/2 + width-cutout_door, 0, 0), (width_door/2-cutout_door, 0, 0), (width_door/2-cutout_door, -cutout_door, 0), (width_door/2-cutout_door - cutout_door, -cutout_door,
                                                                                           0), (width_door/2-cutout_door*2, -cutout_door - strength/2, 0), (width_door/2 + width-cutout_door, -cutout_door - strength/2, 0),
            # oben 1
            (width_door/2 + width-cutout_door, -cutout_door - strength/2, height_door+height), (width_door/2 + width-cutout_door, 0, height_door + height), (width_door/2-cutout_door, 0, height_door - cutout_door),
            (width_door/2-cutout_door, -cutout_door,height_door-cutout_door), (width_door/2-cutout_door-cutout_door, -cutout_door,height_door-cutout_door - cutout_2),(width_door/2-cutout_door-cutout_door, -cutout_door- strength/2,height_door-cutout_door- cutout_2),
            # oben mitte
            (0, -cutout_door - strength/2, height_door+height), (0, 0, height_door + height), (0, 0, height_door - cutout_door),
            (0, -cutout_door,height_door-cutout_door), (0, -cutout_door,height_door-cutout_door - cutout_2),(0, -cutout_door- strength/2,height_door-cutout_door- cutout_2),
            
            ]
        for v in verts:
            bm.verts.new(v)  # add all verts from array
        # bm.verts.new(verts[0])
        bm.verts.ensure_lookup_table()  # add [index] functionality

        #TODO
        faces = [
            (bm.verts[5], bm.verts[0], bm.verts[7], bm.verts[6]),
            (bm.verts[0], bm.verts[1],  bm.verts[8], bm.verts[7]),
            (bm.verts[1],  bm.verts[8], bm.verts[9], bm.verts[2]),
            (bm.verts[2],  bm.verts[3], bm.verts[10], bm.verts[9]),
            (bm.verts[3],  bm.verts[4], bm.verts[11], bm.verts[10]),
            (bm.verts[0], bm.verts[1], bm.verts[2], bm.verts[3], bm.verts[4], bm.verts[5]),
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
        obj = bpy.context.object
        mod = obj.modifiers.new('MirrorX', 'MIRROR')
        mod.use_axis[0] = True
        bpy.ops.object.modifier_apply(modifier='MirrorX')

        obj.matrix_world.translation = (0.0, strength/2+cutout_door, 0.0)
        bpy.ops.object.transform_apply(location=True, scale=False,rotation=False)

        mod = obj.modifiers.new('MirrorY', 'MIRROR')
        mod.use_axis[0] = False
        mod.use_axis[1] = True
        bpy.ops.object.modifier_apply(modifier='MirrorY')
        obj.matrix_world.translation = (0.0, -strength/2-cutout_door, 0.0)
        return mesh


def deleteAll():
    # delete old everything
    bpy.ops.object.select_all(action='SELECT')  # selektiert alle Objekte
    # löscht selektierte objekte
    bpy.ops.object.delete(use_global=False, confirm=False)
    bpy.ops.outliner.orphans_purge()  # löscht überbleibende Meshdaten etc.


# TODO deleteAll entfernen
deleteAll()

door = Door()
door.generate_door(120, 210, 2)  # Masse in cm
door.generate_frame(120, 210, 2, 25, 10, 25)
