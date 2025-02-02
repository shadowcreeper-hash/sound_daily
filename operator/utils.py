import bpy
import os
import webbrowser

from bpy_extras.io_utils import ExportHelper
from bpy.props import EnumProperty, StringProperty, BoolProperty, CollectionProperty, IntProperty, FloatProperty

from ..util import KeyController
from ..util import ignored_keys, get_pref

from .. import __folder_name__


class SD_OT_UrlLink(bpy.types.Operator):
    bl_idname = 'sd.url_link'
    bl_label = 'URL Link'

    url: StringProperty(name='引流链接')

    def execute(self, context):
        if self.url.startswith('https://'):
            webbrowser.open(self.url)
        else:
            self.report({"ERROR"}, '请输入正确链接')
        return {"FINISHED"}


class SD_OT_OpenFolder(bpy.types.Operator):
    """打开文件夹"""
    bl_idname = 'sd.open_folder'
    bl_label = 'Open Folder'

    def execute(self, context):
        addon_folder = os.path.join(bpy.utils.user_resource('SCRIPTS'), "addons", __folder_name__)
        os.startfile(os.path.join(addon_folder, '../res', 'img'))
        return {"FINISHED"}


class SD_OT_BatchImport(bpy.types.Operator, ExportHelper):
    """批量导入音频"""
    bl_idname = 'sd.batch_import'
    bl_label = '批量导入'

    # build-in
    filename_ext = ''

    files: CollectionProperty(name="File Path", type=bpy.types.OperatorFileListElement)
    directory: StringProperty(subtype='DIR_PATH')
    add_type: EnumProperty(items=[
        ('IMG', 'Image Folder', ''),
        ('SOUND', 'Sound', ''),
    ])

    def draw(self, context):
        if self.add_type == 'IMG':
            self.layout.label(text='请选中包含图像文件夹（支持jpg,png,exr,hdr）', icon='ERROR')
        else:
            self.layout.label(text='请选中音乐文件', icon='ERROR')

    def execute(self, context):
        self.add_sound()
        context.area.tag_redraw()
        return {'FINISHED'}

    def add_image(self):
        for file_elem in self.files:
            filepath = os.path.join(self.directory, file_elem.name)
            bpy.ops.sd.image_list_action(action='ADD',
                                         path=filepath)

    def add_sound(self):
        for file_elem in self.files:
            filepath = os.path.join(self.directory, file_elem.name)
            bpy.ops.sd.sound_list_action(action='ADD',
                                         path=filepath,
                                         name=file_elem.name)


class SD_OT_SetKeymap(bpy.types.Operator):
    """按下以设置绑定键"""
    bl_idname = "sd.get_event"
    bl_label = "Get event"

    item = None
    key_input = None

    def append_handle(self):
        bpy.context.window_manager.modal_handler_add(self)

    def remove_handle(self):
        pass

    def invoke(self, context, event):
        pref = get_pref()
        if len(pref.sound_list) == 0: return {'FINISHED'}

        self.key_input = KeyController()
        # start listening
        context.window_manager.sd_listening = 1
        self.append_handle()
        self.item = pref.sound_list[pref.sound_list_index]

        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        self.detect_keyboard(event)

        if context.window_manager.sd_listening == 0:
            context.area.tag_redraw()
            return {"FINISHED"}

        return {"PASS_THROUGH"}

    def detect_keyboard(self, event):
        if event.value == "PRESS" and event.type not in ignored_keys:
            self.key_input.set_item_keymap(self.item, event)
            bpy.context.window_manager.sd_listening = 0  # stop listening when get a key
            bpy.context.area.tag_redraw()


def register():
    bpy.utils.register_class(SD_OT_BatchImport)
    bpy.utils.register_class(SD_OT_OpenFolder)
    bpy.utils.register_class(SD_OT_SetKeymap)
    bpy.utils.register_class(SD_OT_UrlLink)


def unregister():
    bpy.utils.unregister_class(SD_OT_BatchImport)
    bpy.utils.unregister_class(SD_OT_OpenFolder)
    bpy.utils.unregister_class(SD_OT_SetKeymap)
    bpy.utils.unregister_class(SD_OT_UrlLink)
