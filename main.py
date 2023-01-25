import engine

# Noah Betz moved engine creation to main.py
if __name__ == '__main__':
    fps = 10
    tile = 30
    width, height = 720, 480

    e = engine.Engine(game_fps=fps, tile_size=tile, screen_width=width, screen_height=height)
    e.loop()

