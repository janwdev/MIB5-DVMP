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

import bpy
import random

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

    #UI Slider Options TODO M oder CM???

    #Base Enum List Propertys (identifier, name, description)
    BASE_WIDTH: bpy.props.IntProperty(name="Base Width", default=10, min=3, max=100)
    BASE_LENGTH: bpy.props.IntProperty(name="Base Length", default=10, min=3, max=100)
    BASE_HEIGHT: bpy.props.IntProperty(name="Base Height", default=2, min=2, max=100)
    BASE_WALLTHICKNESS: bpy.props.FloatProperty(name="Base Wall Thickness", default=0.2, min=1, max=50)
    BASE_MATERIAL: bpy.props.EnumProperty(items = [('None','No Smooth','')],name="Base Material")
    # TODO Define Materials

    #Roof Enum List Propertys (identifier, name, description)
    # ROOF_WIDTH: bpy.props.IntProperty(name="Roof Width", default=10, min=3, max=100) //defined by base
    # ROOF_LENGTH: bpy.props.IntProperty(name="Roof Length", default=10, min=3, max=100) // defined by base
    ROOF_HEIGHT: bpy.props.IntProperty(name="Roof Height", default=2, min=2, max=100)
    ROOF_OVERHANG_SIZE: bpy.props.FloatProperty(name="Roof Overhang Size", default=0.2, min=0.01, max=10)
    ROOF_OVERHANG: bpy.props.BoolProperty(name="Roof Overhang", default=True) #OVERHNAG is also an length of overhang attribute. Insert here and in function call
    ROOF_TYPE: bpy.props.EnumProperty(items = [('TriangleRoof','Triangle Roof',''),('FlatRoof','Flat Roof',''),('PointyTriangleRoof','Pointy Triangle Roof','')],name="Roof Type")
    ROOF_MATERIAL: bpy.props.EnumProperty(items = [('None','No Smooth','')],name="Roof Material")
    # TODO Define Materials

    #Door Enum List Propertys (identifier, name, description)
    DOOR_WIDTH: bpy.props.IntProperty(name="Door Width", default=100, min=100, max=500)
    DOOR_HEIGHT: bpy.props.IntProperty(name="Door Height", default=100, min=100, max=500)
    DOOR_THICKNESS: bpy.props.FloatProperty(name="Door Thickness", default=0.03, min=0.03, max=50)
    DOOR_QUANTITY: bpy.props.IntProperty(name="Door Quantity", default=1, min=0, max=10)

    DOOR_FRAMEWIDTH: bpy.props.IntProperty(name="Door Frame Width", default=100, min=100, max=500)
    DOOR_FRAMEHEIGHT: bpy.props.IntProperty(name="Door Frame Height", default=100, min=100, max=500)

    DOOR_MATERIAL: bpy.props.EnumProperty(items = [('None','No Smooth','')],name="Door Material")
    # TODO Define Materials
    DOOR_KEYHOLEMATERIAL: bpy.props.EnumProperty(items = [('None','No Smooth','')],name="Keyhole Material")
    # TODO Define Materials
    DOOR_DOORKNOBMATERIAL: bpy.props.EnumProperty(items = [('None','No Smooth','')],name="Doorknob Material")
    # TODO Define Materials
    DOOR_FRAMEMATERIAL: bpy.props.EnumProperty(items = [('None','No Smooth','')],name="Door Frame Material")
    # TODO Define Materials

    #Rail Enum List Propertys (identifier, name, description)
    RAIL_LENGTH: bpy.props.IntProperty(name="Rail Length", default=10, min=1, max=50)
    RAIL_HEIGHT: bpy.props.IntProperty(name="Rail Height", default=2, min=1, max=50)
    RAIL_VERTICALSTRUTS: bpy.props.IntProperty(name="Rail Vertical Struts", default=5, min=1, max=200)
    RAIL_FILLSTRUTS: bpy.props.BoolProperty(name="Fill Vertical Struts", default=False)
    RAIL_QUANTITY: bpy.props.IntProperty(name="Rail Quantity", default=1, min=0, max=10)
    RAIL_MATERIAL: bpy.props.EnumProperty(items = [('None','No Smooth','')],name="Roof Material")
    # TODO Define Materials

    #Window Enum List Propertys (identifier, name, description) TODO Abhängigkeiten von Wandbreite
    WINDOW_LENGTH: bpy.props.IntProperty(name="Window Length", default=2, min=1, max=50)
    WINDOW_HEIGHT: bpy.props.IntProperty(name="Window Height", default=2, min=1, max=50)
    WINDOW_THICKNESS: bpy.props.FloatProperty(name="Window Thickness", default=0.05, min=0.02, max=1)
    WINDOW_BRACING: bpy.props.IntProperty(name="Window Bracing", default=2, min=0, max=3)
    WINDOW_ACCESSORY: bpy.props.IntProperty(name="Window Accessory (0 = none)", default=2, min=0, max=2)
    WINDOW_SILL: bpy.props.BoolProperty(name="Window Sill", default=True)
    WINDOW_QUANTITY: bpy.props.IntProperty(name="Window Quantity", default=1, min=0, max=10)
    WINDOW_MATERIAL: bpy.props.EnumProperty(items = [('None','No Smooth','')],name="Roof Material")
    # TODO Define Materials
    WINDOW_SILLMATERIAL: bpy.props.EnumProperty(items = [('None','No Smooth','')],name="Roof Material")
    # TODO Define Materials

    def execute(self, context):        # execute() is called when running the operator.
        bpy.data.scenes["Scene"].eevee.use_ssr = True
        print(self.ROOF_TYPE)
        #base = Basis.create_basis(self.BASE_WIDTH, self.BASE_HEIGHT, self.BASE_LENGTH, self.BASE_WALLTHICKNESS)
        #roof = Roof.generateRoof(self.ROOF_TYPE, self.BASE_LENGTH, self.BASE_WIDTH, self.ROOF_HEIGHT, "Roof", "RoofMesh", self.ROOF_OVERHANG, self.ROOF_OVERHANG_SIZE)

        window = Windows.create_window(self.WINDOW_HEIGHT, self.WINDOW_LENGTH, )

        # objects = bpy.data.objects
        # wall = False
        # scale_x = 0.09
        # scale_y = 0.09
        # length = 10
        # height = 0.9
        # amount = 7
        # Handrail.handrail(objects, wall, scale_x, scale_y, length, height, amount)

        # windowheight = random.randint(4, 10)
        # windowwidth = random.randint(2, 7)
        # windowdepth = random.uniform(0.2, 0.8)

        # windowsill = random.randint(1, 2)
        # windowaccessoir = random.randit(1, 3)
        # windowleaf = random.randint(1,4)

        # Windows.create_window(windowheight, windowwidth, windowdepth, windowsill, windowaccessoir,windowleaf)


        return {'FINISHED'}            # Lets Blender know the operator finished successfully.




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