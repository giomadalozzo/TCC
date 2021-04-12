nodes = []
leftMannings = []
rightMannings = []
river = []
reach = []

nodes_aux = []
leftMannings_aux = []
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
            rightMannings.append(rightMannings_aux)

            nodes_aux = []
            leftMannings_aux = []
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
            leftMannings_aux.append("0." + lines[i+1].replace(" 0", ",").split(".")[1].split(",")[0].strip())
            rightMannings_aux.append("0." + lines[i+1].replace(" 0", ",").split(".")[-1].split(",")[0].strip())

    if reach_aux != []:
        reach.append(reach_aux)
        river.append(river_aux)
        nodes.append(nodes_aux)
        leftMannings.append(leftMannings_aux)
        rightMannings.append(rightMannings_aux)

print("river")
print(river)
print("reach")
print(reach)
print("Nodes")
print(nodes)
print("left manning")
print(leftMannings)
print("right manning")
print(rightMannings)
