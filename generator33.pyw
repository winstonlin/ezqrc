import os
import configparser

from PyQt4 import QtGui, QtCore
from xml.etree import ElementTree as ET

class MainWindow(QtGui.QMainWindow):

    VERSION = "1.00"

    CONFIG_PATH = "config.cfg"
    IMAGE_ROOT_PATH = ""
    PYRCC4_PATH = "C:\Python27\Lib\site-packages\PyQt4\pyrcc4.exe"
    RES_QRC_PATH = "resources.qrc"
    RES_PYTHON_PATH = "resources.py"

    SCREEN_X = 600
    SCREEN_Y = 275

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Handle configuration file
        if os.path.exists(self.CONFIG_PATH):
            self.config = SimpleConfig(self.CONFIG_PATH)
        else:
            self.config = SimpleConfig()
            self.config["image_root_path"] = self.IMAGE_ROOT_PATH
            self.config["pyrcc4_path"] = self.PYRCC4_PATH
            self.config["res_qrc_path"] = self.RES_QRC_PATH
            self.config["res_python_path"] = self.RES_PYTHON_PATH
            self.config["python3_mode"] = False
            self.config.save(self.CONFIG_PATH)
            self.config.load(self.CONFIG_PATH)

        self.__init_ui()


    def __init_ui(self):
        self.setWindowTitle("EZQRC - PyQt Resource Generator %s" % self.VERSION)
        self.setFixedSize(self.SCREEN_X, self.SCREEN_Y)
        self.statusBar().setSizeGripEnabled(False)
        self.__set_status("Ready")
        self.main_widget = QtGui.QFrame(self)
        self.setCentralWidget(self.main_widget)

        self.txt_image_root = QtGui.QLineEdit(self.config["image_root_path"])
        self.txt_pyrcc4_path = QtGui.QLineEdit(self.config["pyrcc4_path"])
        self.txt_res_qrc_path = QtGui.QLineEdit(self.config["res_qrc_path"])
        self.txt_res_python_path = QtGui.QLineEdit(self.config["res_python_path"])

        self.btn_browse_image_root = QtGui.QPushButton("Browse")
        self.btn_browse_image_root.clicked.connect(self.__browse_image_root)

        self.btn_browse_pyrcc4 = QtGui.QPushButton("Browse")
        self.btn_browse_pyrcc4.clicked.connect(self.__browse_pyrcc4)

        self.chk_python3 = QtGui.QCheckBox("Python 3 Mode")
        self.chk_python3.setChecked(self.config["python3_mode"])

        self.btn_generate = QtGui.QPushButton("Generate QRC")
        self.btn_generate.clicked.connect(self.__generate)
        self.btn_generate.setFixedWidth(self.btn_generate.sizeHint().width())

        self.btn_config = QtGui.QPushButton("Save Config Changes")
        self.btn_config.clicked.connect(self.__save_config)
        self.btn_config.setFixedWidth(self.btn_config.sizeHint().width())

        act_about = QtGui.QAction("About", self.menuBar(), triggered=self.__about)
        self.menuBar().addAction(act_about)

        main_layout = QtGui.QVBoxLayout()
        grid_layout = QtGui.QGridLayout()
        grid_layout.addWidget(QtGui.QLabel("Root path to images:"), 0, 0)
        grid_layout.addWidget(self.txt_image_root, 1, 0)
        grid_layout.addWidget(self.btn_browse_image_root, 1, 1)
        grid_layout.addWidget(QtGui.QLabel("Path to pyrcc4.exe:"), 2, 0)
        grid_layout.addWidget(self.txt_pyrcc4_path, 3, 0)
        grid_layout.addWidget(self.btn_browse_pyrcc4, 3, 1)
        grid_layout.addWidget(self.chk_python3, 4, 0)

        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.btn_generate, alignment=QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.btn_config, alignment=QtCore.Qt.AlignCenter)
        main_layout.addStretch()
        self.main_widget.setLayout(main_layout)


    def __browse_image_root(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, caption="Select Images Root Folder")
        if not directory:
            return
        self.txt_image_root.setText(directory)


    def __browse_pyrcc4(self):
        filepath = QtGui.QFileDialog.getOpenFileName(self, "Select Pyrcc4.exe", directory=".", filter="Executables (*.exe)")
        if not filepath:
            return
        self.txt_pyrcc4_path.setText(filepath)


    def __generate(self):
        generator = PyQtResourceGenerator()
        try:
            if not os.path.exists(self.txt_pyrcc4_path.text()):
                raise Exception("The following pyrcc4 path is invalid: %s" % self.txt_pyrcc4_path.text())

            image_list = generator.generate_image_list(str(self.txt_image_root.text()))
            xml_content = generator.generate_qrc(image_list)
            generator.save(xml_content, str(self.txt_res_qrc_path.text()))
            generator.call_pyrcc4(str(self.txt_res_qrc_path.text()),
                                  str(self.txt_res_python_path.text()),
                                  str(self.txt_pyrcc4_path.text()),
                                  self.chk_python3.isChecked())

            msg = "Resource file generated: %s" % self.txt_res_python_path.text()
            QtGui.QMessageBox.information(self, "Success!", msg)
            self.__set_status(msg)
        except Exception as e:
            msg = "Error: %s" % e
            QtGui.QMessageBox.warning(self, "Error", msg)
            self.__set_status(msg)


    def __save_config(self):
        self.config["image_root_path"] = self.txt_image_root.text()
        self.config["pyrcc4_path"] = self.txt_pyrcc4_path.text()
        self.config["res_qrc_path"] = self.txt_res_qrc_path.text()
        self.config["res_python_path"] = self.txt_res_python_path.text()
        self.config["python3_mode"] = str(self.chk_python3.isChecked())
        self.config.save(self.CONFIG_PATH)

        msg = "Configuration saved: %s" % self.CONFIG_PATH
        QtGui.QMessageBox.information(self, "Success!", msg)
        self.__set_status(msg)


    def __set_status(self, message):
        self.statusBar().showMessage(message)


    def __about(self):
        QtGui.QMessageBox.about(self,
                                "About",
                                "The MIT License (MIT)\nCopyright (c) 2013 Winston Lin")

class SimpleConfig(dict):
    """
    Simple configuration file
    """
    MAIN_SECTION = "Config"
    def __init__(self, filepath=None):
        """
        @param filepath String Optionally provide a path to load a config file on init
        """
        if filepath is not None:
            self.load(filepath)


    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        else:
            raise Exception("Tried to access a non-existent key in the configuration: %s" % key)


    def load(self, filepath):
        """
        Load the configuration file
        @param filepath String Path for the configuration file to be loaded
        """
        # Load configuration file
        if os.path.exists(filepath):
            config = configparser.RawConfigParser()
            try:
                config.read(filepath)
                print(("Local configuration loaded: %s" % filepath))
            except Exception as e:
                raise Exception("Failed to read configuration file: %s" % e)

            # Load dictionary with config parameters
            if config.has_section(self.MAIN_SECTION):
                import ast
                for key, value in config.items(self.MAIN_SECTION):
                    # Handle floats and integers
                    try:
                        self[key] = ast.literal_eval(value)
                    except:
                        self[key] = value

            return True
        else:
            raise Exception("Configuration (%s) could not be found. No file was loaded." % filepath)


    def save(self, filepath):
        """
        Save the configuration file
        @param filepath String Path for the configuration file to be saved
        """
        config = configparser.RawConfigParser()
        config.add_section(self.MAIN_SECTION)

        for key, value in list(self.items()):
            config.set(self.MAIN_SECTION, key, str(value))

        try:
            with open(filepath, 'w') as config_file:
                config.write(config_file)
        except Exception as e:
            raise Exception("Failed to save local configuration :: %s" % e)


class PyQtResourceGenerator(object):

    def __init__(self):
        pass


    def generate_image_list(self, image_root_path):
        """
        Recursively search from the root path for images and return a list of image paths
        @param image_root_path This is the root path of where to start looking for images
        @return tuple(string, string) with (relative path to image from image_root_path) and (relative path to image from qrc_root_path)
        """
        import imghdr
        images = []

        # pyrcc4 will be executed from this path
        qrc_root_path = os.path.dirname(__file__)

        for root, _, files in os.walk(image_root_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                # Select only images
                if imghdr.what(filepath) is not None:
                    relative_path = os.path.relpath(filepath, qrc_root_path)
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

        return ET.tostring(root, "unicode")


    def save(self, xml_content, dest_path):
        """
        Generate the qrc file
        """
        try:
            with open(dest_path, 'w') as f:
                f.write(xml_content)
        except Exception as e:
            raise Exception("Failed to save qrc file: %s" % e)


    def call_pyrcc4(self, source_qrc, dest_python, pyrcc4_path, python3_mode=False):
        """
        Call pyrcc4.exe in order to generate the python file
        @param source_qrc String Path to generated QRC file
        @param dest_python String Path to Python file to be generated
        @param pyrcc4_path String Path to pyrcc4
        """
        command = pyrcc4_path
        if python3_mode:
            command += ' -py3 '
        command += ' -compress 9 -o "' + dest_python + '" "' + source_qrc + '"'

        import subprocess
        print(("Executing command: %s" % command))
        process = subprocess.Popen(command, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if process.returncode != 0:
            raise Exception("Command: %s\nPyrcc4 STDERR: %s" % (command, err))


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    app.exec_()
