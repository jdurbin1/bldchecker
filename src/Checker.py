class Cube:
    
    def __init__(self):
        self.edgePermutation = [0,1,2,3,4,5,6,7,8,9,10,11]
        self.edgeOrientation = [0,0,0,0,0,0,0,0,0,0,0,0]
        self.cornerPermutation = [0,1,2,3,4,5,6,7]
        self.cornerOrientation = [0,0,0,0,0,0,0,0]

    def set_sample_state(self):
        self.cornerPermutation = [3, 0, 1, 7, 4, 5, 6, 2]
        self.cornerOrientation = [0, 0, 2, 1, 1, 2, 2, 1]
        self.edgePermutation = [4, 7, 6, 2, 8, 11, 10, 0, 9, 5, 3, 1]
        self.edgeOrientation = [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
        pass

#EDGEMAP: Determines if a piece is in the correct orientation when an edge swap occurs
# "Pole" pieces are ABCD, RTJL, UVWX
edgeMap = {
    'A' : [0,0],
    'B' : [1,0],
    'C' : [2,0],
    'D' : [3,0],
    'E' : [3,1],
    'F' : [7,1],
    'G' : [11,1],
    'H' : [4,1],
    'I' : [2,1],
    'J' : [6,0],
    'K' : [8,1],
    'L' : [7,0],
    'M' : [1,1],
    'N' : [5,1],
    'O' : [9,1],
    'P' : [6,1],
    'Q' : [0,1],
    'R' : [4,0],
    'S' : [10,1],
    'T' : [5,0],
    'U' : [8,0],
    'V' : [9,0],
    'W' : [10,0],
    'X' : [11,0],
}
# CORNERMAP: The rotation a piece is in when it enters the P position and is ready to be swapped (1: CW, 2: CCW)
# "Pole" pieces are ABCD, UVWX
cornerMap = {
    'A' : [0,2],
    'B' : [1,2],
    'C' : [2,2],
    'D' : [3,2],
    'E' : [0,1],
    'F' : [3,0],
    'G' : [4,1],
    'H' : [7,0],
    'I' : [3,1],
    'J' : [2,0],
    'K' : [5,1],
    'L' : [4,0],
    'M' : [2,1],
    'N' : [1,0],
    'O' : [6,1],
    'P' : [5,0],
    'Q' : [1,1],
    'R' : [0,0],
    'S' : [7,1],
    'T' : [6,0],
    'U' : [4,2],
    'V' : [5,2],
    'W' : [6,2],
    'X' : [7,2],
}
inverse = {0:0, 1:2, 2:1}

# corner orientation: # means the number of clockwise rotations to reach either up or down
# edge orientation: 0 means correct orientation, 1 means incorrect orientation

def printCube(cube):
    print("CORNERS: ")
    print(cube.cornerPermutation)
    print(cube.cornerOrientation)
    print("EDGES: ")
    print(cube.edgePermutation)
    print(cube.edgeOrientation)

#
# PIECE SWAPPING ALGORITHMS
#

# Swaps two edges, flipping orientation if necessary
def edgeSwap(cube, a, b):
    # Flip edge orientation if it is incorrect orientation
    edgePermutation = cube.edgePermutation
    edgeOrientation = cube.edgeOrientation
    aPos = edgeMap[a][0]
    bPos = edgeMap[b][0]
    if edgeMap[a][1] == 1:
        edgeOrientation[aPos] = 1 if edgeOrientation[aPos] == 0 else 0
        edgeOrientation[bPos] = 1 if edgeOrientation[bPos] == 0 else 0
    # Swap permutations
    temp = edgePermutation[aPos]
    edgePermutation[aPos] = edgePermutation[bPos]
    edgePermutation[bPos] = temp
    # Swap orientations
    temp = edgeOrientation[aPos]
    edgeOrientation[aPos] = edgeOrientation[bPos]
    edgeOrientation[bPos] = temp
    return

# Swaps pieces but does not check to apply rotations
def lazyEdgeSwap(cube, a, b):
    edgePermutation = cube.edgePermutation
    edgeOrientation = cube.edgeOrientation
    aPos = edgeMap[a][0]
    bPos = edgeMap[b][0]
   # Swap permutations
    temp = edgePermutation[aPos]
    edgePermutation[aPos] = edgePermutation[bPos]
    edgePermutation[bPos] = temp
    # Swap orientations
    temp = edgeOrientation[aPos]
    edgeOrientation[aPos] = edgeOrientation[bPos]
    edgeOrientation[bPos] = temp
    return

# Swaps two corners
def cornerSwap(cube, a, b):
    cornerPermutation = cube.cornerPermutation
    cornerOrientation = cube.cornerOrientation
    aPerm = cornerMap[a][0]
    bPerm = cornerMap[b][0]
    # Rotate the swapping piece once clockwise and add its orientation offset
    # Rotate the buffer piece once counter-clockwise and then by the inverse of the swapping piece's orientation offset
    cornerOrientation[aPerm] = (cornerOrientation[aPerm] + 1 + cornerMap[a][1]) % 3
    cornerOrientation[bPerm] = (cornerOrientation[bPerm] + 2 + inverse[cornerMap[a][1]]) % 3
    # Swap permutations
    temp = cornerPermutation[aPerm]
    cornerPermutation[aPerm] = cornerPermutation[bPerm]
    cornerPermutation[bPerm] = temp
    # Swap orientations
    temp = cornerOrientation[aPerm]
    cornerOrientation[aPerm] = cornerOrientation[bPerm]
    cornerOrientation[bPerm] = temp
    return

# Swaps pieces but does not check to apply rotations
def lazyCornerSwap(cube, a, b):
    cornerPermutation = cube.cornerPermutation
    cornerOrientation = cube.cornerOrientation
    aPerm = cornerMap[a][0]
    bPerm = cornerMap[b][0]
    # Swap permutations
    temp = cornerPermutation[aPerm]
    cornerPermutation[aPerm] = cornerPermutation[bPerm]
    cornerPermutation[bPerm] = temp
    # Swap orientations
    temp = cornerOrientation[aPerm]
    cornerOrientation[aPerm] = cornerOrientation[bPerm]
    cornerOrientation[bPerm] = temp
    return

# Applies a specific rotation to a piece. Value of 0 specifies edge flip. DO THIS AFTER ANY PERMUTATION CHANGES, NOT BEFORE 
def applyRotation(cube, piece, value):
    if value > 0:
        rotation = cube.cornerOrientation
        rotation[cornerMap[piece][0]] = (rotation[cornerMap[piece][0]] + value) % 3
    else:
        rotation = cube.edgeOrientation
        rotation[edgeMap[piece][0]] = 1 if rotation[edgeMap[piece][0]] == 0 else 0
    return

#
# CUBE MOVES
#

class Moves:
    # R: Corners: B->T, T->V, V->J, J->B. Edges: B->T, T->V, V->J, J->B
    def R(cube):
        lazyCornerSwap(cube, 'B', 'T')
        lazyCornerSwap(cube, 'B', 'V')
        lazyCornerSwap(cube, 'B', 'J')
        applyRotation(cube, 'B', 1)
        applyRotation(cube, 'T', 2)
        applyRotation(cube, 'V', 1)
        applyRotation(cube, 'J', 2)
        lazyEdgeSwap(cube, 'B', 'T')
        lazyEdgeSwap(cube, 'B', 'V')
        lazyEdgeSwap(cube, 'B', 'J')

    # L: Corners: A->I, I->U, U->S, S->A. Edges: D->L, L->X, X->R, R->D 
    def L(cube):
        lazyCornerSwap(cube, 'A', 'I')
        lazyCornerSwap(cube, 'A', 'U')
        lazyCornerSwap(cube, 'A', 'S')
        applyRotation(cube, 'A', 2)
        applyRotation(cube, 'I', 1)
        applyRotation(cube, 'U', 2)
        applyRotation(cube, 'S', 1)
        lazyEdgeSwap(cube, 'D', 'L')
        lazyEdgeSwap(cube, 'D', 'X')
        lazyEdgeSwap(cube, 'D', 'R')
        return

    # U: A->B, B->C, C->D, D->A
    def U(cube):
        lazyCornerSwap(cube, 'A', 'B')
        lazyCornerSwap(cube, 'A', 'C')
        lazyCornerSwap(cube, 'A', 'D')
        lazyEdgeSwap(cube, 'A', 'B')
        lazyEdgeSwap(cube, 'A', 'C')
        lazyEdgeSwap(cube, 'A', 'D')
        return

    # D: U->V, V->w, W->X, X->U
    def D(cube):
        lazyCornerSwap(cube, 'U', 'V')
        lazyCornerSwap(cube, 'U', 'W')
        lazyCornerSwap(cube, 'U', 'X')
        lazyEdgeSwap(cube, 'U', 'V')
        lazyEdgeSwap(cube, 'U', 'W')
        lazyEdgeSwap(cube, 'U', 'X')
        return

    # F: Corners: D->M, M->V, V->G, G->D. Edges: C->P, P->U, U->F, F->C
    def F(cube):
        lazyCornerSwap(cube, 'D', 'M')
        lazyCornerSwap(cube, 'D', 'V')
        lazyCornerSwap(cube, 'D', 'G')
        applyRotation(cube, 'D', 2)
        applyRotation(cube, 'M', 1)
        applyRotation(cube, 'V', 2)
        applyRotation(cube, 'G', 1)
        lazyEdgeSwap(cube, 'C', 'P')
        lazyEdgeSwap(cube, 'C', 'U')
        lazyEdgeSwap(cube, 'C', 'F')
        applyRotation(cube, 'C', 0)
        applyRotation(cube, 'P', 0)
        applyRotation(cube, 'U', 0)
        applyRotation(cube, 'F', 0)
        return

    # B: A->H, H->W, W->N, N->A
    def B(cube):
        lazyCornerSwap(cube, 'A', 'H')
        lazyCornerSwap(cube, 'A', 'W')
        lazyCornerSwap(cube, 'A', 'N')
        applyRotation(cube, 'A', 1)
        applyRotation(cube, 'N', 2)
        applyRotation(cube, 'W', 1)
        applyRotation(cube, 'H', 2)
        lazyEdgeSwap(cube, 'A', 'H')
        lazyEdgeSwap(cube, 'A', 'W')
        lazyEdgeSwap(cube, 'A', 'N')
        applyRotation(cube, 'A', 0)
        applyRotation(cube, 'N', 0)
        applyRotation(cube, 'W', 0)
        applyRotation(cube, 'H', 0)
        return

#
# MOVE READERS
#

# Returns True if scramble is valid. Valid: Follows standard scramble convention (all caps, 2 or ' to denote prime or double)
def isValidScramble(scramble):
    validMoves = ['U','D','R','L','F','B']
    extensions = ['2', "'"]
    last = ''
    for char in scramble:
        if char == ' ':
            last = ''
            continue
        if char in validMoves:
            if last != '':
                return False
        elif char in extensions:
            if last not in validMoves:
                return False
        last = char
    return True

def scrambleCube(cube, scramble):
    if not isValidScramble(scramble):
        return
    validMoves = ['U','D','R','L','F','B']
    moveList = []
    last = ''
    for char in scramble:
        if char == ' ':
            last = ''
            continue
        else:
            if char == "'":
                moveList.append(last)
                moveList.append(last)
            elif char == '2':
                moveList.append(last)
            elif char in validMoves:
                last = char
                moveList.append(char)
    for move in moveList:
        moveFunc = getattr(Moves, move)
        moveFunc(cube)
    return


def isValidSolution(solution):
    solution = solution.upper()
    newLineAppeared = 0
    for char in solution:
        if not char.isalpha():
            if char == '\n':
                if newLineAppeared > 1:
                    return 1
                newLineAppeared += 1
            elif not char.isspace():
                return 2
        else:
            if char == 'Y' or char == 'Z' or newLineAppeared > 1:
                return 3
    return 0

# Executes a Blindfolded solution onto a cube, where \n denotes the switch from edges to corners
def executeSolution(cube, solution):
    corners = False
    for char in solution:
        # Determine if a character is a space, a letter, or a \n
        if char.isspace() and char != '\n':
            continue
        else:
            if char == '\n' and not corners:
                corners = True
                continue
            if corners:
                # Old Pochman's corner swap
                cornerSwap(cube, char, 'A')
                lazyEdgeSwap(cube, 'A', 'D')
            else:
                # Old Pochman's edge swap
                edgeSwap(cube, char, 'B')
                lazyCornerSwap(cube, 'B', 'C')
    return

#
# SOLUTION CHECKING
#

# Checks if a cube's state matches the state of a solved cube. 
# Prints the first noticed issue if not matching and returns false, returns true otherwise.
def checkSolved(cube):
    i = 0
    # Check each edge to make sure it is in the proper permutation and orientation
    for edge in range(len(cube.edgePermutation)):
        if cube.edgePermutation[edge] != i or cube.edgeOrientation[edge] != 0:
            print("Incorrect edge at " + str(edge))
            return False
        i += 1 
    i = 0
    # Perform same check but for corners
    for corner in range(len(cube.cornerPermutation)):
        if cube.cornerPermutation[corner] != i or cube.cornerOrientation[corner] != 0:
            print("Incorrect corner at " + str(corner))
            return False
        i += 1
    print("Cube is solved")
    return True 

def main():
    print(isValidSolution("NOWIGLUPHAEA\nPSMBFLKV"))


if __name__ == "__main__":
    main()