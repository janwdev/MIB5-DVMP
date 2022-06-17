import bpy
import bmesh
import random
import typing


class Windows:
    @staticmethod
    def __create_vert(bm, width, width2, depth, height, height2):

        vert1 = bm.verts.new((width, 0, height))
        vert2 = bm.verts.new((width2, 0, height))
        vert3 = bm.verts.new((width, 0, height2))
        vert4 = bm.verts.new((width2, 0, height2))

        vert1_2 = bm.verts.new((width, depth, height))
        vert2_2 = bm.verts.new((width2, depth, height))
        vert3_2 = bm.verts.new((width, depth, height2))
        vert4_2 = bm.verts.new((width2, depth, height2))

        bm.faces.new((vert1, vert2, vert4, vert3))
        bm.faces.new((vert1_2, vert2_2, vert4_2, vert3_2))
        bm.faces.new((vert1_2, vert1, vert3, vert3_2))
        bm.faces.new((vert2, vert2_2, vert4_2, vert4))
        bm.faces.new((vert4_2, vert4, vert3, vert3_2))
        bm.faces.new((vert1_2, vert1, vert2, vert2_2))

    @staticmethod
    def __create_glass_material():
        glass_material = bpy.data.materials.new("Glass")
        glass_material.use_nodes = True
        nodes: typing.List[bpy.types.Nodes] = glass_material.node_tree.nodes
        node_glass: bpy.types.Node = nodes.new("ShaderNodeBsdfGlass")
        glass_material.node_tree.nodes.remove(
            glass_material.node_tree.nodes.get('Principled BSDF'))
        material_output = glass_material.node_tree.nodes.get('Material Output')
        glass_material.node_tree.links.new(
            material_output.inputs[0], node_glass.outputs[0])
        return glass_material

    @staticmethod
    def __create_random_basis(windowheight, windowwidth, leafdepth, windowframewidth, windowdepth, windowsill, windowaccessoir):

        windowmesh = bpy.data.meshes.new("WindowFrameMesh")
        windowobject = bpy.data.objects.new("WindowFrame", windowmesh)
        bpy.context.collection.objects.link(
            windowobject)  # put object in collection
        bm = bmesh.new()
        bm.from_mesh(windowmesh)

        Windows.__create_vert(bm, -windowwidth, windowwidth,
                            windowdepth, 0, windowheight)

        bm.to_mesh(windowmesh)
        bm.free()
        return windowobject

    @staticmethod
    def create_window(windowheight, windowwidth, leafdepth, windowframewidth, windowdepth, windowsill, windowaccessoir):
        basis: bpy.types.object = Windows.__create_random_basis(
            windowheight, windowwidth, leafdepth, windowframewidth, windowdepth, windowsill, windowaccessoir)
        glass: bpy.types.Material = Windows.__create_glass_material()
        #obj: bpy.types.object = bpy.context.object
        basis.data.materials.append(glass)


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


windowheight = random.randint(4, 10)
windowwidth = random.randint(2, 7)
leafdepth = random.uniform(0.05, 0.1)
windowframewidth = random.uniform(0.05, 0.2)
windowdepth = random.uniform(0.2, 0.8)

windowsill = random.randint(1, 2)
windowaccessoir = random.uniform(1, 3)

deleteAll()

bpy.data.scenes["Scene"].eevee.use_ssr = True

Windows.create_window(windowheight, windowwidth, leafdepth,
                      windowframewidth, windowdepth, windowsill, windowaccessoir)
