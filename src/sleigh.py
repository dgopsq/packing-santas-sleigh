from itertools import combinations

class Sleigh:
    def __init__(self, size_x, size_y):
        # Present parameters
        self.present_max_rotations = 5
        self.max_consecutive_not_fitted = 10

        # Matrix parameters
        self.size_x = size_x
        self.size_y = size_y

        # Layer parameters
        self.layer = 1
        self.layer_bottom = 0

        # Maxrects free space
        self.free_space = [(1, 1, self.size_x, self.size_y)]

        # Non-fitted presents
        self.consecutive_not_fitted = 0

    # Loop to fit a present
    def fit_present(self, present):
        while True:
<<<<<<< HEAD
            point = False

            # Start finding a space to fit the
            # present.
            # Heuristic stuff...

            # Top-left most
            '''
            self.free_space = sorted(self.free_space, key = lambda s: (s[1], s[0]))
            for space in self.free_space:
                if(space[2] >= present.x and space[3] >= present.y):
                    point = (space[0], space[1], self.layer)
                    break
            '''

            # Best area fit
            fit_spaces = [s for s in self.free_space if s[2] >= present.x and s[3] >= present.y]
            fit_spaces = sorted(fit_spaces, key = lambda s: s[2] * s[3])

            if(len(fit_spaces) > 0):
                point = (fit_spaces[0][0], fit_spaces[0][1], self.layer)

            # No space found
            if(point == False):
                self.consecutive_not_fitted += 1
                self.next_empty_layer()
=======
            for rotation in range(0, self.present_max_rotations):
                # If there is not enough orizontal space
                if(self.shelf_x + present.x > self.size_x):
                    present.next_rotation()
                    continue

                # If there is not enough vertical space
                if(self.shelf_y + present.y > self.size_y):
                    present.next_rotation()
                    continue

                point = (self.shelf_x, self.shelf_y, self.layer)

                # Update shelf position
                self.shelf_x += present.x + 1

                # Update shelf height
                if(self.shelf_bottom < self.shelf_y + present.y):
                    self.shelf_bottom = self.shelf_y + present.y

                # Update layer height
                if(self.layer_bottom < self.layer + present.z):
                    self.layer_bottom = self.layer + present.z

                # Present fitted!
                return point

            # Reset present
            present.set_default_rotation()

            # If we completed the layer
            if(self.shelf_bottom >= self.size_y):
                self.next_layer()
>>>>>>> 4798d980bdc750b0196c20788182d73b8749f516
                continue

            # Update layer height.
            if(self.layer_bottom < self.layer + present.z):
                self.layer_bottom = self.layer + present.z

            # Update free space
            self.update_space(point, present)

            # Reset not fitted items
            self.consecutive_not_fitted = 0

            return point
    
    # Set next layer
    def next_layer(self):
        # Change layer
        self.layer += 1

    # Set next empty layer
    def next_empty_layer(self):
        # Change layer
        self.layer = self.layer_bottom + 1
        self.layer_bottom += 1

        # Reset free space    
        self.free_space = [(1, 1, self.size_x, self.size_y)]

        # Reset not fitted items
        self.consecutive_not_fitted = 0
    
    # Check whether it's time to switch
    # to a whole new layer.
    def is_time_to_change(self):
        return self.consecutive_not_fitted >= self.max_consecutive_not_fitted

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
        flat_list = []

        for sublist in self.free_space:
            # If it's a tuple, then don't flat it
            if(isinstance(sublist, tuple)):
                flat_list.append(sublist)
            else:
                for item in sublist:
                    flat_list.append(item)
        
        self.free_space = flat_list

        # Remove duplicates and contained spaces
        self._remove_duplicates()
    
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

    # Remove duplicates and contained spaces
    def _remove_duplicates(self):
        contained = set()
        for s1, s2 in combinations(self.free_space, 2):
            if(self._contains(s1, s2)):
                contained.add(s2)
            elif(self._contains(s2, s1)):
                contained.add(s1)

        self.free_space = [s for s in self.free_space if s not in contained]
        
    # Check wheter space1 contains space2
    def _contains(self, space1, space2):
        return (space1[0] <= space2[0] and \
                space1[1] <= space2[1] and \
                space1[0] + space1[2] >= space2[0] + space2[2] and \
                space1[1] + space1[3] >= space2[1] + space2[3])