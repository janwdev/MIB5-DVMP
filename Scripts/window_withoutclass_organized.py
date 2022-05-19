from venv import create
import bpy
import bmesh 
import random

global windowheight 
global windowwidth 
global leafdepth 
global windowframewidth 

windowheight = random.randint(4,10)
windowwidth = random.randint(2,7)
leafdepth = random.uniform(0.05,0.1)
windowframewidth = random.uniform(0.05,0.2)

def create_vert(width,width2,depth,height,height2):

    vert1=bm.verts.new((width,0,height))
    vert2=bm.verts.new((width2,0,height))
    vert3=bm.verts.new((width,0,height2))
    vert4=bm.verts.new((width2,0,height2))

    vert1_2=bm.verts.new((width,depth,height))
    vert2_2=bm.verts.new((width2,depth,height))
    vert3_2=bm.verts.new((width,depth,height2))
    vert4_2=bm.verts.new((width2,depth,height2))

    bm.faces.new((vert1,vert2,vert4,vert3))
    bm.faces.new((vert1_2,vert2_2,vert4_2,vert3_2))
    bm.faces.new((vert1_2,vert1,vert3,vert3_2))
    bm.faces.new((vert2,vert2_2,vert4_2,vert4))
    bm.faces.new((vert4_2,vert4,vert3,vert3_2))
    bm.faces.new((vert1_2,vert1,vert2,vert2_2))

def create_random_basis():
    windowdepth = random.uniform(0.2,0.8)
    create_vert(-windowwidth,windowwidth,windowdepth,0,windowheight)
    create_window_frame()
    windowsill = random.randint(1,2)
    if (windowsill==1):
        create_window_sill()
    
def create_window_frame():
    create_vert(-windowwidth - windowframewidth,windowwidth + windowframewidth,-leafdepth,windowheight,windowheight+ windowframewidth)
    create_vert(-windowwidth - windowframewidth,windowwidth + windowframewidth,-leafdepth,0,0- windowframewidth,)
    create_vert(-windowwidth - windowframewidth,-windowwidth ,-leafdepth,0- windowframewidth,windowheight+ windowframewidth)
    create_vert(windowwidth,windowwidth + windowframewidth,-leafdepth,0- windowframewidth,windowheight+ windowframewidth)

def create_window_sill():
    windowsilllength = random.uniform(1,2)
    create_vert(-windowwidth - windowframewidth,windowwidth + windowframewidth, -windowsilllength,0- windowframewidth,0- windowframewidth-leafdepth )

def vertical_window():
    height= windowheight
    width = windowwidth/10
    return height,width

def horizontal_window():
    height= windowheight/10
    width= windowwidth
    return height,width 

def create_two_leaf_window():
    format2leaf= random.randint(1,2)
    if (format2leaf==1):
        # vertical
        leafheight,leafwidth=vertical_window()
        create_vert(-leafwidth,leafwidth,-leafdepth,0,leafheight)

    else:
        # horizontal
        leafheight,leafwidth=horizontal_window() 
        create_vert(-leafwidth,leafwidth,-leafdepth,(windowheight/2 + leafheight/2),(windowheight/2 - leafheight/2))

def create_three_leaf_window():
    format3leaf=random.randint(1,6)
    if(format3leaf==1):
        # two vertical leafs
        leafheight,leafwidth=vertical_window()
        create_vert((windowwidth/3-leafwidth/2),(windowwidth/3+leafwidth/2),-leafdepth,0,leafheight)
        create_vert((-windowwidth/3-leafwidth/2),(-windowwidth/3+leafwidth/2),-leafdepth,0,leafheight)

    elif(format3leaf==2):
        #  two horizontal leafs
        leafheight,leafwidth=horizontal_window() 
        create_vert(-leafwidth,leafwidth,-leafdepth,(windowheight/3 + leafheight/2),(windowheight/3 - leafheight/2))
        create_vert(-leafwidth,leafwidth,-leafdepth,(windowheight*(2/3) + leafheight/2),(windowheight*(2/3) - leafheight/2))

    elif(format3leaf==3):
        # horizontal & half vertical (top)
        # horizontal
        leafheight,leafwidth=horizontal_window()
        create_vert(-leafwidth,leafwidth,-leafdepth,(windowheight/2 + leafheight/2),(windowheight/2 - leafheight/2))
        # vertical half top part
        leaf2height,leaf2width=vertical_window()
        create_vert(-leaf2width,leaf2width,-leafdepth,(windowheight/2 + leafheight/2),leaf2height)

    elif(format3leaf==4):
        # horizontal & half vertical (bottom)
        # horizontal
        leafheight,leafwidth=horizontal_window() 
        create_vert(-leafwidth,leafwidth,-leafdepth,(windowheight/2 + leafheight/2),(windowheight/2 - leafheight/2))
        # vertical half bottom part
        leaf2height,leaf2width=vertical_window()
        create_vert(-leaf2width,leaf2width,-leafdepth,0,(leaf2height/2 - leafheight/2))

    elif(format3leaf==5):
        # vertical & horizontal left
        #vertical
        leafheight,leafwidth=vertical_window()
        create_vert(-leafwidth,leafwidth,-leafdepth,0,leafheight)
        #horizontal left 
        leaf2height,leaf2width=horizontal_window() 
        create_vert(-windowwidth,-leafwidth,-leafdepth,(windowheight/2 + leaf2height/2),(windowheight/2 - leaf2height/2))

    else:
        # vertical & horizontal right
        #vertical
        leafheight,leafwidth=vertical_window()
        create_vert(-leafwidth,leafwidth,-leafdepth,0,leafheight)
        #horizontal right
        leaf2height,leaf2width=horizontal_window() 
        create_vert(leafwidth,windowwidth,-leafdepth,(windowheight/2 + leaf2height/2),(windowheight/2 - leaf2height/2))

def create_four_leaf_window():
    format4leaf=random.randint(1,9)
    if(format4leaf==1):
        # three vertical leafs 
        leafheight,leafwidth=vertical_window()
        create_vert((windowwidth/2-leafwidth),(windowwidth/2+leafwidth),-leafdepth,0,leafheight)
        create_vert((-windowwidth/2-leafwidth),(-windowwidth/2+leafwidth),-leafdepth,0,leafheight)
        create_vert(-leafwidth,leafwidth,-leafdepth,0,leafheight)   

    elif(format4leaf==2):
        #  two horizontal leafs
        leafheight,leafwidth=horizontal_window() 
        create_vert(-leafwidth,leafwidth,-leafdepth,(windowheight/4 + leafheight/2),(windowheight/4 - leafheight/2))
        create_vert(-leafwidth,leafwidth,-leafdepth,(windowheight*(3/4) + leafheight/2),(windowheight*(3/4) - leafheight/2))
        create_vert(-leafwidth,leafwidth,-leafdepth,(windowheight/2 + leafheight/2),(windowheight/2 - leafheight/2))
        
    elif(format4leaf==3):
        # a cross
        # vertical leaf
        leafheight,leafwidth=vertical_window()
        create_vert(-leafwidth,leafwidth,-leafdepth,0,leafheight)
        #horizontal leaf
        leaf2height,leaf2width=horizontal_window() 
        create_vert(-leaf2width,leaf2width,-leafdepth,(windowheight/2 + leaf2height/2),(windowheight/2 - leaf2height/2))
     
    elif(format4leaf==4):
        # two vertical one horizontal on the left
        # two vertical
        leafheight,leafwidth=vertical_window()
        create_vert((windowwidth/3-leafwidth/2),(windowwidth/3+leafwidth/2),-leafdepth,0,leafheight)
        create_vert((-windowwidth/3-leafwidth/2),(-windowwidth/3+leafwidth/2),-leafdepth,0,leafheight)
        # horizontal left
        leaf3height,leaf3width=horizontal_window() 
        create_vert(-leaf3width,(-windowwidth*(1/3)-leafwidth/2),-leafdepth,(windowheight/2 + leaf3height/2),(windowheight/2 - leaf3height/2))
            
    elif(format4leaf==5):
        # two vertical one horizontal in the middle
        # two vertical leafs
        leafheight,leafwidth=vertical_window()
        create_vert((windowwidth/3-leafwidth/2),(windowwidth/3+leafwidth/2),-leafdepth,0,leafheight)
        create_vert((-windowwidth/3-leafwidth/2),(-windowwidth/3+leafwidth/2),-leafdepth,0,leafheight)#
        # horizontal middle
        leaf3height,leaf3width=horizontal_window() 
        create_vert((-windowwidth*(1/3)+ leafwidth/2),(windowwidth/3-leafwidth/2),-leafdepth,(windowheight/2 + leaf3height/2),(windowheight/2 - leaf3height/2))
         
    elif(format4leaf==6):
        # two vertical one horizontal on the right
        # two vertical
        leafheight,leafwidth=vertical_window()
        create_vert((windowwidth/3-leafwidth/2),(windowwidth/3+leafwidth/2),-leafdepth,0,leafheight)
        create_vert((-windowwidth/3-leafwidth/2),(-windowwidth/3+leafwidth/2),-leafdepth,0,leafheight)
        # horizontal right
        leaf3height,leaf3width=horizontal_window() 
        create_vert(leaf3width,(windowwidth*(1/3)+ leafwidth/2),-leafdepth,(windowheight/2 + leaf3height/2),(windowheight/2 - leaf3height/2))
    
    elif(format4leaf==7):
        # two horizontal one vertical on the top
        # two horizontal
        leafheight,leafwidth=horizontal_window()  
        create_vert(-leafwidth,leafwidth,-leafdepth,(windowheight/3 + leafheight/2),(windowheight/3 - leafheight/2))
        create_vert(-leafwidth,leafwidth,-leafdepth,(windowheight*(2/3) + leafheight/2),(windowheight*(2/3) - leafheight/2))
        # vertical top
        leaf3height,leaf3width=vertical_window()
        create_vert(-leaf3width,leaf3width,-leafdepth,(windowheight*(2/3) + leafheight/2),leaf3height)
        
    elif(format4leaf==8):
        # two horizontal one vertical in the middle
        # two horizontal
        leafheight,leafwidth=horizontal_window() 
        create_vert(-leafwidth,leafwidth,-leafdepth,(windowheight/3 + leafheight/2),(windowheight/3 - leafheight/2))
        create_vert(-leafwidth,leafwidth,-leafdepth,(windowheight*(2/3) + leafheight/2),(windowheight*(2/3) - leafheight/2))
        # vertical top
        leaf3height,leaf3width=vertical_window()
        create_vert(-leaf3width,leaf3width,-leafdepth,(windowheight/3 + leafheight/2),(windowheight*(2/3) - leafheight/2))
        
    else:
        # two horizontal one vertical on the bottom
        # two horizontal
        leafheight,leafwidth=horizontal_window() 
        create_vert(-leafwidth,leafwidth,-leafdepth,(windowheight/3 + leafheight/2),(windowheight/3 - leafheight/2))
        create_vert(-leafwidth,leafwidth,-leafdepth,(windowheight*(2/3) + leafheight/2),(windowheight*(2/3) - leafheight/2))
        # vertical top
        leaf3height,leaf3width=vertical_window()
        create_vert(-leaf3width,leaf3width,-leafdepth,0,(windowheight/3 - leafheight/2))
  
# creates main object and mesh
windowmesh = bpy.data.meshes.new("WindowFrameMesh")
windowobject = bpy.data.objects.new("WindowFrame", windowmesh)
bpy.context.collection.objects.link(windowobject)# put object in collection  

bm = bmesh.new()
bm.from_mesh(windowmesh)
create_random_basis()

windowleaf = random.randint(1,4)
if(windowleaf==2):
    create_two_leaf_window()

elif(windowleaf==3):
    create_three_leaf_window()
    
elif(windowleaf==4):
    create_four_leaf_window()
          
bm.to_mesh(windowmesh)
bm.free()

        

        


        
