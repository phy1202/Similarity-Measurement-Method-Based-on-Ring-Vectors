class Constants:

    """
    记录直线上坐标变化的四种情况
    """
    Y_TO_POSITIVE = 1
    Y_TO_NEGATIVE = 2
    X_TO_POSITIVE = 3
    X_TO_NEGATIVE = 4

    """
    记录象限的常量
    """
    FIRST_QUADRAN = 1
    SECOND_QUADRAN  = 2
    THIRD_QUADRAN = 3
    FOURTH_QUADRAN = 4

    """
    异常常量
    """
    Y_IS_ZERO = -9999999
    X_IS_ZERO = -9999998

    """
    三环经纬度范围
    """
    SANHUAN_LAT_MAX = 39.967249
    SANHUAN_LAT_MIN = 39.856128
    SANHUAN_LNG_MIN = 116.304153
    SANHUAN_LNG_MAX = 116.455655


    """
    四环经纬度范围
    """

    SIHUAN_LAT_MAX = 39.98624
    SIHUAN_LAT_MIN = 39.83077
    SIHUAN_LNG_MAX = 116.48379
    SIHUAN_LNG_MIN = 116.26803

    """
    北京市经纬度范围
    """

    BJ_LAT_MAX =  40.557625
    BJ_LAT_MIN = 39.4390
    BJ_LNG_MAX = 117.5102
    BJ_LNG_MIN = 115.4164

    """
    六环经纬度范围
    """
    LIUHUAN_LNG_MIN = 116.08824
    LIUHUAN_LNG_MAX = 116.73703
    LIUHUAN_LAT_MIN = 39.68903
    LIUHUAN_LAT_MAX = 40.25058


    """
    底层数据类型
    """
    WIFI = "WIFI"
    POI = "POI"
    DEM = "DEM"

    """
    栅格范围
    """

    SIHUAN = "SIHUAN"
    BEIJING = "BEIJING"
    LIUHUAN = "LIUHUAN"

    """
    距离计算方式
    """
    EUCLIDEAN_DISTANCE = "EUCLIDEAN_DISTANCE"
    EMD = "EMD"
    COSINE_DISTANCE = "COSINE_DISTANCE"
