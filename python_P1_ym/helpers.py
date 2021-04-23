
import datetime

# strptime： string类型 转化成 datetime类型
def cd_to_datetime(calendar_date):
    """
    :参数 calendar_date: A calendar date in YYYY-bb-DD hh:mm format.
    :return: A naive `datetime` corresponding to the given calendar date and time.
    """
    return datetime.datetime.strptime(calendar_date, "%Y-%b-%d %H:%M")

# strftime：datetime 类型转化成 string类型
def datetime_to_str(dt):
    """
    :param dt: A naive Python datetime.
    :return: That datetime, as a human-readable string without seconds.
    """
    return datetime.datetime.strftime(dt, "%Y-%m-%d %H:%M")