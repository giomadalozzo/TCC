from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
import win32com.client
import sys

import GUI

class MyFileBrowser(GUI.Ui_MainWindow, QtWidgets.QMainWindow):
    prj_path = ""
    version = ""
    manning = False
    flow = False
    normalDepth = False
    waterStage = False
    iterManning = 0
    iterFlow = 0
    iterNormalDepth = 0
    iterWaterStage = 0

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
            self.manning = True
        if self.checkBox_2.isChecked():
            print("Vazão")
            self.flow = True
        if self.checkBox_3.isChecked():
            print("WS")
            self.waterStage = True
        if self.checkBox_4.isChecked():
            print("Normal depth")
            self.normalDepth = True

        if self.normalDepth or self.waterStage or self.flow or self.manning:
            return True
        else:
            self.label_5.setText("VOCÊ ESQUECEU DE MARCAR OS \nPARÂMETROS DA ANÁLISE!")
            myFont=QtGui.QFont()
            myFont.setBold(True)
            self.label_5.setFont(myFont)
            self.label_5.setStyleSheet("color: red")
            return False

        

    def checkIterations(self):
        self.iterFlow = self.spinBox.value()
        self.iterManning = self.spinBox_2.value()
        self.iterNormalDepth = self.spinBox_3.value()
        self.iterWaterStage = self.spinBox_4.value()

        simulations = []
        iters = []

        if self.manning:
            simulations.append("Manning")
            if self.iterManning != 0:
                print(self.spinBox.value())
                iters.append("Manning")
        if self.flow:
            simulations.append("Flow")
            if self.iterFlow != 0:
                print(self.spinBox_2.value())
                iters.append("Flow")
        if self.normalDepth:
            simulations.append("NormalDepth")
            if self.iterNormalDepth != 0:
                print(self.spinBox_3.value())
                iters.append("NormalDepth")
        if self.waterStage:
            simulations.append("WaterStage")
            if self.iterWaterStage != 0:
                print(self.spinBox_4.value())
                iters.append("WaterStage")
        
        if simulations == iters:
            return True
        else:
            self.label_5.setText("VOCÊ ESQUECEU DE ESCOLHER O NÚMERO DE ITERAÇÕES!")
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
            return True
            

    def checks(self):
        if self.checkPrjFile() and self.checkAnalysis() and self.checkVersion() and self.checkIterations():
            self.inputsCorrects()
            app.processEvents()
            self.startController()
        else:
            print("erro")
        
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