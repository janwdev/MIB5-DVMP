import bpy
import mathutils
import typing

objects = bpy.data.objects



scale_x = 0.09
scale_y = 0.09
length = 10
height = 0.9
amount = 7
wall = False
#592F25 dark wood
#BF895A light wood


bpy.data.scenes["Scene"].eevee.use_ssr = True

## clear all materials
#for material in bpy.data.materials:
    #material.user_clear()
    #bpy.data.materials.remove(material)

## clear all objects
for object in bpy.context.scene.objects:
    object.select_set(True)
bpy.ops.object.delete()





def handrail(scale_x, scale_y, length, height, amount):
    
    ##########  MATERIALS ##########
    
    # glass_material
    glass_material = bpy.data.materials.new("Glass")
    glass_material.use_nodes = True
    nodes: typing.List[bpy.types.Nodes] = glass_material.node_tree.nodes
    node_glass: bpy.types.Node = nodes.new("ShaderNodeBsdfGlass")
    glass_material.node_tree.nodes.remove(glass_material.node_tree.nodes.get('Principled BSDF'))
    material_output = glass_material.node_tree.nodes.get('Material Output')
   
    glass_material.node_tree.links.new(material_output.inputs[0], node_glass.outputs[0])
    
    
    
    
    # metal_material
    metal_material = bpy.data.materials.new("Metal")
    metal_material.use_nodes = True
    nodes: typing.List[bpy.types.Nodes] = metal_material.node_tree.nodes
    bsdf = glass_material.node_tree.nodes.get('Principled BSDF')
    bpy.data.materials["Metal"].node_tree.nodes["Principled BSDF"].inputs[9].default_value = 0.47
    bpy.data.materials["Metal"].node_tree.nodes["Principled BSDF"].inputs[6].default_value = 1

    material_output = metal_material.node_tree.nodes.get('Material Output')
  
    


    # wood_material
    wood_material = bpy.data.materials.new("Wood")
    wood_material.use_nodes = True
    nodes: typing.List[bpy.types.Nodes] = wood_material.node_tree.nodes
    bsdf = wood_material.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs[7].default_value = 0.2

    # texture_coordinate
    tex_coord: bpy.types.Node = nodes.new(type="ShaderNodeTexCoord")
    
    # mapping
    mapping: bpy.types.Node = nodes.new(type="ShaderNodeMapping")
    
    # noise
    nodes.new(type="ShaderNodeValToRGB")
    noise_texture: bpy.types.Node = nodes.new(type="ShaderNodeTexNoise")
    noise_texture.inputs[1].default_value = 3
    noise_texture.inputs[2].default_value = 3.8
    noise_texture.inputs[3].default_value = 0.545833
    noise_texture.inputs[4].default_value = 1.6
   
    # color ramp
    color_ramp_color = wood_material.node_tree.nodes.get('ColorRamp')
   
    color_ramp_color.color_ramp.elements[0].color = (0.520995,0.250,0.102,1.0)
    color_ramp_color.color_ramp.elements[1].color = (0.100,0.028,0.0185,1)
    
    # brightness/contrast
    brightness_contrast: bpy.types.Node = nodes.new(type="ShaderNodeBrightContrast")
    brightness_contrast.inputs[2].default_value = 1

    # color ramp bump
    color_ramp_bump: bpy.types.Node = nodes.new(type="ShaderNodeValToRGB")
    color_ramp_bump.color_ramp.elements[1].position = 0.025
    
    bump: bpy.types.Node = nodes.new(type="ShaderNodeBump")
    bump.inputs[1].default_value = 0.01
    
    
    ### linking nodes ###
    
    #textcoord to mapping
    wood_material.node_tree.links.new(mapping.inputs[0], tex_coord.outputs[0])
    #mapping to noise
    wood_material.node_tree.links.new(noise_texture.inputs[0], mapping.outputs[0])
    #noise to ramp
    wood_material.node_tree.links.new(color_ramp_color.inputs[0], noise_texture.outputs[1])
    #ramp to bsdf
    wood_material.node_tree.links.new(bsdf.inputs[0], color_ramp_color.outputs[0])
    #ramp to bright/contr
    wood_material.node_tree.links.new(brightness_contrast.inputs[0], color_ramp_color.outputs[0])
    #bright/contr to bump_ramp
    wood_material.node_tree.links.new(color_ramp_bump.inputs[0], brightness_contrast.outputs[0])
    #bump_ramp to bump
    wood_material.node_tree.links.new(bump.inputs[2], color_ramp_bump.outputs[0])
    #bump to bsdf
    wood_material.node_tree.links.new(bsdf.inputs[22], bump.outputs[0])

    
    ##########  MESH ##########

    stab_material = wood_material

    mesh_length = scale_x*(amount-(amount-2))
    space_length = length-mesh_length
    space_between = space_length/(amount-1)
   

    ## geländer_stäbe senkrecht
    
    bpy.ops.mesh.primitive_cube_add(location=(scale_x,0,height), scale=(scale_x, scale_y, height))
    bpy.context.active_object.name = 'Geländer_Stab'
    bpy.ops.object.modifier_add(type='ARRAY')
    stab = objects['Geländer_Stab']
    stab.modifiers['Array'].count = amount
    stab.modifiers['Array'].use_relative_offset = False
    stab.modifiers['Array'].use_constant_offset = True
    stab.modifiers['Array'].constant_offset_displace[0] = space_between
    
    bpy.ops.object.modifier_add(type='BEVEL')
    stab.modifiers['Bevel'].width = 0.04
    stab.modifiers['Bevel'].segments = 12
    stab.data.materials.append(stab_material)


    ## geländer_stab_oben
    
    bpy.ops.mesh.primitive_cube_add(location=(length/2,0,(height*2) + scale_x), scale=(length/2, scale_y, scale_x))
    bpy.context.active_object.name = 'Geländer_Stab_Oben'
    stab_oben = objects['Geländer_Stab_Oben']


    bpy.ops.object.modifier_add(type='BEVEL')
    stab_oben.modifiers['Bevel'].width = 0.02
    stab_oben.modifiers['Bevel'].segments = 3
    
    bpy.ops.object.select_all(action='DESELECT') #deselect all object

    stab.select_set(True)
    stab_oben.select_set(True)     #select the object for the 'parenting'

    bpy.context.view_layer.objects.active = stab_oben    #the active object will be the parent of all selected object

    bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
    
    
    
    stab_oben.data.materials.append(stab_material)
      
    if(wall):
        wall_padding = 0.05
        wall_thickness = 0.05
        wall_length_raw = space_length/(amount-1)/2-scale_x
        wall_length = wall_length_raw-wall_padding
        wall_height = height-wall_padding
        offset = scale_x*2+wall_length_raw;
        for i in range(1, amount):
            
            bpy.ops.mesh.primitive_cube_add(location=(offset,0,height), scale=(wall_length, wall_thickness, wall_height))
           
           
            offset += wall_length_raw*2 + scale_x*2
            
            wallMesh = bpy.context.active_object
            wallMesh.data.materials.append(glass_material)
            wallMesh.active_material = glass_material
            wallMesh.active_material.use_screen_refraction = True
    
        
handrail(scale_x, scale_y, length, height, amount)