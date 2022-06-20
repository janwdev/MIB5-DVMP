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

    def execute(self, context):        # execute() is called when running the operator.
        bpy.data.scenes["Scene"].eevee.use_ssr = True
        door = Door.generate_door()  # Masse in cm
        # Roof.createFlatRoof(5, 5, 2, "Roof", "Roof", True, 2)  # length, width, height
        
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
        # leafdepth = random.uniform(0.05, 0.1)
        # windowframewidth = random.uniform(0.05, 0.2)
        # windowdepth = random.uniform(0.2, 0.8)

        # windowsill = random.randint(1, 2)
        # windowaccessoir = random.randit(1, 3)
        #windowleaf = random.randint(1,4)

        # Windows.create_window(windowheight, windowwidth, leafdepth,
        #                     windowframewidth, windowdepth, windowsill, windowaccessoir,windowleaf)


        return {'FINISHED'}            # Lets Blender know the operator finished successfully.




def menu_func(self, context):
    self.layout.operator(BUILDINGGENERATOR.bl_idname)

def register():
    from .Scripts.doors import Door
    from .Scripts.handrail import Handrail
    from .Scripts.roof import Roof
    from .Scripts.generic import Gen
    from .Scripts.window import Windows
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