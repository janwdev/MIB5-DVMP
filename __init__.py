# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import math
import bpy

from .Scripts.doors import Door
from .Scripts.handrail import Handrail
from .Scripts.roof import Roof
from .Scripts.generic import Gen
from .Scripts.window import Windows
from .Scripts.basis import Basis

bl_info = {
    "name" : "Building Generator",
    "description" : "Creates a Building with random attributes.",
    "author" : "Vinzenz Liebherr, Lara Franke, Yannick Reiche, Jannik Weisser",
    "version" : (1, 0, 0),
    "blender" : (3, 10, 0),
    "location": "View3D > Add > Mesh",
    "category" : "Add Mesh",
}

class BUILDINGGENERATOR(bpy.types.Operator):
    """My Object Moving Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "building.generatordvmp"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Generate Building"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    #UI Slider Options TODO
    #Base Enum List Propertys (identifier, name, description)
    EMPTY_HEADLINE: bpy.props.StringProperty(name="",description="", default="")
    BASE_HEADLINE: bpy.props.StringProperty(name="BASE SETTINGS",description="BASE SETTINGS", default="BASE SETTINGS")
    
    BASE_WIDTH: bpy.props.IntProperty(name="Width (M)", default=10, min=3, max=100)
    BASE_LENGTH: bpy.props.IntProperty(name="Length (M)", default=10, min=3, max=100)
    BASE_HEIGHT: bpy.props.IntProperty(name="Floors", default=1, min=1, max=100)
    BASE_WALLTHICKNESS: bpy.props.IntProperty(name="Wall Thickness (CM)", default=20, min=1, max=500)
    BASE_MATERIAL: bpy.props.EnumProperty(items = [('Plaster','Plaster',''), ('Wood','Wood',''), ('Glas','Glas',''), ('Brick','Brick',''), ('Metal','Metal',''), ('Metal 2','Metal2','')],name="Base Material")

    #Roof Enum List Propertys (identifier, name, description)
    EMPTY2_HEADLINE: bpy.props.StringProperty(name="",description="", default="")
    ROOF_HEADLINE: bpy.props.StringProperty(name="ROOF SETTINGS",description="ROOF SETTINGS", default="ROOF SETTINGS")
    
    ROOF_HEIGHT: bpy.props.IntProperty(name="Height (M)", default=2, min=2, max=100)
    ROOF_OVERHANG_SIZE: bpy.props.IntProperty(name="Overhang Size (CM)", default=1, min=1, max=200)
    ROOF_OVERHANG: bpy.props.BoolProperty(name="Overhang", default=True) #OVERHNAG is also an length of overhang attribute. Insert here and in function call
    ROOF_TYPE: bpy.props.EnumProperty(items = [('TriangleRoof','Triangle Roof',''),('FlatRoof','Flat Roof',''),('PointyTriangleRoof','Pointy Triangle Roof','')],name="Roof Type")
    ROOF_MATERIAL: bpy.props.EnumProperty(items = [('Brick','Brick',''), ('Plaster','Plaster',''), ('Glas','Glas',''), ('Wood','Wood',''), ('Metal','Metal',''), ('Metal 2','Metal2','')],name="Roof Material")

    #Door Enum List Propertys (identifier, name, description)
    EMPTY3_HEADLINE: bpy.props.StringProperty(name="",description="", default="")
    DOOR_HEADLINE: bpy.props.StringProperty(name="DOOR SETTINGS",description="DOOR SETTINGS", default="DOOR SETTINGS")
    
    DOOR_WIDTH: bpy.props.FloatProperty(name="Width (CM)", default=120.0, min=100.0, max=500.0)
    DOOR_HEIGHT: bpy.props.FloatProperty(name="Height (CM)", default=210.0, min=100.0, max=500.0)
    DOOR_THICKNESS: bpy.props.FloatProperty(name="Thickness (CM)", default=3.0, min=3.0, max=50)
    DOOR_QUANTITY: bpy.props.IntProperty(name="Quantity", default=1, min=0, max=4)
    DOOR_FRAMEWIDTH: bpy.props.FloatProperty(name="Frame Width (CM)", default=20.0, min=5.0, max=50.0)
    DOOR_FRAMEHEIGHT: bpy.props.FloatProperty(name="Frame Height (CM)", default=20.0, min=5.0, max=50.0)
    DOOR_MATERIAL: bpy.props.EnumProperty(items = [('Wood','Wood',''), ('Plaster','Plaster',''), ('Glas','Glas',''), ('Brick','Brick',''), ('Metal','Metal',''), ('Metal 2','Metal2','')],name="Door Material")
    DOOR_KEYHOLEMATERIAL: bpy.props.EnumProperty(items = [('Metal','Metal',''), ('Wood','Wood',''), ('Plaster','Plaster',''), ('Glas','Glas',''), ('Brick','Brick',''), ('Metal 2','Metal2','')],name="Keyhole Material")
    DOOR_DOORKNOBMATERIAL: bpy.props.EnumProperty(items = [('Metal','Metal',''), ('Wood','Wood',''), ('Plaster','Plaster',''), ('Glas','Glas',''), ('Brick','Brick',''), ('Metal 2','Metal2','')],name="Doorknob Material")
    DOOR_FRAMEMATERIAL: bpy.props.EnumProperty(items = [('Wood','Wood',''), ('Plaster','Plaster',''), ('Glas','Glas',''), ('Brick','Brick',''), ('Metal','Metal',''), ('Metal 2','Metal2','')],name="Door Frame Material")

    #Rail Enum List Propertys (identifier, name, description)
    #RAIL_LENGTH: bpy.props.IntProperty(name="Rail Length", default=10, min=1, max=50)
    #RAIL_HEIGHT: bpy.props.IntProperty(name="Rail Height", default=2, min=1, max=50)
    #RAIL_VERTICALSTRUTS: bpy.props.IntProperty(name="Rail Vertical Struts", default=5, min=1, max=200)
    EMPTY4_HEADLINE: bpy.props.StringProperty(name="",description="", default="")
    RAIL_HEADLINE: bpy.props.StringProperty(name="RAIL SETTINGS",description="RAIL SETTINGS", default="RAIL SETTINGS")
   
    RAIL_FILLSTRUTS: bpy.props.BoolProperty(name="Fill Vertical Struts", default=False)
    #RAIL_QUANTITY: bpy.props.IntProperty(name="Rail Quantity", default=1, min=0, max=10)
    RAIL_MATERIAL: bpy.props.EnumProperty(items = [('Metal','Metal',''), ('Plaster','Plaster',''), ('Glas','Glas',''), ('Brick','Brick',''), ('Wood','Wood',''), ('Metal 2','Metal2','')],name="Rail Material")

    #Window Enum List Propertys (identifier, name, description)
    EMPTY5_HEADLINE: bpy.props.StringProperty(name="",description="", default="")
    WINDOW_HEADLINE: bpy.props.StringProperty(name="WINDOW SETTINGS",description="WINDOW SETTINGS", default="WINDOW SETTINGS")
    
    WINDOW_LENGTH: bpy.props.IntProperty(name="Length (CM)", default=120, min=10, max=500)
    WINDOW_HEIGHT: bpy.props.IntProperty(name="Height (CM)", default=120, min=10, max=500)
    #WINDOW_THICKNESS: bpy.props.FloatProperty(name="Window Thickness", default=0.05, min=0.02, max=1) Abhängig von Wand Breite
    WINDOW_BRACING: bpy.props.IntProperty(name="Bracing", default=2, min=1, max=4)
    WINDOW_ACCESSORY: bpy.props.IntProperty(name="Accessory (1 = none)", default=2, min=1, max=3)
    WINDOW_SILL: bpy.props.BoolProperty(name="Sill", default=True)
    WINDOW_QUANTITY_WALL_F: bpy.props.IntProperty(name="Quant Front", default=1, min=0, max=100)
    WINDOW_QUANTITY_WALL_R: bpy.props.IntProperty(name="Quant Right", default=1, min=0, max=100)
    WINDOW_QUANTITY_WALL_L: bpy.props.IntProperty(name="Quant Left", default=1, min=0, max=100)
    WINDOW_QUANTITY_WALL_B: bpy.props.IntProperty(name="Quant Back", default=1, min=0, max=100)
    WINDOW_MATERIAL: bpy.props.EnumProperty(items = [('Wood','Wood',''), ('Plaster','Plaster',''), ('Glas','Glas',''), ('Brick','Brick',''), ('Metal','Metal',''), ('Metal 2','Metal2','')],name="Window Material")
    WINDOW_SILLMATERIAL: bpy.props.EnumProperty(items = [('Wood','Wood',''), ('Plaster','Plaster',''), ('Glas','Glas',''), ('Brick','Brick',''), ('Metal','Metal',''), ('Metal 2','Metal2','')],name="Window Sill Material")

    def execute(self, context):        # execute() is called when running the operator.
        bpy.data.scenes["Scene"].eevee.use_ssr = True
 
        base = Basis.create_basis(self.BASE_WIDTH, self.BASE_HEIGHT, self.BASE_LENGTH, Gen.cm_to_m(self.BASE_WALLTHICKNESS), Gen.getMaterialFromEnm(self.BASE_MATERIAL))
        roof = Roof.generateRoof(self.ROOF_TYPE, self.BASE_LENGTH, self.BASE_WIDTH, self.ROOF_HEIGHT, "Roof", "RoofMesh", self.ROOF_OVERHANG, self.ROOF_OVERHANG_SIZE, Gen.getMaterialFromEnm(self.ROOF_MATERIAL), self.BASE_HEIGHT, Gen.cm_to_m(self.BASE_WALLTHICKNESS))
        
        self.moveObjects(base)
        self.moveWindow((0,0,0),0,self.WINDOW_QUANTITY_WALL_F,self.BASE_WIDTH,self.WINDOW_LENGTH,self.DOOR_WIDTH+self.DOOR_FRAMEWIDTH*2)
        self.moveWindow((self.BASE_WIDTH,0,0),90,self.WINDOW_QUANTITY_WALL_R,self.BASE_WIDTH,self.WINDOW_LENGTH)
        self.moveWindow((0,self.BASE_LENGTH,0),180,self.WINDOW_QUANTITY_WALL_B,self.BASE_WIDTH,self.WINDOW_LENGTH)
        self.moveWindow((0,0,0),270,self.WINDOW_QUANTITY_WALL_L,self.BASE_WIDTH,self.WINDOW_LENGTH)
        

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.


    def moveObjects(self, base):

        positions = []
        positions.append((0,0,0))
        positions.append((10,10,0))

        rotations = []
        rotations.append((0,0,0))
        rotations.append((0,0,180))
        doorRot = 180
        windowRot = 0

        for i in range(self.DOOR_QUANTITY):
            
            door = Door.generate_door(Gen.cm_to_m(self.DOOR_WIDTH), Gen.cm_to_m(self.DOOR_HEIGHT), Gen.getMaterialFromEnm(self.DOOR_MATERIAL), Gen.cm_to_m(self.DOOR_THICKNESS), Gen.cm_to_m(self.DOOR_FRAMEWIDTH), Gen.cm_to_m(self.BASE_WALLTHICKNESS), Gen.cm_to_m(self.DOOR_FRAMEHEIGHT), Gen.getMaterialFromEnm(self.DOOR_FRAMEMATERIAL), Gen.getMaterialFromEnm(self.DOOR_KEYHOLEMATERIAL), Gen.getMaterialFromEnm(self.DOOR_DOORKNOBMATERIAL))
            # boolean = base.modifiers.new(name=("base_bool_door_"+str(i)), type="BOOLEAN")
            # boolean.object = door
            # boolean.operation = "DIFFERENCE"
            door.location = positions[i]
            door.rotation_euler[2] =math.radians(doorRot)
            doorRot += 90


            # if self.DOOR_QUANTITY == 1:
            #    door.location = self.BASE_WIDTH/2 +0
            
            # elif self.DOOR_QUANTITY == 2:
            #     self.BASE_WIDTH/2 +0
            #     self.BASE_WIDTH + self.BASE_LENGTH/2
            
            # elif self.DOOR_QUANTITY == 3:
            #     self.BASE_WIDTH/2 +0
            #     self.BASE_WIDTH + self.BASE_LENGTH/2
            #     self.BASE_WIDTH/2 + self.BASE_LENGTH
            
            # elif self.DOOR_QUANTITY == 4:
            #     self.BASE_WIDTH/2 +0
            #     self.BASE_WIDTH + self.BASE_LENGTH/2
            #     self.BASE_WIDTH/2 + self.BASE_LENGTH
            #     0 + self.BASE_LENGTH/2

    
    
    def moveWindow(self, offset, rotation, window_quant, base_width, window_width, door_width=0):

        window_width = Gen.cm_to_m(window_width)
        door_width = Gen.cm_to_m(door_width)

        size_one_window = (base_width - door_width)/window_quant
        
        if (window_width + Gen.cm_to_m(self.WINDOW_HEIGHT/20)*2 ) * window_quant > base_width - (door_width):
            print("Error, return from moveWindow")
            return -1

        windows = []
        print("moveWindow")

        for i in range (window_quant):
            window = Windows.create_window(Gen.cm_to_m(self.WINDOW_HEIGHT), Gen.cm_to_m(self.WINDOW_LENGTH), Gen.cm_to_m(self.BASE_WALLTHICKNESS), self.WINDOW_SILL, self.WINDOW_ACCESSORY, self.WINDOW_BRACING, Gen.getMaterialFromEnm(self.WINDOW_MATERIAL),Gen.getMaterialFromEnm(self.WINDOW_SILLMATERIAL))
            windows.append(window)
            print("GenerateWindow: " + str(i))

        offset_width = offset[0]
        offset_length = offset[1]
        offset_height = offset[2]

        centerpoint = size_one_window/2
        if(door_width>0):
            for i in range(1, window_quant+1):
                print(centerpoint)
                

                if (rotation/90)%2 == 0:
                    pos = (centerpoint + offset_width, 0 + offset_length, Gen.cm_to_m(110-self.WINDOW_HEIGHT/2)+offset_height)
                else:
                    pos = (0+offset_width, centerpoint, Gen.cm_to_m(110-self.WINDOW_HEIGHT/2)+offset_height)

                windows[i-1].rotation_euler[2] =math.radians(rotation)
                windows[i-1].location = pos
                
                if i+1 == math.ceil((window_quant+1)/2):
                    centerpoint=centerpoint+size_one_window/2 + door_width + size_one_window/2
                else:
                    centerpoint += size_one_window
                
        else:
            for i in range(window_quant):
                if (rotation/90)%2 == 0:
                    pos = (centerpoint + offset_width, 0 + offset_length, Gen.cm_to_m(110-self.WINDOW_HEIGHT/2)+offset_height)
                else:
                    pos = (0+offset_width, centerpoint, Gen.cm_to_m(110-self.WINDOW_HEIGHT/2)+offset_height)
                

                windows[i].rotation_euler[2] =math.radians(rotation)
                windows[i].location = pos

                centerpoint += size_one_window
        


def menu_func(self, context):
    self.layout.operator(BUILDINGGENERATOR.bl_idname)

def register():
    from .Scripts.doors import Door
    from .Scripts.handrail import Handrail
    from .Scripts.roof import Roof
    from .Scripts.generic import Gen
    from .Scripts.window import Windows
    from .Scripts.basis import Basis
    print("starting")
    bpy.utils.register_class(BUILDINGGENERATOR)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.
    print("Building-Generator started")

def unregister():
    bpy.utils.unregister_class(BUILDINGGENERATOR)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()