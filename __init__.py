import datetime, pytz
from pydantic import BaseModel,root_validator


class GDateTime(BaseModel):
    year: int = 1970
    month: int = 1
    day: int = 1
    hour: int = 0
    minute: int = 0
    second: int = 0
    microsecond: int = 0

    @root_validator(pre=True)
    def check_before(cls, values):
        """前置检查"""
        # _month = values
        # if int(_month) < 10:
        #     values.update({'month',"0{0}".format(_month)})
        return values

    @root_validator(pre=False)
    def check_after(cls, values):
        """后置检查"""
        _year = values.get('year')
        _month = values.get('month')
        _day = values.get('day')
        _hour = values.get('hour')
        _minute = values.get('minute')
        _second = values.get('second')
        _microsecond = values.get('microsecond')
        _week = values.get('tzone')

        if _year < 1 or _year > 9999:
            raise ValueError("year value range (1-9999), 年份的值必须在(1-9999), you are input: {0} .".format(_year))

        if _month < 1 or _month > 12:
            raise ValueError("month value range (1-12), 月份的值必须在(1-12), you are input: {0} .".format(_month))

        if _day < 1 or _day > 31:
            raise ValueError("day value range (1-31), 天的值必须在(1-31), you are input: {0} .".format(_day))

        if _hour < 0 or _hour > 23:
            raise ValueError("hour value range (0-23), 小时的值必须在(0-23), you are input: {0} .".format(_hour))

        if _minute < 0 or _minute >= 60:
            raise ValueError("minute value range (0-59), 分钟的值必须在(0-59), you are input: {0} .".format(_minute))

        if _second < 0 or _second >= 60:
            raise ValueError("second value range (0-59), 秒数的值必须在(0-59), you are input: {0} .".format(_second))

        if _microsecond < 0 or _microsecond >= 1000000:
            raise ValueError(
                "stamp value range (0 - 999 999), 秒数的值必须在(0-999 999 ), you are input: {0} .".format(_microsecond))


        return values

DateTimeDict = {
    'year': 1970,
    "month": 1,
    "day": 1,
    "hour": 0,
    "minute": 0,
    "second": 0,
    "microsecond": 0,
    }

class gtime(object):
    """整合 datetime 和time 模块, 增强日期时间功能, Mate in China"""

    def __new__(cls, year=1970, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, tzone="utc"):
        self: gtime = object.__new__(cls)
        
        _dt_dict = {
            'year': year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "second": second,
            "microsecond": microsecond,
        }
        _val_dict = GDateTime(**_dt_dict)

        # 创建时间对象
        self._year = _val_dict.year
        self._month = _val_dict.month
        self._day = _val_dict.day
        self._hour = _val_dict.hour
        self._minute = _val_dict.minute
        self._sec = _val_dict.second
        self._msec = _val_dict.microsecond
        self._tzone = tzone

        _dt = datetime.datetime(self._year, self._month, self._day, self._hour, self._minute, self._sec, self._msec)

        _dt_tuple = _dt.timetuple()
        self._msec = _dt.microsecond
        self._days = _dt_tuple.tm_yday
        self._week = _dt.weekday()
        # 修正星期
        # 保持和JavaScript日期一致
        # 0: 星期日 -> 6: 星期六
        if self._week == 0:
            self._week = 1
        elif self._week == 1:
            self._week = 2
        elif self._week == 2:
            self._week = 3
        elif self._week == 3:
            self._week = 4
        elif self._week == 4:
            self._week = 5
        elif self._week == 5:
            self._week = 6
        else:
            self._week = 0

        self._iweek = _dt.isoweekday()  # 1: 星期1 -> 7: 星期日
        self._isdst = _dt_tuple.tm_isdst
        self._datetime: datetime = _dt  # 返回原始时间格式
        

        return self

    # ------属性区--------
    @property
    def year(self) -> int:
        return self._year

    @property
    def month(self) -> int:
        return self._month

    @property
    def day(self) -> int:
        return self._day

    @property
    def hour(self) -> int:
        return self._hour

    @property
    def minute(self) -> int:
        return self._minute

    @property
    def sec(self) -> int:
        return self._sec

    @property
    def msec(self) -> int:
        return self._msec

    @property
    def week(self) -> int:
        return self._week

    @property
    def iweek(self) -> int:
        return self._iweek

    @property
    def days(self) -> int:
        return self._days

    @property
    def isdst(self) -> int:
        return self._isdst

    @property
    def tzone(self) -> str:
        return self._tzone

    @property
    def data(self) -> datetime.date:
        return datetime.date(self._year,self._month,self._day)

    @property
    def time(self) -> datetime.time:
        return datetime.time(self._hour,self._minute,self._sec,self._msec)
    
    # ---------类方法功能区--------------

    @classmethod
    def now(cls, timezone: str = "cn"):
        """时区选择,请参考该模块文档里面的时区表"""
        _timezone = cls.__timezone_str(timezone)
        _dt = datetime.datetime.now(pytz.timezone(_timezone))
        return cls.__time_to_class(_dt, tzone=timezone)

    @classmethod
    def fromstr(cls, datetime_str: str, format_str: str = "autom"):
        """
        字符串 -> 日期时间
        :param datetime_str:
        :param format_str:
        :return:
        """
        _format_str = cls.__format_str(format_str)
        _dt = datetime.datetime.strptime(datetime_str, _format_str)
        return cls.__time_to_class(_dt)

    @classmethod
    def fromsec(cls, seconds: int | float):
        """
        秒数 -> 日期时间
        :param seconds:
        :return:
        """
        _dt = datetime.datetime.fromtimestamp(seconds)
        return cls.__time_to_class(_dt)

    @classmethod
    def fromtuple(cls, tuples: tuple):
        """
        (year, month, day, hour, minute, second, microsecond)
        :param tuples:
        :return:
        """
        if len(tuples) >= 8:
            print(len(tuples))
            raise "fromtuple: 元素个数不得超过8个"
        if tuples:
            _count = 0
            for item in DateTimeDict.keys():
                
                if _count >= len(tuples):
                    break
                DateTimeDict[item] = tuples[_count]
                _count += 1
        _dt_dict = GDateTime(**DateTimeDict).dict()
        return cls(**_dt_dict)

    @classmethod
    def fromdict(cls, dicts: dict):
        """
        {year, month, day, hour, minute, second, microsecond}
        :param dicts:
        :return:
        """
        _dt_dict = GDateTime(**dicts).dict()
        return cls(**_dt_dict)

    @classmethod
    def fromlist(cls, lists: list):
        """
        [year, month, day, hour, minute, second, microsecond]
        :param lists:
        :return:
        """
        if len(lists) >= 8:
            print(len(lists))
            raise "fromlist: 元素个数不得超过8个"
        if lists:
            _count = 0
            for item in DateTimeDict.keys():
                if _count >= len(lists):
                    break
                DateTimeDict[item] = lists[_count]
                _count += 1
        _dt_dict = GDateTime(**DateTimeDict).dict()
        return cls(**_dt_dict)

    @classmethod
    def __time_to_class(cls, date_time: datetime.datetime, tzone: str = None):
        """修正日期时间"""
        _dt = date_time.timetuple()
        # pattern = re.search(r'.*?:.*?:.*?\.([0-9]{6})', str(date_time))
        _dt_dict = {
            'year': date_time.year,
            "month": date_time.month,
            "day": date_time.day,
            "hour": date_time.hour,
            "minute": date_time.minute,
            "second": date_time.second,
            "microsecond": date_time.microsecond,
            "tzone": tzone
        }
        return cls(**_dt_dict)

    @classmethod
    def __timezone_str(cls, timezone: str = "utc"):
        _timezone = "utc"
        if timezone == "Asia/Shanghai" or timezone == "cn" or timezone == "china" or timezone == "chinese" \
                or timezone == "beijing" or timezone == "shanghai":
            _timezone = "Asia/Shanghai"
        return _timezone

    # ----------实例化方法功能区
    @property
    def datetime(self) -> datetime.datetime:
        return self._datetime

    # @datetime.setter
    # def datetime(self, value):
    #     self._datetime = value

    def tostr(self, format_str: str = "auto") -> str:
        """
        formet:str = 'autom'
        """
        return self.__tostr(format_str)

    def __tostr(self, format_str: str = "auto") -> str:
        """
        formet:str = 'autom'
        """
        _format_str = self.__format_str(format_str)
        return self.datetime.strftime(_format_str)

    @classmethod
    def __format_str(cls, format_str: str = "auto") -> str:
        """
        格式化转换时间类型
        auto:  "%Y-%m-%d %H:%M:%S"       # No Microseconds 标准模式无微秒
        autom: "%Y-%m-%d %H:%M:%S.%f"    # Are Microseconds 标准模式有微秒
        autod: "%Y-%m-%d"    # Standard mode only has dates 标准模式只有日期
        autot: "%H:%M:%S"    # Standard mode only has dates 标准模式只有时间
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

        if format_str == "auto":
            _format = "%Y-%m-%d %H:%M:%S"
            return _format
        elif format_str == "autom":
            _format = "%Y-%m-%d %H:%M:%S.%f"
            return _format
        elif format_str == "autod":
            _format = "%Y-%m-%d"
            return _format
        elif format_str == "autot":
            _format = "%H:%M:%S"
            return _format
        elif format_str == "autotm":
            _format = "%H:%M:%S.%f"
            return _format
        elif format_str == "slash":
            _format = "%Y-%m-%d %H:%M:%S"
            return _format
        elif format_str == "slashm":
            _format = "%Y/%m/%d %H:%M:%S.%f"
            return _format
        elif format_str == "lslash":
            _format = "%H:%M:%S %Y/%m/%d"
            return _format
        elif format_str == "lslashm":
            _format = "%H:%M:%S.%f %Y/%m/%d"
            return _format
        elif format_str == "dot":
            _format = "%Y.%m.%d %H:%M:%S"
            return _format
        elif format_str == "dotm":
            _format = "%Y.%m.%d %H:%M:%S.%f"
            return _format
        elif format_str == "cn":
            _format = "%Y年%m月%d日 %H时%M分%S秒"
            return _format
        elif format_str == "cnm":
            _format = "%Y年%m月%d日 %H时%M分%S秒.%f微秒"
            return _format
        elif format_str == "cn":
            _format = "%Y年%m月%d日 %H时%M分%S秒"
            return _format
        elif format_str == "cnm":
            _format = "%Y年%m月%d日 %H时%M分%S秒.%f微秒"
            return _format
        elif format_str == "cnd":
            _format = "%Y年%m月%d日"
            return _format
        elif format_str == "cnt":
            _format = "%H时%M分%S秒"
            return _format
        else:
            return format_str

    def tosec(self, is_timestamp: bool = False) -> int | float:
        """

        :param is_timestamp: 是否需要时间戳, 默认不需要
        :return: 返回值是1970年1月1日 00:00:00 到现在秒数
        """
        return self.__tosec(is_timestamp)

    def __tosec(self, is_timestamp: bool = False) -> int | float:
        if is_timestamp:
            return self.datetime.timestamp()
        else:
            return int(self.datetime.timestamp())

    def totuple(self):
        """
        将时间解构到元祖中
        时间结构: (year, month, day, hour, minute, sec, msec, week,iweek days, tzone, isdst)
        :return: 返回时间解构的元祖对象
        """
        return self.__totuple()

    def __totuple(self):
        _dt_tuple = (self.year, self.month, self.day, self.hour, self.minute, self.sec, \
                     self.msec, self.week, self.iweek, self.days, self.tzone, self.isdst)
        return _dt_tuple

    def tolist(self):
        return self.__tolist()

    def __tolist(self):
        _dt_list = [self.year, self.month, self.day, self.hour, self.minute, self.sec, \
                    self.msec, self.week, self.iweek, self.days, self.tzone, self.isdst]
        return _dt_list

    def todict(self):
        _dt_dict = {
            'year': self.year,
            "month": self.month,
            "day": self.day,
            "hour": self.hour,
            "minute": self.minute,
            "sec": self.sec,
            "msec": self.msec,
            "week": self.week,
            "iweek": self.iweek,
            "tzone": self.tzone,
            "isdst": self.isdst
        }
        return _dt_dict

    # ------- 重载方法 --------
    def __repr__(self) -> str:
        """返回时间拼接结果"""
        return "<class gtime, 时间格式: {0} ,如果需要转换成字符串使用tostr()方法 >".format(self.datetime)

    def __eq__(self, other) -> bool:
        """
        重载 == !=
        """
        if isinstance(other, gtime):
            _t1 = self.__totuple()
            _t2 = other.__totuple()
            for i in range(6):
                if _t1[i] != _t2[i]:
                    return False
            return True

        elif not isinstance(other, gtime):
            return NotImplemented
        else:
            return False

    def __lt__(self, other):
        """
        重载 <
        """
        if isinstance(other, gtime):
            _t1 = self.__totuple()
            _t2 = other.__totuple()
            for i in range(6):
                if _t1[i] == _t2[i]:
                    continue
                elif _t1[i] < _t2[i]:
                    return True
            return False

        elif not isinstance(other, gtime):
            return NotImplemented
        else:
            return False

    def __le__(self, other):
        """
        重载 <=
        """
        if isinstance(other, gtime):
            _t1 = self.__totuple()
            _t2 = other.__totuple()
            for i in range(6):
                if _t1[i] > _t2[i]:
                    return False
            return True

        elif not isinstance(other, gtime):
            return NotImplemented
        else:
            return False

    def __gt__(self, other):
        """
        重载 >
        """
        if isinstance(other, gtime):
            _t1 = self.__totuple()
            _t2 = other.__totuple()
            for i in range(6):
                if _t1[i] == _t2[i]:
                    continue
                if _t1[i] > _t2[i]:
                    return True
            return False

        elif not isinstance(other, gtime):
            return NotImplemented
        else:
            return False

    def __ge__(self, other):
        """
        重载 >=
        """
        if isinstance(other, gtime):
            _t1 = self.__totuple()
            _t2 = other.__totuple()
            for i in range(6):
                if _t1[i] < _t2[i]:
                    return False
            return True

        elif not isinstance(other, gtime):
            return NotImplemented
        else:
            return False

    def __add__(self, other):
        """
        重载 +
        """
        if isinstance(other, gtime):
            _seconds = self.__tosec(True) + other.tosec(True)
            return self.fromsec(_seconds)
        elif isinstance(other, int | float):
            _seconds = self.__tosec(True) + other
            return self.fromsec(_seconds)
        else:
            return NotImplemented

    def __sub__(self, other):
        """
        重载 -
        """
        if isinstance(other, gtime):
            _seconds = self.__tosec(True) - other.tosec(True)
            return self.fromsec(_seconds)
        elif isinstance(other, int | float):
            _seconds = self.__tosec(True) - other
            return self.fromsec(_seconds)
        else:
            return NotImplemented

    # def __str__(self):
    #     return self.__tostr()


# if __name__ in "__main__":
#     pass