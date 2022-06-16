import bpy
import typing


class Materials():

    bsdf_normal_input = 22

    @staticmethod
    def create_wood_material():
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

        color_ramp_color.color_ramp.elements[0].color = (
            0.520995, 0.250, 0.102, 1.0)
        color_ramp_color.color_ramp.elements[1].color = (
            0.100, 0.028, 0.0185, 1)

        # brightness/contrast
        brightness_contrast: bpy.types.Node = nodes.new(
            type="ShaderNodeBrightContrast")
        brightness_contrast.inputs[2].default_value = 1

        # color ramp bump
        color_ramp_bump: bpy.types.Node = nodes.new(type="ShaderNodeValToRGB")
        color_ramp_bump.color_ramp.elements[1].position = 0.025

        bump: bpy.types.Node = nodes.new(type="ShaderNodeBump")
        bump.inputs[1].default_value = 0.01

        ### linking nodes ###

        # textcoord to mapping
        wood_material.node_tree.links.new(
            mapping.inputs[0], tex_coord.outputs[3])
        # mapping to noise
        wood_material.node_tree.links.new(
            noise_texture.inputs[0], mapping.outputs[0])
        # noise to ramp
        wood_material.node_tree.links.new(
            color_ramp_color.inputs[0], noise_texture.outputs[1])
        # ramp to bsdf
        wood_material.node_tree.links.new(
            bsdf.inputs[0], color_ramp_color.outputs[0])
        # ramp to bright/contr
        wood_material.node_tree.links.new(
            brightness_contrast.inputs[0], color_ramp_color.outputs[0])
        # bright/contr to bump_ramp
        wood_material.node_tree.links.new(
            color_ramp_bump.inputs[0], brightness_contrast.outputs[0])
        # bump_ramp to bump
        wood_material.node_tree.links.new(
            bump.inputs[2], color_ramp_bump.outputs[0])
        # bump to bsdf
        wood_material.node_tree.links.new(bsdf.inputs[22], bump.outputs[0])
        return wood_material

    @staticmethod
    def create_glass_material():
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
    def metal(condition = 1):
        # conditions :
        # 1 = mint
        # 2 = used
        # 3 = rusted
        
        
        material = bpy.data.materials.new("Metal")
        material.use_nodes = True
        bsdf = Materials.get_node(material, "Principled BSDF")

        bsdf.inputs[9].default_value = 0.15
        bsdf.inputs[6].default_value = 1
        bsdf.inputs[7].default_value = 0

        tex_coords = Materials.add_tex_coords_node(material)
        mapping = Materials.add_mapping_node(material)
        noise = Materials.add_noise_node(material)
        pre_noise = Materials.add_noise_node(material)
        mix_rgb = Materials.add_node(material, "ShaderNodeMixRGB")
        mix_rgb_2 = Materials.add_node(material, "ShaderNodeMixRGB")
        mix_rgb_3 = Materials.add_node(material, "ShaderNodeMixRGB") # roughness color
        musgrave = Materials.add_node(material, "ShaderNodeTexMusgrave")
        ramp = Materials.add_ramp_node(material)
        ramp_2 = Materials.add_ramp_node(material)
        math = Materials.add_node(material, "ShaderNodeMath")
        wave = Materials.add_node(material, "ShaderNodeTexWave")
        bump = Materials.add_bump_node(material)

        mapping.inputs[3].default_value[0] = 80
        mapping.inputs[3].default_value[1] = 0.1

        noise.inputs[2].default_value = 6
        noise.inputs[3].default_value = 16
        noise.inputs[4].default_value = 0.6
        noise.inputs[5].default_value = 0.1

        pre_noise.inputs[2].default_value = 8

        mix_rgb.inputs[0].default_value = 0.2
      
        c = 0.08
        c_2 = 0.2
        ramp = Materials.adjust_ramp_pos(ramp, 0, 0.236)
        ramp = Materials.adjust_ramp_color(ramp, 0,(c, c, c, 1))
        ramp = Materials.adjust_ramp_pos(ramp, 1, 0.830)
        ramp = Materials.adjust_ramp_color(ramp, 1, (c_2, c_2, c_2, 1))


        # roughness 
        musgrave.inputs[2].default_value = 0.1
        musgrave.inputs[3].default_value = 16
        musgrave.inputs[4].default_value = 0.1
        musgrave.inputs[5].default_value = 2

        c = 0.044
        c_2 = 0.142
        ramp_2 = Materials.adjust_ramp_color(ramp_2, 0, (c, c, c, 1))
        ramp_2 = Materials.adjust_ramp_color(ramp_2, 1, (c_2, c_2, c_2, 1))

        math.operation = "MULTIPLY"
        math.inputs[1].default_value = 2.9


        # scratches

        scratch_noise = Materials.add_noise_node(material)
        noise_mix_rgb = Materials.add_mix_rgb_node(material)
        scratch_ramp = Materials.add_ramp_node(material)
        math_subtract = Materials.add_math_node(material)
        scratch_noise_ramp = Materials.add_ramp_node(material)
        scratch_noise_2 = Materials.add_noise_node(material)

        wave.inputs[1].default_value = 1
        wave.inputs[2].default_value = 25
        wave.inputs[3].default_value = 0
        wave.inputs[4].default_value = 5
        wave.inputs[5].default_value = 0.75



        scratch_noise.inputs[2].default_value = 6
        scratch_noise.inputs[3].default_value = 16
        scratch_noise.inputs[4].default_value = 0.6
        scratch_noise.inputs[5].default_value = 0.1

        Materials.link_nodes(material, tex_coords, 0, noise_mix_rgb, 1)
        Materials.link_nodes(material, scratch_noise, 0, noise_mix_rgb, 2)
        Materials.link_nodes(material, noise_mix_rgb, 0, wave, 0)

        scratch_ramp = Materials.adjust_ramp_pos(scratch_ramp, 0, 0.955)
        scratch_ramp = Materials.adjust_ramp_color(scratch_ramp, 0, (1, 1, 1, 1))
        scratch_ramp = Materials.adjust_ramp_pos(scratch_ramp, 1, 1)
        scratch_ramp = Materials.adjust_ramp_color(scratch_ramp, 1, (0, 0, 0, 1))
        
        Materials.link_nodes(material, wave, 0, scratch_ramp, 0)

        scratch_noise_ramp.color_ramp.interpolation = "CONSTANT"
        scratch_noise_ramp = Materials.adjust_ramp_pos(scratch_noise_ramp, 0, 0.480)
        scratch_noise_ramp = Materials.adjust_ramp_pos(scratch_noise_ramp, 1, 0.520)
        
        Materials.link_nodes(material, scratch_noise_2, 0, scratch_noise_ramp, 0)
        Materials.link_nodes(material, scratch_noise_ramp, 0, math_subtract, 0)
        Materials.link_nodes(material, scratch_ramp, 0, math_subtract, 1)
        math_subtract.operation = "SUBTRACT"
        math_subtract.use_clamp = True
        bump.invert = True
        bump.inputs[0].default_value = 0.2
        bump.inputs[1].default_value = 0.01
        add_bumps = Materials.add_math_node(material)


        if(condition == 1):
            bump.inputs[0].default_value = 0
            bump.inputs[1].default_value = 0
        elif(condition == 2):
            c = 0.277
            mix_rgb_3.inputs[2].default_value = (c, c, c, 1)
        elif(condition == 3):
            mix_rgb_3.inputs[2].default_value = (0.131, 0.051, 0.022, 1)
            c = 0.151
            mix_rgb_2.inputs[2].default_value = (c, c, c, 1)

        Materials.link_nodes(material, tex_coords, 3, mapping, 0)
        Materials.link_nodes(material, tex_coords, 3, pre_noise, 0)
        Materials.link_nodes(material, tex_coords, 3, musgrave, 0)
        Materials.link_nodes(material, mapping, 0, mix_rgb, 1)
        Materials.link_nodes(material, pre_noise, 0, mix_rgb, 2)
        Materials.link_nodes(material, mix_rgb, 0, noise, 0)
        Materials.link_nodes(material, noise, 0, ramp, 0)
        Materials.link_nodes(material, ramp, 0, mix_rgb_2, 1)
        Materials.link_nodes(material, mix_rgb_2, 0, mix_rgb_3, 1)
        Materials.link_nodes(material, mix_rgb_3, 0, bsdf, 0)

        #roughness
        Materials.link_nodes(material, musgrave, 0, ramp_2, 0)
        Materials.link_nodes(material, musgrave, 0, mix_rgb_3, 0)
        Materials.link_nodes(material, ramp_2, 0, math, 0)
        Materials.link_nodes(material, math, 0, bsdf, 9)
        Materials.link_nodes(material, math_subtract, 0, add_bumps, 0)
        Materials.link_nodes(material, ramp, 0, add_bumps, 1)
        Materials.link_nodes(material, add_bumps, 0, bump, 2)
        Materials.link_nodes(material, bump, 0, bsdf, Materials.bsdf_normal_input)
        return material



  
    def plaster():
        material = bpy.data.materials.new("Plaster")
        
        material.use_nodes = True
       
        bsdf = Materials.get_node(material, "Principled BSDF")
        output = Materials.get_output(material)
        voronoi = Materials.add_node(material, "ShaderNodeTexVoronoi")
        noise = Materials.add_node(material, "ShaderNodeTexNoise")
        voronoi.distance = 'MANHATTAN'
        voronoi.inputs[2].default_value = 30

        tex_coords = Materials.add_tex_coords_node(material)
        mapping = Materials.add_mapping_node(material)

        ramp = Materials.add_ramp_node(material)
        c = 0.223
        c_darker = 0.116
        ramp = Materials.adjust_ramp(ramp, 0, 0.187, (c, c, c, 1))
        ramp = Materials.adjust_ramp(ramp, 1, 0.773, (c_darker, c_darker, c_darker, 1))

        bump = Materials.add_bump_node(material)
        bump.inputs[0].default_value = 0.5
        bump_2 = Materials.add_bump_node(material)
        bump_2.inputs[0].default_value = 0.2

        noise_2 = Materials.add_node(material, "ShaderNodeTexNoise")

        bump_ramp = Materials.add_ramp_node(material)
        bump_ramp = Materials.adjust_ramp(bump_ramp, 0, 0.290)
        bump_ramp = Materials.adjust_ramp(bump_ramp, 1, 0.684)


        mix_rgb = Materials.add_node(material, "ShaderNodeMixRGB")

        Materials.link_nodes(material, tex_coords, 3, mapping, 0)
        Materials.link_nodes(material, mapping, 0, noise, 0)
        Materials.link_nodes(material, mapping, 0, noise_2, 0)
        Materials.link_nodes(material, noise, 1, voronoi, 0)
        Materials.link_nodes(material, voronoi, 0, mix_rgb, 1)
        Materials.link_nodes(material, noise_2, 0, mix_rgb, 2)
        Materials.link_nodes(material, mix_rgb, 0, ramp, 0)
        Materials.link_nodes(material, ramp, 0, bsdf, 0)
        Materials.link_nodes(material, bsdf, 0, output, 0)

        Materials.link_nodes(material, voronoi, 0, bump_ramp, 0)
        Materials.link_nodes(material, bump_ramp, 0, bump, 2)
        Materials.link_nodes(material, noise_2, 0, bump_2, 2)
        Materials.link_nodes(material, bump, 0, bump_2, 5)
        Materials.link_nodes(material, bump_2, 0, bsdf, Materials.bsdf_normal_input)
        


    def get_material(name):
        for i in len(bpy.data.materials):
            if str(name) == bpy.data.materials[i].name:
                return bpy.ddata.materials[i].name
    def remove_node(material, name):
        material.node_tree.nodes.remove(material.node_tree.nodes.get(name))

    def add_node(material, name):
        node: bpy.types.Node = material.node_tree.nodes.new(name)
        return node

    def link_nodes(material, s_1, s1_output, s_2, s_2_input):
        material.node_tree.links.new(s_2.inputs[s_2_input], s_1.outputs[s1_output])

    def add_tex_coords_node(material):
        return Materials.add_node(material, "ShaderNodeTexCoord")
    def add_mapping_node(material):
        return Materials.add_node(material, "ShaderNodeMapping")
    def add_ramp_node(material):
        return Materials.add_node(material, "ShaderNodeValToRGB")
    def add_bump_node(material):
        return Materials.add_node(material, "ShaderNodeBump")
    def add_noise_node(material):
        return Materials.add_node(material, "ShaderNodeTexNoise")
    def get_node(material, name):
        return material.node_tree.nodes.get(name)
    def get_output(material):
        return Materials.get_node(material, "Material Output")
    def adjust_ramp(ramp, handle_index, pos, color = -1):
        if(color != -1):
            ramp.color_ramp.elements[handle_index].color = color
            
        ramp.color_ramp.elements[handle_index].position = pos
        return ramp
        

       



