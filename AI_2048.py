import math

class AI_search():
    def __init__(self, grid):
        # // grid是当前的16个cell里面的数字列表 [[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,2,2,2]]
        self.grid = grid
        self.out(self.grid)
        self.playerTurn = True

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

    # availableCells 这个是当前为0的cell的个数
    def availableCells(self, field):
        count = 0
        for row in field:
            for i in range(len(row)):
                if row[i] == 0:
                    count += 1
        return count

    # 格局评价---启发指标采用了加权策略  static evaluation function
    def eval(self, field):
        # emptyCells 这个是当前为0的cell的个数
        emptyCells = self.availableCells(field)

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
        if (self.playerTurn):
            bestScore = alpha
            for direction in [0, 1, 2, 3]:
                newGrid = self.grid
                if newGrid.move(direction).moved:
                    positions+=1
                    if newGrid.isWin():
                        return {move: direction, score:10000, positions: positions, cutoffs: cutoffs}
                    var newAI = new AI(newGrid)

                    if depth == 0:
                        result = { move: direction, score: newAI.eval() }
                    else:
                        result = newAI.search(depth-1, bestScore, beta, positions, cutoffs)
                        # // win
                        if result.score > 9900:
                            # // to slightly penalize higher depth from win
                            result.score-=1
                        positions = result.positions
                        cutoffs = result.cutoffs

                    if result.score > bestScore:
                        bestScore = result.score
                        bestMove = direction

                    if bestScore > beta:
                        cutoffs+=1
                        return { move: bestMove, score: beta, positions: positions, cutoffs: cutoffs }

        # // computer's turn, we'll do heavy pruning to keep the branching factor low
        else:
            bestScore = beta
        # try a 2 and 4 in each cell and measure how annoying it is
        # with metrics from eval
            candidates = []
            cells = self.grid.availableCells()
            scores = {2: [], 4: []}
            for value in scores:
                for i in cells:
                    scores[value].push(null)
                    cell = cells[i]
                    tile = new Tile(cell, parseInt(value, 10))
                    self.grid.insertTile(tile)
                    scores[value][i] = - self.grid.smoothness() + self.grid.islands()
                    self.grid.removeTile(cell)

        # // now just pick out the most annoying moves
            maxScore = Math.max(Math.max.apply(null, scores[2]), Math.max.apply(null, scores[4]));
            # // 2 and 4
            for value in scores:
                i = 0
                for i < scores[value].length:
                    if scores[value][i] == maxScore:
                        candidates.push( {position: cells[i], value: parseInt(value, 10)} )
                    i+=1

        # // search on each candidate
            for (var i=0; i < candidates.length; i++):
                position = candidates[i].position
                value = candidates[i].value
                newGrid = self.grid.clone()
                tile = new Tile(position, value)
                newGrid.insertTile(tile)
                newGrid.playerTurn = true
                positions+=1
                newAI = new AI(newGrid)
                result = newAI.search(depth, alpha, bestScore, positions, cutoffs)
                positions = result.positions
                cutoffs = result.cutoffs

                if result.score < bestScore:
                    bestScore = result.score

                if bestScore < alpha:
                    cutoffs+=1
                    return {move: null, score: alpha, positions: positions, cutoffs: cutoffs}

        return {move: bestMove, score: bestScore, positions: positions, cutoffs: cutoffs}

    #  // performs a search and returns the best move

    def getBest(self):
        return self.iterativeDeep()

# // performs iterative deepening over the alpha-beta search

    def iterativeDeep(self):
        start = (new Date()).getTime()
        depth = 0
        best={}
        do {
            newBest = self.search(depth, -10000, 10000, 0 ,0)
            if newBest.move == -1:
                break
            else:
                best = newBest
            depth+=1
        } while ( (new Date()).getTime() - start < minSearchTime)
        return best

    def translate(self,move):
        return {
        0: 'up',
        1: 'right',
        2: 'down',
        3: 'left'
        }[move]