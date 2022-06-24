import bpy


class Gen:
    @staticmethod
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

    @staticmethod
    def parenting(elements, parent):
        bpy.ops.object.select_all(action='DESELECT')  # deselect all object
        for element in elements:
            element.select_set(True)  # select the object for the 'parenting'
        # the active object will be the parent of all selected object
        bpy.context.view_layer.objects.active = parent
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

    @staticmethod
    def prepare_mesh(meshname: str, object_name: str):
        mesh = bpy.data.meshes.new(meshname)  # add a new mesh
        # add a new object using the mesh
        obj = bpy.data.objects.new(object_name, mesh)
        scene = bpy.context.scene
        # put the object into the scene (link)
        scene.collection.objects.link(obj)
        # set as the active object in the scene
        bpy.context.view_layer.objects.active = obj
        obj.select_set(state=True)  # select object

        mesh = bpy.context.object.data
        return mesh
    @staticmethod
    def cm_to_m(val):
        return val/100
