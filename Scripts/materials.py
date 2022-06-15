import bpy
import typing


class Materials:

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
