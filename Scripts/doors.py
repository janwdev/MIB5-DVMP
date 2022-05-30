import bpy
import bmesh


class Door:

    def generate_normal_door(self,width: float, height: float, strenght: float, cutout_frame: float):
        mesh_name = "normal_door"
        object_name = mesh_name
        mesh = bpy.data.meshes.new(mesh_name)  # add a new mesh
        # add a new object using the mesh
        obj = bpy.data.objects.new(object_name, mesh)
        scene = bpy.context.scene
        # put the object into the scene (link)
        scene.collection.objects.link(obj)
        # set as the active object in the scene
        bpy.context.view_layer.objects.active = obj
        obj.select_set(state=True)  # select object

        mesh = bpy.context.object.data
        bm = bmesh.new()

        # verticies
        verts = [
            (-width/2, strenght/2, 0),(width/2, strenght/2, 0), (width/2, -strenght/2+cutout_frame, 0), (width/2-cutout_frame, -strenght/2+cutout_frame, 0),(width/2-cutout_frame, -strenght/2, 0),(-width/2+cutout_frame, -strenght/2, 0), (-width/2+cutout_frame, -strenght/2+cutout_frame, 0),(-width/2, -strenght/2+cutout_frame, 0),
            (-width/2, strenght/2, height),(width/2, strenght/2, height), (width/2, -strenght/2+cutout_frame, height), (width/2-cutout_frame, -strenght/2+cutout_frame, height-cutout_frame),(width/2-cutout_frame, -strenght/2, height-cutout_frame),(-width/2+cutout_frame, -strenght/2, height-cutout_frame), (-width/2+cutout_frame, -strenght/2+cutout_frame, height-cutout_frame),(-width/2, -strenght/2+cutout_frame, height)
        ]
        for v in verts:
            bm.verts.new(v)  # add all verts from array

        bm.verts.ensure_lookup_table()  # add [index] functionality
        # No edges, because should be defined through faces

        # faces
        faces = [
            (bm.verts[0], bm.verts[1], bm.verts[2], bm.verts[3], bm.verts[4], bm.verts[5], bm.verts[6], bm.verts[7]),
            (bm.verts[8], bm.verts[9], bm.verts[10],bm.verts[15]),
            (bm.verts[10], bm.verts[11], bm.verts[14],bm.verts[15]),
            (bm.verts[11], bm.verts[12], bm.verts[13],bm.verts[14]),
            (bm.verts[0],bm.verts[8],bm.verts[15],bm.verts[7]),
            (bm.verts[0],bm.verts[8],bm.verts[9],bm.verts[1]),
            (bm.verts[1],bm.verts[9],bm.verts[10],bm.verts[2]),
            (bm.verts[2],bm.verts[10],bm.verts[11],bm.verts[3]),
            (bm.verts[3],bm.verts[11],bm.verts[12],bm.verts[4]),
            (bm.verts[4],bm.verts[12],bm.verts[13],bm.verts[5]),
            (bm.verts[5],bm.verts[13],bm.verts[14],bm.verts[6]),
            (bm.verts[6],bm.verts[14],bm.verts[15],bm.verts[7])
        ]
        for f in range(len(faces)):
            bm.faces.new(faces[f])  # add all faces from array

        # make the bmesh the object's mesh
        bm.to_mesh(mesh)
        bm.free()  # always do this when finished
        return mesh

    def generate_door(self, width: float, height: float, material: bpy.types.Material = None, strenght: float = 4,
                      handle: bpy.types.Mesh = None, keyhole: bpy.types.Mesh = None, frame: bpy.types.Mesh = None,
                      handle_side_right: bool = False, inside: bool = True, double_doors: bool = False, sliding_door: bool = False):
        print("Generate Door")
        width = width  /100
        height = height / 100
        strenght = strenght / 100
        cutout_frame = 2 / 100
        normal_door_mesh = self.generate_normal_door(width, height, strenght, cutout_frame)

def deleteAll():
    # delete old everything
    bpy.ops.object.select_all(action='SELECT')  # selektiert alle Objekte
    # löscht selektierte objekte
    bpy.ops.object.delete(use_global=False, confirm=False)
    bpy.ops.outliner.orphans_purge()  # löscht überbleibende Meshdaten etc.

# TODO deleteAll entfernen
deleteAll()

door = Door()
door.generate_door(120, 210) # Masse in cm
