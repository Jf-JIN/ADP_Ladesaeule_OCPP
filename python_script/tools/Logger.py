import pprint
import sys
import os
import inspect
import re
import traceback
import logging
from datetime import datetime

_LOG_FOLDER_NAME = 'Logs'
_LOG_GROUP_FOLDER_NAME = '#Global_Log'


class EnumBaseMeta(type):
    def __new__(mcs, name, bases, dct: dict):
        if len(bases) == 0:
            return super().__new__(mcs, name, bases, dct)
        dct['_members_'] = {}
        members = {key: value for key, value in dct.items() if not key.startswith('__')}
        cls = super().__new__(mcs, name, bases, dct)
        cls._members_['isAllowedSetValue'] = True
        for key, value in members.items():
            if key != 'isAllowedSetValue' or key != '_members_':
                cls._members_[key] = value
                setattr(cls, key, value)
        cls._members_['isAllowedSetValue'] = False
        return cls

    def __setattr__(cls, key, value) -> None:
        if key in cls._members_ and not cls._members_['isAllowedSetValue']:
            raise AttributeError(f'Disable external modification of enumeration items\t< {key} > = {cls._members_[key]}')
        super().__setattr__(key, value)

    def __contains__(self, item) -> bool:
        return item in self._members_.values()


class EnumBase(metaclass=EnumBaseMeta):
    pass


class _ColorMap(EnumBase):
    """ 颜色枚举类 """
    BLACK = '#010101'
    RED = '#DE382B'
    GREEN = '#39B54A'
    YELLOW = '#FFC706'
    BLUE = '#006FB8'
    PINK = '#762671'
    CYAN = '#2CB5E9'
    WHITE = '#CCCCCC'
    GRAY = '#808080'
    LIGHTRED = '#FF0000'
    LIGHTGREEN = '#00FF00'
    LIGHTYELLOW = '#FFFF00'
    LIGHTBLUE = '#0000FF'
    LIGHTPINK = '#FF00FF'
    LIGHTCYAN = '#00FFFF'
    LIGHTWHITE = '#FFFFFF'
    MAP_RGB_ANSI_TXT: dict = {
        '#010101': '30',  # BLACK
        '#DE382B': '31',  # RED
        '#39B54A': '32',  # GREEN
        '#FFC706': '33',  # YELLOW
        '#006FB8': '34',  # BLUE
        '#762671': '35',  # PINK
        '#2CB5E9': '36',  # CYAN
        '#CCCCCC': '37',  # WHITE
        '#808080': '90',  # GRAY
        '#FF0000': '91',  # LIGHTRED
        '#00FF00': '92',  # LIGHTGREEN
        '#FFFF00': '93',  # LIGHTYELLOW
        '#0000FF': '94',  # LIGHTBLUE
        '#FF00FF': '95',  # LIGHTPINK
        '#00FFFF': '96',  # LIGHTCYAN
        '#FFFFFF': '97',  # LIGHTWHITE
    }
    MAP_RGB_ANSI_BG: dict = {
        '#010101': '40',  # BLACK
        '#DE382B': '41',  # RED
        '#39B54A': '42',  # GREEN
        '#FFC706': '43',  # YELLOW
        '#006FB8': '44',  # BLUE
        '#762671': '45',  # PINK
        '#2CB5E9': '46',  # CYAN
        '#CCCCCC': '47',  # WHITE
        '#808080': '100',  # GRAY
        '#FF0000': '101',  # LIGHTRED
        '#00FF00': '102',  # LIGHTGREEN
        '#FFFF00': '103',  # LIGHTYELLOW
        '#0000FF': '104',  # LIGHTBLUE
        '#FF00FF': '105',  # LIGHTPINK
        '#00FFFF': '106',  # LIGHTCYAN
        '#FFFFFF': '107',  # LIGHTWHITE
    }
    MAP_RGB_HTML: dict = {
        '#010101': '#010101',
        '#DE382B': '#DE382B',
        '#39B54A': '#39B54A',
        '#FFC706': '#FFC706',
        '#006FB8': '#006FB8',
        '#762671': '#762671',
        '#2CB5E9': '#2CB5E9',
        '#CCCCCC': '#CCCCCC',
        '#808080': '#808080',
        '#FF0000': '#FF0000',
        '#00FF00': '#00FF00',
        '#FFFF00': '#FFFF00',
        '#0000FF': '#0000FF',
        '#FF00FF': '#FF00FF',
        '#00FFFF': '#00FFFF',
        '#FFFFFF': '#FFFFFF',
    }


class LogLevel(EnumBase):
    """ 日志级别枚举类 """
    NOTSET = 'NOTSET'
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'
    NOOUT = 'NOOUT'


class _HighlightType(EnumBase):
    """ 高亮类型枚举类 """
    ASNI = 'ASNI'
    HTML = 'HTML'
    NONE = None


def asni_ct(
    text: str,
    txt_color: str | None = None,
    bg_color: str | None = None,
    dim: bool = False,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    blink: bool = False,
    *args, **kwargs
) -> str:
    """
    ANSI转义序列生成器

    参数:
    - text: 需要转义的文本
    - txt_color: 文本颜色
    - bg_color: 背景颜色
    - dim: 是否为暗色
    - bold: 是否为粗体
    - italic: 是否为斜体
    - underline: 是否为下划线
    - blink: 是否为闪烁

    返回:
    - 转义后的文本
    """
    style_list = []
    style_list.append('1') if bold else ''  # 粗体
    style_list.append('2') if dim else ''  # 暗色
    style_list.append('3') if italic else ''  # 斜体
    style_list.append('4') if underline else ''  # 下划线
    style_list.append('5') if blink else ''  # 闪烁
    style_list.append(_ColorMap.MAP_RGB_ANSI_TXT[txt_color]) if txt_color in _ColorMap else ''  # 字体颜色
    style_list.append(_ColorMap.MAP_RGB_ANSI_BG[bg_color]) if bg_color in _ColorMap else ''  # 背景颜色
    style_str = ';'.join(item for item in style_list if item)
    return f'\x1B[{style_str}m{text}\x1B[0m'


def html_ct(
    text: str,
    txt_color: str | None = None,
    bg_color: str | None = None,
    dim: bool = False,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    blink: bool = False,
    *args, **kwargs
) -> str:
    """
    HTML转义序列生成器

    参数:
    - text: 需要转义的文本
    - txt_color: 文本颜色
    - bg_color: 背景颜色
    - dim: 是否为暗色
    - bold: 是否为粗体
    - italic: 是否为斜体
    - underline: 是否为下划线
    - blink: 是否为闪烁

    返回:
    - 转义后的文本
    """

    style_list = []
    style_list.append(f'color: {_ColorMap.MAP_RGB_HTML[txt_color]}') if txt_color in _ColorMap else ''
    style_list.append(f'background-color: {_ColorMap.MAP_RGB_HTML[bg_color]}') if bg_color in _ColorMap else ''
    style_list.append('font-weight: bold') if bold else ''
    style_list.append('font-style: italic') if italic else ''
    style_list.append('text-decoration: underline') if underline else ''
    style_list.append('opacity: 0.7;animation: blink 1s step-end infinite') if blink else ''
    style_str = ';'.join(item for item in style_list if item)+';'
    return f'<span style="{style_str}">{text}</span>'


class _LogSignal(object):
    def __init__(self) -> None:
        self.__slots = []

    def connect(self, slot) -> None:
        if callable(slot):
            if slot not in self.__slots:
                self.__slots.append(slot)
        else:
            raise ValueError("Slot must be callable")

    def disconnect(self, slot) -> None:
        if slot in self.__slots:
            self.__slots.remove(slot)

    def emit(self, *args, **kwargs) -> None:
        for slot in self.__slots:
            slot(*args, **kwargs)


class _LoggingListener(logging.Handler):
    def __init__(self, level) -> None:
        super().__init__(level=level)
        self.__signal_debug = _LogSignal()
        self.__signal_info = _LogSignal()
        self.__signal_warning = _LogSignal()
        self.__signal_error = _LogSignal()
        self.__signal_critical = _LogSignal()

    @property
    def signal_debug(self) -> _LogSignal:
        return self.__signal_debug

    @property
    def signal_info(self) -> _LogSignal:
        return self.__signal_info

    @property
    def signal_warning(self) -> _LogSignal:
        return self.__signal_warning

    @property
    def signal_error(self) -> _LogSignal:
        return self.__signal_error

    @property
    def signal_critical(self) -> _LogSignal:
        return self.__signal_critical

    def emit(self, record) -> None:
        level = record.levelname
        # message = self.format(record)
        message = record.getMessage()
        if level == LogLevel.DEBUG:
            self.__signal_debug.emit(message)
        elif level == LogLevel.INFO:
            self.__signal_info.emit(message)
        elif level == LogLevel.WARNING:
            self.__signal_warning.emit(message)
        elif level == LogLevel.ERROR:
            self.__signal_error.emit(message)
        elif level == LogLevel.CRITICAL:
            self.__signal_critical.emit(message)


class _LogMeta(type):
    def __setattr__(self, name, value):
        if 'signal' in name:
            raise AttributeError('signals are read-only attributes, cannot be modified')
        super().__setattr__(name, value)


class Logger(object, metaclass=_LogMeta):
    """
    日志类

    参数:
    - log_name(str): 日志名称
    - log_path(str): 日志路径, 默认为无路径
    - log_sub_folder_name(str): 日志子文件夹名称, 默认无子文件夹
    - log_level(str): 日志级别, 默认为 `INFO`
        - `DEBUG` | `INFO` | `WARNING` | `ERROR` | `CRITICAL`
    - default_level(str): 默认日志级别, 是直接调用类时执行的日志级别, 默认为`INFO`
    - console_output(bool): 是否输出到控制台, 默认输出
    - file_output(bool): 是否输出到文件, 默认输出
    - size_limit(int): 文件大小限制, 单位为 kB, 默认不限制. 此项无法限制单消息长度, 若单个消息长度超过设定值, 为了消息完整性, 即使大小超过限制值, 也会完整写入日志文件, 则当前文件大小将超过限制值
    - count_limit(int): 文件数量限制, 默认不限制
    - days_limit(int): 天数限制, 默认不限制
    - split_by_day(bool): 是否按天分割日志, 默认不分割
    - message_format(str): 消息格式, 可自定义, 详细方法见示例. 默认格式为: `%(consoleLine)s\\n[%(asctime)s] [log: %(logName)s] [module: %(moduleName)s] [class: %(className)s] [function: %(functionName)s] [line: %(lineNum)s]- %(levelName)s\\n%(message)s\\n`
    - exclude_funcs(list[str]): 排除的函数列表, 用于追溯调用位置时, 排除父级调用函数, 排除的函数链应是完整的, 只写顶层的函数名将可能不会产生效果, 默认为空列表
    - highlight_type(str|None): 高亮模式. 默认为 `ASNI`, 取消高亮则使用 None. 当前支持 `ASNI`
    - **kwargs, 消息格式中的自定义参数, 使用方法见示例


    信号:
    - signal_log_public: 公共日志消息信号对象, 用于在类外部接收所有日志类的日志消息
    - signal_log_public_color: 公共日志消息信号对象, 用于在类外部接收所有日志类的日志消息, 并带有颜色高亮
    - signal_log_instance: 日志消息信号对象, 用于在类外部接收当前日志实例的日志消息

    方法:
    - debug(*message) # 输出调试信息, 支持多参数
    - info(*message)  # 输出普通信息, 支持多参数
    - warning(*message)  # 输出警告信息, 支持多参数
    - error(*message)  # 输出错误信息, 支持多参数
    - critical(*message)  # 输出严重错误信息, 支持多参数
    - exception(*message)  # 输出异常信息, 支持多参数

    示例:
    1. 通常调用:

        logger = Logger(log_name='test', log_path='D:/test')

        logger.debug('debug message')

    2. (不推荐): 可以直接调用类, 默认是执行info方法, 可以通过修改初始化参数表中的default_level来修改默认类执行的日志级别

        logger('info message')

    3. 关于格式的设置:

    - 提供的默认格式参数有:
        - `asctime` 当前时间
        - `moduleName` 模块名称
        - `functionName` 函数/方法名称
        - `className` 类名称
        - `levelName` 当前日志级别
        - `lineNum` 代码行号
        - `message` 消息内容
        - `scriptName` 脚本名称
        - `scriptPath` 脚本路径
        - `consoleLine` 控制台链接行

    - 如需添加自定义的参数, 可以在初始化中添加, 并可以在后续对相应的属性进行赋值

    logger = Logger(log_name='test', log_path='D:/test', message_format='%(asctime)s-%(levelName)s -%(message)s -%(happyNewYear)s', happyNewYear=False)

    logger.happyNewYear = True

    logger.debug('debug message')

    得到输出: `2025-01-01 06:30:00-INFO -debug message -True`
    """
    __logging_listening_level_int = 100
    __logging_listener_handler = _LoggingListener(0)
    __logging_listener = logging.getLogger()
    signal_log_public = _LogSignal()
    signal_log_public_color = _LogSignal()
    signal_log_public_html = _LogSignal()

    def __init__(
        self,
        log_name: str,
        log_folder_path: str = '',
        log_sub_folder_name: str = '',
        log_level: str = LogLevel.INFO,
        default_level: str = LogLevel.INFO,
        console_output: bool = True,
        file_output: bool = True,
        size_limit: int = -1,  # KB
        count_limit: int = -1,
        days_limit: int = -1,
        split_by_day: bool = False,
        message_format: str = '%(consoleLine)s\n[%(asctime)s] [log: %(logName)s] [module: %(moduleName)s] [class: %(className)s] [function: %(functionName)s] [line: %(lineNum)s]- %(levelName)s\n%(message)s\n',
        exclude_funcs: list = [],
        exclude_classes: list = [],
        exclude_modules: list = [],
        highlight_type: str | None = 'ASNI',
        ** kwargs,
    ) -> None:
        self.__doConsoleOutput = console_output if isinstance(console_output, bool) else True
        self.__doFileOutput = file_output if isinstance(file_output, bool) else True
        self.__log_name = log_name
        if not isinstance(log_folder_path, str):
            raise ValueError(f'<WARNING> Log folder path "{log_folder_path}" is not a string.')
        self.__log_path = os.path.join(log_folder_path, _LOG_FOLDER_NAME) if log_folder_path else ''
        self.__isExistsPath = False
        if log_folder_path and os.path.exists(log_folder_path):
            self.__isExistsPath = True
        elif log_folder_path:
            raise FileNotFoundError(f'Log folder path "{log_folder_path}" does not exist, create it.')
        else:
            self.__printf(
                f'No File Output from <{self.__log_name}>\n   - No log file will be recorded because the log folder path is not specified. The current file path input is {self.__log_path}{type(self.__log_path)}\n')
        self.__log_sub_folder_name = log_sub_folder_name if isinstance(log_sub_folder_name, str) else ''
        self.__log_level = log_level if log_level in LogLevel else LogLevel.INFO
        self.__default_level = default_level if default_level in LogLevel else LogLevel.INFO
        self.__size_limit = size_limit * 1000 if isinstance(size_limit, int) else -1
        self.__count_limit = count_limit if isinstance(count_limit, int) else -1
        self.__days_limit = days_limit if isinstance(days_limit, int) else -1
        self.__doSplitByDay = split_by_day if isinstance(split_by_day, bool) else False
        self.__message_format = message_format if isinstance(
            message_format, str) else '%(consoleLine)s\n[%(asctime)s] [log: %(logName)s] [module: %(moduleName)s] [class: %(className)s] [function: %(functionName)s] [line: %(lineNum)s]- %(levelName)s\n%(message)s\n'
        self.__exclude_funcs_list = exclude_funcs if isinstance(exclude_funcs, list) else []
        self.__exclude_classes_list = exclude_classes if isinstance(exclude_classes, list) else []
        self.__exclude_modules_list = exclude_modules if isinstance(exclude_modules, list) else []
        self.__highlight_type = highlight_type if isinstance(highlight_type, (str, type(None))) and highlight_type in _HighlightType else _HighlightType.ASNI
        self.__kwargs = kwargs
        self.__dict__.update(kwargs)
        self.__init_params()
        self.__clear_files()

    def __init_params(self) -> None:
        self.__var_dict = {  # 日志变量字典
            'logName': '',
            'asctime': '',
            'moduleName': '',
            'functionName': '',
            'className': '',
            'levelName': '',
            'lineNum': '',
            'message': '',
            'scriptName': '',
            'consoleLine': '',
        }
        self.__self_class_name: str = self.__class__.__name__
        self.__self_module_name: str = os.path.splitext(os.path.basename(__file__))[0]
        self.__start_time = datetime.now()
        self.__var_dict.update(self.__kwargs)
        self.__exclude_funcs = set()  # 存储 __find_caller 中忽略的函数
        self.__exclude_funcs.update(self.__class__.__dict__.keys())
        self.__exclude_funcs.difference_update(dir(object))
        self.__exclude_classes: set = {
            self.__self_class_name,
            '_LoggingListener',
            '_LogSignal',
        }
        self.__exclude_modules = set()
        # self.__exclude_modules.add(self.__self_module_name)
        for item in self.__exclude_funcs_list:
            self.__exclude_funcs.add(item)
        for item in self.__exclude_classes_list:
            self.__exclude_classes.add(item)
        for item in self.__exclude_modules_list:
            self.__exclude_modules.add(item)
        self.__current_size = 0
        self.__current_day = datetime.today().date()
        self.__isNewFile = True
        self.__signal_log_instance = _LogSignal()
        self.__level_color_dict = {
            LogLevel.DEBUG: (_ColorMap.LIGHTGREEN, '', False, False),
            LogLevel.INFO: (_ColorMap.BLUE, '', False, False),
            LogLevel.WARNING: (_ColorMap.LIGHTYELLOW, '', True, False),
            LogLevel.ERROR: (_ColorMap.WHITE, _ColorMap.LIGHTRED, True, False),
            LogLevel.CRITICAL: (_ColorMap.LIGHTYELLOW, _ColorMap.RED, True, True),
        }
        self.__log_level_int_dict = {
            LogLevel.NOTSET: 10,
            LogLevel.DEBUG: 10,
            LogLevel.INFO: 20,
            LogLevel.WARNING: 30,
            LogLevel.ERROR: 40,
            LogLevel.CRITICAL: 50,
            LogLevel.NOOUT: 60,
        }
        listen_level_dict = {
            LogLevel.DEBUG: LogLevel.NOTSET,
            LogLevel.INFO: LogLevel.DEBUG,
            LogLevel.WARNING: LogLevel.INFO,
            LogLevel.ERROR: LogLevel.WARNING,
            LogLevel.CRITICAL: LogLevel.ERROR,
            LogLevel.NOOUT: LogLevel.CRITICAL
        }
        name_logging_listening_level = f'_{self.__class__.__name__}__logging_listening_level_int'
        attr_logging_listening_level = getattr(self.__class__, name_logging_listening_level, 100)
        if attr_logging_listening_level >= 100:
            self.__logging_listener_handler.signal_debug.connect(self.debug)
            self.__logging_listener_handler.signal_info.connect(self.info)
            self.__logging_listener_handler.signal_warning.connect(self.warning)
            self.__logging_listener_handler.signal_error.connect(self.error)
            self.__logging_listener_handler.signal_critical.connect(self.critical)
            self.__logging_listener.addHandler(self.__logging_listener_handler)
        if self.__log_level_int_dict[self.__log_level] <= attr_logging_listening_level:
            self.__logging_listener.setLevel(listen_level_dict[self.__log_level])
            setattr(self.__class__, name_logging_listening_level, self.__log_level_int_dict[self.__log_level])

    @property
    def signal_log_instance(self) -> _LogSignal:
        return self.__signal_log_instance

    def __set_log_file_path(self) -> None:
        """ 设置日志文件路径 """
        # 支持的字符 {}[];'',.!~@#$%^&()_+-=
        if self.__isExistsPath is False:
            return
        if not hasattr(self, '_Logger__log_file_path'):  # 初始化, 创建属性
            self.__start_time_format = self.__start_time.strftime("%Y%m%d_%H'%M'%S")
            self.__current_log_folder_path = os.path.join(self.__log_path, self.__log_sub_folder_name)
            if not os.path.exists(self.__current_log_folder_path):
                os.makedirs(self.__current_log_folder_path)
            self.__log_file_path = os.path.join(self.__log_path, self.__log_sub_folder_name, f'{self.__log_name}-[{self.__start_time_format}]--0.log')
        else:
            file_name = os.path.splitext(os.path.basename(self.__log_file_path))[0]
            str_list = file_name.split('--')
            self.__log_file_path = os.path.join(self.__log_path, self.__log_sub_folder_name, f'{str_list[0]}--{int(str_list[-1]) + 1}.log')

    def __call__(self, *args, **kwargs) -> None:
        call_dict = {
            LogLevel.DEBUG: self.debug,
            LogLevel.INFO: self.info,
            LogLevel.WARNING: self.warning,
            LogLevel.ERROR: self.error,
            LogLevel.CRITICAL: self.critical,
        }
        if self.__default_level in call_dict:
            call_dict[self.__default_level](*args, **kwargs)
        else:
            raise TypeError("'module' object is not callable. Please use Logger.debug/info/warning/error/critical to log.")

    def __setattr__(self, name: str, value) -> None:
        if hasattr(self, '_Logger__kwargs') and name == 'signal_log_public' and name in self.__dict__['_Logger__exclude_funcs']:
            raise AttributeError("'signal_log_public' is a read-only property.")
        if hasattr(self, '_Logger__kwargs') and name == 'signal_log_public_color' and name in self.__dict__['_Logger__exclude_funcs']:
            raise AttributeError("'signal_log_public_color' is a read-only property.")
        if hasattr(self, '_Logger__kwargs') and name != '_Logger__kwargs' and name in self.__kwargs:
            self.__kwargs[name] = value
            self.__var_dict[name] = value
        if hasattr(self, '_Logger__kwargs') and (not name.startswith('_Logger__') and name not in self.__dict__):
            raise AttributeError(f"'Logger' object has no attribute '{name}'")
        super().__setattr__(name, value)

    def __clear_files(self) -> None:
        """
        清理日志文件.
        """
        if self.__isExistsPath is False:
            return
        if (not isinstance(self.__count_limit, int) and self.__count_limit < 0) or (not isinstance(self.__days_limit, int) and self.__days_limit <= 0):
            return
        self.__current_log_folder_path = os.path.join(self.__log_path, self.__log_sub_folder_name)
        if not os.path.exists(self.__current_log_folder_path):
            return
        current_file_list = []
        for file in os.listdir(self.__current_log_folder_path):
            fp = os.path.join(self.__current_log_folder_path, file)
            if file.endswith('.log') and os.path.isfile(fp):
                current_file_list.append(fp)
        length_file_list = len(current_file_list)
        # 清理超过文件数量限制的文件
        if (isinstance(self.__count_limit, int) and self.__count_limit >= 0) and length_file_list > self.__count_limit:
            sorted_files = sorted(current_file_list, key=os.path.getctime)
            for file_path in sorted_files[:length_file_list - self.__count_limit]:
                os.remove(file_path)
        # 清理超过天数限制的文件
        elif isinstance(self.__days_limit, int) and self.__days_limit > 0:
            for file_path in current_file_list:
                if (datetime.today() - datetime.fromtimestamp(os.path.getctime(file_path))).days > self.__days_limit:
                    os.remove(file_path)

    def __find_caller(self) -> dict:
        """ 定位调用者 """
        stack = inspect.stack()
        caller_name = ''
        class_name = ''
        linenum = -1
        module_name = ''
        script_name = ''
        script_path = ''
        func = None
        for idx, fn in enumerate(stack):
            unprefix_variable = fn.function.lstrip('__')
            temp_class_name = fn.frame.f_locals.get('self', None).__class__.__name__ if 'self' in fn.frame.f_locals else ''
            temp_module_name = os.path.splitext(os.path.basename(fn.filename))[0]
            if (
                fn.function not in self.__exclude_funcs
                and f'_Logger__{unprefix_variable}' not in self.__exclude_funcs
                and temp_class_name not in self.__exclude_classes
                and temp_module_name not in self.__exclude_modules
            ):  # 不在排除列表中, 同时也排除当前类中的私有方法
                caller_name = fn.function
                class_name = temp_class_name
                linenum = fn.lineno
                module_name = temp_module_name
                script_name = os.path.basename(fn.filename)
                script_path = fn.filename
                func = fn
                break
        return {
            'caller': func,
            'caller_name': caller_name,
            'class_name': class_name,
            'line_num': linenum,
            'module_name': module_name,
            'script_name': script_name,
            'script_path': script_path,
        }

    def __color(self, message: str, *args, highlight_type=None, **kwargs) -> str:
        """ 颜色样式渲染 """
        if highlight_type is None:
            highlight_type = self.__highlight_type
            if self.__highlight_type is None:
                return message
        if highlight_type == _HighlightType.ASNI:
            return asni_ct(text=message, *args, **kwargs)
        if highlight_type == _HighlightType.HTML:
            return html_ct(text=message, *args, **kwargs)
        return message

    def __format(self, log_level: str, *args) -> tuple:
        """ 格式化日志信息 """
        msg_list = []
        for arg in args:
            if isinstance(arg, (dict, list, tuple)):
                msg_list.append(pprint.pformat(arg))
            else:
                msg_list.append(str(arg))
        msg = ' '.join(message for message in msg_list)
        caller_info = self.__find_caller()
        self.__var_dict['logName'] = self.__log_name
        self.__var_dict['asctime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.__var_dict['moduleName'] = caller_info['module_name']
        self.__var_dict['scriptName'] = caller_info['script_name']
        self.__var_dict['scriptPath'] = caller_info['script_path']
        self.__var_dict['functionName'] = caller_info['caller_name']
        self.__var_dict['className'] = caller_info['class_name']
        self.__var_dict['levelName'] = log_level
        self.__var_dict['lineNum'] = caller_info['line_num']
        self.__var_dict['message'] = msg
        script_path = caller_info['script_path']
        line_num = caller_info['line_num']
        self.__var_dict['consoleLine'] = f'File "{script_path}", line {line_num}'
        pattern = r'%\((.*?)\)(\.\d+)?([sdfxXobeEgGc%])'
        used_var_names = re.findall(pattern, self.__message_format)
        # 普通消息
        used_vars = {name[0]: self.__var_dict[name[0]] for name in used_var_names if name[0] in self.__var_dict}
        text = self.__message_format % used_vars + '\n'
        # 高亮消息
        html_dict = {
            'levelName': self.__color(
                log_level,
                txt_color=self.__level_color_dict[log_level][0],
                bg_color=self.__level_color_dict[log_level][1],
                bold=self.__level_color_dict[log_level][2],
                blink=self.__level_color_dict[log_level][3],
                highlight_type='HTML'),
            'logName': self.__color(
                self.__var_dict['logName'],
                txt_color=_ColorMap.CYAN,
                highlight_type='HTML'),
            'asctime': self.__color(
                self.__var_dict['asctime'],
                txt_color=_ColorMap.GREEN,
                bold=True,
                highlight_type='HTML'),
            'moduleName': self.__color(
                self.__var_dict['moduleName'],
                txt_color=_ColorMap.CYAN,
                highlight_type='HTML'),
            'functionName': self.__color(
                self.__var_dict['functionName'],
                txt_color=_ColorMap.CYAN,
                highlight_type='HTML'),
            'className': self.__color(
                self.__var_dict['className'],
                txt_color=_ColorMap.CYAN,
                highlight_type='HTML'),
            'lineNum': self.__color(
                self.__var_dict['lineNum'],
                txt_color=_ColorMap.CYAN,
                highlight_type='HTML'),
            'scriptPath': self.__color(
                self.__var_dict['scriptPath'],
                txt_color=_ColorMap.CYAN,
                highlight_type='HTML'),
            'consoleLine': self.__color(
                self.__var_dict['consoleLine'],
                txt_color=_ColorMap.RED,
                italic=True,
                highlight_type='HTML'),
            'message': msg,
        }
        if log_level in self.__level_color_dict:
            self.__var_dict['levelName'] = self.__color(
                log_level,
                txt_color=self.__level_color_dict[log_level][0],
                bg_color=self.__level_color_dict[log_level][1],
                bold=self.__level_color_dict[log_level][2],
                blink=self.__level_color_dict[log_level][3])
        self.__var_dict['logName'] = self.__color(
            self.__var_dict['logName'],
            txt_color=_ColorMap.CYAN)
        self.__var_dict['asctime'] = self.__color(
            self.__var_dict['asctime'],
            txt_color=_ColorMap.GREEN,
            bold=True)
        self.__var_dict['moduleName'] = self.__color(
            self.__var_dict['moduleName'],
            txt_color=_ColorMap.CYAN)
        self.__var_dict['functionName'] = self.__color(
            self.__var_dict['functionName'],
            txt_color=_ColorMap.CYAN)
        self.__var_dict['className'] = self.__color(
            self.__var_dict['className'],
            txt_color=_ColorMap.CYAN)
        self.__var_dict['lineNum'] = self.__color(
            self.__var_dict['lineNum'],
            txt_color=_ColorMap.CYAN)
        self.__var_dict['scriptPath'] = self.__color(
            self.__var_dict['scriptPath'],
            txt_color=_ColorMap.CYAN)
        self.__var_dict['consoleLine'] = self.__color(
            self.__var_dict['consoleLine'],
            txt_color=_ColorMap.RED,
            italic=True)
        used_vars = {name[0]: self.__var_dict[name[0]] for name in used_var_names if name[0] in self.__var_dict}
        text_with_color = self.__message_format % used_vars + '\n'
        used_vars_html = {name[0]: html_dict[name[0]] for name in used_var_names if name[0] in html_dict}
        html_text = self.__message_format % used_vars_html + '\n'
        pre_blick_text = '<style > @keyframes blink{50% {opacity: 50;}}</style>'
        text_with_color_HTML = (pre_blick_text + html_text).replace('\n', '<br>')
        if self.__highlight_type == _HighlightType.HTML:
            text_with_color = text_with_color_HTML
        return text_with_color, text, text_with_color_HTML

    def __printf(self, message: str) -> None:
        """ 打印日志信息 """
        if not self.__doConsoleOutput:
            return
        sys.stdout.write(message)

    def __write(self, message: str) -> None:
        """ 写入日志信息 """
        if not self.__doFileOutput or self.__isExistsPath is False:
            return
        if self.__size_limit and self.__size_limit > 0:
            # 大小限制
            writting_size = len(message.encode('utf-8'))
            self.__current_size += writting_size
            if self.__current_size >= self.__size_limit:
                self.__isNewFile = True
        if self.__doSplitByDay:
            # 按天分割
            if datetime.today().date() != self.__current_day:
                self.__isNewFile = True
        if self.__isNewFile:
            # 创建新文件
            self.__isNewFile = False
            self.__set_log_file_path()
            self.__current_day = datetime.today().date()
            file_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            start_time = self.__start_time.strftime('%Y-%m-%d %H:%M:%S')
            message = f"""{'#'*66}
# <start time> This Program is started at\t {start_time}.
# <file time> This log file is created at\t {file_time}.
{'#'*66}\n\n{message}"""
            self.__current_size = len(message.encode('utf-8'))
        with open(self.__log_file_path, 'a', encoding='utf-8') as f:
            f.write(message)

    def __output(self, level, *args, **kwargs) -> None:
        txs, tx, thtml = self.__format(level, *args)
        self.__write(tx)
        self.__printf(txs)
        self.__signal_log_instance.emit(tx)
        Logger.signal_log_public.emit(tx)
        Logger.signal_log_public_color.emit(txs)
        Logger.signal_log_public_html.emit(thtml)

    def debug(self, *args, **kwargs) -> None:
        """ 打印调试信息 """
        if self.__log_level_int_dict[self.__log_level] > self.__log_level_int_dict[LogLevel.DEBUG]:
            return
        self.__output(LogLevel.DEBUG, *args, **kwargs)

    def info(self, *args, **kwargs) -> None:
        """ 打印信息 """
        if self.__log_level_int_dict[self.__log_level] > self.__log_level_int_dict[LogLevel.INFO]:
            return
        self.__output(LogLevel.INFO, *args, **kwargs)

    def warning(self, *args, **kwargs) -> None:
        """ 打印警告信息 """
        if self.__log_level_int_dict[self.__log_level] > self.__log_level_int_dict[LogLevel.WARNING]:
            return
        self.__output(LogLevel.WARNING, *args, **kwargs)

    def error(self, *args, **kwargs) -> None:
        """ 打印错误信息 """
        if self.__log_level_int_dict[self.__log_level] > self.__log_level_int_dict[LogLevel.ERROR]:
            return
        self.__output(LogLevel.ERROR, *args, **kwargs)

    def exception(self, *args, **kwargs) -> None:
        """ 打印异常信息 """
        exception_str = traceback.format_exc()
        if exception_str == f'{type(None).__name__}: {None}\n':
            return
        exception_str += '\n'
        self.error(exception_str, *args, **kwargs)

    def critical(self, *args, **kwargs) -> None:
        """ 打印严重错误信息 """
        if self.__log_level_int_dict[self.__log_level] > self.__log_level_int_dict[LogLevel.CRITICAL]:
            return
        self.__output(LogLevel.CRITICAL, *args, **kwargs)


class LoggerGroup(object, metaclass=_LogMeta):
    """
    日志组类

    参数:
    - log_folder_path(str): 日志组文件夹路径
    - size_limit(int): 文件大小限制, 单位为 kB, 默认不限制. 此项无法限制单消息长度, 若单个消息长度超过设定值, 为了消息完整性, 即使大小超过限制值, 也会完整写入日志文件, 则当前文件大小将超过限制值
    - count_limit(int): 文件数量限制, 默认不限制
    - days_limit(int): 天数限制, 默认不限制
    - split_by_day(bool): 是否按天分割日志, 默认不分割

    信号:
    - signal_group_public: 公共日志消息信号对象, 用于在类外部接收所有日志类的日志消息
    - signal_group_public_color: 公共日志消息信号对象, 用于在类外部接收所有日志类的日志消息, 并带有颜色高亮

    方法:
    - set_log_group
    - append_log
    - remove_log
    - clear

    示例:
    1. 通常调用:

        logger = Logger(log_name='test', log_path='D:/test')

        logger.debug('debug message')

    2. (不推荐): 可以直接调用类, 默认是执行info方法, 可以通过修改初始化参数表中的default_level来修改默认类执行的日志级别

        logger('info message')

    3. 关于格式的设置:

    - 提供的默认格式参数有:
        - `logName` 日志名称
        - `asctime` 当前时间
        - `moduleName` 模块名称
        - `functionName` 函数/方法名称
        - `className` 类名称
        - `levelName` 当前日志级别
        - `lineNum` 代码行号
        - `message` 消息内容
        - `scriptName` 脚本名称
        - `scriptPath` 脚本路径
        - `consoleLine` 控制台链接行

    - 如需添加自定义的参数, 可以在初始化中添加, 并可以在后续对相应的属性进行赋值

    logger = Logger(log_name='test', log_path='D:/test', message_format='%(asctime)s-%(levelName)s -%(message)s -%(happyNewYear)s', happyNewYear=False)

    logger.happyNewYear = True

    logger.debug('debug message')

    得到输出: `2025-01-01 06:30:00-INFO -debug message -True`
    """
    __isInstance = False
    signal_group_public = _LogSignal()
    signal_group_public_color = _LogSignal()
    signal_group_public_html = _LogSignal()

    def __new__(cls, *args, **kwargs):
        if cls.__isInstance:
            raise Exception('Logger is a singleton class')
        cls.__isInstance = True
        return super().__new__(cls)

    def __init__(
        self,
        log_folder_path: str,
        log_group: list = [],
        size_limit: int = -1,  # KB
        count_limit: int = -1,
        days_limit: int = -1,
        split_by_day: bool = False,
    ) -> None:
        self.__start_time = datetime.now()
        if not os.path.exists(log_folder_path):
            self.__isExistsPath = False
            raise FileNotFoundError(f'Log folder path {log_folder_path} not found')
        else:
            self.__isExistsPath = True
        self.__isNewFile = True
        self.__size_limit = size_limit * 1000 if isinstance(size_limit, int) else -1
        self.__count_limit = count_limit if isinstance(count_limit, int) else -1
        self.__days_limit = days_limit if isinstance(days_limit, int) else -1
        self.__doSplitByDay = split_by_day if isinstance(split_by_day, bool) else False
        self.__log_folder_path = os.path.join(log_folder_path, _LOG_FOLDER_NAME)
        self.__current_size = 0
        self.__current_day = datetime.today().date()
        self.__set_log_file_path()
        self.set_log_group(log_group)
        self.__clear_files()
        Logger.signal_log_public.connect(self.signal_group_public.emit)
        Logger.signal_log_public_color.connect(self.signal_group_public_color.emit)
        Logger.signal_log_public_html.connect(self.signal_group_public_html.emit)

    def set_log_group(self, log_group: list) -> None:
        if not isinstance(log_group, list):
            raise TypeError('log_group must be list')
        self.__log_group = log_group
        self.__disconnect(log_group)
        if log_group:
            Logger.signal_log_public.disconnect(self.__write)
            self.__connection()
        else:
            Logger.signal_log_public.connect(self.__write)

    def append_log(self, log_obj: Logger | list) -> None:
        if isinstance(log_obj, list | tuple):
            self.__log_group += list(log_obj)
        elif isinstance(log_obj, Logger):
            self.__log_group.append(log_obj)
        else:
            raise TypeError(f'log_obj must be list or Logger, but got {type(log_obj)}')

    def remove_log(self, log_obj: Logger) -> None:
        if isinstance(log_obj, Logger):
            log_obj.signal_log_instance.disconnect(self.__write)
            self.__log_group.remove(log_obj)
        else:
            raise TypeError(f'log_obj must be Logger, but got {type(log_obj)}')
        if len(self.__log_group) == 0:
            Logger.signal_log_public.connect(self.__write)

    def clear(self) -> None:
        self.__disconnect([])
        self.__log_group: list = []
        Logger.signal_log_public.connect(self.__write)

    def __disconnect(self, log_group) -> None:
        for log_obj in self.__log_group:
            log_obj: Logger
            if log_obj not in log_group:
                log_obj.signal_log_instance.disconnect(self.__write)

    def __connection(self) -> None:
        if not self.__log_group:
            return
        for log_obj in self.__log_group:
            log_obj: Logger
            log_obj.signal_log_instance.connect(self.__write)

    def __set_log_file_path(self) -> None:
        """ 设置日志文件路径 """
        # 支持的字符 {}[];'',.!~@#$%^&()_+-=

        if self.__isExistsPath is False:
            return
        if not hasattr(self, f'_{self.__class__.__name__}__log_sub_folder_path'):  # 初始化, 创建属性
            self.__start_time_format = self.__start_time.strftime("%Y%m%d_%H'%M'%S")
            self.__log_sub_folder_path = os.path.join(self.__log_folder_path, _LOG_GROUP_FOLDER_NAME)
            if not os.path.exists(self.__log_sub_folder_path):
                os.makedirs(self.__log_sub_folder_path)
            self.__log_file_path = os.path.join(self.__log_sub_folder_path, f'Global_Log-[{self.__start_time_format}]--0.log')
        else:
            file_name = os.path.splitext(os.path.basename(self.__log_file_path))[0]
            str_list = file_name.split('--')
            self.__log_file_path = os.path.join(self.__log_sub_folder_path, f'{str_list[0]}--{int(str_list[-1]) + 1}.log')

    def __clear_files(self) -> None:
        """
        清理日志文件.
        """
        if self.__isExistsPath is False:
            return
        if (not isinstance(self.__count_limit, int) and self.__count_limit < 0) or (not isinstance(self.__days_limit, int) and self.__days_limit <= 0):
            return
        current_folder_path = os.path.join(self.__log_folder_path, _LOG_GROUP_FOLDER_NAME)
        if not os.path.exists(current_folder_path):
            return
        current_file_list = []
        for file in os.listdir(current_folder_path):
            fp = os.path.join(current_folder_path, file)
            if file.endswith('.log') and os.path.isfile(fp):
                current_file_list.append(fp)
        length_file_list = len(current_file_list)
        # 清理超过文件数量限制的文件
        if (isinstance(self.__count_limit, int) and self.__count_limit >= 0) and length_file_list > self.__count_limit:
            sorted_files = sorted(current_file_list, key=os.path.getctime)
            for file_path in sorted_files[:length_file_list - self.__count_limit]:
                os.remove(file_path)
        # 清理超过天数限制的文件
        elif isinstance(self.__days_limit, int) and self.__days_limit > 0:
            for file_path in current_file_list:
                if (datetime.today() - datetime.fromtimestamp(os.path.getctime(file_path))).days > self.__days_limit:
                    os.remove(file_path)

    def __write(self, message: str) -> None:
        """ 写入日志信息 """
        if self.__isExistsPath is False:
            return
        if self.__size_limit and self.__size_limit > 0:
            # 大小限制
            writting_size = len(message.encode('utf-8'))
            self.__current_size += writting_size
            if self.__current_size >= self.__size_limit:
                self.__isNewFile = True
        if self.__doSplitByDay:
            # 按天分割
            if datetime.today().date() != self.__current_day:
                self.__isNewFile = True
        if self.__isNewFile:
            # 创建新文件
            self.__isNewFile = False
            self.__current_day = datetime.today().date()
            file_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            start_time = self.__start_time.strftime('%Y-%m-%d %H:%M:%S')
            message = f"""{'#'*66}
# <start time> This Program is started at\t {start_time}.
# <file time> This log file is created at\t {file_time}.
{'#'*66}\n\n{message}"""
            self.__current_size = len(message.encode('utf-8'))
        with open(self.__log_file_path, 'a', encoding='utf-8') as f:
            f.write(message)
