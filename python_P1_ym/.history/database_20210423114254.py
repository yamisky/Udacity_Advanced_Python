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

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        # filter()函数用于过滤序列，过滤掉不符合条件的元素，返回符合条件的元素组成新列表。
        if filter:
            for approach in self._approaches:
                if all(map(lambda f: f(approach), filters)):
                    yield approach
        else:
            for approach in self._approaches:
                yield approach