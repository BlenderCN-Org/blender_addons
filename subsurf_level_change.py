# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "Subsurf level",
    "category": "Object",
}

import bpy

class SubsurfLevelChange(bpy.types.Operator):
    """Change subsuf level to objects"""
    bl_idname = "object.subsurflevel"
    bl_label = "Change subsurf level"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        d = bpy.data
        
        for obj in scene.objects:
            if obj.type == 'MESH':
                #get modifiers
                keys = d.objects[obj.name].modifiers.keys()
                for key in keys:
                    #check if have subsurf modifier
                    if d.objects[obj.name].modifiers[key].type == 'SUBSURF':        
                        #appy level of sf
                        d.objects[obj.name].modifiers[key].levels = scene.subdivisions_view
                        d.objects[obj.name].modifiers[key].render_levels = scene.subdivisions_render
                    
        return {'FINISHED'}

def init_properties():
    scene = bpy.types.Scene
    
    scene.subdivisions_view = bpy.props.IntProperty(
        name="View",
        description="Subsurf level to appy to the view",
        default=1,
        min=0,
        max=7)
    scene.subdivisions_render = bpy.props.IntProperty(
        name="Render",
        description="Subsurf level to appy to the render",
        default=3,
        min=0,
        max=7)
        
def clear_properties():
    scene = bpy.types.Scene
    
    del scene.subdivisions_view
    del scene.subdivisions_render

class OBJECT_PT_change_subsurf(bpy.types.Panel):
    """draw panel in propierties panel"""
    bl_label = "Change Subsurf level"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "objectomode"
    
    def draw(self, context):
        sc = context.scene
        layout =  self.layout
                
        split = layout.split()
        col = split.column()
        
        sub = col.column(align=True)
        sub.label(text="Subdivisions:")
        sub.prop(sc, "subdivisions_view", text="View")
        sub.prop(sc, "subdivisions_render", text="Render")
        
        layout.operator("object.subsurflevel", text="Apply")
    
def register():
    init_properties()
    bpy.utils.register_class(SubsurfLevelChange)
    bpy.utils.register_class(OBJECT_PT_change_subsurf)
    
def unregister():
    clear_properties()
    bpy.utils.unregister_class(SubsurfLevelChange)
    py.utils.unregister_class(OBJECT_PT_change_subsurf)
    
if __name__ == "__main__":
    register()