"""
# code * utf-8
# This class is going to create and save .xml document with Labelimg's form.
# To know about how to use it, please refer to the main function.
# version: v_1.0
# update date: 2018-9-13
# coder: holy-c
"""
from lxml import etree, objectify


class XMLSever:

    def __init__(self, folder, filename, image_path, width, height, depth=3):
        """
        # For example: example = XMLServer(folder,filename....)
        :param folder:  the last folder that all the .xml and .jpg will be saved
        :param filename: the filename without .xml
        :param image_path: the absolute path of the image with the suffix.
        :param width: the width of the image that can be got by opencv
        :param height: the height of the image that can be got by opencv
        :param depth: the depth of the image that can be got by opencv
        """
        self.folder = folder
        self.filename = filename
        self.path = image_path
        self.width = width
        self.height = height
        self.depth = depth
        self.E = objectify.ElementMaker(annotate=False)
        self.anno_tree = self.E.annotation(
            self.E.folder(self.folder),
            self.E.filename(self.filename),
            self.E.path(self.path),
            self.E.source(
                self.E.database('Unknown'),
            ),
            self.E.size(
                self.E.width(self.width),
                self.E.height(self.height),
                self.E.depth(self.depth),
            ),
            self.E.segmented(0),
        )

    def add_object(self, label, xmin, ymin, xmax, ymax):
        """
        # This function will add new label and bounding box to the annotation tree
        # For example: example.add_object(label, xmin....)
        :param label:
        :param xmin:
        :param ymin:
        :param xmax:
        :param ymax:
        :return:
        """
        add_tree = self.E.object(
            self.E.name(label),
            self.E.pose("Unspecified"),
            self.E.truncated(0),
            self.E.Difficult(0),
            self.E.bndbox(
                self.E.xmin(xmin),
                self.E.ymin(ymin),
                self.E.xmax(xmax),
                self.E.ymax(ymax),
            ),
            self.E.difficult(0),
        )
        self.anno_tree.append(add_tree)

    def save(self):
        """
        # save .xml to the path, the program will find where the dot is to change the .jpg(and so on) to .xml
        # so don't add  extra dot to your path except image's name.
        :return:
        """
        dot = self.path.find('.')
        etree.ElementTree(self.anno_tree).write(self.path[:dot]+".xml", pretty_print=True)


# for example and test
if __name__ == '__main__':
    """
    # to create a xml_server just like this and if you want to create more, just recreate it.
    """
    server = XMLSever("VID_20180612_203442", "VID_20180612_203442_3",
                      "D:\Holy_cc\Label_demo\VID_20180612_203442\VID_20180612_203442_3.jpg", 1280, 720, 3)
    server.add_object("write", 100, 100, 300, 300)
    server.add_object("write", 300, 300, 600, 600)
    server.save()
    server = XMLSever("VID_20180612_203442", "VID_20180612_203442_4",
                      "D:\Holy_cc\Label_demo\VID_20180612_203442\VID_20180612_203442_4.jpg", 1280, 720, 3)
    server.add_object("write", 100, 100, 300, 300)
    server.add_object("write", 300, 300, 600, 600)
    server.save()

