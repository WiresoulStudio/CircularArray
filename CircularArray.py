bl_info = {
    "name": "Circular Array",
    "author": "Wiresoul Studio",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Item tab",
    "description": "Makro for setting up a circular arrays",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import bpy
from bpy.types import Operator
from bpy.props import FloatProperty, IntProperty
from mathutils import Vector, Euler
from math import *

from bpy.app.handlers import persistent


class OBJECT_OT_circulate(Operator):
    """Create a radial array"""
    bl_idname = "object.circulate"
    bl_label = "Circular Array"
    bl_options = {'REGISTER', 'UNDO'}

    angle: FloatProperty(
        name="angle",
        default=2*pi,
        subtype='ANGLE',
        description="angle",
        soft_min=-2*pi,
        soft_max=2*pi,
    )
    
    count: IntProperty(
        name="count",
        default=6,
        description="number of instances",
        min=2,
        soft_min=2,
        soft_max=24,
    )

    def execute(self, context):

        # sort the selected objects
        actOb = context.object
        if actOb == None:
            return {'FINISHED'}
        
        obToSpin = context.object
        selection = context.selected_objects
        if len(selection) > 1:
            selection.remove(actOb)
            obToSpin = selection[0]
                
        # actOb ~ this is where the axis will be placed
        # obToSpin ~ object that dictates the original transforms
        
        
        # Axis object
        bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(0, 0, 0))
        osa = bpy.context.object
        osa.name = "Axis of " + obToSpin.name
        
        
        # setting the properties
        osa.angle = self.angle
        osa.count = self.count
        
        # Rotation object
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0))
        rots = bpy.context.object
        rots.name = "Angle of " + obToSpin.name
        rots.empty_display_size = 0.01
        
        # placeholder
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0))
        holder = bpy.context.object
        holder.name = "Placeholder of " + obToSpin.name
        holder.empty_display_size = 0.01
        
        # parenting
        osa.parent = actOb
        rots.parent = osa
        holder.parent = rots
        
        # placeholder drivers
        drv = holder.driver_add("location", 0).driver
        drv.type = "SCRIPTED"
        var = drv.variables.new()
        var.targets[0].id = osa
        var.targets[0].data_path = "matrix_world"
        var.name = "matOsa"
        var = drv.variables.new()
        var.targets[0].id = obToSpin
        var.targets[0].data_path = "matrix_world"
        var.name = "matOb"
        drv.expression = "invpos(matOsa, matOb).x"
        
        drv = holder.driver_add("location", 1).driver
        drv.type = "SCRIPTED"
        var = drv.variables.new()
        var.targets[0].id = osa
        var.targets[0].data_path = "matrix_world"
        var.name = "matOsa"
        var = drv.variables.new()
        var.targets[0].id = obToSpin
        var.targets[0].data_path = "matrix_world"
        var.name = "matOb"
        drv.expression = "invpos(matOsa, matOb).y"
        
        drv = holder.driver_add("location", 2).driver
        drv.type = "SCRIPTED"
        var = drv.variables.new()
        var.targets[0].id = osa
        var.targets[0].data_path = "matrix_world"
        var.name = "matOsa"
        var = drv.variables.new()
        var.targets[0].id = obToSpin
        var.targets[0].data_path = "matrix_world"
        var.name = "matOb"
        drv.expression = "invpos(matOsa, matOb).z"
        
        
        drv = holder.driver_add("rotation_euler", 0).driver
        drv.type = "SCRIPTED"
        var = drv.variables.new()
        var.targets[0].id = osa
        var.targets[0].data_path = "matrix_world"
        var.name = "matOsa"
        var = drv.variables.new()
        var.targets[0].id = obToSpin
        var.targets[0].data_path = "matrix_world"
        var.name = "matOb"
        drv.expression = "invrot(matOsa, matOb).x"
        
        drv = holder.driver_add("rotation_euler", 1).driver
        drv.type = "SCRIPTED"
        var = drv.variables.new()
        var.targets[0].id = osa
        var.targets[0].data_path = "matrix_world"
        var.name = "matOsa"
        var = drv.variables.new()
        var.targets[0].id = obToSpin
        var.targets[0].data_path = "matrix_world"
        var.name = "matOb"
        drv.expression = "invrot(matOsa, matOb).y"
        
        drv = holder.driver_add("rotation_euler", 2).driver
        drv.type = "SCRIPTED"
        var = drv.variables.new()
        var.targets[0].id = osa
        var.targets[0].data_path = "matrix_world"
        var.name = "matOsa"
        var = drv.variables.new()
        var.targets[0].id = obToSpin
        var.targets[0].data_path = "matrix_world"
        var.name = "matOb"
        drv.expression = "invrot(matOsa, matOb).z"
        
        
        # modifier
        arMod = obToSpin.modifiers.new("Radial", "ARRAY")
        arMod.use_relative_offset = False
        arMod.use_object_offset = True
        arMod.offset_object = holder
        
        osa["obName"] = obToSpin.name
        osa["modName"] = arMod.name

        countString = "modifiers[\"" + arMod.name + "\"].count"
    
        drv = obToSpin.driver_add(countString).driver
        drv.type = "SUM"
        var = drv.variables.new()
        var.targets[0].id = osa
        var.targets[0].data_path = "count"
        var.name = "varNum"
        
        drv = rots.driver_add('rotation_euler', 2).driver
        drv.type = "SCRIPTED"
        var = drv.variables.new()
        var.targets[0].id = osa
        var.targets[0].data_path = "count"
        var.name = "n"
        var = drv.variables.new()
        var.targets[0].id = osa
        var.targets[0].data_path = "angle"
        var.name = "a"
        drv.expression = "(a/n) if a>6.2825 and a<6.2835 else a/(n-1)"


        # select the original again
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = osa
        osa.select_set(True)

        return {'FINISHED'}


class OBJECT_OT_remCirculate(Operator):
    """Delete a radial array"""
    bl_idname = "object.remcirculate"
    bl_label = "Remove Array"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        osa = context.object
        
        if osa == None:
            return {'FINISHED'}
        if "Axis of" not in osa.name:
            return {'FINISHED'}
        
        # remove modifier
        circled = bpy.data.objects[osa["obName"]]
        countString = "modifiers[\"" + osa["modName"] + "\"].count"
        
        circled.driver_remove(countString)
        
        modifier_to_remove = circled.modifiers.get(osa["modName"])
        circled.modifiers.remove(modifier_to_remove)
        
        # delete helpers
        bpy.ops.object.select_all(action='DESELECT')
        osa.select_set(True)
        osa.children[0].select_set(True)
        osa.children[0].children[0].select_set(True)
        
        bpy.ops.object.delete(use_global=False, confirm=False)

        
        
        return {'FINISHED'}


def circulate_button(self, context):
    self.layout.operator(
        OBJECT_OT_circulate.bl_idname,
        text="Circular Array",
        icon='PHYSICS')


class VIEW3D_PT_circular_array(bpy.types.Panel):
    bl_category = "Item"
    bl_label = "Circular Array"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectmode"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def draw(self, context):
        layout = self.layout
        
        if "Axis of" in context.object.name: 
        
            col = layout.column(align=True)
            col.prop(context.object, "angle", text="Angle")
            col.prop(context.object, "count", text="Count")
            
            col = layout.column(align=True)
            col.operator(OBJECT_OT_remCirculate.bl_idname, text="Remove array", icon="CANCEL")
        else:
            col = layout.column(align=True)
            col.operator(OBJECT_OT_circulate.bl_idname, text="Create array", icon="PHYSICS")
        


def invPos(matA, matB):
    inv = matA.inverted_safe()
    res = inv @ matB
    return res.translation

def invRot(matA, matB):
    inv = matA.inverted_safe()
    res = inv @ matB
    return res.to_euler()


@persistent
def load_handler(dummy):
    #dns = bpy.app.driver_namespace
    print("registering drivers")
    # register your drivers
    bpy.app.driver_namespace["invpos"] = invPos
    bpy.app.driver_namespace["invrot"] = invRot


def register():
    
    bpy.types.Object.angle = FloatProperty(
        name="angle",
        default=2*pi,
        subtype='ANGLE',
        description="angle",
        soft_min=-2*pi,
        soft_max=2*pi,
    )
    
    bpy.types.Object.count = IntProperty(
        name="count",
        default=6,
        description="number of instances",
        min=2,
        soft_min=2,
        soft_max=24,
    )
    
    bpy.utils.register_class(OBJECT_OT_circulate)
    bpy.utils.register_class(OBJECT_OT_remCirculate)
    load_handler(None)
    bpy.app.handlers.load_post.append(load_handler)
    bpy.types.VIEW3D_MT_object.append(circulate_button)
    bpy.types.VIEW3D_MT_object_context_menu.append(circulate_button)
    bpy.utils.register_class(VIEW3D_PT_circular_array)
    


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_circulate)
    bpy.utils.unregister_class(OBJECT_OT_remCirculate)
    bpy.app.handlers.load_post.remove(load_handler)
    bpy.types.VIEW3D_MT_object.remove(circulate_button)
    bpy.types.VIEW3D_MT_object_context_menu.remove(circulate_button)
    bpy.utils.unregister_class(VIEW3D_PT_circular_array)

if __name__ == "__main__":
    register()
    