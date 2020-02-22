
import copy 
import numpy as np

path = []    #Generated Solution Path as Node Indexes is stored in this list 
NodePath = []  #Generated Solution Path as Node States is stored in this list
CurrNode = []  #Current Node 
CurrNodeIndex = 0 #Current Node Index is S
NodesInfo = [] #Node Indexes with their respective parents are stored in this list     
NodeState = [] #Nodes are stored in this list 
ParentNodeIndex = [] #Parent Node Information corresponding to the NodeState is stored in this list 

#Function to get the Initial State from user
def GetInitialNode():
    TempNode = []
    InitialNode = []
    TempNode = list(map(int, input("Enter the row-wise INITIAL Configuration separated by spaces \n 1 2 3 \n 4 5 6 --------------------> 1 2 3 4 5 6 7 0 8 \n 7 0 8: \n ").strip().split()))[:9]
    if len(TempNode) is not 9:
        GetInitialNode()
    InitialNode.append(TempNode[:3])
    InitialNode.append(TempNode[3:6])
    InitialNode.append(TempNode[6:9])
    return InitialNode

#Function to get the Goal State from user
def GetGoalNode():
    TempNode = []
    GoalNode = []
    TempNode = list(map(int, input("Enter the row-wise GOAL Configuration separated by spaces \n 1 2 3 \n 4 5 6 --------------------> 1 2 3 4 5 6 7 8 0 \n 7 8 0: \n ").strip().split()))[:9]
    if len(TempNode) is not 9:
        GetGoalNode()
    GoalNode.append(TempNode[:3])
    GoalNode.append(TempNode[3:6])
    GoalNode.append(TempNode[6:9])
    return GoalNode


#Function to check if the provided Initial State is solvable or not
"""Only works if the goal configuration is
		1 2 3
		4 5 6
		7 8 0
""" 
def SolvabilityCheck(StartNode):
    if GoalNode == [[1,2,3],[4,5,6],[7,8,0]]:
        TestNode=[]
        InvCount = 0
        for i in range(len(StartNode)):
            for j in range(len(StartNode[i])):
                if StartNode[i][j] is 0:
                    continue
                TestNode.append(StartNode[i][j])
        for i in range(len(TestNode)-1):
            for j in range(i+1,len(TestNode)):
                if(TestNode[i]>TestNode[j]):
                    InvCount+=1
        if(InvCount%2 is 0):
            return True
        else :
            return False
    else:
        return True

#Function to find the Blank Tile Location in a State
def BlankTileLocation(CurrentNode):
    for i in range(len(CurrentNode)):
        for j in range(len(CurrentNode[i])):
            if CurrentNode[i][j] is 0:
                return i,j

#Function to move the blank tile to the left if valid
def ActionMoveLeft(CurrentNode):
    i,j = BlankTileLocation(CurrentNode)
    if j is not 0:
        NewNode = copy.deepcopy(CurrentNode)
        NewNode[i][j],NewNode[i][j-1] = NewNode[i][j-1],NewNode[i][j] 
        return BlankTileLocation(NewNode),NewNode

#Function to move the blank tile to the right if valid 
def ActionMoveRight(CurrentNode):
    i,j = BlankTileLocation(CurrentNode)
    if j is not 2:
        NewNode = copy.deepcopy(CurrentNode)
        NewNode[i][j],NewNode[i][j+1] = NewNode[i][j+1],NewNode[i][j] 
        return BlankTileLocation(NewNode),NewNode

#Function to move the blank tile up if valid
def ActionMoveUp(CurrentNode):
    i,j = BlankTileLocation(CurrentNode)
    if i is not 0:
        NewNode = copy.deepcopy(CurrentNode)
        NewNode[i][j],NewNode[i-1][j] = NewNode[i-1][j],NewNode[i][j] 
        return BlankTileLocation(NewNode),NewNode

#Function to move the blank tile down if valid
def ActionMoveDown(CurrentNode):
    i,j = BlankTileLocation(CurrentNode)
    if i is not 2:
        NewNode = copy.deepcopy(CurrentNode)
        NewNode[i][j],NewNode[i+1][j] = NewNode[i+1][j],NewNode[i][j] 
        return BlankTileLocation(NewNode),NewNode

#Function to check if a node is new and add it to the list
def AddNode(NewNode):
    if not (NewNode in NodeState):
        global CurrNodeIndex
        NodeState.append(NewNode)
        ParentNodeIndex.append(CurrNodeIndex)
       
#Function to Find the Solution Path using the BFS
def SolvePuzzle(InitialNode):
    NodeState.append(InitialNode)
    ParentNodeIndex.append(len(NodeState)-1)
    global CurrNode
    global CurrNodeIndex
    global GoalNode
    CurrNode = copy.deepcopy(InitialNode)
    while(CurrNode != GoalNode):
        if ActionMoveLeft(CurrNode) is not None:
            AddNode(ActionMoveLeft(CurrNode)[1])
        if ActionMoveRight(CurrNode) is not None:
            AddNode(ActionMoveRight(CurrNode)[1])
        if ActionMoveUp(CurrNode) is not None:
            AddNode(ActionMoveUp(CurrNode)[1])
        if ActionMoveDown(CurrNode) is not None:
            AddNode(ActionMoveDown(CurrNode)[1])
        CurrNodeIndex +=  1
        CurrNode = NodeState[CurrNodeIndex]
        NodesInfo.append([CurrNodeIndex, ParentNodeIndex[CurrNodeIndex],0])
    return CurrNode

#Function to Generate the Path Sequence to be followed to reach goal
def GeneratePath(CurrNode):
    path.append(CurrNodeIndex)
    while(path[0] != 0):
        path.insert(0,ParentNodeIndex[NodeState.index(CurrNode)])
        CurrNode = NodeState[path[0]]

    for i in range(len(path)):
        NodePath.append(NodeState[path[i]])

#Function to Generate the required output files in the defined format
def GenerateOutputFiles():    
    f = open("NodesInfo.txt", "wt")
    for i in range(len(NodesInfo)):
        for j in range(len(NodesInfo[0]) ):
            f.write(str(NodesInfo[i][j]) + ' ')
        f.write('\n')

    f.close()

    f = open("Nodes.txt", "wt")
    for i in range(len(NodeState)):
        
        for j in range(len(NodeState[i])):
            for k in range(len(NodeState[i][j])):
                f.write(str(NodeState[i][k][j]) + ' ')
        f.write('\n')

    f.close()

    f = open("nodePath.txt","wt")
    for i in range(len(NodePath)):
        for j in range(len(NodePath[i])):
            for k in range(len(NodePath[i][j])):
                f.write(str(NodePath[i][k][j]) + ' ')
        f.write('\n')

    f.close()

#Provided Fucntion to Print the Matrix
def print_matrix(state):
    counter = 0
    for row in range(0, len(state), 3):
        if counter == 0 :
            print("-------------")
        for element in range(counter, len(state), 3):
            if element <= counter:
                print("|", end=" ")
            print(int(state[element]), "|", end=" ")
        counter = counter +1
        print("\n-------------")

# Provided Function to Print the Solution 
def PrintSolution():    
    fname = 'nodePath.txt'
    data = np.loadtxt(fname)
    if len(data[1]) is not 9:
        print("Format of the text file is incorrect, retry ")
    else:
        for i in range(0, len(data)):
            if i == 0:
                print("Start Node")
            elif i == len(data)-1:
                print("Achieved Goal Node")
            else:
                print("Step ",i)
            print_matrix(data[i])
            print()


InitialNode = GetInitialNode()
GoalNode = GetGoalNode()
if(SolvabilityCheck(InitialNode)):
    SolutionNode = SolvePuzzle(InitialNode)
    GeneratePath(SolutionNode)
    GenerateOutputFiles()
    PrintSolution()

else:
    print("The provided Initial Configuration is unsolvable")

