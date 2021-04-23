"""
功能：新数据库类，封装NEOs数据和close approach数据），

2021年4月23日
"""


class NEODatabase:
    def __init__(self, neos, approaches):
        self._neos = neos
        self._approaches = approaches

        self._data = {}

        for approach in self._approaches:
            if approach._designation not in self._data:
                self._data[approach._designation] = {
                    'approaches': [],
                    'neo': None,
                }
            self._data[approach._designation]['approaches'].append(approach)

        for neo in self._neos:
            if neo.designation not in self._data:
                self._data[neo.designation] = {
                    'approaches': [],
                    'neo': None,
                }
            self._data[neo.designation]['neo'] = neo

            if neo.name not in self._data:
                self._data[neo.name] = neo.designation
            
            #???????????????
            neo.approaches.extend(self._data[neo.designation]['approaches'])

        #???????????????
        for approach in self._approaches:
            approach.neo = self._data[approach._designation]['neo']


    def get_neo_by_desiganetion(self, designation):
        if designation in self._data:
            return self._data[designation]['neo']
        return None

    def get_neo_by_name(self, name):
        if name in self._data:
            return self.get_neo_by_designation(self._data[name])
        return None