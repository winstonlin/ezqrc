EZQRC
=====
EZQRC is a PyQt4 Resource Generator. This project provides an easy-to-use GUI interface (created with PyQt) for automatically generating the PyQt Python module that can then subsequently be imported into your Python project.

One of the recurring issues that users often face when using PyQt resources is that they must generate a QRC file for their resources. Oftentimes, this is accomplished manually by hand. Although functional in the short term, it quickly becomes cumbersome when modifications are made, files are added, and so on. Thus the existence of EZQRC!

Installation
-----
1.  Download EZQRC onto your computer. There are two ways to do this. The first is use Git to clone the source from GitHub. If you do not have Git setup, then simply navigate https://github.com/winstonlin/ezqrc/ and click the ZIP button to download a ZIP file onto your computer.
2.  Make sure that you have Python installed.
3.  Make sure that you have PyQt installed for the version of Python that you will be using.
4.  Run generator.pyw or generator33.pyw to start the application!

generator.pyw vs generator33.pyw
-----
**generator.pyw** is meant to be used with Python 2.7.x

**generator33.pyw** is meant to be used with Python 3.3.x

Usage Instructions
-----
1.  Select the root path for your resources. EZQRC will scan recursively through the folders in search of all resources.
2.  Select the path to pyrcc4.exe. The default path given may not be correct!
3.  Click on Generate QRC to generate the Python module. It will output the resource file into the same folder as the location of the script.
4.  Click on Save Config Changes to save your configuration parameters so that they are the same the next time you load the application.
