import bpy
import bmesh

def deleteAll():
    # delete old everything
    bpy.ops.object.select_all(action='SELECT')  # selektiert alle Objekte
    # löscht selektierte objekte
    bpy.ops.object.delete(use_global=False, confirm=False)
    bpy.ops.outliner.orphans_purge()  # löscht überbleibende Meshdaten etc.

def createTriangleRoof(length, width, height, objectName, meshName):

    mesh = bpy.data.meshes.new(meshName)  # add a new mesh

    # add a new object using the mesh
    obj = bpy.data.objects.new(objectName, mesh)

    scene = bpy.context.scene
    scene.collection.objects.link(obj)  # put the object into the scene (link)
    # set as the active object in the scene
    bpy.context.view_layer.objects.active = obj
    obj.select_set(state=True)  # select object

    mesh = bpy.context.object.data
    bm = bmesh.new()

    # verts
    verts = [(width/2, length, height), (width, length, 0), (width/2, 0, height), (width, 0, 0), (width/2, length, height), (0, length, 0), (width/2, 0, height), (0, 0, 0)]

    for v in verts:
        bm.verts.new(v)  # add all verts from array

    bm.verts.ensure_lookup_table() # add [index] functionality

    # # edges
    # edges = [(bm.verts[1], bm.verts[5]), (bm.verts[5], bm.verts[7]), (bm.verts[7], bm.verts[3]), (bm.verts[3], bm.verts[1]), (bm.verts[1], bm.verts[0]), (bm.verts[5], bm.verts[4]), (bm.verts[7], bm.verts[6]), (bm.verts[3], bm.verts[2]), (bm.verts[0], bm.verts[2]), (bm.verts[4], bm.verts[6]), (bm.verts[2], bm.verts[6]), (bm.verts[0], bm.verts[4])]

    # for e in range(len(edges)):
    #     bm.edges.new(edges[e])  # add all edges from array

    # faces
    faces = [(bm.verts[2], bm.verts[3], bm.verts[6], bm.verts[7]), (bm.verts[1], bm.verts[5], bm.verts[0], bm.verts[4]), (bm.verts[1], bm.verts[3], bm.verts[2], bm.verts[0]), (bm.verts[5], bm.verts[4], bm.verts[6], bm.verts[7]), (bm.verts[0], bm.verts[4], bm.verts[2], bm.verts[6]), (bm.verts[1], bm.verts[3], bm.verts[7], bm.verts[5])]

    for f in range(len(faces)):
        bm.faces.new(faces[f])  # add all faces from array

    # make the bmesh the object's mesh
    bm.to_mesh(mesh)
    bm.free()  # always do this when finished

def createPointyTriangleRoof(length, width, height, objectName, meshName):

    mesh = bpy.data.meshes.new(meshName)  # add a new mesh

    # add a new object using the mesh
    obj = bpy.data.objects.new(objectName, mesh)

    scene = bpy.context.scene
    scene.collection.objects.link(obj)  # put the object into the scene (link)
    # set as the active object in the scene
    bpy.context.view_layer.objects.active = obj
    obj.select_set(state=True)  # select object

    mesh = bpy.context.object.data
    bm = bmesh.new()

    # verts
    verts = [(0, 0, 0), (width/2, length/2, height), (0, length, 0),(width/2, length/2, height), (width, 0, 0), (width/2, length/2, height), (width, length, 0), (width/2, length/2, height)]

    for v in verts:
        bm.verts.new(v)  # add all verts from array

    bm.verts.ensure_lookup_table() # add [index] functionality

    # # edges
    edges = [(bm.verts[0], bm.verts[2]), (bm.verts[2], bm.verts[6]), (bm.verts[6], bm.verts[4]), (bm.verts[4], bm.verts[0]), (bm.verts[0], bm.verts[1]), (bm.verts[2], bm.verts[3]), (bm.verts[6], bm.verts[7]), (bm.verts[4], bm.verts[5]), (bm.verts[1], bm.verts[3]), (bm.verts[1], bm.verts[5]), (bm.verts[7], bm.verts[3]), (bm.verts[7], bm.verts[5])]

    for e in range(len(edges)):
        bm.edges.new(edges[e])  # add all edges from array

    # # faces
    faces = [(bm.verts[0], bm.verts[2], bm.verts[6], bm.verts[4]), (bm.verts[0], bm.verts[1], bm.verts[3], bm.verts[2]), (bm.verts[0], bm.verts[1], bm.verts[5], bm.verts[4]), (bm.verts[4], bm.verts[5], bm.verts[7], bm.verts[6]), (bm.verts[6], bm.verts[7], bm.verts[3], bm.verts[2]), (bm.verts[1], bm.verts[3], bm.verts[7], bm.verts[5])]

    for f in range(len(faces)):
        bm.faces.new(faces[f])  # add all faces from array

    # make the bmesh the object's mesh
    bm.to_mesh(mesh)
    bm.free()  # always do this when finished

deleteAll()
createTriangleRoof(5, 5, 2, "Roof", "Roof")  # length, width, height
