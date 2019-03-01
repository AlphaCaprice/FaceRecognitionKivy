'''
Basic camera example
Default picture is saved as
/sdcard/org.test.cameraexample/enter_file_name_here.jpg
'''

import string
from os import getcwd
from os.path import exists, split
from os.path import splitext
from random import randint

import kivy

kivy.require('1.8.0')

from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.logger import Logger
from kivy.uix.image import Image

from kivy.app import App
from os.path import exists
# from jnius import autoclass, cast
# from android import activity, mActivity
from functools import partial
from kivy.clock import Clock
from kivy.uix.scatter import Scatter

# from PIL import Image

#from plyer import camera

# PythonActivity = autoclass('org.renpy.android.PythonActivity')
# Intent = autoclass('android.content.Intent')
# MediaStore = autoclass('android.provider.MediaStore')
# Uri = autoclass('android.net.Uri')
# Environment = autoclass('android.os.Environment')
# Activity = autoclass('android.app.Activity')

# Value of MediaStore.Images.Media.DATA
MediaStore_Images_Media_DATA = "_data"


class CameraDemo(FloatLayout):

    def __init__(self):
        super(CameraDemo, self).__init__()
        self.cwd = getcwd() + "/"
        self.res_array = ["Male!", "Female!", "Male!"]
        # self.ids.path_label.text = self.cwd

    def do_capture(self):

        filepath = (self.cwd + self.ids.filename_text.text)

        if (exists(filepath)):
            popup = MsgPopup("Picture with this name already exists!")
            popup.open()
            return False

        try:
            camera.take_picture(filename=filepath,
                                on_complete=self.camera_callback)

        except NotImplementedError:
            popup = MsgPopup(
                "This feature has not yet been implemented for this platform.")
            popup.open()

    def camera_callback(self, filepath):
        if exists(filepath):
            popup = MsgPopup("Picture saved!")
            popup.open()
            # self.add_photo()

        else:
            popup = MsgPopup("Could not save your picture!")
            popup.open()

    def watch_photo(self):
        filepath = (self.cwd + self.ids.filename_text.text)
        if not (exists(filepath)):
            popup = MsgPopup("Can not find filepath")
            popup.open()
            return False
        self.ids.picture.source = filepath
        self.ids.filename_text.text = '1' + self.ids.filename_text.text

    def callback(self, picPath):

        if not (exists(picPath)):
            popup = MsgPopup("Can not load picture")
            popup.open()
            return False
        #popup = MsgPopup("Picture!")
        #popup.open()
        self.ids.picture.source = picPath

    #######################################

    def add_picture(self):
        """Open Gallery Activity and call callback with absolute image filepath of image user selected.
        None if user canceled.
        """

        # PythonActivity.mActivity is the instance of the current Activity
        # BUT, startActivity is a method from the Activity class, not from our
        # PythonActivity.
        # We need to cast our class into an activity and use it
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)

        # Value of MediaStore.Images.Media.DATA
        MediaStore_Images_Media_DATA = "_data"

        # Custom request codes
        RESULT_LOAD_IMAGE = 1


        # Forum discussion: https://groups.google.com/forum/#!msg/kivy-users/bjsG2j9bptI/-Oe_aGo0newJ
        def on_activity_result(request_code, result_code, intent):
            if request_code != RESULT_LOAD_IMAGE:
                Logger.warning('user_select_image: ignoring activity result that was not RESULT_LOAD_IMAGE')
                return

            if result_code == Activity.RESULT_CANCELED:
                Clock.schedule_once(lambda dt: self.callback("None"), 0)
                return

            if result_code != Activity.RESULT_OK:
                # This may just go into the void...
                raise NotImplementedError('Unknown result_code "{}"'.format(result_code))

            selectedImage = intent.getData()  # Uri
            filePathColumn = [MediaStore_Images_Media_DATA]  # String[]
            # Cursor
            cursor = currentActivity.getContentResolver().query(selectedImage,
                                                                filePathColumn, None, None, None)
            cursor.moveToFirst()

            # int
            columnIndex = cursor.getColumnIndex(filePathColumn[0])
            # String
            picturePath = cursor.getString(columnIndex)
            cursor.close()
            Logger.info('android_ui: user_select_image() selected %s', picturePath)


            # This is possibly in a different thread?
            Clock.schedule_once(lambda dt: self.callback(picturePath), 0)

        # See: http://pyjnius.readthedocs.org/en/latest/android.html
        activity.bind(on_activity_result=on_activity_result)

        intent = Intent()

        # http://programmerguru.com/android-tutorial/how-to-pick-image-from-gallery/
        # http://stackoverflow.com/questions/18416122/open-gallery-app-in-android
        intent.setAction(Intent.ACTION_PICK)
        # TODO internal vs external?
        intent.setData(Uri.parse('content://media/internal/images/media'))
        # TODO setType(Image)?

        currentActivity.startActivityForResult(intent, RESULT_LOAD_IMAGE)

        #####################################################

    def send_photo(self):
        res = self.res_array[0]
        self.res_array = self.res_array[1:]
        popup = MsgPopup(res)
        popup.open()



class CameraDemoApp(App):
    def __init__(self):
        super(CameraDemoApp, self).__init__()
        self.demo = None

    def build(self):
        self.demo = CameraDemo()
        return self.demo

    def on_pause(self):
        return True

    def on_resume(self):
        pass


class MsgPopup(Popup):
    def __init__(self, msg):
        super(MsgPopup, self).__init__()
        self.ids.message_label.text = msg


if __name__ == '__main__':
    CameraDemoApp().run()
