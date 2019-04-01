import math
import numpy as np

# file1d这个地方的值是grid的实例
# type object argument after * must be an iterable, not grid
def transpose(field):
    return [list(row) for row in zip(*field)]

def invert(field):
    return [row[::-1] for row in field]

def move_is_possible(direction, field1):
    def row_is_left_movable(row):
        def change(i):  # true if there'll be change in i-th tile
            if row[i] == 0 and row[i + 1] != 0: # Move
                return True
            if row[i] != 0 and row[i + 1] == row[i]: # Merge
                return True
            return False
        return any(change(i) for i in range(len(row) - 1))

    # //direction   0: up, 1: right, 2: down, 3: left
    check = {}
    check['Left'] = lambda field:                              \
            any(row_is_left_movable(row) for row in field)

    check['Right'] = lambda field:                              \
                check['Left'](invert(field))

    check['Up'] = lambda field:                              \
            check['Left'](transpose(field))

    check['Down'] = lambda field:                              \
            check['Right'](transpose(field))

    if direction in check:
        # //direction   0: up, 1: right, 2: down, 3: left
        return check[direction](field1)
    else:
        return False

class grid():

    def __init__(self, current_grid):
        self.current_grid = current_grid
        self.score = 0
        self.won = False
        self.win_value = 2048
        self.playerTurn = True

    def move(self, direction):
        def move_row_left(row):
            def tighten(row): # squeese non-zero elements together
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row

            def merge(row):
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(2 * row[i])
                        self.score += 2 * row[i]
                        pair = False
                    else:
                        if i + 1 < len(row) and row[i] == row[i + 1]:
                            pair = True
                            new_row.append(0)
                        else:
                            new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row
            return tighten(merge(tighten(row)))

        moves = {}
        moves['Left'] = lambda field:                              \
                [move_row_left(row) for row in field]
        moves['Right'] = lambda field:                              \
                invert(moves['Left'](invert(field)))
        moves['Up'] = lambda field:                              \
                transpose(moves['Left'](transpose(field)))
        moves['Down'] = lambda field:                              \
                transpose(moves['Right'](transpose(field)))

        if direction in moves:
            # //direction   0: up, 1: right, 2: down, 3: left
            if move_is_possible(direction, self.current_grid):
                self.current_grid = moves[direction](self.current_grid)
                return True
            else:
                return False

    def get_current_grid(self):
        return self.current_grid

    def is_win(self):
        if any(any(i >= self.win_value for i in row) for row in self.current_grid):
            return True
        else:
            return False

    def cellContent(self, list1):
        if self.withinBounds(list1):
            return self.current_grid[list1[0]][list1[1]]

    def cellAvailable(self, list1):
        use_value = ''
        if self.current_grid[list1[0]][list1[1]] == 0:
            use_value = False
            use_value = True
        else:
            use_value = True
            use_value = False
        return use_value

    # // measures how smooth the grid is (as if the values of the pieces
    # // were interpreted as elevations). Sums of the pairwise difference
    # // between neighboring tiles (in log space, so it represents the
    # // number of merges that need to happen before they can merge).
    # // Note that the pieces can be distant
    def smoothness(self):
        smoothness = 0
        for x in range(len(np.transpose(self.current_grid))):
            for y in range(len(np.transpose(self.current_grid[x]))):
                list1 = [x, y]
                # 注意，因为原始代码x，y轴是颠倒的，所以需要np.transpose改变x y对应的坐标
                current_grid_transpose = np.transpose(self.current_grid)
                use_value = current_grid_transpose[x][y]
                if use_value:
                    # print("x={},y={},value1={}".format(x, y, current_grid_transpose[x][y]))
                    value = math.log(current_grid_transpose[x][y])/math.log(2)
                    # print("value= ", value)
                    direction = 1
                    while direction <= 2:
                        vector = self.getVector(direction)
                        # print("vector= ", vector)
                        list1_convert = {'x': list1[0], 'y': list1[1]}
                        # print("list1_convert= ", list1_convert)
                        targetCell = self.findFarthestPosition(list1_convert, vector)['next']
                        # print("targetCell= ", targetCell)
                        targetCell_list = [targetCell['x'], targetCell['y']]

                        if self.cellOccupied_transpose(targetCell_list):
                            target = self.cellContent_transpose(targetCell_list)
                            # print("target= ", target)
                            targetValue = math.log(target) / math.log(2)
                            # print("targetValue= ", targetValue)
                            smoothness -= abs(value - targetValue)
                            # print("smoothness_temp= ", smoothness)
                        direction += 1
        # print("smoothness= ", smoothness)
        return smoothness

    # measures how monotonic the grid is. This means the values of the tiles are strictly increasing
    # // or decreasing in both the left/right and up/down directions
    def monotonicity2(self):
        # // scores for all four directions
        totals = [0, 0, 0, 0]
        size = len(self.current_grid)
        for x in range(size):
            current = 0
            next = current + 1
            while next < 4:
                while next < 4 and self.cellAvailable([x, next]):
                    next += 1
                if next >= 4:
                    next -= 1

                if self.cellOccupied([x, current]):
                    currentValue = math.log(self.cellContent([x, current])) / math.log(2)
                else:
                    currentValue = 0

                if self.cellOccupied([x, next]):
                    nextValue = math.log(self.cellContent([x, next])) / math.log(2)
                else:
                    nextValue = 0
                # //direction   0: up, 1: right, 2: down, 3: left
                if currentValue > nextValue:
                    totals[0] += nextValue - currentValue
                elif nextValue > currentValue:
                    totals[2] += currentValue - nextValue
                current = next
                next += 1

    # // left / right  direction
        for y in range(size):
            current = 0
            next = current + 1
            while next < 4:
                while next < 4 and self.cellAvailable([next, y]):
                    next += 1
                if next >= 4:
                    next -= 1

                if self.cellOccupied([current, y]):
                    currentValue = math.log(self.cellContent([current, y])) / math.log(2)
                else:
                    currentValue = 0

                if self.cellOccupied([next, y]):
                    nextValue = math.log(self.cellContent([next, y])) / math.log(2)
                else:
                    nextValue = 0
                # //direction   0: up, 1: right, 2: down, 3: left
                if currentValue > nextValue:
                    totals[3] += nextValue - currentValue
                elif nextValue > currentValue:
                    totals[1] += currentValue - nextValue
                current = next
                next += 1

        # print("monotonicity2= ",(max(totals[0], totals[2]) + max(totals[3], totals[1])))
        return max(totals[0], totals[2]) + max(totals[3], totals[1])

    def maxValue(self):
        max = 0
        for x in range(len(self.current_grid)):
            for y in range(len(self.current_grid[x])):
                if self.current_grid[x][y] > max:
                    max = self.current_grid[x][y]

        # print("maxValue=",(math.log(max) / math.log(2)))
        return math.log(max) / math.log(2)

    # // counts the number of isolated groups.
    def islands(self):
        size = len(self.current_grid)
        # 先定义一个row ，colum的空2维数组 每个cell里面的值为0
        # 程序中动态定义生成一个2维数组
        list_new = [[0 for col in range(size)] for row in range(size)]

        def list_convert():
            for x in range(size):
                for y in range(size):
                    list_new[x][y] = {'value': 0, 'marked': ''}

            for x in range(len(self.current_grid)):
                for y in range(len(self.current_grid[x])):
                    list_new[x][y]['value'] = self.current_grid[x][y]

        def mark(x, y, value):
            if x >= 0 \
                    and x <= len(list_new) \
                    and y >= 0 \
                    and y <= len(list_new) \
                    and list_new[x][y] != 0 \
                    and list_new[x][y]['value'] == value \
                    and not list_new[x][y]['marked']:

                list_new[x][y]['marked'] = True
                for direction in [0, 1, 2, 3]:
                    vector = self.getVector(direction)
                    mark(x + vector['x'], y + vector['y'], value)

        # 数组转换操　　self.current_grid　→　list_new
        list_convert()
        islands = 0
        for x in range(len(list_new)):
            for y in range(len(list_new[x])):
                if list_new[x][y]['value'] != 0:
                    list_new[x][y]['marked'] = False

        for x in range(len(list_new)):
            for y in range(len(list_new[x])):
                if list_new[x][y]['value'] != 0 and not list_new[x][y]['marked']:
                    islands += 1
                    mark(x, y, list_new[x][y]['value'])

        return islands

    def getVector(self, direction):
        # 0: {x: 0, y: -1}, // up
        # 3: {x: -1, y: 0} // left
        # 2: {x: 0, y: 1}, // down
        # 1: {x: 1, y: 0}, // right
        vector = {0: {'x': 0, 'y': -1}, 3: {'x': -1, 'y': 0}, 2: {'x': 0, 'y': 1}, 1: {'x': 1, 'y': 0}}
        return vector[direction]

    def cellOccupied(self, list1):
        if self.withinBounds(list1):
            if self.current_grid[list1[0]][list1[1]] == 0:
                return False
            else:
                return True
        else:
            return False

    def withinBounds(self, list1):
        size = len(self.current_grid)
        if list1[0]>=0 and list1[0]<size and list1[1]>=0 and list1[1]<size:
            return True
        else:
            return False

    def cellOccupied_transpose(self, list1):
        if self.withinBounds(list1):
            if np.transpose(self.current_grid)[list1[0]][list1[1]] == 0:
                return False
            else:
                return True
        else:
            return False

    def cellAvailable_transpose(self, list1):
        use_value = ''
        if np.transpose(self.current_grid)[list1[0]][list1[1]] == 0:
            use_value = False
            use_value = True
        else:
            use_value = True
            use_value = False
        return use_value

    def cellContent_transpose(self, list1):
        if self.withinBounds(list1):
            return np.transpose(self.current_grid)[list1[0]][list1[1]]

    def findFarthestPosition(self, cell, vector):
        previous = []
        # cell sample   cell=[x,y]
        # // Progress towards the vector direction until an obstacle is found
        while True:
            previous = cell
            cell = {'x': previous['x'] + vector['x'], 'y': previous['y'] + vector['y']}
            list1 = [cell['x'], cell['y']]
            if not (self.withinBounds(list1) and self.cellAvailable_transpose(list1)):
                break
        # // Used to check if a merge is required
        return {'farthest': previous, 'next': cell}

