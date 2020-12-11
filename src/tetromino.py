class Tetromino:
    configurations = [
        [[1,5,9,13], [4,5,6,7]], # Line
        [[1,4,5,6], [1,4,5,9], [1,5,6,9], [4,5,6,9]], # T
        [[1,2,5,9,13], [4,5,6,7,11], [2,6,10,14,13], [4,8,9,10,11]], # L1
        [[1,2,6,10,14], [7,8,9,10,11], [1,5,9,13,14], [4,5,6,7,8]], # L2
        [[1,2,5,6]], # Box
        [[1,5,6,10], [6,7,9,10]], # Step 1
        [[2,5,6,9], [5,6,10,11]] # Step 2
    ]

    def __init__(self, x, y, typ):
        self.x = x
        self.y = y
        self.type = typ # random.randint(0, len(self.configurations) - 1)
        self.rotation = 0

    def current(self):
        return self.configurations[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.configurations[self.type])

