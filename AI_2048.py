import math
import time
from grid import grid
minSearchTime = 100

class AI_2048():
    def __init__(self, grid):
        # // grid是当前的16个cell里面的数字列表 [[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,2,2,2]]  and playerTurn
        self.grid = grid
        self.original_grid = grid
        self.out(self.grid.get_current_grid())

    def get_field_to_str(self, field):
        row_str = ''
        row_str_all = ''
        for row in field:
            for i in range(len(row)):
                maped_num = map(str, row)  # 格納される数値を文字列にする
                row_str = ','.join(maped_num)
            row_str_all += " " + row_str
        return row_str_all

    def out(self, info):
        f = open("out.txt", 'a+')
        f.write(self.get_field_to_str(info))

    # availableCells 这个是当前为0的cell的列表
    def availableCells_length(self):
        count = 0
        for row in self.grid.get_current_grid():
            for i in range(len(row)):
                if row[i] == 0:
                    count += 1
        return count

    # 格局评价---启发指标采用了加权策略  static evaluation function
    def eval(self):
        # emptyCells 这个是当前为0的cell的个数
        emptyCells = self.availableCells_length()

        smoothWeight = 0.1
        # monoWeight   = 0.0,
        # islandWeight = 0.0,
        mono2Weight = 1.0
        emptyWeight = 2.7
        maxWeight = 1.0

    #  最后算出一个格局评价的值然后返回
        return self.grid.smoothness() * smoothWeight \
            + self.grid.monotonicity2() * mono2Weight \
            + math.log(emptyCells) * emptyWeight \
            + self.grid.maxValue() * maxWeight    #  // maxValue代表当前方格中的最大数字
            # + self.grid.monotonicity() * monoWeight
            # - self.grid.islands() * islandWeight

    # // alpha-beta depth first search
    def search(self, depth, alpha, beta, positions, cutoffs):
        bestScore = 0
        bestMove = -1
        result = {}

        # // the maxing player
        if (self.grid.playerTurn):
            bestScore = alpha
            for direction in [0, 1, 2, 3]:
                newGrid = grid(self.original_grid)
                if newGrid.move(direction):
                    positions += 1
                    if newGrid.is_win():
                        return {'move': direction, 'score': 10000, 'positions': positions, 'cutoffs': cutoffs}

                    newAI = AI_2048(newGrid)

                    if depth == 0:
                        result = { 'move': direction, 'score': newAI.eval()}
                    else:
                        result = newAI.search(depth-1, bestScore, beta, positions, cutoffs)
                        # // win
                        if result['score'] > 9900:
                            # // to slightly penalize higher depth from win
                            result['score'] -= 1
                        positions = result['positions']
                        cutoffs = result['cutoffs']

                    if result['score'] > bestScore:
                        bestScore = result['score']
                        bestMove = direction

                    if bestScore > beta:
                        cutoffs += 1
                        return { 'move': bestMove, 'score': beta, 'positions': positions, 'cutoffs': cutoffs }

        # // computer's turn, we'll do heavy pruning to keep the branching factor low
        else:
            bestScore = beta
        # try a 2 and 4 in each cell and measure how annoying it is
        # with metrics from eval
            candidates = []
            cells = self.grid.get_current_grid()
            scores = {2: [], 4: []}
            for value in scores:
                for i in range(len(cells)):
                    for n in range(len(cells[i])):
                    # cell  [[2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2]]
                    # scores的格式sample
                    # scores = {2: [[2, [0, 2]], [5, [1, 3]], [7, [0, 4]]],
                    #           4: [[21, [10, 21]], [51, [2, 31]], [71, [0, 41]]]}
                        if cells[i][n]==0:
                            cells[i][n]=value
                            scores[value][i][0] = - self.grid.smoothness() + self.grid.islands()
                            scores[value][i][1] =[i,n]
                            cells[i][n]=0

        # // now just pick out the most annoying moves
            maxScore = (max(max(scores[2]),max(scores[4])))
            # // 2 and 4
            for value in scores:
                for i in range(len(scores[value])):
                    if scores[value][i][0] == maxScore:
                        candidates.append({'position': scores[value][i][1], 'value': value})

        # // search on each candidate
            for i in range(len(candidates)):
                position = candidates[i]['position']
                value = candidates[i]['value']
                newGrid = self.original_grid
                newGrid[position[0]][position[1]] = value
                newGrid.playerTurn = True
                positions += 1
                newAI = AI_2048(newGrid)
                result = newAI.search(depth, alpha, bestScore, positions, cutoffs)
                positions = result['positions']
                cutoffs = result['cutoffs']

                if result['score'] < bestScore:
                    bestScore = result['score']

                if bestScore < alpha:
                    cutoffs+=1
                    return {'move': '', 'score': alpha, 'positions': positions, 'cutoffs': cutoffs}

        return {'move': bestMove, 'score': bestScore, 'positions': positions, 'cutoffs': cutoffs}

    #  // performs a search and returns the best move

    def getBest(self):
        return self.iterativeDeep()

# // performs iterative deepening over the alpha-beta search

    def iterativeDeep(self):
        start = time.time()
        print("start", start)
        depth = 0
        best = {}
        while True:
            newBest = self.search(depth, -10000, 10000, 0, 0)
            if newBest['move'] == -1:
                break
            else:
                best = newBest
            depth += 1
            if minSearchTime < (time.time() - start)*1000:
                break
        print("best={}".format(best))
        return best