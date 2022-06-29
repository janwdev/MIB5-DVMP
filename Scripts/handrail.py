import bpy

from . materials import Materials

class Handrail:

    #for development on mac
    # def create_metal_material():
    #     metal_material = bpy.data.materials.new("Metal")
    #     metal_material.use_nodes = True
    #     metal_material.node_tree.nodes["Principled BSDF"].inputs[9].default_value = 0.15
    #     metal_material.node_tree.nodes["Principled BSDF"].inputs[6].default_value = 1
    #     return metal_material

    @staticmethod
    def handrail(length, height, amount, wall, stab_material, scale_x=0.02, scale_y=0.1):
        material_between = Materials.create_glass_material()
        ##########  MESH ##########

        mesh_length = scale_x*(amount-(amount-2))
        space_length = length-mesh_length
        space_between = space_length/(amount-1)

        height = height/2
        # geländer_stäbe senkrecht
        stab_name = "Geländer_Stab"
        existing = bpy.context.scene.objects.get(stab_name)
        i = 0
        while(existing):
            stab_name = "Geländer_Stab_" + str(i)
            existing = bpy.context.scene.objects.get(stab_name)
            i += 1

        bpy.ops.mesh.primitive_cube_add(location=(scale_x,0,height), scale=(scale_x, scale_y, height))
        bpy.context.active_object.name = stab_name
        bpy.ops.object.modifier_add(type='ARRAY')
        stab = bpy.context.scene.objects[stab_name]
        stab.modifiers['Array'].count = amount
        stab.modifiers['Array'].use_relative_offset = False
        stab.modifiers['Array'].use_constant_offset = True
        stab.modifiers['Array'].constant_offset_displace[0] = space_between

        bevel = False
        if(bevel):
            
            bpy.ops.object.modifier_add(type='BEVEL')
            stab_oben.modifiers['Bevel'].width = 0.02
            stab_oben.modifiers['Bevel'].segments = 3

       
        stab.data.materials.append(stab_material)

        # geländer_stab_oben
        stab_oben_name = "Geländer_Stab_Oben"
        existing = bpy.context.scene.objects.get(stab_oben_name)
        i = 0
        while(existing):
            stab_oben_name = "Geländer_Stab_Oben_" + str(i)
            existing = bpy.context.scene.objects.get(stab_oben_name)
            i += 1
        bpy.ops.mesh.primitive_cube_add(location=(
            length/2, 0, (height*2) + scale_x), scale=(length/2, scale_y, scale_x))
        bpy.context.active_object.name = stab_oben_name
        stab_oben = bpy.context.scene.objects[stab_oben_name]
        if(bevel):
            bpy.ops.object.modifier_add(type='BEVEL')
            stab_oben.modifiers['Bevel'].width = 0.02
            stab_oben.modifiers['Bevel'].segments = 3

        bpy.ops.object.select_all(action='DESELECT')  # deselect all object

        stab.select_set(True)
        stab_oben.select_set(True)  # select the object for the 'parenting'

        # the active object will be the parent of all selected object
        bpy.context.view_layer.objects.active = stab_oben

        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

        stab_oben.data.materials.append(stab_material)

        if(wall):
            wall_padding = 0.05
            wall_thickness = 0.05
            wall_length_raw = space_length/(amount-1)/2-scale_x
            wall_length = wall_length_raw-wall_padding
            wall_height = height-wall_padding
            offset = scale_x*2+wall_length_raw
            for i in range(1, amount):

                bpy.ops.mesh.primitive_cube_add(location=(offset, 0, height), scale=(
                    wall_length, wall_thickness, wall_height))

                offset += wall_length_raw*2 + scale_x*2

                wallMesh = bpy.context.active_object
                wallMesh.data.materials.append(material_between)
                wallMesh.active_material = material_between
                wallMesh.active_material.use_screen_refraction = True
        return stab_oben
   