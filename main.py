import engine
import scene

# Noah Betz moved engine creation to main.py
if __name__ == '__main__':
    fps = 10
    tile = 30
    width, height = 720, 480

    e = engine.Engine(game_fps=fps, screen_width=width, screen_height=height)
    game_scene = scene.MazeScene(tile_size=tile)
    e.add_scene(game_scene)
    e.set_active_scene(game_scene)
    e.loop()
