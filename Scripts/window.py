import bpy
import bmesh
import random

from .materials import Materials
from . generic import Gen

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
    def __create_random_basis(windowheight, windowwidth,  windowdepth):

        windowmesh = bpy.data.meshes.new("WindowMesh")
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
    def __create_window_frame(windowheight,windowwidth,leafdepth,windowframewidth):
        framemesh = bpy.data.meshes.new("WindowFrameMesh")
        frameobject = bpy.data.objects.new("WindowFrame", framemesh)
        bpy.context.collection.objects.link(
            frameobject)  # put object in collection
        bm = bmesh.new()
        bm.from_mesh(framemesh)
        
        Windows.__create_vert(bm,-windowwidth - windowframewidth,windowwidth + windowframewidth,-leafdepth,windowheight,windowheight+ windowframewidth)
        Windows.__create_vert(bm,-windowwidth - windowframewidth,windowwidth + windowframewidth,-leafdepth,0,0- windowframewidth,)
        Windows.__create_vert(bm,-windowwidth - windowframewidth,-windowwidth ,-leafdepth,0- windowframewidth,windowheight+ windowframewidth)
        Windows.__create_vert(bm,windowwidth,windowwidth + windowframewidth,-leafdepth,0- windowframewidth,windowheight+ windowframewidth)
        
        bm.to_mesh(framemesh)
        bm.free()
        return frameobject

    @staticmethod
    def __vertical_window(windowheight,windowwidth):
        height= windowheight
        width = windowwidth/10
        return height,width

    @staticmethod
    def __horizontal_window(windowheight,windowwidth):
        height= windowheight/10
        width= windowwidth
        return height,width 

    @staticmethod
    def __create_windowleaf(windowheight,windowwidth,leafdepth,windowleaf):
        leafmesh = bpy.data.meshes.new("WindowFrameMesh")
        leafobject = bpy.data.objects.new("WindowFrame", leafmesh)
        bpy.context.collection.objects.link(
            leafobject)  # put object in collection
        bm = bmesh.new()
        bm.from_mesh(leafmesh)
         
        if(windowleaf==2):
            Windows.__create_two_leaf_window(bm, windowheight,windowwidth,leafdepth)

        elif(windowleaf==3):
            Windows.__create_three_leaf_window(bm, windowheight,windowwidth,leafdepth)
            
        else:
            Windows.__create_four_leaf_window(bm, windowheight,windowwidth,leafdepth)

        bm.to_mesh(leafmesh)
        bm.free()
        return leafobject

    @staticmethod
    def __create_two_leaf_window(bm,windowheight,windowwidth,leafdepth,):
        format2leaf= random.randint(1,2)

        if (format2leaf==1):
            # vertical
            leafheight,leafwidth=Windows.__vertical_window(windowheight,windowwidth)
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,0,leafheight)

        else:
            # horizontal
            leafheight,leafwidth=Windows.__horizontal_window(windowheight,windowwidth) 
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,(windowheight/2 + leafheight/2),(windowheight/2 - leafheight/2))
        
    @staticmethod
    def __create_three_leaf_window(bm,windowheight,windowwidth,leafdepth):
        format3leaf=random.randint(1,6)

        if(format3leaf==1):
            # two vertical leafs
            leafheight,leafwidth=Windows.__vertical_window(windowheight,windowwidth)
            Windows.__create_vert(bm,(windowwidth/3-leafwidth/2),(windowwidth/3+leafwidth/2),-leafdepth,0,leafheight)
            Windows.__create_vert(bm,(-windowwidth/3-leafwidth/2),(-windowwidth/3+leafwidth/2),-leafdepth,0,leafheight)

        elif(format3leaf==2):
            #  two horizontal leafs
            leafheight,leafwidth=Windows.__horizontal_window(windowheight,windowwidth) 
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,(windowheight/3 + leafheight/2),(windowheight/3 - leafheight/2))
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,(windowheight*(2/3) + leafheight/2),(windowheight*(2/3) - leafheight/2))

        elif(format3leaf==3):
            # horizontal & half vertical (top)
            # horizontal
            leafheight,leafwidth=Windows.__horizontal_window(windowheight,windowwidth)
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,(windowheight/2 + leafheight/2),(windowheight/2 - leafheight/2))
            # vertical half top part
            leaf2height,leaf2width=Windows.__vertical_window(windowheight,windowwidth)
            Windows.__create_vert(bm,-leaf2width,leaf2width,-leafdepth,(windowheight/2 + leafheight/2),leaf2height)

        elif(format3leaf==4):
            # horizontal & half vertical (bottom)
            # horizontal
            leafheight,leafwidth=Windows.__horizontal_window(windowheight,windowwidth) 
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,(windowheight/2 + leafheight/2),(windowheight/2 - leafheight/2))
            # vertical half bottom part
            leaf2height,leaf2width=Windows.__vertical_window(windowheight,windowwidth)
            Windows.__create_vert(bm,-leaf2width,leaf2width,-leafdepth,0,(leaf2height/2 - leafheight/2))

        elif(format3leaf==5):
            # vertical & horizontal left
            #vertical
            leafheight,leafwidth=Windows.__vertical_window(windowheight,windowwidth)
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,0,leafheight)
            #horizontal left 
            leaf2height,leaf2width=Windows.__horizontal_window(windowheight,windowwidth) 
            Windows.__create_vert(bm,-windowwidth,-leafwidth,-leafdepth,(windowheight/2 + leaf2height/2),(windowheight/2 - leaf2height/2))

        else:
            # vertical & horizontal right
            #vertical
            leafheight,leafwidth=Windows.__vertical_window(windowheight,windowwidth)
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,0,leafheight)
            #horizontal right
            leaf2height,leaf2width=Windows.__horizontal_window(windowheight,windowwidth) 
            Windows.__create_vert(bm,leafwidth,windowwidth,-leafdepth,(windowheight/2 + leaf2height/2),(windowheight/2 - leaf2height/2))
        
    @staticmethod
    def __create_four_leaf_window(bm,windowheight,windowwidth,leafdepth):
        format4leaf=random.randint(1,9)

        if(format4leaf==1):
            # three vertical leafs 
            leafheight,leafwidth=Windows.__vertical_window(windowheight,windowwidth)
            Windows.__create_vert(bm,(windowwidth/2-leafwidth),(windowwidth/2+leafwidth),-leafdepth,0,leafheight)
            Windows.__create_vert(bm,(-windowwidth/2-leafwidth),(-windowwidth/2+leafwidth),-leafdepth,0,leafheight)
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,0,leafheight)   

        elif(format4leaf==2):
            #  two horizontal leafs
            leafheight,leafwidth=Windows.__horizontal_window(windowheight,windowwidth) 
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,(windowheight/4 + leafheight/2),(windowheight/4 - leafheight/2))
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,(windowheight*(3/4) + leafheight/2),(windowheight*(3/4) - leafheight/2))
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,(windowheight/2 + leafheight/2),(windowheight/2 - leafheight/2))
            
        elif(format4leaf==3):
            # a cross
            # vertical leaf
            leafheight,leafwidth=Windows.__vertical_window(windowheight,windowwidth)
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,0,leafheight)
            #horizontal leaf
            leaf2height,leaf2width=Windows.__horizontal_window(windowheight,windowwidth) 
            Windows.__create_vert(bm,-leaf2width,leaf2width,-leafdepth,(windowheight/2 + leaf2height/2),(windowheight/2 - leaf2height/2))
        
        elif(format4leaf==4):
            # two vertical one horizontal on the left
            # two vertical
            leafheight,leafwidth=Windows.__vertical_window(windowheight,windowwidth)
            Windows.__create_vert(bm,(windowwidth/3-leafwidth/2),(windowwidth/3+leafwidth/2),-leafdepth,0,leafheight)
            Windows.__create_vert(bm,(-windowwidth/3-leafwidth/2),(-windowwidth/3+leafwidth/2),-leafdepth,0,leafheight)
            # horizontal left
            leaf3height,leaf3width=Windows.__horizontal_window(windowheight,windowwidth) 
            Windows.__create_vert(bm,-leaf3width,(-windowwidth*(1/3)-leafwidth/2),-leafdepth,(windowheight/2 + leaf3height/2),(windowheight/2 - leaf3height/2))
                
        elif(format4leaf==5):
            # two vertical one horizontal in the middle
            # two vertical leafs
            leafheight,leafwidth=Windows.__vertical_window(windowheight,windowwidth)
            Windows.__create_vert(bm,(windowwidth/3-leafwidth/2),(windowwidth/3+leafwidth/2),-leafdepth,0,leafheight)
            Windows.__create_vert(bm,(-windowwidth/3-leafwidth/2),(-windowwidth/3+leafwidth/2),-leafdepth,0,leafheight)#
            # horizontal middle
            leaf3height,leaf3width=Windows.__horizontal_window(windowheight,windowwidth) 
            Windows.__create_vert(bm,(-windowwidth*(1/3)+ leafwidth/2),(windowwidth/3-leafwidth/2),-leafdepth,(windowheight/2 + leaf3height/2),(windowheight/2 - leaf3height/2))
            
        elif(format4leaf==6):
            # two vertical one horizontal on the right
            # two vertical
            leafheight,leafwidth=Windows.__vertical_window(windowheight,windowwidth)
            Windows.__create_vert(bm,(windowwidth/3-leafwidth/2),(windowwidth/3+leafwidth/2),-leafdepth,0,leafheight)
            Windows.__create_vert(bm,(-windowwidth/3-leafwidth/2),(-windowwidth/3+leafwidth/2),-leafdepth,0,leafheight)
            # horizontal right
            leaf3height,leaf3width=Windows.__horizontal_window(windowheight,windowwidth) 
            Windows.__create_vert(bm,leaf3width,(windowwidth*(1/3)+ leafwidth/2),-leafdepth,(windowheight/2 + leaf3height/2),(windowheight/2 - leaf3height/2))
        
        elif(format4leaf==7):
            # two horizontal one vertical on the top
            # two horizontal
            leafheight,leafwidth=Windows.__horizontal_window(windowheight,windowwidth)  
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,(windowheight/3 + leafheight/2),(windowheight/3 - leafheight/2))
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,(windowheight*(2/3) + leafheight/2),(windowheight*(2/3) - leafheight/2))
            # vertical top
            leaf3height,leaf3width=Windows.__vertical_window(windowheight,windowwidth)
            Windows.__create_vert(bm,-leaf3width,leaf3width,-leafdepth,(windowheight*(2/3) + leafheight/2),leaf3height)
            
        elif(format4leaf==8):
            # two horizontal one vertical in the middle
            # two horizontal
            leafheight,leafwidth=Windows.__horizontal_window(windowheight,windowwidth) 
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,(windowheight/3 + leafheight/2),(windowheight/3 - leafheight/2))
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,(windowheight*(2/3) + leafheight/2),(windowheight*(2/3) - leafheight/2))
            # vertical top
            leaf3height,leaf3width=Windows.__vertical_window(windowheight,windowwidth)
            Windows.__create_vert(bm,-leaf3width,leaf3width,-leafdepth,(windowheight/3 + leafheight/2),(windowheight*(2/3) - leafheight/2))
            
        else:
            # two horizontal one vertical on the bottom
            # two horizontal
            leafheight,leafwidth=Windows.__horizontal_window(windowheight,windowwidth) 
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,(windowheight/3 + leafheight/2),(windowheight/3 - leafheight/2))
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,(windowheight*(2/3) + leafheight/2),(windowheight*(2/3) - leafheight/2))
            # vertical top
            leaf3height,leaf3width=Windows.__vertical_window(windowheight,windowwidth)
            Windows.__create_vert(bm,-leaf3width,leaf3width,-leafdepth,0,(windowheight/3 - leafheight/2))

    @staticmethod
    def __create_window_sill(windowwidth,leafdepth,windowframewidth):
        windowsillmesh = bpy.data.meshes.new("WindowSillMesh")
        windowsillobject = bpy.data.objects.new("WindowFrame", windowsillmesh)
        bpy.context.collection.objects.link(
            windowsillobject)  # put object in collection
        bm = bmesh.new()
        bm.from_mesh(windowsillmesh)
        windowsilllength = random.uniform(1,2)
        
        Windows.__create_vert(bm,-windowwidth - windowframewidth,windowwidth + windowframewidth, -windowsilllength,0- windowframewidth,0- windowframewidth-leafdepth )

        bm.to_mesh(windowsillmesh)
        bm.free()
        return windowsillobject

    @staticmethod
    def __create_window_accessoir(windowheight,windowwidth,windowframewidth,leafdepth,accessoir):   
        windowaccessoirmesh = bpy.data.meshes.new("WindowAccesoirMesh")
        windowaccessoirobject = bpy.data.objects.new("WindowFrame", windowaccessoirmesh)
        bpy.context.collection.objects.link(
            windowaccessoirobject)  # put object in collection
        bm = bmesh.new()
        bm.from_mesh(windowaccessoirmesh)
        if (accessoir==2):
            #Blackbox / Rolladenbox
            blackboxdepth = random.uniform(1,1.6)
            Windows.__create_vert(bm,-windowwidth - windowframewidth,windowwidth + windowframewidth,-blackboxdepth,windowheight,windowheight+blackboxdepth)
        else:
            # Windowshutter
            #  left
            Windows.__create_vert(bm,(-windowwidth*2),(-windowwidth-windowframewidth),(-leafdepth*3),0,windowheight)
            Windows.__create_vert(bm,(-windowwidth*2+windowwidth/4 ),(-windowwidth-windowframewidth-windowwidth/4),(-leafdepth*6),(windowheight - windowheight/10),(windowheight/2 + windowheight/12))
            Windows.__create_vert(bm,(-windowwidth*2+windowwidth/4 ),(-windowwidth-windowframewidth-windowwidth/4),(-leafdepth*6),(windowheight/10),(windowheight/2 - windowheight/12))
            Windows.__create_vert(bm,(-windowwidth*2),(-windowwidth*2+windowwidth/7),(-leafdepth*6),0,windowheight)
            Windows.__create_vert(bm,(-windowwidth-windowframewidth-windowwidth/7),(-windowwidth-windowframewidth),(-leafdepth*6),0,windowheight)
            Windows.__create_vert(bm,(-windowwidth*2),(-windowwidth-windowframewidth),(-leafdepth*6),(windowheight/2 + windowheight/20),(windowheight/2 - windowheight/20))
            Windows.__create_vert(bm,(-windowwidth*2),(-windowwidth-windowframewidth),(-leafdepth*6),(windowheight),(windowheight - windowheight/15))
            Windows.__create_vert(bm,(-windowwidth*2),(-windowwidth-windowframewidth),(-leafdepth*6),(windowheight/15),0)

            # right 
            Windows.__create_vert(bm,(windowwidth+ windowframewidth),(windowwidth*2),(-leafdepth*3),0,windowheight)
            Windows.__create_vert(bm,(windowwidth+ windowframewidth),(windowwidth+ windowframewidth+ windowwidth/7),(-leafdepth*6),0,windowheight)
            Windows.__create_vert(bm,(windowwidth*2- windowwidth/7),(windowwidth*2),(-leafdepth*6),0,windowheight)
            Windows.__create_vert(bm,(windowwidth+ windowframewidth),(windowwidth*2),(-leafdepth*6),(windowheight),(windowheight - windowheight/15))
            Windows.__create_vert(bm,(windowwidth+ windowframewidth),(windowwidth*2),(-leafdepth*6),(windowheight/15),0)
            Windows.__create_vert(bm,(windowwidth+ windowframewidth),(windowwidth*2),(-leafdepth*6),(windowheight/2 + windowheight/20),(windowheight/2 - windowheight/20))
            Windows.__create_vert(bm,(windowwidth+ windowframewidth+windowwidth/4 ),(windowwidth*2-windowwidth/4),(-leafdepth*6),(windowheight - windowheight/10),(windowheight/2 + windowheight/12))
            Windows.__create_vert(bm,(windowwidth+ windowframewidth+windowwidth/4 ),(windowwidth*2-windowwidth/4),(-leafdepth*6),(windowheight/10),(windowheight/2 - windowheight/12))
              
        bm.to_mesh(windowaccessoirmesh)
        bm.free()
        return windowaccessoirobject

    @staticmethod
    def create_window(windowheight, windowwidth, windowdepth, windowsillr, windowaccessoirr,windowleafr, material, sillmaterial):
        leafdepth = windowdepth/4
        windowframewidth = windowheight/20
        #create object
        basis: bpy.types.object = Windows.__create_random_basis(
            windowheight, windowwidth, windowdepth)
        windowframe: bpy.types.object = Windows.__create_window_frame(windowheight,windowwidth,leafdepth,windowframewidth)
        #material
        glass: bpy.types.Material = Materials.create_glass_material()
        # append materials
        basis.data.materials.append(glass)
        windowframe.data.materials.append(material)
        
        if (windowleafr!= 1):
            windowleaf: bpy.types.object = Windows.__create_windowleaf(windowheight,windowwidth,leafdepth,windowleafr)
            windowleaf.data.materials.append(material)
        if (windowsillr==1):
            windowsill: bpy.types.object =Windows.__create_window_sill(windowwidth,leafdepth,windowframewidth)
            windowsill.data.materials.append(sillmaterial)
        if (windowaccessoirr!=1):
            windowaccessoir: bpy.types.object =Windows.__create_window_accessoir(windowheight,windowwidth,windowframewidth,leafdepth,windowaccessoirr)
            windowaccessoir.data.materials.append(material)
        #parenting
        Gen.parenting([windowframe, windowleaf, windowsill, windowaccessoir], basis)
        return basis