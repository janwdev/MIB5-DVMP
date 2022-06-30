import bpy
import bmesh


class Roof:
    #Method for Roof generation and return
    #differentiate between Roof Type
    @staticmethod
    def generateRoof(type, length, width, height, objectName, meshName, overhang, overhangSize, material, base_height, wall_thickness):
        if type == "TriangleRoof":
            roof = Roof.createTriangleRoof(length, width, height, objectName, meshName, overhang, overhangSize, base_height, wall_thickness)
        if type == "FlatRoof":
            roof = Roof.createFlatRoof(length, width, height, objectName, meshName, overhang, overhangSize, base_height, wall_thickness)
        if type == "PointyTriangleRoof":
            roof = Roof.createPointyTriangleRoof(length, width, height, objectName, meshName, overhang, overhangSize, base_height, wall_thickness)
        #append given Material
        roof.data.materials.append(material)
        #return finished Roof
        return roof

    @staticmethod
    def createTriangleRoof(length, width, height, objectName, meshName, overhang, overhangSize, base_height, wall_thickness):

        #base height multipled with floor height
        base_height = base_height *2.2

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

        # define verts
        verts = [(width/2, length, height + base_height), (width, length, base_height), (width/2, 0, height + base_height), (width, 0, base_height), (width/2, length, height + base_height), (0, length, base_height), (width/2, 0, height + base_height), (0, 0, base_height)]

        # overhang_Size
        if overhang is True:
            # duplicate verts for overhang width, length, height
            overhang_verts = [(0 , 0 - overhangSize, base_height), (width , 0 - overhangSize, base_height), (width/2, 0 - overhangSize, height + base_height),
                              (0 , length + overhangSize, base_height), (width , length + overhangSize, base_height), (width/2, length + overhangSize, height + base_height)]
            for o in overhang_verts:
                verts.append(o)  # add all verts from array

            # duplicate verts for overhangThickness
            overhangThickness_verts = [(0 +(height/3), 0 - overhangSize, base_height), (width - (height/3), 0 - overhangSize, base_height), (width/2, 0 - overhangSize, height - (height/3) + base_height), (0 + (height/3), length + overhangSize, base_height), (width - (height/3), length + overhangSize, base_height), (width/2, length + overhangSize, height -
                                                                                                                                                                                                                                                                                       (height/3) + base_height), (width/2, length + overhangSize, height - (height/3) + base_height), (0 + (height/3), 0, base_height), (width - (height/3), 0, base_height), (width/2, 0, height - (height/3) + base_height), (0 + (height/3), length, base_height), (width - (height/3), length, base_height), (width/2, length, height - (height/3) + base_height)]
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
        return obj

    @staticmethod
    def createPointyTriangleRoof(length, width, height, objectName, meshName, overhang, overhangSize, base_height, wall_thickness):

        #base height multipled with floor height
        base_height = base_height *2.2

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

        # verts without overhang
        if overhang is False:
            verts = [(0 , 0, base_height), (width/2, length/2, height + base_height), (0 , length, base_height), (width/2, length/2, height + base_height),
                     (width , 0, base_height), (width/2, length/2, height + base_height), (width , length, base_height), (width/2, length/2, height + base_height)]

        # verts with active overhang
        if overhang is True:
            verts = [(-overhangSize , -overhangSize, base_height), (width/2, length/2, height + base_height), (-overhangSize , length + overhangSize, base_height), (width/2, length/2, height + base_height),
                     (overhangSize + width , -overhangSize, base_height), (width/2, length/2, height + base_height), (overhangSize + width , overhangSize + length, base_height), (width/2, length/2, height + base_height)]

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

        return obj

    @staticmethod
    def createFlatRoof(length, width, height, objectName, meshName, overhang, overhangSize, base_height, wall_thickness):

        #base height multipled with floor height
        base_height = base_height *2.2

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

        # verts without overhang
        if overhang is False:
            verts = [(0 , 0, base_height), (0 , length, base_height), (width , length, base_height), (width , 0, base_height), (0 , 0,
                                                                                    height + base_height), (0 , length, height + base_height), (width , length, height + base_height), (width , 0, height + base_height)]

        #verts with overhang
        if overhang is True:
            verts = [(-overhangSize , -overhangSize, base_height), (-overhangSize , length + overhangSize, base_height), (width + overhangSize , length + overhangSize, base_height), (width + overhangSize , -overhangSize, base_height),
                     (-overhangSize , -overhangSize, height + base_height), (-overhangSize , length + overhangSize, height + base_height), (width + overhangSize , length + overhangSize, height + base_height), (width + overhangSize , -overhangSize, height + base_height)]

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
        #return finished object
        return obj
