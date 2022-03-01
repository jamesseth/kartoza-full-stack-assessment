import geopy.distance

def calculate_distance(coord_start, coord_end ):
    return geopy.distance.vincenty(coord_start, coord_end).km
