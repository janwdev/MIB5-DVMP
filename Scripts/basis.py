import bpy
import bmesh
import random

from . materials import Materials

class Basis:
    
    @staticmethod
    def __create_vert(bm, width, width2, depth,depth2, height, height2):

        vert1 = bm.verts.new((width, depth, height))
        vert2 = bm.verts.new((width2, depth, height))
        vert3 = bm.verts.new((width, depth, height2))
        vert4 = bm.verts.new((width2, depth, height2))

        vert1_2 = bm.verts.new((width, depth2, height))
        vert2_2 = bm.verts.new((width2, depth2, height))
        vert3_2 = bm.verts.new((width, depth2, height2))
        vert4_2 = bm.verts.new((width2, depth2, height2))

        bm.faces.new((vert1, vert2, vert4, vert3))
        bm.faces.new((vert1_2, vert2_2, vert4_2, vert3_2))
        bm.faces.new((vert1_2, vert1, vert3, vert3_2))
        bm.faces.new((vert2, vert2_2, vert4_2, vert4))
        bm.faces.new((vert4_2, vert4, vert3, vert3_2))
        bm.faces.new((vert1_2, vert1, vert2, vert2_2))

    @staticmethod
    def create_square(width, height,length,wallthickness):
        basismesh = bpy.data.meshes.new("BasisMesh")
        basisobject = bpy.data.objects.new("Basis", basismesh)
        bpy.context.collection.objects.link(basisobject)  # put object in collection

        bm = bmesh.new()
        bm.from_mesh(basismesh)

        # left side
        Basis.__create_vert(bm,(0-wallthickness),0,0,length,0,height)
        #right side
        Basis.__create_vert(bm,width,(width+wallthickness),0,length,0,height)
        # front side
        Basis.__create_vert(bm,0,width,0,wallthickness,0,height)
        # backside
        Basis.__create_vert(bm,0,width,(length-wallthickness),length ,0,height)

        bm.to_mesh(basismesh)
        bm.free()

        return basisobject

    @staticmethod
    def create_basis(width, height,length, wallthickness, material):
        height = height*2.2

        basis: bpy.types.object = Basis.create_square(width, height,length,wallthickness)
        basis.data.materials.append(material)
        return basis
