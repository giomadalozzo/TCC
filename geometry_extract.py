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

with open('./Arquivos HECRAS/ItajaiProjeto.g10','r') as file:
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



"""
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
"""