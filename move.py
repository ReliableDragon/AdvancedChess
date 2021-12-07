
class Move():
    def __init__(self, coords, path=None):
        self.row = coords[0]
        self.col = coords[1]
        self.path = path

    def to_json_compatible(self):
        return [[self.row, self.col], self.path]

    def __str__(self):
        return f"({self.row}, {self.col}){str(self.path)})"

    def __repr__(self):
        return f"Move(({self.row}, {self.col}), {str(self.path)})"

    def __lt__(self, other):
        if self.row < other.row:
            return True
        if self.col < other.col:
            return True
        if self.path < other.path:
            return True

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col and self.path == other.path

    def __hash__(self):
        return hash(self.row) ^ hash(self.col) ^ hash(tuple(self.path))
