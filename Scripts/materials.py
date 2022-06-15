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
            mapping.inputs[0], tex_coord.outputs[0])
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
    def create_metal_material():
        metal_material = bpy.data.materials.new("Metal")
        metal_material.use_nodes = True
        metal_material.node_tree.nodes["Principled BSDF"].inputs[9].default_value = 0.15
        metal_material.node_tree.nodes["Principled BSDF"].inputs[6].default_value = 1
        return metal_material


  
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
    def get_node(material, name):
        return material.node_tree.nodes.get(name)
    def get_output(material):
        return Materials.get_node(material, "Material Output")
    def adjust_ramp(ramp, handle_index, pos, color = -1):
        if(color != -1):
            ramp.color_ramp.elements[handle_index].color = color
            
        ramp.color_ramp.elements[handle_index].position = pos
        return ramp
        

       



