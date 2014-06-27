from math import *
import random
import sys

global grid

row = [x for x in range(3)]
col = [y for y in range(3)]		
grid = [{'row': x, 'col': y, 'char':'-'} for x in row for y in col]
randompool = [x for x in range(len(grid))]
P1Connect = []
P2Connect = []

def printGrid():
    for i in range(len(grid)):
        print(grid[i]['char'], end='   ')
        if i in (2, 5, 8):  
            print("\n")
			
def getCoordinate(sublist):
    return [(grid[sublist[i]]['row'], grid[sublist[i]]['col']) for i in range(len(sublist))]

def slope(dy, dx):
    try:
        return int(dy/dx)
    except ZeroDivisionError:
        pass

def getIndex(x, y):
    for index in range(len(grid)):
        if (grid[index]['row'] == x) & (grid[index]['col'] == y):
            return index
		
def getCriticalP2(list):
        cor_list = getCoordinate(list) 
        x0, y0 = cor_list[0]
        x1, y1 = cor_list[1]
        dx = x1 - x0
        dy = y1 - y0
        if (dx == 0) & (abs(dy) >= 1): 
            x = x0
            y = 3 - y0 - y1
            index_for_P2 = getIndex(x, y)
        elif (dy == 0) & (abs(dx) >= 1):
            y = y0
            x = 3 - x0 - x1
            index_for_P2 = getIndex(x, y)	
        elif slope(abs(dy), abs(dx)) == 1:
            x = 3 - x0 - x1
            y = 3 - y0 - y1
            if (slope(abs(y - y1), abs(x - x1)) == 1) & (slope(abs(y - y0), abs(x - x0)) == 1):
                index_for_P2 = getIndex(x, y)
            else:
                index_for_P2 = None
        return index_for_P2


def P2RandomIndex():
    v = random.choice(randompool)
    p = randompool.index(v)
    randomindex = randompool.pop(p)    
    return randomindex

def FoundConnected2(list):  # find 2 connected P2 spots AND the third spot is available
    global p, finalindex
    status = False
    for i in range(len(list)):
        if len(list[i]) == 2:  
            tempindex = getCriticalP2(list[i])
            if tempindex == None:   # the third spot is not available 
                status = False
            else: 				
                if grid[tempindex]['char'] == '-':  
                    p = i
                    finalindex = tempindex
                    status = True
                    break
                elif grid[tempindex]['char'] != '-': # the third spot is blocked by P1
                    status = False
    return status

def optimizedP2Selection(list, index):
    flag = False
    for i in range(len(list)):
        if len(list[i]) == 1:
            if calculation1(list[i], index) == True:
                list[i].append(index)
                flag = True 
        elif len(list[i]) == 2:
            temp = [[x] for x in list[i]] 
            for j in range(2):
                if calculation1(temp[j], index) == True:
                    temp[j].append(index)
                    list.append(temp[j]) 
                    flag = True                                
    if flag == True:
        return index	
    elif flag == False:
        index = random.choice(randompool)
        return optimizedP2Selection(list, index)

def calculation1(sublist, index):
    #print("now compare ", sublist[0], " with index ", index)
    x0 = grid[sublist[0]]['row']
    y0 = grid[sublist[0]]['col']
    x = grid[index]['row']
    y = grid[index]['col']
    dx = x - x0
    dy = y - y0
    if ((dx == 0) & (abs(dy) >= 1)) | ((dy == 0) & (abs(dx) >= 1)) | (slope(abs(dy), abs(dx)) == 1):
        return True
    else:
        return False
        
def calculation2(sublist, index):
    oneline = False
    cor_list = getCoordinate(sublist)
    print(cor_list)
    x0, y0 = cor_list[0]
    x1, y1 = cor_list[1]
    x = grid[index]['row']
    y = grid[index]['col']
    dx = x - x0 - x1
    dy = y - y0 - y1
    sumx = x + x0 + x1
    sumy = y + y0 + y1	
    #print(type((abs(y - y1)/abs(x - x1))))
    if ((x0 == x1 == x) & (sumy == 3 )) | ((y0 == y1 == y) & (sumx == 3 )) | (sumx == 3) & (sumy == 3) & ((slope(abs(y - y1), abs(x - x1)) == 1) & (slope(abs(y - y0), abs(x - x0)) == 1)):
        oneline = True
    return oneline		
        
def split(player, sublist, index): 
   temp = [[x] for x in sublist]
   #print("temp = ", temp)
   connected = False   
   for j in range(2):
       if calculation1(temp[j], index) == True:
           temp[j].append(index)
           print(temp[j])
           if player == 1:
               P1Connect.append(temp[j])
           elif player == 2:
               P2Connect.append(temp[j])
           connected = True		   
   if connected == False:
       if player == 1:   
           P1Connect.append([index])
       elif player == 2:
           P2Connect.append([index])
   return connected	
   
 
def checkP1Connect(index): 
    player = 1
    randompool.pop(randompool.index(index))
    if len(P1Connect) == 0:
        P1Connect.append([index])
    else:
        for i in range(len(P1Connect)):
            flag = False
            if len(P1Connect[i]) == 2: # split or create a link with 3 dots
                oneline = calculation2(P1Connect[i], index)
                if oneline == True:
                    P1Connect[i].append(index)
                    grid[index]['char'] = 'X'
                    #showwinner()
                    if grid[P1Connect[i][0]]['char'] == grid[P1Connect[i][1]]['char'] == grid[P1Connect[i][2]]['char']:
                        print("*** P1 wins! ***")
                        printGrid()
                        print("P1Connect= ", P1Connect)
                        sys.exit()	
                elif oneline == False:
                    connected = split(player, P1Connect[i], index)
                    if connected == True:
                        flag == True			
            elif len(P1Connect[i]) == 1:
                if calculation1(P1Connect[i], index) == True:
                    P1Connect[i].append(index)
                    flag = True
                #elif calculation1(P1Connect[i], index) == False:  # logic need modification
                #    P1Connect.append([index])
        if flag == False:
            P1Connect.append([index])
    grid[index]['char'] = 'X'
    print("P1Connect = ", P1Connect)

def checkP1ConnectForP2(index):
    player = 2
    randompool.pop(randompool.index(index))
    if len(P2Connect) == 0:
        P2Connect.append([index])
    else:
        for i in range(len(P2Connect)):
            flag = False
            if len(P2Connect[i]) == 2: # split or create a link with 3 dots
                oneline = calculation2(P2Connect[i], index)
                if oneline == True:
                    P2Connect[i].append(index)
                    grid[index]['char'] = 'O'
                    #showwinner()
                    if grid[P2Connect[i][0]]['char'] == grid[P2Connect[i][1]]['char'] == grid[P2Connect[i][2]]['char']:
                        print("*** P2 wins! ***")
                        printGrid()
                        print("P2Connect= ", P2Connect)
                        sys.exit()
                elif oneline == False:
                    connected = split(player, P2Connect[i], index)
                    if connected == True:
                        flag == True			
            elif len(P2Connect[i]) == 1:
                if calculation1(P2Connect[i], index) == True:
                    P2Connect[i].append(index)
                    flag = True
                #elif calculation1(P1Connect[i], index) == False:  # logic need modification
                #    P1Connect.append([index])
        if flag == False:
            P2Connect.append([index])
    grid[index]['char'] = 'O'
    print("P2Connect = ", P2Connect)
    

def checkP2Connect():
  player = 2
  if len(randompool) == 0:
    print("P2Connect = ", P2Connect)
    print("*** Stalemate! No winner is found in this round of game. ***")
  else:
    global index2
    player = 2
    found2 = False
    if len(P2Connect) == 0:
        index2 = random.choice(randompool)
        print("index2 = ", index2)
        P2Connect.append([index2])
        print("P2Connect = ", P2Connect)
        grid[index2]['char'] = 'O'
        randompool.pop(randompool.index(index2))
    else:
        found2 = FoundConnected2(P2Connect)
        if found2 == True:
            index2 = finalindex # P2 wins
            randompool.pop(randompool.index(index2))
            P2Connect[p].append(index2)
            grid[index2]['char'] = 'O'
            print("index2 = ", index2)
            print("P2Connect = ", P2Connect)
            if grid[P2Connect[p][0]]['char'] == grid[P2Connect[p][1]]['char'] == grid[P2Connect[p][2]]['char']:
                print("*** P2 wins! ***")
                printGrid()
                sys.exit()
        else:
            found2 = FoundConnected2(P1Connect)
            if found2 == True:
                index2 = finalindex # block P1
                for i in range(len(P2Connect)):  # add index2 to P2Connect
                    flag = False
                    if len(P2Connect[i]) == 1:
                        if calculation1(P2Connect[i], index2) == True:
                            P2Connect[i].append(index2)
                            flag = True
                    elif len(P2Connect[i]) == 2:
                        temp = [[x] for x in P2Connect[i]] 
                        for j in range(2):
                            if calculation1(temp[j], index2) == True:
                                temp[j].append(index2)
                                P2Connect.append(temp[j]) 
                                flag = True           
                if flag == False:
                    P2Connect.append([index2])
                print("*** P1 blocked ***")				
            elif found2 == False:
                 randindex = random.choice(randompool) # pick a dot next to the any of the dot in P2Connect
                 index2 = optimizedP2Selection(P2Connect, randindex)
                 print("*** A placement randomly picked for P2 ***")
            grid[index2]['char'] = 'O'			
            randompool.pop(randompool.index(index2))
            print("index2 = ", index2)	
            print("P2Connect = ", P2Connect)	

def placementP1():
    index = int(input("Enter index number for Player1: "))
    while grid[index]['char'] != '-':
        print("This spot is not available")
        index = int(input("Enter index number for Player1: "))
    return index