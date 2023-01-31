import game_object
import pygame


class Scene:

    def __init__(self, engine):
        self.engine = engine
        self.screen = engine._screen
        self.tile_size = engine._tile_size
        self.height = engine._screen_height
        self.width = engine._screen_width
        self.game_objects = []
        self.previous_game_objects = []


    def initial_grid(self):
        for y in range(0, self.height, self.tile_size):
            for x in range(0, self.width, self.tile_size):
                rectangle = game_object.Rectangle(False, x, y)
                self.game_objects.append(rectangle)
                self.draw()
        pass

    def input(self):
        pass

    def update(self):
        #for cell in self.game_objects:
            #self.check_cell(cell)
        pass

    def valid_input(self, x, y):
        if x >= 0 and x < self.width:
            if y>=0 and y < self.height:
                return 1

        return 0
        pass


    def check_cell(self, cell):
        currentIndex = self.game_objects.index(cell)
        count = 0
        #top left
        if self.valid_input(cell.x-self.tile_size, cell.y-self.tile_size) == 1:
            if self.game_objects[int(currentIndex-(self.width/self.tile_size)+1)].isAlive == True:
                count = count+1
        #top
        if self.valid_input(cell.x, cell.y-self.tile_size) == 1:
            if self.game_objects[int(currentIndex-(self.width/self.tile_size))].isAlive == True:
                count = count+1
        #top right
        if self.valid_input(cell.x+self.tile_size, cell.y-self.tile_size) == 1:
            if self.game_objects[int(currentIndex-(self.width/self.tile_size)-1)].isAlive == True:
                count = count+1
        #left
        if self.valid_input(cell.x-self.tile_size, cell.y) == 1:
            if self.game_objects[currentIndex-1].isAlive == True:
                count = count+1
        #right
        if self.valid_input(cell.x+self.tile_size, cell.y) == 1:
            if self.game_objects[currentIndex-1].isAlive == True:
                count = count+1
        #bottom left
        if self.valid_input(cell.x-self.tile_size, cell.y+self.tile_size) == 1:
            if self.game_objects[int(currentIndex+(self.width/self.tile_size)-1)].isAlive == True:
                count = count+1
        #bottom
        if self.valid_input(cell.x, cell.y+self.tile_size) == 1:
            if self.game_objects[int(currentIndex+(self.width/self.tile_size))].isAlive == True:
                count = count+1
        #bottom right
        if self.valid_input(cell.x+self.tile_size, cell.y+self.tile_size) == 1:
            if self.game_objects[int(currentIndex+(self.width/self.tile_size)+1)].isAlive == True:
                count = count+1

        if cell.isAlive == True:
            if count < 1 or count > 4:
                cell.isAlive = False
        else:
            if count == 3:
                cell.isAlive = True
        pass



    def draw(self):
        for item in self.game_objects:
            color = item.color
            rect = pygame.Rect(item.x, item.y, self.tile_size-1, self.tile_size-1)
            pygame.draw.rect(self.screen, color, rect)
        pass

    #def update_all_objects(self):
        # calls update() method for all updatable game objects in scene
        #[game_obj.update() for game_obj in self.game_objects if isinstance(game_obj, game_object.Updatable)]

    #def draw_all_objects(self):
        # calls draw() method for all drawable game objects in scene
        #[game_obj.draw() for game_obj in self.game_objects if isinstance(game_obj, game_object.Drawable)]

