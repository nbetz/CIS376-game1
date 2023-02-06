import argparse

import engine
import scene

if __name__ == '__main__':
    # setup command line arguments to accept input for width, height, fps,
    parser = argparse.ArgumentParser()
    parser.add_argument('--fps', nargs='?', type=int, default=10,
                        help='Specify the fps for the game')
    parser.add_argument('--tile_size', nargs='?', type=int, default=30,
                        help='Specify the size of the tiles for the game')
    parser.add_argument('--width', nargs='?', type=int, default=720,
                        help='Specify the width of the screen')
    parser.add_argument('--height', nargs='?', type=int, default=480,
                        help='Specify the height of the screen')
    parser.add_argument('--no_walls_start', action='store_false', help='Starts the game with random walls')
    args = parser.parse_args()

    fps = args.fps
    tile = args.tile_size
    width = args.width
    height = args.height
    random_walls_start = True
    randoms_walls_start = args.no_walls_start

    e = engine.Engine(game_fps=fps, screen_width=width, screen_height=height)
    game_scene = scene.MazeScene(tile_size=tile)
    e.add_scene(game_scene)
    e.set_active_scene(game_scene, has_walls=random_walls_start)
    e.loop()
