import os
from xml.etree import ElementTree as ET

class PyQtResourceGeneratorError(Exception):
    pass

class PyQtResourceGenerator():

    def __init__(self):
        pass


    def generate_image_list(self, qrc_root_path, image_root_path=''):
        """
        Recursively search from the root path for images and return a list of image paths
        @param qrc_root_path This is the root path where pyrcc4 will be run (it has to be the path of the file that calls the function call_pyrcc4())
        @param image_root_path This is the root path of where to start looking for images (note that it must be within the qrc_root_path)
        @return tuple(string, string) with (relative path to image from image_root_path) and (relative path to image from qrc_root_path)
        """
        import imghdr
        images = []
        
        if image_root_path == '':
            image_root_path = qrc_root_path
        
        for root, _, files in os.walk(image_root_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                if imghdr.what(filepath) is not None:
                    relative_path = filepath.replace(qrc_root_path, '')
                    alias_path = filepath.replace(image_root_path, '')[1:]
                    images.append((alias_path, relative_path))

        return images


    def generate_qrc(self, images):
        """
        Generate the QRC (resource collection) file based on a list of images
        @param images List<String> List of strings that contain the filepaths to the images. 
        @return String consisting of the QRC XML
        """
        # Create the root element
        root = ET.Element('RCC')
        # Create the sub-sections
        qresource_root = ET.SubElement(root, 'qresource')

        for alias_path, qrc_relative_path in images:
            img_element = ET.SubElement(qresource_root, 'file')
            img_element.text = qrc_relative_path
            img_element.attrib = {'alias': alias_path}

        return ET.tostring(root, 'unicode')


    def save(self, xml_content, dest_path):
        """
        Generate the qrc file
        """
        try:
            with open(dest_path, 'w') as f:
                f.write(xml_content)
        except Exception as e:
            raise PyQtResourceGeneratorError("Failed to save qrc file: %s" % e)


    def call_pyrcc4(self, source_qrc, dest_python, pyrcc4_path="C:\Python33\Lib\site-packages\PyQt4\pyrcc4.exe", args=['-py3', '-compress 9', '-o']):
        """
        Call pyrcc4.exe in order to generate the python file
        """
        command = pyrcc4_path

        for arg in args:
            command += ' ' + arg
        command += ' "' + dest_python + '" "' + source_qrc + '"'

        from subprocess import check_call
        check_call(command)