from math import sin, cos, asin, sqrt, pi


class Distance(object):
    """计算两个经纬度之间的距离"""
    EARTH_REDIUS = 6378.137

    @classmethod
    def rad(cls, d):
        return d * pi / 180.0

    @classmethod
    def getDistance(cls, lat1, lng1, lat2, lng2):
        """返回距离的单位是米"""
        radLat1 = cls.rad(lat1)
        radLat2 = cls.rad(lat2)
        a = radLat1 - radLat2
        b = cls.rad(lng1) - cls.rad(lng2)
        s = 2 * asin(sqrt(pow(sin(a / 2), 2) + cos(radLat1) * cos(radLat2) * pow(sin(b / 2), 2)))
        s = s * cls.EARTH_REDIUS
        return s * 1000


if __name__ == '__main__':
    print(Distance.getDistance(116.383177, 39.68516, 116.289286, 39.685216))