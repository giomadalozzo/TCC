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

listParam.append(initialParam)
listParam.sort()
print(listParam)
