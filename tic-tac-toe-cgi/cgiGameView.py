#!C:\Python33\python.exe

from functionbank import *
from math import *
from types import *
import random
import sys
import cgi, cgitb
cgitb.enable()
form = cgi.FieldStorage() 


print("Content-Type: text/html")
print()

print("<html>")
print("<head>")
print("<title>")
print("This is the FE of the game")
print("</title>")
print("</head>")
print("<body>")

gridFE = []

global index
index = 0

def printform():
    print('<form action = "print_form_new.py" method = "get">')
    print('<p>Tic Tac Toe Game:</p>', '<br>')
    printGridwithTextFields()
    print('<br>')
    print('<input type = "submit" name ="submit" value = "Submit" />')
    print('</form>')

def printGridwithTextFields():
    p = 0
    print('<table border = "1">')
    for i in row:
        print("<tr>")
        for j in col:
            print("<td>", '<input type = "text" ', 'name = "'+str(p) +'" value = "'+grid[p]['char']+'" />', "</td>")
            p = p + 1
        print("</tr>")
    print("</table>")	
    #print('<input type = "hidden" ', 'name = "'+'index' +'" value = "'+ str(y) +'" />')

def mapgridtogridFE():
  i = 0
  for x in range(len(row)):
      temp = []
      for y in range(len(col)):
          temp.append(grid[i]['char'])
          i = i + 1	
      gridFE.append(temp)
  print('<p> gridFE = ', gridFE, '</p>')
	
def printGridwithindex():
    p = 0
    mapgridtogridFE()
    print('<table border = "1">')
    for i in row:
        print("<tr>")
        for j in col:
            print("<td>", randompool[p], "</td>")
            p = p + 1			
        print("</tr>")
    print("</table>")

#print('<p>Index reference: </p>')
#printGridwithindex()
#print('<p>Grid: </p>')
#printGrid()
#print('<br>')

#y = form.getvalue('index')

keys = [str(i) for i, v in enumerate(grid)]
print(keys)

print('<pre>')
getValueCount = 0
for x in range(len(keys)):
    if form.getvalue(keys[x]): #keys[x] stores the name of each input text field
        getValueCount += 1
        #grid[x]['char'] = form.getvalue(keys[x])
        if form.getvalue(keys[x]) == 'X':
            checkP1Connect(x)
        elif form.getvalue(keys[x]) == 'O':
            checkP1ConnectForP2(x)
    else:
        grid[x]['char'] = '-'

if getValueCount > 0:
	checkP2Connect()
printGrid()
print('</pre>')

print('<p>grid = ', [grid[i]['char'] for i in range(len(grid))], '</p>')

print('<form action = "cgiGameView.py" method = "get">')
print('<p>Tic Tac Toe Game:</p>', '<br>')
printGridwithTextFields()

print('<br>')
print('<input type = "submit" name ="submit" value = "Submit" />')
print('</form>')
