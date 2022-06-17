import bpy
import bmesh
import random

from .materials import Materials

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
    def __create_random_basis(windowheight, windowwidth, leafdepth, windowframewidth, windowdepth, windowsill, windowaccessoir):

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
    def __create_windowleaf(windowheight,windowwidth,leafdepth,windowframewidth):
         
        # windowleaf = 3
        windowleaf = random.randint(1,4)
        leaf = None
        if(windowleaf==2):
            leaf =Windows.__create_two_leaf_window(windowheight,windowwidth,leafdepth)

        elif(windowleaf==3):
            leaf= Windows.__create_three_leaf_window(windowheight,windowwidth,leafdepth)
            
        elif(windowleaf==4):
            leaf= Windows.__create_four_leaf_window(windowheight,windowwidth,leafdepth)
        return leaf
            
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
    def __create_two_leaf_window(windowheight,windowwidth,leafdepth,):
        leafmesh = bpy.data.meshes.new("WindowFrameMesh")
        leafobject = bpy.data.objects.new("WindowFrame", leafmesh)
        bpy.context.collection.objects.link(
            leafobject)  # put object in collection
        bm = bmesh.new()
        bm.from_mesh(leafmesh)
        
        format2leaf= random.randint(1,2)
        if (format2leaf==1):
            # vertical
            leafheight,leafwidth=Windows.__vertical_window(windowheight,windowwidth)
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,0,leafheight)

        else:
            # horizontal
            leafheight,leafwidth=Windows.__horizontal_window(windowheight,windowwidth) 
            Windows.__create_vert(bm,-leafwidth,leafwidth,-leafdepth,(windowheight/2 + leafheight/2),(windowheight/2 - leafheight/2))
        
        bm.to_mesh(leafmesh)
        bm.free()
        return leafobject

    @staticmethod
    def __create_three_leaf_window(windowheight,windowwidth,leafdepth):
        leafmesh = bpy.data.meshes.new("WindowFrameMesh")
        leafobject = bpy.data.objects.new("WindowFrame", leafmesh)
        bpy.context.collection.objects.link(
            leafobject)  # put object in collection
        bm = bmesh.new()
        bm.from_mesh(leafmesh)
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
        
        bm.to_mesh(leafmesh)
        bm.free()
        return leafobject

    @staticmethod
    def __create_four_leaf_window(windowheight,windowwidth,leafdepth):
        leafmesh = bpy.data.meshes.new("WindowFrameMesh")
        leafobject = bpy.data.objects.new("WindowFrame", leafmesh)
        bpy.context.collection.objects.link(
            leafobject)  # put object in collection
        bm = bmesh.new()
        bm.from_mesh(leafmesh)
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
        bm.to_mesh(leafmesh)
        bm.free()
        return leafobject

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
    def __create_window_accessoir(windowheight,windowwidth,windowframewidth,accessoir):   
        windowaccessoirmesh = bpy.data.meshes.new("WindowAccesoirMesh")
        windowaccessoirobject = bpy.data.objects.new("WindowFrame", windowaccessoirmesh)
        bpy.context.collection.objects.link(
            windowaccessoirobject)  # put object in collection
        bm = bmesh.new()
        bm.from_mesh(windowaccessoirmesh)
        if (accessoir==2):
            #Blackbox / Rolladenbox
            blackbox = random.randint(1,3)
            blackboxdepth = random.uniform(1,1.6)
            if(blackbox==1):
                #square
                Windows.__create_vert(bm,-windowwidth - windowframewidth,windowwidth + windowframewidth,-blackboxdepth,windowheight,windowheight+blackboxdepth)
            elif(blackbox==2):
                #square with one flat corner
                a=9
            else:
                #round
                d=2
            x=1
        else:
            #window shutter / Fensterladen
            x=1
        bm.to_mesh(windowaccessoirmesh)
        bm.free()
        return windowaccessoirobject

    @staticmethod
    def create_window(windowheight, windowwidth, leafdepth, windowframewidth, windowdepth, windowsill, windowaccessoir):
        windowsillr = random.randint(1,2)
        windowaccessoirr = random.uniform(1,3)

        basis: bpy.types.object = Windows.__create_random_basis(
            windowheight, windowwidth, leafdepth, windowframewidth, windowdepth, windowsill, windowaccessoir)
        glass: bpy.types.Material = Materials.create_glass_material()
        #obj: bpy.types.object = bpy.context.object
        basis.data.materials.append(glass)
        windowframe: bpy.types.object = Windows.__create_window_frame(windowheight,windowwidth,leafdepth,windowframewidth)
        wood:  bpy.types.Material = Materials.create_wood_material()
        windowframe.data.materials.append(wood)
        windowleaf: bpy.types.object = Windows.__create_windowleaf(windowheight,windowwidth,leafdepth,windowframewidth)
        if windowleaf != None:
            windowleaf.data.materials.append(wood)
        if (windowsillr==1):
            windowsill: bpy.types.object =Windows.__create_window_sill(windowwidth,leafdepth,windowframewidth)
            windowsill.data.materials.append(wood)
        if (windowaccessoirr!=1):
            windowaccessoir: bpy.types.object =Windows.__create_window_accessoir(windowheight,windowwidth,windowframewidth,windowaccessoirr)
            windowaccessoir.data.materials.append(wood)

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
