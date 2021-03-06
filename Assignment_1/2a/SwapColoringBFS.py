import copy
import datetime
import queue;
import random
import time


# -------------------------------------------------


class PuzzleNode:

    # constructor
    def __init__(self, state=None, parent=None):
        self.state = state;
        self.parent = None;
        self.action = None;
        self.path_cost = 0;
        self.children = None;

    def setState(self, state):
        self.state = state;

    def getState(self):
        return self.state;

    def setParent(self, parent):
        self.parent = parent;

    def getParent(self):
        return self.parent;

    def setAction(self, action):
        self.action = action;

    def getAction(self):
        return self.action;

    def setPathCost(self, path_cost):
        self.path_cost = path_cost;

    def getPathCost(self):
        return self.path_cost;

    def setChildren(self, children):
        self.children = children;

    def getChildren(self):
        return self.children;


# -------------------------------------------------

def compareLeft(currentState, k, l):  # k=i,l=j

    if (l != 0):
        return not (currentState[k][l] == currentState[k][l - 1]);
    return True;


def compareRight(currentState, k, l):  # k=i,l=j
    if (l != len(currentState) - 1):
        return not (currentState[k][l] == currentState[k][l + 1]);
    return True;


def compareUp(currentState, k, l):  # k=i,l=j
    if (k != 0):
        return not (currentState[k][l] == currentState[k - 1][l]);
    return True;


def compareDown(currentState, k, l):  # k=i,l=j # returns True if not equal or ok..else false(equal)
    if (k != len(currentState) - 1):
        return not (currentState[k][l] == currentState[k + 1][l]);
    return True;


def GoalTest(currentState):
    goal = True;

    for i in range(0, len(currentState)):
        for j in range(0, len(currentState)):

            goal = compareLeft(currentState, i, j);
            if (goal == False):
                return goal;

            goal = compareRight(currentState, i, j);
            if (goal == False):
                return goal;

            goal = compareUp(currentState, i, j);
            if (goal == False):
                return goal;

            goal = compareDown(currentState, i, j);
            if (goal == False):
                return goal;
    return goal;


# def frequencyCheck(currentState, frequency):
#     currentStateFreq = [0, 0, 0, 0];
#     freqCheck = False;
#     for i in range(0, len(currentState)):
#         for j in range(0, len(currentState)):
#             if (currentState[i][j] == 1):
#                 currentStateFreq[0] += 1;
#
#             elif (currentState[i][j] == 2):
#                 currentStateFreq[1] += 1;
#
#             elif (currentState[i][j] == 3):
#                 currentStateFreq[2] += 1;
#
#             elif (currentState[i][j] == 4):
#                 currentStateFreq[3] += 1;
#
#     print('current Frequency:', currentStateFreq);
#     if (frequency == currentStateFreq):
#         freqCheck = True;
#
#     return freqCheck;


def coloringBFS(puzzleNode):
    print('In ColoringBFS....');
    node = puzzleNode;
    node.path_cost = 0;

    # if (GoalTest(node.getState()) and frequencyCheck(node.getState(), frequency)):
    if (GoalTest(node.getState())):
        print('first **********Goal Found.**********');
        return node;

    frontier = queue.Queue();
    frontier.put(node);
    # explored = set();

    explored = [];

    for ele in frontier.queue:
        print(ele.getState());
        print('==');

    # explored.add(node.getState());

    while (True):

        failure = None;
        if (frontier.empty()):
            print('Goal Not Found..');
            return failure;

        print('--->frontier:', frontier.qsize());
        node = frontier.get();
        print('----------------current Node----------------');
        print(node.getState());

        # time.sleep(1);

        if (node.getState() in explored):
            continue;

        if (node.getState() not in explored):
            explored.append(node.getState());

        print('explored:', explored);
        print('-->explored:', len(explored));

        # colorI, colorJ = getIndexOfSameColor(node.getState());

        collisionIndices = [];
        collisionIndices = getIndexOfCollisions(node.getState());
        # print('colorI:', colorI, ' colorJ:', colorJ);

        # if (colorI != None and colorJ != None):
        #     swapRight(node, colorI, colorJ);
        #     swapDown(node, colorI, colorJ);
        #     swapLeft(node, colorI, colorJ);
        #     swapUp(node, colorI, colorJ);

        if (len(collisionIndices) == 0):
            print('no collisions:');
            return node;

        # time.sleep(1);
        if (len(collisionIndices) != 0):
            # for collisionIndex in collisionIndices:
            #     print(collisionIndex);

            for collisionIndex in collisionIndices:
                swapRight(node, collisionIndex[0], collisionIndex[1]);
                swapDown(node, collisionIndex[0], collisionIndex[1]);
                swapLeft(node, collisionIndex[0], collisionIndex[1]);
                swapUp(node, collisionIndex[0], collisionIndex[1]);

        # print('child Size:', len(children));
        # print('----------------children----------------');
        # for ele in children:
        #     print('-->', ele.getState(), '-->', ele.getParent().getState());
        # # time.sleep(1);
        # print('------------------');

        listObj = [];
        for obj in frontier.queue:
            listObj.append(obj.getState());

        # print('listObj:', listObj);

        print('\n');

        for ele in children:
            # print('parent:', ele.getParent());
            # time.sleep(1);
            if ((ele.getState() not in listObj) or (ele.getState() not in explored)):
                # if (GoalTest(ele.getState()) and frequencyCheck(ele.getState(), frequency)):
                if (GoalTest(ele.getState())):
                    print('\n**********Goal Found.**********');
                    print(ele.getState());

                    print('frontier nodes:', frontier.qsize());
                    print('explored nodes:', len(explored));
                    print('goal node path cost:', ele.getPathCost());

                    return ele;
                frontier.put(ele);

        children.clear();
        print('\n');


def swapLeft(currentNode, colorI, colorJ):
    tempNode = PuzzleNode();
    tempNode = copy.deepcopy(currentNode);

    if (colorJ != 0):
        temp = tempNode.getState()[colorI][colorJ];
        tempNode.getState()[colorI][colorJ] = tempNode.getState()[colorI][colorJ - 1];
        tempNode.getState()[colorI][colorJ - 1] = temp;

        tempNode.setPathCost(tempNode.getPathCost() + 1);
        tempNode.setParent(currentNode);
        children.append(tempNode);


def swapRight(currentNode, colorI, colorJ):
    tempNode = PuzzleNode();
    tempNode = copy.deepcopy(currentNode);

    if (colorJ != len(currentNode.getState()) - 1):
        temp = tempNode.getState()[colorI][colorJ];
        tempNode.getState()[colorI][colorJ] = tempNode.getState()[colorI][colorJ + 1];
        tempNode.getState()[colorI][colorJ + 1] = temp;

        tempNode.setPathCost(tempNode.getPathCost() + 1);
        tempNode.setParent(currentNode);

        children.append(tempNode);


def swapDown(currentNode, colorI, colorJ):
    tempNode = PuzzleNode();
    tempNode = copy.deepcopy(currentNode);

    if (colorI != len(currentNode.getState()) - 1):
        temp = tempNode.getState()[colorI][colorJ];
        tempNode.getState()[colorI][colorJ] = tempNode.getState()[colorI + 1][colorJ];
        tempNode.getState()[colorI + 1][colorJ] = temp;

        tempNode.setPathCost(tempNode.getPathCost() + 1);

        tempNode.setParent(currentNode);
        children.append(tempNode);


def swapUp(currentNode, colorI, colorJ):
    tempNode = PuzzleNode();
    tempNode = copy.deepcopy(currentNode);

    if (colorI != 0):
        temp = tempNode.getState()[colorI][colorJ];
        tempNode.getState()[colorI][colorJ] = tempNode.getState()[colorI - 1][colorJ];
        tempNode.getState()[colorI - 1][colorJ] = temp;

        tempNode.setPathCost(tempNode.getPathCost() + 1);

        tempNode.setParent(currentNode);
        children.append(tempNode);


def getIndexOfCollisions(currentState):
    # print('--------------getIndexOfCollisions--------------')
    indexI, indexJ = None, None;
    collisionIndices = [];

    for i in range(0, len(currentState)):
        for j in range(0, len(currentState)):

            if (not compareDown(currentState, i, j) or not compareUp(currentState, i, j) or not compareRight(
                    currentState, i,
                    j) or not compareLeft(
                currentState, i, j)):
                indexI, indexJ = i, j;

                collisionIndices.append([indexI, indexJ]);

                # return indexI, indexJ;
                # return i, j;
    return collisionIndices;


start_time = time.time();
print('start_time:', start_time);

n = int(input('enter n:'));

a = [[0] * n for i in range(n)];

for i in range(0, n):
    for j in range(0, n):
        a[i][j] = random.randint(1, 4);

# a = [[2, 1], [4, 4]];

# a = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]; # goal not found
# a = [[1, 1, 1], [1, 1, 1], [1, 1, 1]];# goal not found
# a = [[1, 2, 3, 4], [1, 1, 1, 1], [1, 2, 3, 4], [1, 1, 1, 1]];# goal not found
# a = [[1, 1], [1, 1]]; # goal not found
# a = [[1, 2, 3], [2, 3, 1], [3, 1, 2]]; # goal found
# a = [[1, 2, 3], [2, 3, 1], [1, 1, 1]]; # goal found
# a = [[1, 2], [3, 4]];# goal found
# a = [[1, 1], [1, 3]];  # goal not found

# a = [[1, 1], [2, 3]];
# a = [[1, 1, 2], [1, 1, 2], [1, 2, 2]]; # goal found

# a = [[1, 1, 2, 2], [1, 1, 2, 2], [3, 3, 4, 4], [3, 3, 4, 4]];  # goal found


for i in range(0, n):
    print(a[i]);

puzzleNode = PuzzleNode(a);

print('Initial state:');
for i in range(0, n):
    print(puzzleNode.getState()[i]);

children = [];

result = coloringBFS(puzzleNode);

if (result != None):
    output = [];
    while (result != None):
        output.append(result.getState());
        result = result.getParent();
    output.reverse();
    for i in output:
        for j in range(0, len(i)):
            print(i[j]);
        print('---')

print('end time:', time.time());
print(time.time() - start_time);
elapsed_time_secs = time.time() - start_time;
print('%s sec' % datetime.timedelta(seconds=round(elapsed_time_secs)));
