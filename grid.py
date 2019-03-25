import math

def transpose(field):
    return [list(row) for row in zip(*field)]


def invert(field):
    return [row[::-1] for row in field]


def move_is_possible(direction, field):
    def row_is_left_movable(row):
        def change(i):  # true if there'll be change in i-th tile
            if row[i] == 0 and row[i + 1] != 0: # Move
                return True
            if row[i] != 0 and row[i + 1] == row[i]: # Merge
                return True
            return False
        return any(change(i) for i in range(len(row) - 1))

    check = {}
    check[3] = lambda field:                              \
            any(row_is_left_movable(row) for row in field)

    check[1] = lambda field:                              \
                check['Left'](invert(field))

    check[0] = lambda field:                              \
            check['Left'](transpose(field))

    check[2] = lambda field:                              \
            check['Right'](transpose(field))

    if direction in check:
        # //direction   0: up, 1: right, 2: down, 3: left
        return check[direction](field)
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
        moves[3] = lambda field:                              \
                [move_row_left(row) for row in field]
        moves[1] = lambda field:                              \
                invert(moves['Left'](invert(field)))
        moves[0] = lambda field:                              \
                transpose(moves['Left'](transpose(field)))
        moves[2] = lambda field:                              \
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
        for x in range(len(self.current_grid)):
            for y in range(len(self.current_grid[x])):
                list1=[x,y]
                use_value = self.cellAvailable(list1)
                if use_value:
                    value = math.log(self.cellContent(list1))/math.log(2)
                    direction = 1
                    while direction <= 2:
                        vector = self.getVector(direction)
                        targetCell = self.findFarthestPosition(list1, vector)['next']
                        list1 = [targetCell['x'], targetCell['y']]
                        if self.cellOccupied(list1):
                            target = self.cellContent(list1)
                            targetValue = math.log(target) / math.log(2)
                            smoothness -= abs(value - targetValue)
                        direction += 1
        return smoothness

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

    def cellOccupied(self,list1):
        if self.current_grid[list1[0]][list1[1]] == 0:
            return False
        else:
            return True

    def withinBounds(self,list1):
        size = len(self.current_grid)
        if list1[0]>=0 and list1[0]<size and list1[1]>=0 and list1[1]<size:
            return True
        else:
            return False

    def findFarthestPosition(self, cell, vector):
        previous = []
        # cell sample   cell=[x,y]
        # // Progress towards the vector direction until an obstacle is found
        while True:
            previous = cell
            cell = {'x': previous[0] + vector['x'], 'y': previous[1] + vector['y']}
            list1 = [cell['x'], cell['y']]
            if not (self.withinBounds(list1) and self.cellAvailable(list1)):
                break

        # // Used to check if a merge is required
        return {'farthest': previous, 'next': cell}

