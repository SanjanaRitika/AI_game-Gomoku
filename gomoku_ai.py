
import random
from boardstate import *
from copy import deepcopy
from evaluate import *
from gomoku import Gomoku


class gomokuAI(object):

    def __init__(
        self,
        gomoku,
        currentState,
        depth,
        ):

        self.__gomoku = gomoku
        self.__currentState = currentState
        self.__depth = depth
        self.__currentI = -1
        self.__currentJ = -1

    def set_board(
        self,
        i,
        j,
        state,
        ):

        self.__gomoku.set_chessboard_state(i, j, state)

    def has_neighbor(
        self,
        state,
        i,
        j,
        ):

        directions = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1),
                      (1, -1)], [(-1, -1), (1, 1)]]
        for axis in directions:
            for (xdirection, ydirection) in axis:

                if xdirection != 0 and (j + xdirection < 0 or j
                        + xdirection >= N):
                    break
                if ydirection != 0 and (i + ydirection < 0 or i
                        + ydirection >= N):
                    break
                if self.__gomoku.get_chessMap()[i + ydirection][j
                        + xdirection] != BoardState.EMPTY:
                    return True

                if xdirection != 0 and (j + xdirection * 2 < 0 or j
                        + xdirection * 2 >= N):
                    break

                if ydirection != 0 and (i + ydirection * 2 < 0 or i
                        + ydirection * 2 >= N):
                    break

                if self.__gomoku.get_chessMap()[i + ydirection * 2][j
                        + xdirection * 2] != BoardState.EMPTY:
                    return True

        return False

    def direction_count(
        self,
        i,
        j,
        xdirection,
        ydirection,
        state,
        ):

        count = 0
        for step in range(1, 5): 
            if xdirection != 0 and (j + xdirection * step < 0 or j
                                    + xdirection * step >= N):
                break
            if ydirection != 0 and (i + ydirection * step < 0 or i
                                    + ydirection * step >= N):
                break
            if self.__gomoku.get_chessMap()[i + ydirection * step][j
                    + xdirection * step] == state:
                count += 1
            else:
                break
        return count

    def direction_pattern(
        self,
        i,
        j,
        xdirection,
        ydirection,
        state,
        ):


        pattern = []
        for step in range(-1, 5):  # generate a list with len 10
            if xdirection != 0 and (j + xdirection * step < 0 or j
                                    + xdirection * step >= N):
                break
            if ydirection != 0 and (i + ydirection * step < 0 or i
                                    + ydirection * step >= N):
                break

            pattern.append(self.__gomoku.get_chessMap()[i + ydirection
                           * step][j + xdirection * step])

        return pattern

    def has_checkmate(
        self,
        state,
        i,
        j,
        ):

        directions = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1),
                      (1, -1)], [(-1, -1), (1, 1)]]

        for axis in directions:
            axis_count = 1
            for (xdirection, ydirection) in axis:
                axis_count += self.direction_count(i, j, xdirection,
                        ydirection, state)
                if axis_count >= 5:
                    return True
        return False

    def has_check(
        self,
        state,
        i,
        j,
        ):

        directions = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1),
                      (1, -1)], [(-1, -1), (1, 1)]]

        for axis in directions:
            currentPattern = []
            for (xdirection, ydirection) in axis:
                currentPattern += self.direction_pattern(i, j,
                        xdirection, ydirection, state)
                if len(currentPattern) > 2:
                    currentPattern[1] = state
                if enum_to_string(currentPattern) == WHITE_6PATTERNS[0]:
                    return True
                if enum_to_string(currentPattern) == BLACK_6PATTERNS[0]:
                    return True
        return False

    def opponent_has_checkmate(self, state):

        vectors = []

        #exhaustive search

        for i in range(N):
            vectors.append(self.__gomoku.get_chessMap()[i])

        for j in range(N):
            vectors.append([self.__gomoku.get_chessMap()[i][j] for i in
                           range(N)])

        vectors.append([self.__gomoku.get_chessMap()[x][x] for x in
                       range(N)])
        for i in range(1, N - 4):
            v = [self.__gomoku.get_chessMap()[x][x - i] for x in
                 range(i, N)]
            vectors.append(v)
            v = [self.__gomoku.get_chessMap()[y - i][y] for y in
                 range(i, N)]
            vectors.append(v)

        vectors.append([self.__gomoku.get_chessMap()[x][N - x - 1]
                       for x in range(N)])
        for i in range(4, N - 1):
            v = [self.__gomoku.get_chessMap()[x][i - x] for x in
                 range(i, -1, -1)]
            vectors.append(v)
            v = [self.__gomoku.get_chessMap()[x][N - x + N - i - 2]
                 for x in range(N - i - 1, N)]
            vectors.append(v)

        #checkmate
        for vector in vectors:
            temp = enum_to_string(vector)
            if state == BoardState.BLACK:
                for pattern in WHITE_5PATTERNS:
                    if sublist(pattern, temp):
                        return True
            if state == BoardState.WHITE:
                for pattern in BLACK_5PATTERNS:
                    if sublist(pattern, temp):
                        return True
        return False

    def generate(self):

        frontierList = []
        for i in range(N):
            for j in range(N):
                if self.__gomoku.get_chessMap()[i][j] \
                    != BoardState.EMPTY:
                    continue  # only search for available spots
                if not self.has_neighbor(self.__gomoku.get_chessMap()[i][j],
                        i, j):
                    continue

                if self.__currentState == BoardState.WHITE:
                    nextState = BoardState.BLACK
                else:
                    nextState = BoardState.WHITE

                nextPlay = gomokuAI(deepcopy(self.__gomoku), nextState,
                                    self.__depth - 1)
                nextPlay.set_board(i, j, self.__currentState)

                frontierList.append((nextPlay, i, j))


        frontierScores = []
        for node in frontierList:
            frontierScores.append(self.evaluate_point(node[1], node[2]))

        frontierZipped = zip(frontierList, frontierScores)
        frontierSorted = sorted(frontierZipped, key=lambda t: t[1])
        (frontierList, frontierScores) = zip(*frontierSorted)
        return frontierList

    def negate(self):
        return -self.evaluate()

    def evaluate(self):

        vectors = []

        for i in range(N):
            vectors.append(self.__gomoku.get_chessMap()[i])

        for j in range(N):
            vectors.append([self.__gomoku.get_chessMap()[i][j] for i in
                           range(N)])

        vectors.append([self.__gomoku.get_chessMap()[x][x] for x in
                       range(N)])
        for i in range(1, N - 4):
            v = [self.__gomoku.get_chessMap()[x][x - i] for x in
                 range(i, N)]
            vectors.append(v)
            v = [self.__gomoku.get_chessMap()[y - i][y] for y in
                 range(i, N)]
            vectors.append(v)

        vectors.append([self.__gomoku.get_chessMap()[x][N - x - 1]
                       for x in range(N)])

        for i in range(4, N - 1):
            v = [self.__gomoku.get_chessMap()[x][i - x] for x in
                 range(i, -1, -1)]
            vectors.append(v)
            v = [self.__gomoku.get_chessMap()[x][N - x + N - i - 2]
                 for x in range(N - i - 1, N)]
            vectors.append(v)

        board_score = 0

        for v in vectors:
            score = evaluate_vector(v)
            if self.__currentState == BoardState.WHITE:
                board_score += score['black'] - score['white']
            else:
                board_score += score['white'] - score['black']
        return board_score

    def evaluate_point(self, i, j):

        vectors = []
        vectors.append(self.__gomoku.get_chessMap()[i])
        vectors.append([self.__gomoku.get_chessMap()[i][j] for i in
                       range(N)])

        if j > i:
            v = [self.__gomoku.get_chessMap()[x][x + j - i] for x in
                 range(0, N - j + i)]
            vectors.append(v)
        elif j == i:

            vectors.append([self.__gomoku.get_chessMap()[x][x] for x in
                           range(N)])
        elif j < i:

            v = [self.__gomoku.get_chessMap()[x + i - j][x] for x in
                 range(0, N - i + j)]
            vectors.append(v)

        if i + j == N - 1:
            vectors.append([self.__gomoku.get_chessMap()[x][N - 1 - x]
                           for x in range(N)])
        elif i + j < N - 1:

            v = [self.__gomoku.get_chessMap()[x][N - 1 - x - abs(i
                 - j)] for x in range(N - abs(i - j))]
            vectors.append(v)
        elif i + j > N - 1:

            vectors.append([self.__gomoku.get_chessMap()[x][N - 1 - x
                           + i + j - N + 1] for x in range(i + j - N
                           + 1, N)])

        point_score = 0
        for v in vectors:
            score = evaluate_vector(v)
            if self.__currentState == BoardState.WHITE:
                point_score += score['white']
            else:
                point_score += score['black']
        return point_score

    def alpha_beta_prune(
        self,
        ai,
        alpha=-10000000,
        beta=10000000,
        ):

        if ai.__depth <= 0:
            score = ai.negate()
            return score
        for (nextPlay, i, j) in ai.generate():
            temp_score = -self.alpha_beta_prune(nextPlay, -beta, -alpha)
            if temp_score > beta:
                return beta
            if temp_score > alpha:
                alpha = temp_score
                (ai.__currentI, ai.__currentJ) = (i, j)
        return alpha

    def first_step(self):
        self.__gomoku.set_chessboard_state(7, 7, self.__currentState)
        return True

    def one_step(self):
        for i in range(N):
            for j in range(N):
                if self.__gomoku.get_chessMap()[i][j] \
                    != BoardState.EMPTY:
                    continue  

                if self.has_checkmate(self.__currentState, i, j):
                    print ('has checkmate')
                    self.__gomoku.set_chessboard_state(i, j,
                            self.__currentState)
                    return True

                if not self.has_neighbor(self.__gomoku.get_chessMap()[i][j],
                        i, j):
                    continue

                if self.has_check(self.__currentState, i, j):
                    print ('has check, checking if opponent already has one...')

                    if self.opponent_has_checkmate(self.__currentState) \
                        is True:

                        print ('not safe, searching other moves...')
                    elif self.opponent_has_checkmate(self.__currentState) \
                        is False:

                        print ('safe')
                        self.__gomoku.set_chessboard_state(i, j,
                                self.__currentState)
                        return True

        node = gomokuAI(self.__gomoku, self.__currentState,
                        self.__depth)
        score = self.alpha_beta_prune(node)
        print (score)
        (i, j) = (node.__currentI, node.__currentJ)

        if not i is None and not j is None:
            if self.__gomoku.get_chessboard_state(i, j) \
                != BoardState.EMPTY:
                self.one_step()
            else:
                self.__gomoku.set_chessboard_state(i, j,
                        self.__currentState)
                return True
        return False



            