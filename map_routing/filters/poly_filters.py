import statistics
from typing import List
from typing import Tuple

class CoordSpike():
    def __init__(self,series, index, value):
        self.series = series
        self.index = index
        self.value = value
        self.results = value



class PolySpikeFilter():
    """
    Filter a polygon via coordinates with no time or sample data rate.
    The filtering takes the following steps:
        1. Split coordinates into latitude and longitude lists.
        2. Calculate the first difference for both list of coordinates.
        3. Calculate the standard deviation for both set of coordinates.
        4. Remplace out lying values with dummy values.
        5. Replace dummy values using linear interprolation.
        6. join processed coordinates into a list of paired coordinates.
        7. return the results.
    """

    def __init__(self, poly):
        """Instantiate object."""
        self.polygon = poly
        self.lat_coords = []
        self.lon_coords = []
        self.dummy_value = '*'
        self.split_coords()

    def split_coords(self) -> None:
        """
        Take the polygon coordinates and splits them into two lists.

        One for latitudes and one for longitudes.
        """
        for point in self.polygon:
            for lat, lon in point:
                self.lat_coords.append(lat)
                self.lon_coords.append(lon)

    def join_coords(self) -> List[Tuple]:
        """
        Takes the lat and lon coordinates and returns a list of tuples of coordinates.
        :return: A list of tuples.
        """
        return list(zip(*[self.lat_coords, self.lon_coords]))

    def get_difference(self, numbers, count=1):
        if count > 0:
            count -= 1
            results = []
            for index in range(0, len(numbers) - 1):
                results.append(numbers[index + 1] - numbers[index])

            return self.get_difference(results, count)

    def interpolate_coords(self, coords):
        previous_number = None
        spike_found = False
        spike_index = None

        while self.dummy_value in coords:
            for index, value in enumerate(coords):
                if value != self.dummy_value and spike_found is False:
                    previous_number = value
                elif value == self.dummy_value and spike_found is False:
                    spike_found = True
                    spike_index = index

                elif value != self.dummy_value and spike_found is True:
                    coords[spike_index] = (value + previous_number) / 2
                    previous_number = None
                    spike_found = False
                    spike_index = None
                    break
        return coords

    def filter_by_stddev(self, numbers, tolerance=1.2):
        curr_stdev = statistics.stdev(numbers)

        results = []
        for index in range(0, len(numbers)-1):
            if curr_stdev * -tolerance <= numbers[index] - numbers[index + 1] <= curr_stdev * tolerance:
                results.append(numbers[index])
            else:
                results.append(270.0)

        return self.interpolate_coords(results)
