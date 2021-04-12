from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
import win32com.client
import sys

import GUI

class Project(object):
    def __init__(self, nodes, reaches, rivers, RC):
        self.nodes = nodes
        self.reaches = reaches
        self.rivers = rivers
        self.RC = RC
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
    project = Project("","","","")

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
        string = "RAS" + self.version + ".HECRASCONTROLLER"
        self.project.RC = win32com.client.Dispatch(string)
        self.project.RC.ShowRAS()
        self.project.RC.Project_Open(self.prj_path)
        
        self.gettingInfo()
        self.changeMannings()

        Simulation = self.project.RC.Compute_CurrentPlan(None,None,True)


        print("rodando")
        #self.project.RC.Project_Close()
        #self.project.RC.QuitRas()
        print("quitou")

    def incrementFactor(self):
        percentageMax = 50
        percentageMin = -50
        discretization = 10
        initialParam = 10

        factorMax = initialParam * (1+(percentageMax/100))
        factorMin = initialParam * (1+(percentageMin/100))

        increment = (factorMax-factorMin)/(discretization-1)

        listParam = []
        for x in range(0, discretization):
            listParam.append(factorMin+(increment*x))

        #np.random.uniforme(min,max)
        
        listParam.append(initialParam)
        listParam.sort()
        print(listParam)

    def gettingInfo(self):
        #saída -> num de rios (int), nome dos rios do modelo (string)
        aux = self.project.RC.Geometry_GetRivers()[1]
        if aux != None:
            aux = list(aux)
        river = aux

        print("Rios:")
        print(river)

        reach = []
        for x in range(0,len(river)):
            #entrada -> river ID para achar os trechos(int)
            #saída -> num de trechos do rio (int), nome dos trechos do rio (string)
            aux = self.project.RC.Geometry_GetReaches(x+1)[2]
            if aux != None:
                aux = list(aux)
            reach.append(aux)

        print("Reaches:")
        print(reach)

        #entrada -> river ID (int) e reach ID (int) para achar os nodes
        #saída -> num de nós (int), nome dos nós do trecho (string), tipo do nó (int) - caso tenha ponte e estruturas são considerados nós com um código
        nodes = []
        
        for x in range(0,len(river)):
            nodes_aux = []
            for y in range(0, len(reach[x])):
                aux = self.project.RC.Geometry_GetNodes(x+1,y+1)[3]
                if aux != None:
                    aux = list(aux)
                    nodes_aux.append(aux)
                else:
                    aux2 = []
                    aux2.append(aux)
                    nodes_aux.append(aux2)
            nodes.append(nodes_aux)

        print("Nodes:")
        print(nodes)

        self.project.nodes = nodes
        self.project.reaches = reach
        self.project.rivers = river

    def extractResults(self):
        #entrada -> river ID (int), reach ID (int), node ID (int), param para obras hidráulicas (int) (dá pra usar None), profile ID (int), var ID (int) (WS = 2, vazão = 9, velocidade = 23)
        #saída -> resultado para dada seção
        RC.Output_NodeOutput()

    def changeMannings(self):
        #entrada -> river (string), reach (string), node(string), Manning left bank(float), Manning channel(float), Manning right bank(float)
        #botar None para não mudar o manning (testar)
        for x in range(0,len(self.project.rivers)):
            for y in range(0,len(self.project.reaches[x])):
                for z in range(0, len(self.project.nodes[x][y])):
                    self.project.RC.Geometry_SetMann_LChR(self.project.rivers[x], self.project.reaches[x][y], self.project.nodes[x][y][z], None, 0.02112, None)
                    print("River {} Reach {} Node {}".format(self.project.rivers[x], self.project.reaches[x][y], self.project.nodes[x][y][z]))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    fb = Interface()
    fb.show()
    app.exec_()