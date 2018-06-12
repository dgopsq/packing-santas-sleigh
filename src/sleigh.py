class Sleigh:
    def __init__(self, size_x, size_y):
        # Present parameters
        self.present_max_rotations = 3

        # Matrix parameters
        self.size_x = size_x
        self.size_y = size_y

        # Layer parameters
        self.layer = 1
        self.layer_bottom = 0

        # Shelf size
        self.shelf_x = 1
        self.shelf_y = 1
        self.shelf_bottom = 1

    # Loop to fit a present
    def fit_present(self, present):
        while True:
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
                continue

            # If adding a new shelf is not wrong
            # the let's add it
            self.next_shelf()

    # Set next shelf
    def next_shelf(self):
        self.shelf_x = 1
        self.shelf_y = self.shelf_bottom + 1
        self.shelf_bottom += 1

    # Set next layer
    def next_layer(self):
        # Change layer
        self.layer = self.layer_bottom + 1
        self.layer_bottom += 1

        # Reset shelf    
        self.shelf_x = 1
        self.shelf_y = 1
        self.shelf_bottom = 1 