from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
import win32com.client
import sys
import os

import GUI

class Project(object):
    def __init__(self, nodes, reaches, rivers, leftMannings, channelMannings, rightMannings, RC, planFile, geometryFile):
        self.nodes = nodes
        self.reaches = reaches
        self.rivers = rivers
        self.leftMannings = leftMannings
        self.channelMannings = channelMannings
        self.rightMannings = rightMannings
        self.planFile = planFile
        self.geometryFile = geometryFile
        self.RC = RC
        self.manningsModified = []

class Interface(GUI.Ui_MainWindow, QtWidgets.QMainWindow):
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
    limitsManning = [0,0]
    limitsFlow = [0,0]
    limitsNormalDepth = [0,0]
    limitsWaterStage = [0,0]
    project = Project("","","","","","","","","")

    def __init__(self):
        super(Interface, self).__init__()
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
        #index = self.treeView.currentIndex()
        #self.prj_path = self.model.filePath(index)
        self.prj_path = "F:\Hid. Computacional\ItajaiProjeto.prj"

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
            
    def checkLimits(self):
        if self.manning:
            if self.spinBox_8.value() == 0 or self.spinBox_7.value() == 0:
                self.label_5.setText("VOCÊ ESQUECEU DE DIGITAR OS \nLIMITES DE PERTURBAÇÃO DO PARÂMETRO!")
                myFont=QtGui.QFont()
                myFont.setBold(True)
                self.label_5.setFont(myFont)
                self.label_5.setStyleSheet("color: red")
                return False
            else:
                self.limitsManning = [self.spinBox_8.value(),self.spinBox_7.value()]
                return True
        if self.flow:
            if self.spinBox_5.value() == 0 or self.spinBox_6.value() == 0:
                self.label_5.setText("VOCÊ ESQUECEU DE DIGITAR OS \nLIMITES DE PERTURBAÇÃO DO PARÂMETRO!")
                myFont=QtGui.QFont()
                myFont.setBold(True)
                self.label_5.setFont(myFont)
                self.label_5.setStyleSheet("color: red")
                return False
            else:
                self.limitsFlow = [self.spinBox_5.value(),self.spinBox_6.value()]
                return True
        if self.normalDepth:
            if self.spinBox_10.value() == 0 or self.spinBox_9.value() == 0:
                self.label_5.setText("VOCÊ ESQUECEU DE DIGITAR OS \nLIMITES DE PERTURBAÇÃO DO PARÂMETRO!")
                myFont=QtGui.QFont()
                myFont.setBold(True)
                self.label_5.setFont(myFont)
                self.label_5.setStyleSheet("color: red")
                return False
            else:
                self.normalDepth = [self.spinBox_10.value(),self.spinBox_9.value()]
                return True
        if self.waterStage:
            if self.spinBox_12.value() == 0 or self.spinBox_11.value() == 0:
                self.label_5.setText("VOCÊ ESQUECEU DE DIGITAR OS \nLIMITES DE PERTURBAÇÃO DO PARÂMETRO!")
                myFont=QtGui.QFont()
                myFont.setBold(True)
                self.label_5.setFont(myFont)
                self.label_5.setStyleSheet("color: red")
                return False
            else:
                self.waterStage = [self.spinBox_12.value(),self.spinBox_11.value()]
                return True

    def checks(self):
        if self.checkPrjFile() and self.checkAnalysis() and self.checkVersion() and self.checkIterations() and self.checkLimits():
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
        string = "RAS" + self.version + ".HECRASCONTROLLER"
        self.project.RC = win32com.client.Dispatch(string)
        self.project.RC.ShowRAS()
        self.project.RC.Project_Open(self.prj_path)
        self.getFiles()

        if self.manning:
            self.monteCarloManning()


        print("rodando")
        #self.project.RC.Project_Close()
        #self.project.RC.QuitRas()
        print("quitou")

    def monteCarloManning(self):
        self.getMannings()
        self.project.manningsModified = self.incrementFactorMultiply(self.limitsManning[1],self.limitsManning[0], self.project.channelMannings, self.iterManning)
        for z in range (0, self.iterManning+1):
            self.changeMannings(z)
            Simulation = self.project.RC.Compute_CurrentPlan(None,None,True)


    def incrementFactorMultiply(self, percentageMax, percentageMin, parameters, discretization):
        parametersModified = []
        listParam2 = []
        for x in range(0, len(parameters)):
            listParam = []
            for y in range(0, len(parameters[x])):
                factorMax = float(parameters[x][y]) * (1+(percentageMax/100))
                factorMin = float(parameters[x][y]) * (1+(-percentageMin/100))

                increment = (factorMax-factorMin)/(discretization-1)
                for z in range(0, discretization):
                    listParam2.append(factorMin+(increment*z))
                listParam2.append(float(parameters[x][y]))
                listParam2.sort()
                listParam.append(listParam2)
                listParam2 = []
            parametersModified.append(listParam)
        print("Modified")
        print(parametersModified)
        return parametersModified

    def extractResults(self):
        #entrada -> river ID (int), reach ID (int), node ID (int), param para obras hidráulicas (int) (dá pra usar None), profile ID (int), var ID (int) (WS = 2, vazão = 9, velocidade = 23)
        #saída -> resultado para dada seção
        RC.Output_NodeOutput()

    def changeMannings(self, z):
        #entrada -> river (string), reach (string), node(string), Manning left bank(float), Manning channel(float), Manning right bank(float)
        
        for x in range(0,len(self.project.rivers)):
            for y in range(0, len(self.project.nodes[x])):
                self.project.RC.Geometry_SetMann_LChR(self.project.rivers[x][0], self.project.reaches[x][0], self.project.nodes[x][y], self.project.leftMannings[x][y], self.project.manningsModified[x][y][z], self.project.rightMannings[x][y])
        print("River {} Reach {} Node {} L {} C {} R {}".format(self.project.rivers[x][0], self.project.reaches[x][0], self.project.nodes[x][y], self.project.leftMannings[x][y], self.project.manningsModified[x][y][z], self.project.rightMannings[x][y]))
                   

    def getFiles(self):
        filename = self.project.RC.CurrentPlanFile()
        geometryFile = ""
        planFile = ""
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if "Geom File=" in line:
                    geometryFile = line.split("=")[1].replace("\n", "")
                if "Flow File=" in line:
                    planFile = line.split("=")[1].replace("\n", "")
                if geometryFile != "" and planFile != "":
                    break

        path = self.prj_path.replace(self.prj_path.split("\\")[-1], "")

        for file in os.listdir(path):
            if file.endswith(planFile):
                self.project.planFile = os.path.join(path, file)
            elif file.endswith(geometryFile):
                self.project.geometryFile = os.path.join(path, file)
        
    def getMannings(self):
        nodes = []
        leftMannings = []
        channelMannings = []
        rightMannings = []
        river = []
        reach = []

        nodes_aux = []
        leftMannings_aux = []
        channelMannings_aux = []
        rightMannings_aux = []
        river_aux = []
        reach_aux = []

        with open(self.project.geometryFile,'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines)):
                line = lines[i]
                if "River Reach=" in line and len(river_aux)>0:
                    reach.append(reach_aux)
                    river.append(river_aux)
                    nodes.append(nodes_aux)
                    leftMannings.append(leftMannings_aux)
                    channelMannings.append(channelMannings_aux)
                    rightMannings.append(rightMannings_aux)

                    nodes_aux = []
                    leftMannings_aux = []
                    channelMannings_aux = []
                    rightMannings_aux = []
                    river_aux = []
                    reach_aux = []
                if "River Reach=" in line:
                    if "CM River Reach=" not in line:
                        reach_aux.append(line.split(",")[1].replace("\n",""))
                        river_aux.append(line.split(",")[0].split("=")[1])
                elif "Type RM Length L Ch R" in line:
                    nodes_aux.append(line.split("=")[1].split(",")[1])
                elif "#Mann" in line:
                    n=8
                    line_aux = lines[i+1]
                    listing = [line_aux[u:u+n] for u in range(0, len(line_aux), n)]
                    leftMannings_aux.append(listing[1].strip())
                    channelMannings_aux.append(listing[4].strip())
                    rightMannings_aux.append(listing[7].strip())

            if reach_aux != []:
                reach.append(reach_aux)
                river.append(river_aux)
                nodes.append(nodes_aux)
                leftMannings.append(leftMannings_aux)
                channelMannings.append(channelMannings_aux)
                rightMannings.append(rightMannings_aux)

        self.project.rivers = river
        self.project.reaches = reach
        self.project.nodes = nodes
        self.project.leftMannings = leftMannings
        self.project.channelMannings = channelMannings
        self.project.rightMannings = rightMannings
        print("river")
        print(river)
        print("reach")
        print(reach)
        print("Nodes")
        print(nodes)
        print("left manning")
        print(leftMannings)
        print("channel manning")
        print(channelMannings)
        print("right manning")
        print(rightMannings)       

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    fb = Interface()
    fb.show()
    app.exec_()