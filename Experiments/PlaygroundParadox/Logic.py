from casino_games.BloodTiles import BloodTiles
from Components.casino_terminal import casino

def blood_tiles(post_data):
    blood_experiment = BloodTiles()
    get_data = blood_experiment.start_simulate(post_data)
    return get_data



casino(1000, blood_tiles_fun=blood_tiles)



