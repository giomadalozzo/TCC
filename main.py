from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
import win32com.client
import sys

import GUI

class MyFileBrowser(GUI.Ui_MainWindow, QtWidgets.QMainWindow):
    prj_path = ""
    version = ""
    def __init__(self):
        super(MyFileBrowser, self).__init__()
        self.setupUi(self)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.populate()
        self.pushButton.clicked.connect(self.checks)
        

    def populate(self):
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setSortingEnabled(True)
        self.treeView.setColumnWidth(0, 260)
        self.treeView.setColumnWidth(1, 50)
        self.treeView.setColumnWidth(2, 100)
        self.treeView.setColumnWidth(3, 100)
        self.treeView.clicked.connect(self.openFile)
        
        
    def openFile(self):
        index = self.treeView.currentIndex()
        self.prj_path = self.model.filePath(index)

    def checkVersion(self):
        if self.radioButton.isChecked():
            self.version = "501"
            return True
        elif self.radioButton_2.isChecked():
            #RC = win32com.client.Dispatch("RAS503.HECRASCONTROLLER")
            print("503")
            self.version = "503"
            return True
        elif self.radioButton_3.isChecked():
            #RC = win32com.client.Dispatch("RAS505.HECRASCONTROLLER")
            print("505")
            self.version = "505"
            return True
        elif self.radioButton_4.isChecked():
            #RC = win32com.client.Dispatch("RAS506.HECRASCONTROLLER")
            print("506")
            self.version = "506"
            return True
        elif self.radioButton_5.isChecked():
            #RC = win32com.client.Dispatch("RAS507.HECRASCONTROLLER")
            print("507")
            self.version = "507"
            return True
        else:
            #RC = win32com.client.Dispatch("RAS507.HECRASCONTROLLER")
            self.label_5.setText("VOCÊ ESQUECEU DE MARCAR A \nVERSÃO DO SEU HEC-RAS!")
            myFont=QtGui.QFont()
            myFont.setBold(True)
            self.label_5.setFont(myFont)
            self.label_5.setStyleSheet("color: red")
            return False

    def checkAnalysis(self):
        if self.checkBox.isChecked():
            print("Manning")
            return True
            print(self.prj_path)
        elif self.checkBox_2.isChecked():
            print("Vazão")
            return True
        elif self.checkBox_3.isChecked():
            print("WS")
            return True
        elif self.checkBox_4.isChecked():
            print("Normal depth")
            return True
        else:
            #RC = win32com.client.Dispatch("RAS507.HECRASCONTROLLER")
            self.label_5.setText("VOCÊ ESQUECEU DE MARCAR OS \nPARÂMETROS DA ANÁLISE!")
            myFont=QtGui.QFont()
            myFont.setBold(True)
            self.label_5.setFont(myFont)
            self.label_5.setStyleSheet("color: red")
            return False

    def checkIterations(self):
        if self.spinBox.value() != 0:
            print(self.spinBox.value())
            return True
        else:
            self.label_5.setText("VOCÊ ESQUECEU DE MARCAR O \nNÚMERO DE ITERAÇÕES!")
            myFont=QtGui.QFont()
            myFont.setBold(True)
            self.label_5.setFont(myFont)
            self.label_5.setStyleSheet("color: red")
            return False
            

    def checkPrjFile(self):
        if self.prj_path == "":
            self.label_5.setText("VOCÊ ESQUECEU DE SELECIONAR O \nARQUIVO PRJ!")
            myFont=QtGui.QFont()
            myFont.setBold(True)
            self.label_5.setFont(myFont)
            self.label_5.setStyleSheet("color: red")
            return False
        else:
            print("boa prj")
            return True
            

    def checks(self):
        if self.checkPrjFile() and self.checkAnalysis() and self.checkVersion() and self.checkIterations():
            self.inputsCorrects()
            app.processEvents()
            self.startController()
        else:
            print("erro no check")
        
    def inputsCorrects(self):
        self.label_5.setText("EXECUTANDO...AGUARDE!")
        myFont=QtGui.QFont('Times', 20)
        myFont.setBold(True)
        self.label_5.setFont(myFont)
        self.label_5.setStyleSheet("color: green")
        self.label_5.show()

    def startController(self):
        nmsg = None
        msg = None
        string = "RAS" + self.version + ".HECRASCONTROLLER"
        RC = win32com.client.Dispatch(string)
        RC.Project_Open(self.prj_path)
        RC.Compute_CurrentPlan(nmsg,msg)
        RC.Project_Close()
        RC.QuitRas()
    



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    fb = MyFileBrowser()
    fb.show()
    app.exec_()