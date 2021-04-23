"""提供用于查询 close approaches 的筛选器并限制生成的结果。
"""

import operator
from itertools import islice


class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""


class AttributeFilter:
    """可比较属性过滤器的通用父类。
    """
    def __init__(self, op, value):
        """从一个二元谓词和一个引用值构造一个新的“AttributeFilter”。

        :param op: A 2-argument predicate comparator (such as `operator.le`).
        :param value: The reference value to compare against.
        """
        self.op = op
        self.value = value

    def __call__(self, approach):
        """Invoke `self(approach)`."""
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """从 CloseApproach 中获取感兴趣的属性

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of an attribute of interest, comparable to `self.value` via `self.op`.
        """
        raise UnsupportedCriterionError

    def __repr__(self):
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"




class DistanceFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.distance


class DateFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.time.date()


class VelocityFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.velocity


class DiameterFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.neo.diameter


class HazardousFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.neo.hazardous



def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None):
    """从用户指定的条件创建筛选器集合。

    :param date: A `date` on which a matching `CloseApproach` occurs.
    :param start_date: A `date` on or after which a matching `CloseApproach` occurs.
    :param end_date: A `date` on or before which a matching `CloseApproach` occurs.
    :param distance_min: A minimum nominal approach distance for a matching `CloseApproach`.
    :param distance_max: A maximum nominal approach distance for a matching `CloseApproach`.
    :param velocity_min: A minimum relative approach velocity for a matching `CloseApproach`.
    :param velocity_max: A maximum relative approach velocity for a matching `CloseApproach`.
    :param diameter_min: A minimum diameter of the NEO of a matching `CloseApproach`.
    :param diameter_max: A maximum diameter of the NEO of a matching `CloseApproach`.
    :param hazardous: Whether the NEO of a matching `CloseApproach` is potentially hazardous.
    :return: A collection of filters for use with `query`.
    """
    queries = []

    if date:
        queries.append(DateFilter(operator.eq, date))
    if start_date:
        queries.append(DateFilter(operator.ge, start_date))
    if end_date:
        queries.append(DateFilter(operator.le, end_date))
    if distance_min:
        queries.append(DistanceFilter(operator.ge, distance_min))
    if distance_max:
        queries.append(DistanceFilter(operator.le, distance_max))
    if velocity_min:
        queries.append(VelocityFilter(operator.ge, velocity_min))
    if velocity_max:
        queries.append(VelocityFilter(operator.le, velocity_max))
    if diameter_min:
        queries.append(DiameterFilter(operator.ge, diameter_min))
    if diameter_max:
        queries.append(DiameterFilter(operator.le, diameter_max))
    if hazardous is not None:
        queries.append(HazardousFilter(operator.eq, hazardous))

    return queries



def limit(iterator, n=None):
    """从迭代器生成有限定性的values流。

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """
    if n:
        return islice(iterator, n)
    else:
        return iterator
