import sys
from PIL import Image
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog


class ImageProcessing:
    """A class that uses Pillow for processing images and data."""

    def __init__(self, image, watermark_image):
        """
        :param image: [Required] The primary image to be stored and processed.
        :param watermark_image: [Required] The watermark image to be stored and overlayed.
        """

        self.image = image
        self.watermark_image = watermark_image

    def get_original_image(self, max=None):
        """
        Returns the original image without a watermark overlaid.

        :param max: [Optional] Default = None. Size of the longest side in pixels (Width or Height)
        :return: If max=none returns image at original size. If other than None, resizes image with longest
        side being equal to max.
        """

        w = self.image.size[0]
        h = self.image.size[1]

        if max is None:
            resized_image = self.image
        elif w > h:
            ratio = max / w
            resized_image = self.image.resize((int(w * ratio), int(h * ratio)))
        else:
            ratio = max / h
            resized_image = self.image.resize((int(w * ratio), int(h * ratio)))

        return resized_image

    def get_watermark_image(self, max=None):
        """"
        Returns the original image with a watermark overlaid.

        :param max: [Optional] Default = None. Size of the longest side in pixels (Width or Height)
        :return: If max=none returns image at original size. If other than None, resizes image with longest
        side being equal to max.
        """

        new_image = Image.new("RGBA", (self.image.size[0], self.image.size[1]))

        new_image.paste(self.image)
        w = self.watermark_image.size[0]
        h = self.watermark_image.size[1]
        new_image.paste(self.watermark_image, (self.watermark_image.size[0] - w, self.watermark_image.size[1] - h),
                        self.watermark_image)

        w = new_image.size[0]
        h = new_image.size[1]

        if max is None:
            resized_image = new_image
        elif w > h:
            ratio = max / w
            resized_image = new_image.resize((int(w * ratio), int(h * ratio)))
        else:
            ratio = max / h
            resized_image = new_image.resize((int(w * ratio), int(h * ratio)))

        return resized_image


# **********************************************************************************************************************
#
#
# **********************************************************************************************************************

global watermark_location, main_image_location
watermark_location = ""
main_image_location = ""
# Initializes the QWindow variables
app = QtWidgets.QApplication(sys.argv)
window = uic.loadUi("GUI.ui")
window.process_button.setEnabled(False)
window.showMaximized()


def load_watermark_button_clicked():
    global watermark_location, main_image_location
    watermark_location = QFileDialog.getOpenFileName(window, 'Open file',
                                                     'c:\\', "Image files (*.jpg *.gif *.png)")[0]
    print("file=" + watermark_location)

    if len(watermark_location) > 0 and len(main_image_location) > 0:
        window.process_button.setEnabled(True)
    else:
        window.process_button.setEnabled(False)

    try:
        window.watermark_image_label.setPixmap(QPixmap(watermark_location))
    except:
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage("File could not be loaded!")


def load_main_image_button_clicked():
    global main_image_location, watermark_location
    main_image_location = QFileDialog.getOpenFileName(window, 'Open file',
                                                      'c:\\', "Image files (*.jpg *.gif *.png)")[0]

    if len(watermark_location) > 0 and len(main_image_location) > 0:
        window.process_button.setEnabled(True)
    else:
        window.process_button.setEnabled(False)

    try:
        window.main_image_label.setPixmap(QPixmap(main_image_location))
    except:
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage("File could not be loaded!")


def combine_images_button_clicked():
    global main_image_location, watermark_location
    window.save_button.setEnabled(True)

    # Combines watermark and original image.
    main_image = Image.open(main_image_location)
    watermark_image = Image.open(watermark_location)
    image = ImageProcessing(main_image, watermark_image)
    output = image.get_watermark_image()
    output.save("WorkInProgress.png")
    window.output_label.setPixmap(QPixmap("WorkInProgress.png"))


def save_button_clicked():
    save_location = QFileDialog.getSaveFileName(window, "Save File")[0]
    image = Image.open("WorkInProgress.png")
    image.save(save_location + ".png")


# Adds event handling.
window.load_main_image_button.clicked.connect(load_main_image_button_clicked)
window.load_watermark_image_button.clicked.connect(load_watermark_button_clicked)
window.process_button.clicked.connect(combine_images_button_clicked)
window.save_button.clicked.connect(save_button_clicked)

window.show()
app.exec()
