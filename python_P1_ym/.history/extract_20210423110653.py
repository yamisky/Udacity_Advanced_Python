"""
功能：从CSV和json中提取数据

2021年4月22日17:59:47
"""

import csv 
import json

from models import NearEarthObject, CloseApproach

def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.
    """
    neos = []
    with open(neo_csv_path, 'r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            neo = NearEarthObject(designation=row['pdes'],
                                  name=row['name'],
                                  diameter=row['diameter'],
                                  hazardous=row['pha'],)
            neos.append(neo)
    return neos

def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.
    """
    approaches = []
    with open(cad_json_path) as infile:
        content = json.load(infile)
        data = content['data']

        fields = {}
        for key in content['fields']:
            fields[key] = content['fields'].index(key)
        
        for row in data:
            approach = CloseApproach(designation=row[fields['des']],
                                     time=row[fields['cd']],
                                     distance=row[fields['dist']],
                                     velocity=row[fields['v_rel']],)
            approaches.append(approach)
    return approaches
                                




