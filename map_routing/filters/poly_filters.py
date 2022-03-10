"""Implement an Object to apply filtering to a Polygon."""
import statistics
from typing import List
from typing import Tuple


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

    MAP_CENTER = None

    def __init__(self, poly):
        """Instantiate object."""
        self.file_id = poly['file_id']
        self.name = poly.get('name', '')
        self.polygon = poly['coords']
        self.lat_coords = []
        self.lon_coords = []
        self.center_of_poly = None
        self.dummy_value = '*'
        self.filtered_poly = []
        self.split_coords()
        self.execute()

    def split_coords(self) -> None:
        """
        Take the polygon coordinates and splits them into two lists.

        One for latitudes and one for longitudes.
        """
        for point in self.polygon:
            for lon, lat in point:
                self.lat_coords.append(lat)
                self.lon_coords.append(lon)

    def join_coords(self) -> List[Tuple]:
        """
        Take the lat and lon coordinates and return coordinates.

        :return: A list of tuples.
        """
        return list(zip(*[self.lat_coords, self.lon_coords]))

    def get_difference(self, numbers: List[float], count: int = 1) -> List[float]:
        """Calculate the count difference of the parsed numbers."""
        if count > 0:
            count -= 1
            results = []
            for index in range(0, len(numbers) - 1):
                results.append(numbers[index + 1] - numbers[index])

            return self.get_difference(results, count)

    def interpolate_coords(self, coords) -> List[float]:
        """
        Apply linear interpolation to spikes.

        :param coords: List of coordinates to process.
        :return: Interpolate series of coordinates.
        """
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

    def filter_by_stddev(self, numbers: List[float], tolerance: float = 1.2):
        """
        Replace coordinate greater than the standard deviation times a tolerance.

        :param numbers: The list of numbers to filter
        :param tolerance: The tolerance is a value that is multiplied
                          by the standard deviation
        :return: A list of coordinates.
        """
        curr_stdev = statistics.stdev(numbers)

        results = []
        for index in range(0, len(numbers)-1):
            if (curr_stdev * -tolerance <=
                    numbers[index] - numbers[index + 1]
                    <= curr_stdev * tolerance):
                results.append(numbers[index])
            else:
                results.append(self.dummy_value)

        return self.interpolate_coords(results)

    def get_center_of_polly(self):
        """Calculate the center of all polygons to center the map."""
        lat_cnt = (max(self.lat_coords) + min(self.lat_coords)) * .5
        lon_cnt = (max(self.lon_coords) + min(self.lon_coords)) * .5
        if PolySpikeFilter.MAP_CENTER:
            lat_cnt = (lat_cnt + PolySpikeFilter.MAP_CENTER[0]) * .5
            lon_cnt = (lon_cnt + PolySpikeFilter.MAP_CENTER[1]) * .5
        PolySpikeFilter.MAP_CENTER = (lat_cnt, lon_cnt)

    def execute(self):
        """Apply filter to polygon."""
        self.lat_coords = self.filter_by_stddev(self.lat_coords)
        self.lon_coords = self.filter_by_stddev(self.lon_coords)
        self.get_center_of_polly()
        self.filtered_poly = self.join_coords()
