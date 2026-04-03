from .casino_games.BloodTiles import BloodTiles


def blood_tiles(post_data):
    blood_experiment = BloodTiles()
    get_data = blood_experiment.start_simulate(post_data)
    return get_data
