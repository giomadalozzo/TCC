import pandas as pd
list_of_dfs = []

d1 = {
    'Name':['Alisa','Bobby','Cathrine','Madonna','Rocky','Sebastian','Jaqluine',
   'Rahul','David','Andrew','Ajay','Teresa'],
   'Score1':[61,47,55,74,31,77,85,63,42,32,71,57],
   'Score2':[89,87,67,55,47,72,76,79,44,92,99,69],
   'Score3':[56,86,77,45,73,62,74,89,71,67,97,68]}

d2 = {
    'Name':['Alisa','Bobby','Cathrine','Madonna','Rocky','Sebastian','Jaqluine',
   'Rahul','David','Andrew','Ajay','Teresa'],
   'Score1':[62,47,55,74,31,77,85,63,42,32,71,57],
   'Score2':[89,87,67,55,47,72,76,79,44,92,99,69],
   'Score3':[56,86,77,45,73,62,74,89,71,67,97,68]}

d3 = {
    'Name':['Alisa','Bobby','Cathrine','Madonna','Rocky','Sebastian','Jaqluine',
   'Rahul','David','Andrew','Ajay','Teresa'],
   'Score1':[63,47,55,74,31,77,85,63,42,32,71,57],
   'Score2':[89,87,67,55,47,72,76,79,44,92,99,69],
   'Score3':[56,86,77,45,73,62,74,89,71,67,97,68]}

df1 = pd.DataFrame(d1)
df2 = pd.DataFrame(d2)
df3 = pd.DataFrame(d3)

list_of_dfs.append(df1)
list_of_dfs.append(df2)
list_of_dfs.append(df3)

writer = pd.ExcelWriter('pandas_multiple.xlsx', engine='xlsxwriter')
stdList = []
meanList = []
coefList = []
for x in range(0, len(list_of_dfs)):
    sheetName = "sheet" + str(x)
    stdList.append(list_of_dfs[x]['Score1'].std())
    meanList.append(list_of_dfs[x]['Score1'].mean())
    coefList.append(stdList[0]/meanList[0])
    size = len(list_of_dfs[x]['Score1'])-1
    print(size)
    [stdList.append("") for y in range(0, size)]
    [meanList.append("") for y in range(0, size)]
    [coefList.append("") for y in range(0, size)]
    print(len(coefList))
    list_of_dfs[x]['Desvio Padrão'] = stdList
    list_of_dfs[x]['Média'] = meanList
    list_of_dfs[x]['Coeficiente de variação (DP/média)'] = coefList
    #result = pd.concat(list_aux)
    list_of_dfs[x].to_excel(writer, sheet_name=sheetName, index=False)
    stdList = []
    meanList = []
    coefList = []
writer.save()