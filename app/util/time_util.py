from datetime import datetime, timedelta
import re


def format_datetime(
        date_str,
        strptime_format: str = "%Y-%m-%dT%H:%M:%SZ",
        strftime_format: str = "%Y-%m-%d %H:%M:%S"
):
    # 原始日期时间字符串
    # date_str = '2024-07-09T10:30:14Z'

    # 将字符串解析为datetime对象 "%Y-%m-%dT%H:%M:%SZ“
    dt = datetime.strptime(date_str, strptime_format)

    # 将datetime对象格式化为指定的格式，输出 2024-07-15 10:35:05
    formatted_time = dt.strftime(strftime_format)
    return formatted_time


# 正则表达式匹配日期格式
date_patterns = {
    r"\w{3}, \d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2} [\+\-]\d{4}": "%a, %d %b %Y %H:%M:%S %z",
    r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\s*[\+\-]\d{4}": "%Y-%m-%d %H:%M:%S %z",
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}": "%Y-%m-%dT%H:%M:%S%z",
    r"\w{3}, \d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2} GMT": "%a, %d %b %Y %H:%M:%S %Z",
    r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}": "%Y-%m-%d %H:%M:%S",
}

# 资讯统一时间格式 Jun 14, 2024 at 02:54:35 PM
def rss_format_datetime(date_str, input_format="%Y-%m-%d %H:%M:%S"):
    # 将输入的字符串日期转换为datetime对象
    dt = datetime.strptime(date_str, input_format)

    # 使用strftime来格式化时间
    formatted_time = dt.strftime("%b %d, %Y at %I:%M:%S %p")

    return formatted_time

# 时间归类统一时间格式 Wednesday, Jun 14
def days_format_time(date_str, input_format="%Y-%m-%d"):
    # 将输入的字符串日期转换为datetime对象
    dt = datetime.strptime(date_str, input_format)

    # 获取今天的日期
    today = datetime.today().date()

    # 检查输入的日期是否是今天
    if dt.date() == today:
        return "Today"

    # 检查输入的日期是否是昨天
    yesterday = today - timedelta(days=1)
    if dt.date() == yesterday:
        return "Yesterday"

    # 如果不是今天或昨天，返回格式化的日期
    return dt.strftime("%A, %b %d")

# 适配字符串日期格式，并统一输出 %Y-%m-%d %H:%M:%S
def format_datetime_pattern(date_str):
    for pattern, strptime_format in date_patterns.items():
        if re.match(pattern, date_str):
            # 默认输出格式 2024-07-15 10:35:05
            return format_datetime(date_str, strptime_format)
    return None  # 如果没有匹配的格式，返回 None 或适当的错误处理


def format_date(time_str):
    # 原始日期时间字符串
    # Fri, 24 May 2024 19:05:59 +0800

    # 使用datetime.strptime进行解析，%a代表星期几的简写，%d代表日，%b代表月份的简写，%Y代表四位数的年份，%H代表小时，%M代表分钟，%S代表秒
    dt = datetime.strptime(time_str, "%a, %d %b %Y %H:%M:%S %z")

    # 使用strftime进行格式化，按照年-月-日 时:分:秒的顺序
    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


def format_time(time_str):
    # 原始日期时间字符串
    # date_string = '2024-07-09T10:30:14Z'

    # 将字符串解析为datetime对象
    # 注意：由于日期字符串包含时区信息（Z表示UTC），我们需要考虑时区
    date_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')

    # 将datetime对象格式化为指定的格式
    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date


def iso8601_to_hhmmss(iso8601_str):
    # 原始日期时间字符串
    # iso8601_str = ‘PT4M13S’

    # 初始化时分秒
    hours = 0
    minutes = 0
    seconds = 0

    # 处理小时
    if 'H' in iso8601_str:
        hours = int(iso8601_str[2:iso8601_str.find('H')])
        # 更新字符串，移除已处理的小时部分
        iso8601_str = iso8601_str[iso8601_str.find('H') + 1:]

    # 处理分钟
    if 'M' in iso8601_str:
        minutes = int(iso8601_str[2:iso8601_str.find('M')] if iso8601_str.startswith('PT') else iso8601_str[
                                                                                                :iso8601_str.find('M')])
        # 更新字符串，移除已处理的分钟部分
        iso8601_str = iso8601_str[iso8601_str.find('M') + 1:]

    # 处理秒
    if 'S' in iso8601_str:
        seconds = int(iso8601_str[2:iso8601_str.find('S')] if iso8601_str.startswith('PT') else iso8601_str[
                                                                                                :iso8601_str.find('S')])

    # 格式化为HH:MM:SS
    return f"{hours:02}:{minutes:02}:{seconds:02}"
