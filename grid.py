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
