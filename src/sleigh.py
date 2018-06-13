class Sleigh:
    def __init__(self, size_x, size_y):
        # Present parameters
        self.present_max_rotations = 5

        # Matrix parameters
        self.size_x = size_x
        self.size_y = size_y

        # Layer parameters
        self.layer = 1
        self.layer_bottom = 0

        # Maxrects free space
        self.free_space = [(1, 1, self.size_x, self.size_y)]

    # Loop to fit a present
    def fit_present(self, present):
        while True:
            point = False

            # Start finding a space to fit the
            # present.
            # (this is not an heuristic search, it just
            # select the left and top most space)
            for space in self.free_space:
                if(space[2] >= present.x and space[3] >= present.y):
                    point = (space[0], space[1], self.layer)
                    break

            # If there are no spaces that fit
            # the present, than change layer.
            if(point == False):
                self.next_layer()
                continue

            # Update layer height.
            if(self.layer_bottom < self.layer + present.z):
                self.layer_bottom = self.layer + present.z

            # Update free space
            self.update_space(point, present)

            return point
    
    # Set next layer
    def next_layer(self):
        # Change layer
        self.layer = self.layer_bottom + 1
        self.layer_bottom += 1

        # Reset free space    
        self.free_space = [(1, 1, self.size_x, self.size_y)]

    # Check if there are spaces that intersect
    # with the given present-point and split them.
    def update_space(self, point, present):
        new_rects = []
        
        for sid in range(0, len(self.free_space)): 
            if(self._intersects(self.free_space[sid], point, present) == True):
                new_rects = self._split(self.free_space[sid], point, present)

                # Change element into his splits
                self.free_space[sid] = new_rects
        
        # Flatten
        # (We have to be sure that the item
        # to flat is not a tuple).
        # i = item  s = sublist
        self.free_space = [i for s in self.free_space for i in s if isinstance(s, list)]

        # Sort
        self.free_space = sorted(self.free_space, key = lambda s: (s[1], s[0]))

    
    # Check if the present at the given point
    # overlaps the given space.
    def _intersects(self, space, point, present):
        # If the point is above
        if(point[1] + present.y < space[1]):
            return False
        # If the point is below
        if(point[1] > space[1] + space[3]):
            return False
        # If the point is to the left
        if(point[0] + present.x < space[0]):
            return False
        # If the point is to the right
        if(point[0] > space[0] + space[2]):
            return False
        # Else...
        return True
    
    # From a point and a present, splits the
    # given space in at most 4 pieces.
    def _split(self, space, point, present):
        new_rects = []
        
        # If present left is more than the space left
        if(point[0] > space[0]):
            new_rects.append((space[0], space[1], point[0] - space[0], space[3]))
        # If present right is less than the space right
        if(point[0] + present.x < space[0] + space[2]):
            new_rects.append((point[0] + present.x, space[1], (space[0] + space[2]) - (point[0] + present.x), space[3]))
        # If present top is more than the space top
        if(point[1] > space[1]):
            new_rects.append((space[0], space[1], space[2], point[1] - space[1]))
        # If present botton is less then the space bottom
        if(point[1] + present.y < space[1] + space[3]):
            new_rects.append((space[0], point[1] + present.y, space[2], (space[1] + space[3]) - (point[1] + present.y)))
       
        return new_rects