import game_object


class Scene:
    game_objects: list

    def __init__(self):
        pass

    def update_all_objects(self):
        # calls update() method for all updatable game objects in scene
        [game_obj.update() for game_obj in self.game_objects if isinstance(game_obj, game_object.Updatable)]

    def draw_all_objects(self):
        # calls draw() method for all drawable game objects in scene
        [game_obj.draw() for game_obj in self.game_objects if isinstance(game_obj, game_object.Drawable)]

    # TODO
    def add_object(self):
        pass

    # TODO
    def remove_object(self):
        pass
