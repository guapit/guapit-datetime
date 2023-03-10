# Guapit Datetime(日期时间简化插件)

<p align="center">
<a href="#"><img src="https://img.shields.io/badge/Module-guapit--datetime-critical.svg"/></a>
<a href="#"><img src="https://img.shields.io/badge/Language-Python-blue"/></a>
    <a href="#"><img src="https://img.shields.io/badge/Version-0.1.0-f1c232"/></a>
<img src="https://img.shields.io/badge/Author-guapit-ff69b4"/>
<a href="https://www.github.com/guapit"><img src="https://img.shields.io/badge/Github-guapit-success"/></a>
<a href="https://www.gitee.com/guapit"><img src="https://img.shields.io/badge/Gitee-guapit-yellowgreen"/></a>
<a href="#"><img src="https://img.shields.io/badge/E--mail-guapit%40qq.com-yellowgreen"/></a>
</p><br>



   This is a standard date-time library based on Python: `datetime` and `time` module, Secondary development of the gtime time function enhancement and simplification plug-in, greatly simplifies the date time format conversion, no longer for a variety of date time format conversion trouble, come to use it, if you encounter a 'Bug' in the use, welcome to `githb.com/guapit` message

这是一个基于Python标准日期时间库: `datetime` `time`模块, 二次开发的gtime时间功能增强简化插件,极大的简化了日期时间格式的转化,不用再为各种日期时间格式的转化的烦恼,快来使用吧,如果你在使用中遇到`Bug`,欢迎到 `githb.com/guapit`留言

Required plugins 必要的插件

```pthon
pip install -U pydantic
pip install -U pytz
```

## pip安装

```bash
pip install guapit-datetime
```



## 常用功能

Function 1: According to the custom time zone conversion time, please refer to the documentation at github.com/guapit/guapit-datetime

Feature 2: According to the datetime format can be arbitrary conversion type

Function 3: You can import any string, meta ancestor, dictionary, list date time format

Function 4: Greatly simplifies the method of time calculation

功能1: 根据自定义时区转换时间, 查找时区表,请参考:`github.com/guapit/guapit-datetime`里面的文档

功能2: 根据日期时间格式可以任意转换类型

功能3: 可以任意导入字符串, 元祖, 字典,列表日期时间格式

功能4: 极大的简化了时间相互运算的方法

```python
# 导入模块
from guapit-datetime import gtime

# Gets the current computer standard date and time
# 获取当前计算机标准日期时间
dt = gtime.now("utc")
print(dt)
# <class gtime, 时间格式: 2023-02-12 05:39:19.090008 ,如果需要转换成字符串使用tostr()方法 >


# Gets the date and time for the specified time zone
# 获取指定时区的日期时间
# 如果你是中国用户,你可以输入 `cn`,`china`,`chinese`,`beijing`, `shanghai`,`Asia/Shanghai`
dt = gtime.now('cn')
print(dt)
# <class gtime, 时间格式: 2023-02-12 13:39:19.241579 ,如果需要转换成字符串使用tostr()方法 >


# # If you want structured data, it's also very simple
# 如果你想得到结构化的数据,也非常简单
dt = gtime.now('beijing')
print(dt.year)   # Get year 获取年份
print(dt.month)  # Get month 获取月份
print(dt.day)    # Get day 获取日份
print(dt.hour)   # Get hour 获取小时
print(dt.minute) # Get minute 获取分钟
print(dt.sec)    # Get second 获取秒数
print(dt.msec)   # Get microsecond 获取微秒
print(dt.week)   # Get week: Sunday: 0 -> Saturday: 6 获取星期: 星期日: 0 -> 星期六: 6
print(dt.iweek)  # Get week: Monday: 1 -> Sunday: 7 获取星期: 星期一: 1 -> 星期日: 7
print(dt.days)   # Gets the number of days since January 1 of the current year 获取从当前年份 1月1日开始到现在的天数
print(dt.tzone)  # Gets the name of the time zone 获取时区的名称


# Import data of any data type and convert to time
# 导入任意数据类型的数据转换成时间
# 1. 自定义日期时间
dt = gtime(2023,2,12,12,28,58)
print(dt)
# <class gtime, 时间格式: 2023-02-12 12:28:58 ,如果需要转换成字符串使用tostr()方法 >

dt = gtime.fromstr("2023-2-15 10:30:58.666666","autom")
print(dt)
# <class gtime, 时间格式: 2023-02-15 10:30:58.666666 ,如果需要转换成字符串使用tostr()方法 >

dt = gtime.fromstr("2023-2-16 10:30:58","auto")
print(dt)
# <class gtime, 时间格式: 2023-02-16 10:30:58 ,如果需要转换成字符串使用tostr()方法 >

# 2. 导入字典转换时间
DateTimeDict = {
    'year': 2023,
    "month": 2,
    "day": 16,
    "hour": 12,
    "minute": 23,
    "second": 58,
    "microsecond": 0,
}

dt = gtime.fromdict(DateTimeDict)
print(dt)
# <class gtime, 时间格式: 2023-02-16 12:23:58 ,如果需要转换成字符串使用tostr()方法 >

# 3. 导入元祖转换时间
datetime_tuple = (2023,2,17,8,8,8,6)
dt = gtime.fromtuple(datetime_tuple)
print(dt)
# <class gtime, 时间格式: 2023-02-17 08:08:08.000006 ,如果需要转换成字符串使用tostr()方法 >

# 4. 导入列表转换成时间
datetime_list = [2023,2,18,8,28,58,666666]
dt = gtime.fromlist(datetime_list)
print(dt)
# <class gtime, 时间格式: 2023-02-18 08:28:58.666666 ,如果需要转换成字符串使用tostr()方法 >

# 5. 导入秒数转换成时间
dt = gtime.now('cn').tosec(True)
print(dt) # 1676182254.425069
dt = gtime.fromsec(dt)
print(dt)
# <class gtime, 时间格式: 2023-02-12 14:10:54.425069 ,如果需要转换成字符串使用tostr()方法 >

# 将时间格式化输出任意类型
"""
格式化转换时间类型
auto:  "%Y-%m-%d %H:%M:%S"       # No Microseconds 标准模式无微秒
autom: "%Y-%m-%d %H:%M:%S.%f"    # Are Microseconds 标准模式有微秒
autod: "%Y-%m-%d"    # Standard mode only has dates 标准模式只有日期
autot: "%H:%M:%S"    # Standard mode only has dates 标准模式只有时间
autotm: "%H:%M:%S.%f"    # Standard mode comes with a timestamp time 标准模式带有时间戳时间
slash: "%Y/%m/%d %H:%M:%S"       # Time with slash and no microseconds 带有斜杠的时间无微秒
slashm: "%Y/%m/%d %H:%M:%S.%f"   # Time with slash and microseconds 带有斜杠的时间有微秒
lslash: "%H:%M:%S %Y/%m/%d"      # Time with right slash and microseconds 左边时间右边日期带有斜杠的时间无微秒
lslashm: "%H:%M:%S.%f %Y/%m/%d"  # Time with right slash and microseconds 左边时间右边日期带有斜杠的时间有微秒
dot: "%Y.%m.%d %H:%M:%S"         # Time with dot and microseconds 带有圆点的日期时间无微秒
dotm: "%Y.%m.%d %H:%M:%S.%f"     # Time with dot and microseconds 带有圆点的日期时间有微秒
cn: "%Y年%m月%d日 %H时%M分%S秒"      # chinese format microseconds 带有中文标签的日期时间无微秒
cnm: "%Y年%m月%d日 %H时%M分%S秒.%f微秒"  # # chinese format microseconds 带有中文标签的日期时间有微秒
cnd: "%Y年%m月%d日"  # 只有中文日期
cnt: "%H时%M分%S秒"  # 只有中文时间
If the above format conversion doesn't have what you need, you can customize it, for example:  "%Y-%m-%d %H:%M:%S"
如果以上格式转换没有你需要的,可以重新自定义,比如"%Y-%m-%d %H:%M:%S"
    """
# 1.转换成 字符串
dt = gtime.now('cn')
print(dt.tostr('auto')) # 默认: 2023-02-12 14:13:06
print(dt.tostr('autom')) # 2023-02-12 14:13:06.888888
print(dt.tostr('autod')) # 2023-02-12
print(dt.tostr('autotm')) # 14:13:06.666666
print(dt.tostr('slash')) # 2023/02/12 14:13:06
print(dt.tostr('slashm')) # 2023/02/12 14:13:06.666666
print(dt.tostr('lslash')) #  14:13:06 2023/02/12
print(dt.tostr('lslashm')) #  14:13:06.666666 2023/02/12
print(dt.tostr('dot')) #  2023.02.12 14:13:06
print(dt.tostr('dotm')) #  2023.02.12 14:13:06.666666
print(dt.tostr('cn')) #  2023年02月12日 14时13分06秒
print(dt.tostr('cnm')) #  2023年02月12日 14时13分06秒666666微秒
print(dt.tostr('cnd')) #  2023年02月12日
print(dt.tostr('cnt')) #  14时13分06秒

# 如果以上的格式都不需要,你可以自定义格式
print(dt.tostr('%Y-%m-%d %H:%M:%S %f')) #  2023-02-12 14:28:03 383898


# 2.转换成秒数
dt = gtime.now('cn')
print(dt.tosec(False))  # False 默认不含有时间戳
# 1676182386
print(dt.tosec(True))  # True 含有时间戳
# 1676182386.403169

# 3.转换成字典
dt = gtime.now('cn')
print(dt.todict())
# {'year': 2023, 'month': 2, 'day': 12, 'hour': 14, 'minute': 29, 'sec': 12, 'msec': 282045, 'week': 0, 'iweek': 7, 'tzone': 'cn', 'isdst': -1}

# 3.转换成元祖
dt = gtime.now('cn')
print(dt.totuple())
# (2023, 2, 12, 14, 29, 12, 282045, 0, 7, 43, 'cn', -1)

# 3.转换成列表
dt = gtime.now('cn')
print(dt.tolist())
# [2023, 2, 12, 14, 29, 12, 282045, 0, 7, 43, 'cn', -1]

# 日期时间算术计算
# 自增加法
dt = gtime.now('cn')
print(dt)  # 2023-02-12 14:31:37.132624
dt = dt + 60  # 表示当前时间加上60秒
print(dt)# 2023-02-12 14:32:37.132624

# 自增减法
dt = gtime.now('cn')
print(dt)  # 2023-02-12 14:31:37.132624
dt = dt - 120 # 表示当前时间减去120秒
print(dt) # 2023-02-12 14:29:37.132624

# 加法
dt = gtime.now('cn') + 86400

# 减法 
dt = gtime.now('cn') - 3600

# 日期时间逻辑运算
# ==
print(gtime(2023, 2, 11, 12, 30, 50) == gtime(2023, 2, 11, 12, 30, 50)) # True

# <
print(gtime(2023, 2, 11, 12, 30, 50) < gtime(2023, 2, 11, 12, 30, 55)) # True

# >
print(gtime(2023, 2, 11, 12, 30, 50) > gtime(2023, 2, 11, 12, 30, 55)) # False

# <=
print(gtime(2023, 2, 11, 12, 30, 50) <= gtime(2023, 2, 11, 12, 30, 50)) # True

# >=
print(gtime(2023, 2, 11, 12, 30, 50) >= gtime(2023, 2, 11, 12, 30, 30)) # True

# 转换成python标准库: datetime, date, time类
# gtime -> datetime
dt = gtime.now("cn")
dt.datetime

# gtime -> date
dt = gtime.now("cn")
dt.data

# gtime -> time
dt = gtime.now("cn")
dt.time

```
