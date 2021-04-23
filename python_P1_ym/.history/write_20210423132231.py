"""Write a stream of close approaches to CSV or to JSON.
"""

import csv
import json

def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = {
                'datetime_utc': 'String date object as UTC',
                'distance_au': 'Distance',
                'velocity_km_s': 'Velocity in km/s',
                'designation': 'Designation',
                'name': 'Name',
                'diameter_km': 'Diameter in km',
                'potentially_hazardous': 'Potentially hazardous',
    }

    with open(filename, 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames.keys())
        writer.writeheader() # 写入表头
        for result in results:
            cad_