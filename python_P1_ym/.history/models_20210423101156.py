"""
功能：接收CSV和json中信息的类

2021年4月23日
"""

from helpers import cd_to_datetime, datetime_to_str

class NearEarthObject:
    """近地天体的基本信息类，处理neos.csv文件
    """
    def __init__(self, **info):
        """参数 info: 一个字典.
        例子：
        dict_info = {'designation':'编号GT520', 'time':'哈雷彗星', 'diameter':101, 'hazardous':'Y'}
        neo = NearEarthObject(**dict_info)
        """
        self.designation = (str(info['designation']) if info['designation'] else '')
        self.name = str(info['name']) if info['name'] else None
        self.diameter = (float(info['diameter']) if info['diameter'] else float('nan'))
        self.hazardous = True if info['hazardous'] == 'Y' else False

        self.approaches = []

    #加了@property后，可以用调用属性的形式来调用方法,后面不需要加（）
    @property
    def fullname(self):
        return f"{self.designation} ({self.name or 'N/A'})"

    #print(类的实例名)时，会调用此方法。功能相当于此实例的“自我介绍”。
    def __str__(self):
        return (f"""{self.fullname} 是一个直径为 """
                f"""{self.diameter:.3f}km 且 """
                f"""{'具有' if self.hazardous else '不具有'} 危险的近地天体。""")

    # print(类的实例名)时，当类中没有__str__方法的时候，会去调用__repr__方法，所以一般类中需要定义repr方法
    # 也可以直接这样调用__repr__方法：print(repr(类的实例名))
    # 如果没有自定义__repr__方法和__str__方法，print(类的实例名)时输出默认的__repr__方法：“类名+object at+内存地址”
    def __repr__(self):
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")


class CloseApproach:
    """临近地球时的状态类，处理cad.json文件
    """
    def __init__(self, **info):
        """参数 info: 一个字典.
        """
        self._designation = (str(info['designation']) if info['designation'] else '')
        self.time = cd_to_datetime(info['time']) if info['time'] else None
        self.distance = float(info['distance']) if info['distance'] else 0.0
        self.velocity = float(info['velocity']) if info['velocity'] else 0.0
        self.neo = None

    @property
    def fullname(self):
        return f"{self._designation} ({self.neo.name or 'N/A'})"

    def serialize(self):
        result = {
            'datetime_utc': datetime_to_str(self.time),
            'distance_au': self.distance,
            'velocity_km_s': self.velocity,
            'neo': {
                'designation': self.neo.designation,
                'name': self.neo.name,
                'diameter_km': self.neo.diameter,
                'potentially_hazardous': self.neo.hazardous
            },
        }
        return result