import bpy
import bmesh


class Roof:
    @staticmethod
    def createTriangleRoof(length, width, height, objectName, meshName, overhang, overhangThickness):

        mesh = bpy.data.meshes.new(meshName)  # add a new mesh

        # add a new object using the mesh
        obj = bpy.data.objects.new(objectName, mesh)

        scene = bpy.context.scene
        # put the object into the scene (link)
        scene.collection.objects.link(obj)
        # set as the active object in the scene
        bpy.context.view_layer.objects.active = obj
        obj.select_set(state=True)  # select object

        mesh = bpy.context.object.data
        bm = bmesh.new()

        # verts
        verts = [(width/2, length, height), (width, length, 0), (width/2, 0, height), (width,
                                                                                       0, 0), (width/2, length, height), (0, length, 0), (width/2, 0, height), (0, 0, 0)]

        # overhang
        if overhang is True:
            # duplicate verts for overhang width, length, height
            overhang_verts = [(0, 0 - overhang, 0), (width, 0 - overhang, 0), (width/2, 0 - overhang, height),
                              (0, length + overhang, 0), (width, length + overhang, 0), (width/2, length + overhang, height)]
            for o in overhang_verts:
                verts.append(o)  # add all verts from array

            # duplicate verts for overhangThickness
            overhangThickness_verts = [(0 + overhangThickness, 0 - overhang, 0), (width - overhangThickness, 0 - overhang, 0), (width/2, 0 - overhang, height - overhangThickness), (0 + overhangThickness, length + overhang, 0), (width - overhangThickness, length + overhang, 0), (width/2, length + overhang, height -
                                                                                                                                                                                                                                                                                       overhangThickness), (width/2, length + overhang, height - overhangThickness), (0 + overhangThickness, 0, 0), (width - overhangThickness, 0, 0), (width/2, 0, height - overhangThickness), (0 + overhangThickness, length, 0), (width - overhangThickness, length, 0), (width/2, length, height - overhangThickness)]
            for o in overhangThickness_verts:
                verts.append(o)  # add all verts from array

        for v in verts:
            bm.verts.new(v)  # add all verts from array

        bm.verts.ensure_lookup_table()  # add [index] functionality

        # faces
        faces = [(bm.verts[2], bm.verts[3], bm.verts[6], bm.verts[7]), (bm.verts[1], bm.verts[5], bm.verts[0], bm.verts[4]), (bm.verts[1], bm.verts[3], bm.verts[2], bm.verts[0]),
                 (bm.verts[5], bm.verts[4], bm.verts[6], bm.verts[7]), (bm.verts[0], bm.verts[4], bm.verts[2], bm.verts[6]), (bm.verts[1], bm.verts[3], bm.verts[7], bm.verts[5])]

        # overhang
        if overhang is True:
            # faces for overhang
            overhang_faces = [(bm.verts[8], bm.verts[7], bm.verts[6], bm.verts[10]), (bm.verts[3], bm.verts[9], bm.verts[10], bm.verts[2]), (bm.verts[9], bm.verts[15], bm.verts[16], bm.verts[10]), (bm.verts[14], bm.verts[8], bm.verts[10], bm.verts[16]), (bm.verts[15], bm.verts[16], bm.verts[23], bm.verts[22]), (bm.verts[14], bm.verts[21], bm.verts[23], bm.verts[16]), (bm.verts[21], bm.verts[7], bm.verts[8], bm.verts[14]), (bm.verts[22], bm.verts[3], bm.verts[9], bm.verts[15]), (
                bm.verts[12], bm.verts[1], bm.verts[0], bm.verts[13]), (bm.verts[11], bm.verts[5], bm.verts[4], bm.verts[13]), (bm.verts[12], bm.verts[18], bm.verts[20], bm.verts[13]), (bm.verts[13], bm.verts[20], bm.verts[17], bm.verts[11]), (bm.verts[20], bm.verts[26], bm.verts[24], bm.verts[17]), (bm.verts[20], bm.verts[26], bm.verts[25], bm.verts[18]), (bm.verts[18], bm.verts[12], bm.verts[1], bm.verts[25]), (bm.verts[24], bm.verts[5], bm.verts[11], bm.verts[17])]
            for o in overhang_faces:
                faces.append(o)  # add all verts from array

        for f in range(len(faces)):
            bm.faces.new(faces[f])  # add all faces from array

        # make the bmesh the object's mesh
        bm.to_mesh(mesh)
        bm.free()  # always do this when finished

    @staticmethod
    def createPointyTriangleRoof(length, width, height, objectName, meshName, overhang, overhangSize):

        mesh = bpy.data.meshes.new(meshName)  # add a new mesh

        # add a new object using the mesh
        obj = bpy.data.objects.new(objectName, mesh)

        scene = bpy.context.scene
        # put the object into the scene (link)
        scene.collection.objects.link(obj)
        # set as the active object in the scene
        bpy.context.view_layer.objects.active = obj
        obj.select_set(state=True)  # select object

        mesh = bpy.context.object.data
        bm = bmesh.new()

        # verts
        if overhang is False:
            verts = [(0, 0, 0), (width/2, length/2, height), (0, length, 0), (width/2, length/2, height),
                     (width, 0, 0), (width/2, length/2, height), (width, length, 0), (width/2, length/2, height)]

        if overhang is True:
            verts = [(-overhangSize, -overhangSize, 0), (width/2, length/2, height), (-overhangSize, length + overhangSize, 0), (width/2, length/2, height),
                     (overhangSize + width, -overhangSize, 0), (width/2, length/2, height), (overhangSize + width, overhangSize + length, 0), (width/2, length/2, height)]

        for v in verts:
            bm.verts.new(v)  # add all verts from array

        bm.verts.ensure_lookup_table()  # add [index] functionality

        # # faces
        faces = [(bm.verts[0], bm.verts[2], bm.verts[6], bm.verts[4]), (bm.verts[0], bm.verts[1], bm.verts[3], bm.verts[2]), (bm.verts[0], bm.verts[1], bm.verts[5], bm.verts[4]),
                 (bm.verts[4], bm.verts[5], bm.verts[7], bm.verts[6]), (bm.verts[6], bm.verts[7], bm.verts[3], bm.verts[2]), (bm.verts[1], bm.verts[3], bm.verts[7], bm.verts[5])]

        for f in range(len(faces)):
            bm.faces.new(faces[f])  # add all faces from array

        # make the bmesh the object's mesh
        bm.to_mesh(mesh)
        bm.free()  # always do this when finished

    @staticmethod
    def createFlatRoof(length, width, height, objectName, meshName, overhang, overhangsize):

        mesh = bpy.data.meshes.new(meshName)  # add a new mesh

        # add a new object using the mesh
        obj = bpy.data.objects.new(objectName, mesh)

        scene = bpy.context.scene
        # put the object into the scene (link)
        scene.collection.objects.link(obj)
        # set as the active object in the scene
        bpy.context.view_layer.objects.active = obj
        obj.select_set(state=True)  # select object

        mesh = bpy.context.object.data
        bm = bmesh.new()

        # verts
        if overhang is False:
            verts = [(0, 0, 0), (0, length, 0), (width, length, 0), (width, 0, 0), (0, 0,
                                                                                    height), (0, length, height), (width, length, height), (width, 0, height)]

        if overhang is True:
            verts = [(-overhangsize, -overhangsize, 0), (-overhangsize, length + overhangsize, 0), (width + overhangsize, length + overhangsize, 0), (width + overhangsize, -overhangsize, 0),
                     (-overhangsize, -overhangsize, height), (-overhangsize, length + overhangsize, height), (width + overhangsize, length + overhangsize, height), (width + overhangsize, -overhangsize, height)]

        for v in verts:
            bm.verts.new(v)  # add all verts from array

        bm.verts.ensure_lookup_table()  # add [index] functionality

        # # faces
        faces = [(bm.verts[0], bm.verts[4], bm.verts[7], bm.verts[3]), (bm.verts[0], bm.verts[4], bm.verts[5], bm.verts[1]), (bm.verts[1], bm.verts[5], bm.verts[6], bm.verts[2]),
                 (bm.verts[3], bm.verts[7], bm.verts[6], bm.verts[2]), (bm.verts[4], bm.verts[5], bm.verts[6], bm.verts[7]), (bm.verts[0], bm.verts[1], bm.verts[2], bm.verts[3])]

        for f in range(len(faces)):
            bm.faces.new(faces[f])  # add all faces from array

        # make the bmesh the object's mesh
        bm.to_mesh(mesh)
        bm.free()  # always do this when finished
