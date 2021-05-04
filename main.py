from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
import win32com.client
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from shutil import copyfile
import time
import datetime
import csv

import GUI

class Project(object):
    def __init__(self, nodes, reaches, rivers, centerLengths,leftMannings, channelMannings, rightMannings, RC, planFile, geometryFile):
        self.nodes = nodes
        self.reaches = reaches
        self.rivers = rivers
        self.centerLengths = centerLengths
        self.leftMannings = leftMannings
        self.channelMannings = channelMannings
        self.rightMannings = rightMannings
        self.planFile = planFile
        self.geometryFile = geometryFile
        self.RC = RC
        self.manningsModified = []
        self.resultsFlowManning = []
        self.resultsWSManning = []
        self.resultsVManning = []
        self.inputFlows = []
        self.modifiedFlows = []
        self.inputNormalDepth = []
        self.modifiedNormalDepth = []
        self.inputStages = []
        self.modifiedStages = []

        self.dfResultsManning = []
        self.dfResultsFlows = []
        self.dfResultsNormalDepth = []
        self.dfResultsStages = []
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
    incrementWaterStage = 0
    project = Project("","","","","","","","","","")
    start_time = ""
    pathResults = ""

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
        self.prj_path = "C:\\Users\\Giovanni\\Desktop\\Projetos GitHub\\TCC\\Arquivos HECRAS\\ItajaiProjeto.prj"

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
        if self.normalDepth:
            if self.spinBox_10.value() == 0 or self.spinBox_9.value() == 0:
                self.label_5.setText("VOCÊ ESQUECEU DE DIGITAR OS \nLIMITES DE PERTURBAÇÃO DO PARÂMETRO!")
                myFont=QtGui.QFont()
                myFont.setBold(True)
                self.label_5.setFont(myFont)
                self.label_5.setStyleSheet("color: red")
                return False
            else:
                self.limitsNormalDepth = [self.spinBox_10.value(),self.spinBox_9.value()]
        if self.waterStage:
            if self.doubleSpinBox.value() == 0.00:
                self.label_5.setText("VOCÊ ESQUECEU DE DIGITAR OS \nLIMITES DE PERTURBAÇÃO DO PARÂMETRO!")
                myFont=QtGui.QFont()
                myFont.setBold(True)
                self.label_5.setFont(myFont)
                self.label_5.setStyleSheet("color: red")
                return False
            else:
                self.incrementWaterStage = self.doubleSpinBox.value()

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
        self.start_time = time.time()
        myFont=QtGui.QFont('Times', 20)
        myFont.setBold(True)
        self.label_5.setFont(myFont)
        self.label_5.setStyleSheet("color: green")
        self.label_5.show()

    def startController(self):
        string = "RAS" + self.version + ".HECRASCONTROLLER"
        print(self.prj_path)
        self.project.RC = win32com.client.Dispatch(string)
        self.project.RC.ShowRAS()
        self.project.RC.Project_Open(self.prj_path)
        self.getFiles()
        self.createBackup()
        self.project.RC.Project_Open(self.prj_path)
        print("Running")

        actualPath = os.path.dirname(os.path.abspath(__file__))
        directory = "Results Files"
        pathResultsGeneral = os.path.join(actualPath, directory)
        if os.path.isdir(pathResultsGeneral) is False:
            os.mkdir(pathResultsGeneral)

        now = datetime.datetime.now()
        dt_string = now.strftime("%d%m%Y_%H%M%S")

        directory2 = dt_string
        self.pathResults = os.path.join(pathResultsGeneral, directory2)
        if os.path.isdir(self.pathResults) is False:
            os.mkdir(self.pathResults)

        if self.manning:
            self.monteCarloManning()
            RC=self.project.RC
            plan = self.project.planFile
            geom = self.project.geometryFile
            self.project = Project("","","","","","","", RC, plan, geom)

        if self.flow:
            self.monteCarloFlow()
            RC=self.project.RC
            plan = self.project.planFile
            geom = self.project.geometryFile
            self.project = Project("","","","","","","", RC, plan, geom)

        if self.normalDepth:
            self.monteCarloNormalDepth()
            RC=self.project.RC
            plan = self.project.planFile
            geom = self.project.geometryFile
            self.project = Project("","","","","","","", RC, plan, geom)

        if self.waterStage:
            self.monteCarloStage()
            RC=self.project.RC
            plan = self.project.planFile
            geom = self.project.geometryFile
            self.project = Project("","","","","","","", RC, plan, geom)

        self.project.RC.Project_Close()
        self.project.RC.QuitRas()
        print("quitou")

        gapTime = time.time() - self.start_time
        executionTime = str(datetime.timedelta(seconds=gapTime)).split(".")[0]
        self.label_5.setText("PROCESSO FINALIZADO EM " + executionTime + " !")
        self.label_17.setText("Resultados na pasta: " + self.pathResults)
        myFont=QtGui.QFont('Times', 20)
        myFont.setBold(True)
        self.label_5.setFont(myFont)
        self.label_5.setStyleSheet("color: green")
        self.label_17.setStyleSheet("color: green")
        self.label_5.show()
        self.label_17.show()

    def monteCarloStage(self):
        self.getStages()
        self.project.modifiedStages = self.incrementFactorSum(self.iterWaterStage, self.iterWaterStage, self.project.inputStages, self.incrementWaterStage)
        iterations = (2*self.iterWaterStage)+1
        parameterInfo = []
        for x in range(-self.iterWaterStage, self.iterWaterStage+1):
            if x == 0:
                parameterInfo.append("Water Stage Original")
            else:
                actual = round(x*float(self.incrementWaterStage), 2)
                string = "Water Stage " + str(actual) + "m"
                parameterInfo.append(string)

        for z in range (0, iterations):
            self.changeStages(z)
            self.project.RC.Compute_CurrentPlan(None,None,True)
            df = self.extractResults(parameterInfo[z], "Water Stage")
            self.project.dfResultsStages.append(df)
        self.project.RC.Project_Close()
        self.updateFiles()
        #print(self.project.dfResultsStages)
        #print(len(self.project.dfResultsStages))
        self.resultSummary(self.project.dfResultsStages)
        self.project.RC.Project_Open(self.prj_path)


    def monteCarloManning(self):
        self.getMannings()
        self.project.manningsModified = self.incrementFactorMultiply(self.limitsManning[1],self.limitsManning[0], self.project.channelMannings, self.iterManning)
        
        modifiedValues = (self.iterManning)//2
        maxIncrement = self.limitsManning[1]/modifiedValues
        minIncrement = self.limitsManning[0]/modifiedValues

        parameterInfo = []
        #print(modifiedValues)
        for x in range(-modifiedValues, modifiedValues+1):
            if x == 0:
                parameterInfo.append("Manning Original")
            elif x<0:
                actual = round(x*float(minIncrement), 2)
                string = "Manning " + str(actual) + "%"
                parameterInfo.append(string)
            else:
                actual = round(x*float(maxIncrement), 2)
                string = "Manning " + str(actual) + "%"
                parameterInfo.append(string)

        #print(parameterInfo)
        for z in range (0, self.iterManning+1):
            self.changeMannings(z)
            self.project.RC.Compute_CurrentPlan(None,None,True)
            df = self.extractResults(parameterInfo[z], "Manning")
            #print(df)
            self.project.dfResultsManning.append(df)
        self.project.RC.Project_Close()
        self.updateFiles()
        self.resultSummary(self.project.dfResultsManning)
        self.project.RC.Project_Open(self.prj_path)

    def monteCarloFlow(self):
        self.getFlows()
        self.project.modifiedFlows = self.incrementFactorMultiply(self.limitsFlow[1],self.limitsFlow[0], self.project.inputFlows, self.iterFlow)
        modifiedValues = (self.iterFlow)//2
        maxIncrement = self.limitsFlow[1]/modifiedValues
        minIncrement = self.limitsFlow[0]/modifiedValues

        parameterInfo = []
        #print(modifiedValues)
        for x in range(-modifiedValues, modifiedValues+1):
            if x == 0:
                parameterInfo.append("Vazão Original")
            elif x<0:
                actual = round(x*float(minIncrement), 2)
                string = "Vazão " + str(actual) + "%"
                parameterInfo.append(string)
            else:
                actual = round(x*float(maxIncrement), 2)
                string = "Vazão " + str(actual) + "%"
                parameterInfo.append(string)

        #print(parameterInfo)
        for z in range (0, self.iterFlow+1):
            self.changeFlows(z)
            self.project.RC.Project_Close()
            self.project.RC.Project_Open(self.prj_path)
            self.project.RC.Compute_CurrentPlan(None,None,True)
            df = self.extractResults(parameterInfo[z], "Vazão")
            self.project.dfResultsFlows.append(df)
        self.project.RC.Project_Close()
        self.updateFiles()
        self.resultSummary(self.project.dfResultsFlows)
        self.project.RC.Project_Open(self.prj_path)

    def monteCarloNormalDepth(self):
        self.getNormalDepth()
        self.project.modifiedNormalDepth = self.incrementFactorMultiply(self.limitsNormalDepth[1],self.limitsNormalDepth[0], self.project.inputNormalDepth, self.iterNormalDepth)
        modifiedValues = (self.iterNormalDepth)//2
        maxIncrement = self.limitsNormalDepth[1]/modifiedValues
        minIncrement = self.limitsNormalDepth[0]/modifiedValues

        parameterInfo = []
        #print(modifiedValues)
        for x in range(-modifiedValues, modifiedValues+1):
            if x == 0:
                parameterInfo.append("Normal Depth Original")
            elif x<0:
                actual = round(x*float(minIncrement), 2)
                string = "Normal Depth " + str(actual) + "%"
                parameterInfo.append(string)
            else:
                actual = round(x*float(maxIncrement), 2)
                string = "Normal Depth " + str(actual) + "%"
                parameterInfo.append(string)

        #print(parameterInfo)
        for z in range (0, self.iterNormalDepth+1):
            self.changeNormalDepth(z)
            self.project.RC.Project_Close()
            self.project.RC.Project_Open(self.prj_path)
            self.project.RC.Compute_CurrentPlan(None,None,True)
            df = self.extractResults(parameterInfo[z], "Normal Depth")
            self.project.dfResultsNormalDepth.append(df)
        self.project.RC.Project_Close()
        self.updateFiles()
        self.resultSummary(self.project.dfResultsNormalDepth)
        self.project.RC.Project_Open(self.prj_path)

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
        #print("Modified")
        #print(parametersModified)
        return parametersModified

    def incrementFactorSum(self, iterationsMax, iterationsMin, parameters, increment):
        #print(increment)
        #print(iterationsMax)
        parametersModified = []
        listParam2 = []
        for x in range(0, len(parameters)):
            listParam = []
            for y in range(0, len(parameters[x])):
                [listParam2.append(float(parameters[x][y])+int(n)*float(increment)) for n in range(-iterationsMin, iterationsMax+1)]
                listParam.append(listParam2)
                listParam2 = []

            parametersModified.append(listParam)

        #print(parametersModified)

        return parametersModified

    def getStages(self):
        #print(self.project.planFile)
        nodes = []
        river = []
        reach = []
        centerLengths = []

        nodes_aux = []
        river_aux = []
        reach_aux = []
        centerLengths_aux = []

        with open(self.project.geometryFile,'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines)):
                line = lines[i]
                if "River Reach=" in line and len(river_aux)>0:
                    reach.append(reach_aux)
                    river.append(river_aux)
                    nodes.append(nodes_aux)
                    centerLengths.append(centerLengths_aux)

                    nodes_aux = []
                    river_aux = []
                    reach_aux = []
                    centerLengths_aux = []
                if "River Reach=" in line:
                    if "CM River Reach=" not in line:
                        reach_aux.append(line.split(",")[1].replace("\n",""))
                        river_aux.append(line.split(",")[0].split("=")[1])
                elif "Type RM Length L Ch R" in line:
                    nodes_aux.append(line.split("=")[1].split(",")[1])
                    centerLengths_aux.append(line.split("=")[1].split(",")[3])

            if reach_aux != []:
                reach.append(reach_aux)
                river.append(river_aux)
                nodes.append(nodes_aux)
                centerLengths.append(centerLengths_aux)

        self.project.rivers = river
        self.project.reaches = reach
        self.project.nodes = nodes
        sumLengths=0

        for x in range(0, len(centerLengths)):
            for y in range(0, len(centerLengths[x])):
                if centerLengths[x][y] == '':
                    centerLengths[x][y] = 0
                sumLengths+=float(centerLengths[x][y])

        for x in range(0, len(centerLengths)):
            for y in range(0, len(centerLengths[x])):
                if y==0:
                    centerLengths[x][y] = sumLengths
                else:
                    centerLengths[x][y] = float(centerLengths[x][y-1]) - float(centerLengths[x][y])

        self.project.centerLengths = centerLengths
        start = False
        with open(self.project.planFile,'r') as file:
            lines = file.readlines()
            for line in lines:
                if "Stage Hydrograph=" in line:
                    start = True
                if "DSS Path=" in line:
                    start = False
                if start and "Stage Hydrograph=" not in line:
                    stagesLine = [line[index : index + 8] for index in range(0, len(line), 8)]
                    stagesLine = [stage.replace(" ", "") for stage in stagesLine]
                    stagesLine.remove("\n")
                    self.project.inputStages.append(stagesLine)

        #print(self.project.inputStages)

    def extractResults(self, iteration, parameter):
        #entrada -> river ID (int), reach ID (int), node ID (int), param para obras hidráulicas (int) (dá pra usar None), profile ID (int), var ID (int) (WS = 2, vazão = 9, velocidade = 23)
        #saída -> resultado para dada seção
        resultsWS = []
        resultsV = []
        resultsFlow = []
        riverIteration = []
        reachIteration = []
        parameterList = []
        iterations = []
        lengths = []
        
        for x in range(0,len(self.project.rivers)):
            for y in range(0, len(self.project.nodes[x])):
                resultsWS.append(self.project.RC.Output_NodeOutput(x+1, x+1, y+1, None, 1, 2)[0])
                resultsV.append(self.project.RC.Output_NodeOutput(x+1, x+1, y+1, None, 1, 23)[0])
                resultsFlow.append(self.project.RC.Output_NodeOutput(x+1, x+1, y+1, None, 1, 9)[0])
                riverIteration.append(self.project.rivers[x][0])
                reachIteration.append(self.project.reaches[x][0])
                if y == len(self.project.nodes[x])-1:
                    self.project.centerLengths[x][y] = 0.0
                lengths.append(self.project.centerLengths[x][y])
                parameterList.append(parameter)
                iterations.append(iteration)

        output = {'Cross Sections': self.project.nodes[x],'River': riverIteration,'Reach': reachIteration, 'Parameter': parameterList, 'Iteration':iterations, 'Center Length(m)':lengths,'WSE(m)':resultsWS, 'Flow(m3/s)':resultsFlow, 'V (m/s)':resultsV}
        df_output = pd.DataFrame(output)
        df_output.set_index('Cross Sections')
#
        #df_output.plot(x = 'Cross Sections', y = 'Flow(m3/s)', kind = 'scatter')
        #plt.tick_params(axis = "x", which = "both", bottom = False, top = False)
        #plt.show()
#
        #df_output.plot(x = 'Cross Sections', y = 'WSE(m)', kind = 'scatter')
        #plt.tick_params(axis = "x", which = "both", bottom = False, top = False)
        #plt.show()
#
        #df_output.plot(x = 'Cross Sections', y = 'V (m/s)', kind = 'scatter')
        #plt.tick_params(axis = "x", which = "both", bottom = False, top = False)
        #plt.show()
        #print("finalizou")

        return df_output

    def changeMannings(self, z):
        #entrada -> river (string), reach (string), node(string), Manning left bank(float), Manning channel(float), Manning right bank(float)
        
        for x in range(0,len(self.project.rivers)):
            for y in range(0, len(self.project.nodes[x])):
                self.project.RC.Geometry_SetMann_LChR(self.project.rivers[x][0], self.project.reaches[x][0], self.project.nodes[x][y], self.project.leftMannings[x][y], self.project.manningsModified[x][y][z], self.project.rightMannings[x][y])
        print("River {} Reach {} Node {} L {} C {} R {}".format(self.project.rivers[x][0], self.project.reaches[x][0], self.project.nodes[x][y], self.project.leftMannings[x][y], self.project.manningsModified[x][y][z], self.project.rightMannings[x][y]))
                   
    def changeNormalDepth(self, z):
        for x in range(0, len(self.project.modifiedNormalDepth)):
            for y in range(0, len(self.project.modifiedNormalDepth[x])):
                newValue = self.project.modifiedNormalDepth[x][y][z]

        with open(self.project.planFile,'r') as file:
            lines = file.readlines()
            for line in lines:
                if "Friction Slope=" in line:
                    part1= line.split("=")[0]
                    part2= line.split("=")[1].split(",")[1]
                    newLine = part1+"="+str(newValue)+","+part2
                    lines = [newLine if string==line else string for string in lines]
        
        with open(self.project.planFile,'w') as file:
            file.writelines(lines)

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
        centerLengths = []

        nodes_aux = []
        leftMannings_aux = []
        channelMannings_aux = []
        rightMannings_aux = []
        river_aux = []
        reach_aux = []
        centerLengths_aux = []

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
                    centerLengths.append(centerLengths_aux)

                    nodes_aux = []
                    leftMannings_aux = []
                    channelMannings_aux = []
                    rightMannings_aux = []
                    river_aux = []
                    reach_aux = []
                    centerLengths_aux = []
                if "River Reach=" in line:
                    if "CM River Reach=" not in line:
                        reach_aux.append(line.split(",")[1].replace("\n",""))
                        river_aux.append(line.split(",")[0].split("=")[1])
                elif "Type RM Length L Ch R" in line:
                    nodes_aux.append(line.split("=")[1].split(",")[1])
                    centerLengths_aux.append(line.split("=")[1].split(",")[3])
                    #print(centerLengths_aux)
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
                centerLengths.append(centerLengths_aux)

        self.project.rivers = river
        self.project.reaches = reach
        self.project.nodes = nodes
        self.project.leftMannings = leftMannings
        self.project.channelMannings = channelMannings
        self.project.rightMannings = rightMannings
        
        sumLengths=0

        for x in range(0, len(centerLengths)):
            for y in range(0, len(centerLengths[x])):
                if centerLengths[x][y] == '':
                    centerLengths[x][y] = 0
                sumLengths+=float(centerLengths[x][y])

        for x in range(0, len(centerLengths)):
            for y in range(0, len(centerLengths[x])):
                if y==0:
                    centerLengths[x][y] = sumLengths
                else:
                    centerLengths[x][y] = float(centerLengths[x][y-1]) - float(centerLengths[x][y])

        self.project.centerLengths = centerLengths
        #print("river")
        #print(river)
        #print("reach")
        #print(reach)
        #print("Nodes")
        #print(nodes)
        #print("left manning")
        #print(leftMannings)
        #print("channel manning")
        #print(channelMannings)
        #print("right manning")
        #print(rightMannings)
        print(self.project.centerLengths)

    def getFlows(self):
        nodes = []
        river = []
        reach = []
        centerLengths = []

        nodes_aux = []
        river_aux = []
        reach_aux = []
        centerLengths_aux = []

        with open(self.project.geometryFile,'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines)):
                line = lines[i]
                if "River Reach=" in line and len(river_aux)>0:
                    reach.append(reach_aux)
                    river.append(river_aux)
                    nodes.append(nodes_aux)
                    centerLengths.append(centerLengths_aux)

                    nodes_aux = []
                    river_aux = []
                    reach_aux = []
                    centerLengths_aux = []
                if "River Reach=" in line:
                    if "CM River Reach=" not in line:
                        reach_aux.append(line.split(",")[1].replace("\n",""))
                        river_aux.append(line.split(",")[0].split("=")[1])
                elif "Type RM Length L Ch R" in line:
                    nodes_aux.append(line.split("=")[1].split(",")[1])
                    centerLengths_aux.append(line.split("=")[1].split(",")[3])

            if reach_aux != []:
                reach.append(reach_aux)
                river.append(river_aux)
                nodes.append(nodes_aux)
                centerLengths.append(centerLengths_aux)

        self.project.rivers = river
        self.project.reaches = reach
        self.project.nodes = nodes
        sumLengths=0

        for x in range(0, len(centerLengths)):
            for y in range(0, len(centerLengths[x])):
                if centerLengths[x][y] == '':
                    centerLengths[x][y] = 0
                sumLengths+=float(centerLengths[x][y])

        for x in range(0, len(centerLengths)):
            for y in range(0, len(centerLengths[x])):
                if y==0:
                    centerLengths[x][y] = sumLengths
                else:
                    centerLengths[x][y] = float(centerLengths[x][y-1]) - float(centerLengths[x][y])

        self.project.centerLengths = centerLengths
        start = False
        isInputFlow = True
        with open(self.project.planFile,'r') as file:
            lines = file.readlines()
            for line in lines:
                if "Flow Hydrograph=" in line:
                    start = True
                if "DSS Path=" in line:
                    start = False
                    isInputFlow = False
                if start and "Flow Hydrograph=" not in line and isInputFlow:
                    listFlowLine = line.split(" ")
                    for x in range(0,len(listFlowLine)):
                        if "\n" in listFlowLine[x]:
                            listFlowLine[x] = listFlowLine[x].replace("\n","")
                    filter_object = filter(lambda x: x != "", listFlowLine)
                    listFlowLine = list(filter_object)
                    self.project.inputFlows.append(listFlowLine)
                    listFlowLine = []

        #print(self.project.inputFlows)

    def getNormalDepth(self):
        nodes = []
        river = []
        reach = []
        centerLengths = []

        nodes_aux = []
        river_aux = []
        reach_aux = []
        centerLengths_aux = []

        with open(self.project.geometryFile,'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines)):
                line = lines[i]
                if "River Reach=" in line and len(river_aux)>0:
                    reach.append(reach_aux)
                    river.append(river_aux)
                    nodes.append(nodes_aux)
                    centerLengths.append(centerLengths_aux)

                    nodes_aux = []
                    river_aux = []
                    reach_aux = []
                    centerLengths_aux = []
                if "River Reach=" in line:
                    if "CM River Reach=" not in line:
                        reach_aux.append(line.split(",")[1].replace("\n",""))
                        river_aux.append(line.split(",")[0].split("=")[1])
                elif "Type RM Length L Ch R" in line:
                    nodes_aux.append(line.split("=")[1].split(",")[1])
                    centerLengths_aux.append(line.split("=")[1].split(",")[3])

            if reach_aux != []:
                reach.append(reach_aux)
                river.append(river_aux)
                nodes.append(nodes_aux)
                centerLengths.append(centerLengths_aux)

        self.project.rivers = river
        self.project.reaches = reach
        self.project.nodes = nodes
        sumLengths=0

        for x in range(0, len(centerLengths)):
            for y in range(0, len(centerLengths[x])):
                if centerLengths[x][y] == '':
                    centerLengths[x][y] = 0
                sumLengths+=float(centerLengths[x][y])

        for x in range(0, len(centerLengths)):
            for y in range(0, len(centerLengths[x])):
                if y==0:
                    centerLengths[x][y] = sumLengths
                else:
                    centerLengths[x][y] = float(centerLengths[x][y-1]) - float(centerLengths[x][y])

        self.project.centerLengths = centerLengths

        listNormalDepth = []
        #print(self.project.planFile)
        with open(self.project.planFile,'r') as file:
            lines = file.readlines()
            for line in lines:
                if "Friction Slope=" in line:
                    listNormalDepth.append(float(line.split("=")[1].split(",")[0]))
                    self.project.inputNormalDepth.append(listNormalDepth)
                    break
        
        #print(self.project.inputNormalDepth)
    def changeFlows(self, z):
        newFlows = []
        for x in range(0, len(self.project.modifiedFlows)):
            flowsString = ""
            for y in range (0,len(self.project.modifiedFlows[x])):
                flow = str(self.project.modifiedFlows[x][y][z])
                if len(flow)<7:
                    for i in range(0, 7-len(flow)):
                        flow+="0"
                if len(flow)>7:
                    value = flow.split(".")[0]
                    gap =  7-len(value)
                    flow = round(float(flow),gap-1)
                    flow = str(flow)
                    while len(flow) < 7:
                        flow += "0"
                
                flowsString += " "+flow
            newFlows.append(flowsString+"\n")

        #print(newFlows)

        with open(self.project.planFile,'r') as file:
            lines = file.readlines()
            start = False
            x=0
            for line in lines:
                if "Flow Hydrograph=" in line:
                    start = True
                if "DSS Path=" in line:
                    start = False
                if start and "Flow Hydrograph=" not in line:
                    lines = [newFlows[x] if string==line else string for string in lines]
                    x+=1
        
        with open(self.project.planFile,'w') as file:
            file.writelines(lines)

    def changeStages(self, z):
        newStages = []
        for x in range(0, len(self.project.modifiedStages)):
            stagesString = ""
            for y in range (0,len(self.project.modifiedStages[x])):
                stage = str(self.project.modifiedStages[x][y][z])
                if len(stage)<7:
                    for i in range(0, 8-len(stage)):
                        stage+="0"
                if len(stage)>7:
                    value = stage.split(".")[0]
                    gap =  8-len(value)
                    stage = round(float(stage),gap-1)
                    stage = str(stage)
                    while len(stage) < 8:
                        stage += "0"
                
                stagesString += " "+stage
            newStages.append(stagesString+"\n")

        #print(newStages)

        with open(self.project.planFile,'r') as file:
            lines = file.readlines()
            start = False
            x=0
            for line in lines:
                if "Stage Hydrograph=" in line:
                    start = True
                if "DSS Path=" in line:
                    start = False
                if start and "Stage Hydrograph=" not in line:
                    lines = [newStages[x] if string==line else string for string in lines]
                    x+=1
        
        with open(self.project.planFile,'w') as file:
            file.writelines(lines)

    def createBackup(self):
        self.project.RC.Project_Close()

        actualPath = os.path.dirname(os.path.abspath(__file__))
        directory = "Backup Files"
        pathBackup = os.path.join(actualPath, directory)
        if os.path.isdir(pathBackup) is False:
            os.mkdir(pathBackup)
        planDestination = os.path.join(pathBackup,self.project.planFile.split('\\')[-1])
        geomDestination = os.path.join(pathBackup,self.project.geometryFile.split('\\')[-1])
        copyfile(self.project.planFile, planDestination)
        copyfile(self.project.geometryFile, geomDestination)

    def updateFiles(self):
        actualPath = os.path.dirname(os.path.abspath(__file__))
        directory = "Backup Files"
        pathBackup = os.path.join(actualPath, directory)
        planDestination = os.path.join(pathBackup,self.project.planFile.split('\\')[-1])
        geomDestination = os.path.join(pathBackup,self.project.geometryFile.split('\\')[-1])
        copyfile(planDestination, self.project.planFile)
        copyfile(geomDestination, self.project.geometryFile)

    def resultSummary(self, dfList):

        self.generateCSV(self.pathResults, dfList)

        fig = plt.figure()
        for frame in dfList:
            print(frame)
            subtitle = frame['Iteration'][0]
            plt.scatter(frame['Center Length(m)'], frame['Flow(m3/s)'], label=subtitle, s=1)
        lgnd = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10),
          fancybox=True, shadow=True, ncol=len(dfList), fontsize=4)
        for x in range(0, len(dfList)):
            lgnd.legendHandles[x]._sizes = [10]
        plt.suptitle('Resultados da perturbação', fontsize=8, weight = 'bold')
        plt.xlabel("River Length(m) →", fontsize=5)
        plt.ylabel("Flow (m3/s)", fontsize=5)
        plt.gca().invert_xaxis()
        ax = plt.gca()
        ax.tick_params(axis = 'both', which = 'major', labelsize = 4)
        ax.tick_params(axis = 'both', which = 'minor', labelsize = 4)
        filename = self.pathResults+ "\\" +frame['Parameter'][0] + '_FlowResults.png'
        fig.savefig(filename, dpi=400)

        fig = plt.figure()
        for frame in dfList:
            subtitle = frame['Iteration'][0]
            plt.scatter(frame['Center Length(m)'], frame['WSE(m)'], label=subtitle, s=1)
        lgnd = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10),
          fancybox=True, shadow=True, ncol=len(dfList), fontsize=4)
        for x in range(0, len(dfList)):
            lgnd.legendHandles[x]._sizes = [10]
        plt.suptitle('Resultados da perturbação', fontsize=8, weight = 'bold')
        plt.xlabel("River Length(m) →", fontsize=5)
        plt.ylabel("WSE (m)", fontsize=5)
        plt.gca().invert_xaxis()
        ax = plt.gca()
        ax.tick_params(axis = 'both', which = 'major', labelsize = 4)
        ax.tick_params(axis = 'both', which = 'minor', labelsize = 4)
        filename = self.pathResults+ "\\" +frame['Parameter'][0] + '_WSEResults.png'
        fig.savefig(filename, dpi=400)

        fig = plt.figure()
        for frame in dfList:
            subtitle = frame['Iteration'][0]
            plt.scatter(frame['Center Length(m)'], frame['V (m/s)'], label=subtitle, s=1)
        lgnd = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10),
          fancybox=True, shadow=True, ncol=len(dfList), fontsize=4)
        for x in range(0, len(dfList)):
            lgnd.legendHandles[x]._sizes = [10]
        plt.suptitle('Resultados da perturbação', fontsize=8, weight = 'bold')
        plt.xlabel("River Length(m) →", fontsize=5)
        plt.ylabel("V (m/s)", fontsize=5)
        plt.gca().invert_xaxis()
        ax = plt.gca()
        ax.tick_params(axis = 'both', which = 'major', labelsize = 4)
        ax.tick_params(axis = 'both', which = 'minor', labelsize = 4)
        filename = self.pathResults+ "\\" +frame['Parameter'][0] + '_VResults.png'
        
        fig.savefig(filename, dpi=400)

    def generateCSV(self, path, list_of_dfs):
        filenameExcel = path + "\\" + list_of_dfs[0]['Parameter'][0] + '.xlsx'

        writer = pd.ExcelWriter(filenameExcel, engine='xlsxwriter')
        stdQ = []
        meanQ = []
        coefQ = []
        stdV = []
        meanV = []
        coefV = []
        stdWSE = []
        meanWSE = []
        for x in range(0, len(list_of_dfs)):
            sheetName = list_of_dfs[x]['Iteration'][0]
            stdQ.append(list_of_dfs[x]['Flow(m3/s)'].std())
            meanQ.append(list_of_dfs[x]['Flow(m3/s)'].mean())
            coefQ.append(stdQ[0]/meanQ[0])
            stdV.append(list_of_dfs[x]['V (m/s)'].std())
            meanV.append(list_of_dfs[x]['V (m/s)'].mean())
            coefV.append(stdV[0]/meanV[0])
            stdWSE.append(list_of_dfs[x]['WSE(m)'].std())
            meanWSE.append(list_of_dfs[x]['WSE(m)'].mean())

            size = len(list_of_dfs[x]['Iteration'])-1

            [stdQ.append("") for y in range(0, size)]
            [meanQ.append("") for y in range(0, size)]
            [coefQ.append("") for y in range(0, size)]
            [stdV.append("") for y in range(0, size)]
            [meanV.append("") for y in range(0, size)]
            [coefV.append("") for y in range(0, size)]
            [stdWSE.append("") for y in range(0, size)]
            [meanWSE.append("") for y in range(0, size)]

            list_of_dfs[x]['Desvio Padrão Vazão (m³/s)'] = stdQ
            list_of_dfs[x]['Média Vazão (m³/s)'] = meanQ
            list_of_dfs[x]['Coeficiente de Variação da Vazão (%)'] = coefQ
            list_of_dfs[x]['Desvio Padrão Velocidade (m/s)'] = stdV
            list_of_dfs[x]['Média Velocidade (m/s)'] = meanV
            list_of_dfs[x]['Coeficiente de Variação da Velocidade (%)'] = coefV
            list_of_dfs[x]['Desvio Padrão WSE (m)'] = stdWSE
            list_of_dfs[x]['Média WSE (m)'] = meanWSE

            stdQ = []
            meanQ = []
            coefQ = []
            stdV = []
            meanV = []
            coefV = []
            stdWSE = []
            meanWSE = []

            list_of_dfs[x].to_excel(writer, sheet_name=sheetName, index=False)
        writer.save()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    fb = Interface()
    fb.show()
    app.exec_()