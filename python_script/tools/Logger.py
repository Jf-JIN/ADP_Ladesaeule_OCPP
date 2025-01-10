import sys
import os
import inspect
import re
import traceback
from datetime import datetime


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
            raise AttributeError(f'禁止外部修改枚举项\t< {key} > = {cls._members_[key]}')
        super().__setattr__(key, value)

    def __contains__(self, item) -> bool:
        return item in self._members_.values()


class EnumBase(metaclass=EnumBaseMeta):
    pass


class _TxtColor(EnumBase):
    """ 文字颜色枚举类 """
    BLACK = '30'
    RED = '31'
    GREEN = '32'
    YELLOW = '33'
    BLUE = '34'
    PINK = '35'
    CYAN = '36'
    WHITE = '37'
    GRAY = '90'
    LIGHTRED = '91'
    LIGHTGREEN = '92'
    LIGHTYELLOW = '93'
    LIGHTBLUE = '94'
    LIGHTPINK = '95'
    LIGHTCYAN = '96'
    LIGHTWHITE = '97'


class _BgColor(EnumBase):
    """ 背景颜色枚举类 """
    BLACK = '40'
    RED = '41'
    GREEN = '42'
    YELLOW = '43'
    BLUE = '44'
    PINK = '45'
    CYAN = '46'
    WHITE = '47'
    GRAY = '100'
    LIGHTRED = '101'
    LIGHTGREEN = '102'
    LIGHTYELLOW = '103'
    LIGHTBLUE = '104'
    LIGHTPINK = '105'
    LIGHTCYAN = '106'
    LIGHTWHITE = '107'


class _LogLevel(EnumBase):
    """ 日志级别枚举类 """
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class _HighlightType(EnumBase):
    """ 高亮类型枚举类 """
    ASNI = 'ASNI'
    NONE = None


def asni_ct(
    text: str,
    txt_color: str | None = None,
    bg_color: str | None = None,
    dim: bool = False,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    blink: bool = False
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
    style_list.append(txt_color) if txt_color in _TxtColor else ''  # 字体颜色
    style_list.append(bg_color) if bg_color in _BgColor else ''  # 背景颜色
    style_str = ';'.join(item for item in style_list if item)
    return f'\x1B[{style_str}m{text}\033[0m'


class Logger(object):
    """
    日志类

    参数:
    - log_name(str): 日志名称
    - log_path(str): 日志路径
    - log_sub_folder_name(str): 日志子文件夹名称，默认无子文件夹
    - log_level(str): 日志级别, 默认为 `INFO`
        - `DEBUG` | `INFO` | `WARNING` | `ERROR` | `CRITICAL`
    - default_level(str): 默认日志级别，是直接调用类时执行的日志级别，默认为`INFO`
    - console_output(bool): 是否输出到控制台，默认输出
    - file_output(bool): 是否输出到文件，默认输出
    - size_limit(int): 文件大小限制，单位为 kB, 默认不限制
    - count_limit(int): 文件数量限制，默认不限制
    - days_limit(int): 天数限制，默认不限制
    - split_by_day(bool): 是否按天分割日志，默认不分割
    - message_format(str): 消息格式，可自定义，详细方法见示例。默认格式为：`%(scriptPath)s", line %(lineNum)s\\n[%(asctime)s] [module: %(moduleName)s] [class: %(className)s] [function: %(functionName)s] [line: %(lineNum)s]- %(levelName)s\\n%(message)s\\n`
    - exclude_funcs(list[str]): 排除的函数列表, 用于追溯调用位置时，排除父级调用函数，排除的函数链应是完整的，只写顶层的函数名将可能不会产生效果, 默认为空列表
    - highlight_type(str|None): 高亮模式. 默认为 `ASNI`，取消高亮则使用 None。当前支持 `ASNI`
    - **kwargs, 消息格式中的自定义参数，使用方法见示例

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

    - 如需添加自定义的参数, 可以在初始化中添加, 并可以在后续对相应的属性进行赋值

    logger = Logger(log_name='test', log_path='D:/test', message_format='%(asctime)s-%(levelName)s -%(message)s -%(happyNewYear)s', happyNewYear=False)

    logger.happyNewYear = True

    logger.debug('debug message')

    得到输出：`2025-01-01 06:30:00-INFO -debug message -True`
    """

    def __init__(
        self,
        log_name: str,
        log_path: str,
        log_sub_folder_name: str = '',
        log_level: str = _LogLevel.INFO,
        default_level: str = _LogLevel.INFO,
        console_output: bool = True,
        file_output: bool = True,
        size_limit: int = -1,  # KB
        count_limit: int = -1,
        days_limit: int = -1,
        split_by_day: bool = False,
        message_format: str = '%(scriptPath)s", line %(lineNum)s\n[%(asctime)s] [module: %(moduleName)s] [class: %(className)s] [function: %(functionName)s] [line: %(lineNum)s]- %(levelName)s\n%(message)s\n',
        exclude_funcs: list = [],
        highlight_type: str | None = 'ASNI',
        ** kwargs,
    ) -> None:
        self.__log_name = log_name
        self.__log_path = os.path.join(log_path, 'Log')
        self.__log_sub_folder_name = log_sub_folder_name if isinstance(log_sub_folder_name, str) else ''
        self.__log_level = log_level if log_level in _LogLevel else _LogLevel.INFO
        self.__default_level = default_level if default_level in _LogLevel else _LogLevel.INFO
        self.__doConsoleOutput = console_output if isinstance(console_output, bool) else True
        self.__doFileOutput = file_output if isinstance(file_output, bool) else True
        self.__size_limit = size_limit * 1000 if isinstance(size_limit, int) else -1
        self.__count_limit = count_limit if isinstance(count_limit, int) else -1
        self.__days_limit = days_limit if isinstance(days_limit, int) else -1
        self.__doSplitByDay = split_by_day if isinstance(split_by_day, bool) else False
        self.__message_format = message_format if isinstance(
            message_format, str) else '%(scriptPath)s", line %(lineNum)s\n[%(asctime)s] [module: %(moduleName)s] [class: %(className)s] [function: %(functionName)s] [line: %(lineNum)s]- %(levelName)s\n%(message)s\n'
        self.__exclude_funcs_list = exclude_funcs if isinstance(exclude_funcs, list) else []
        self.__highlight_type = highlight_type if isinstance(highlight_type, (str, type(None))) and highlight_type in _HighlightType else _HighlightType.ASNI
        self.__kwargs = kwargs
        self.__dict__.update(kwargs)
        self.__init_params()
        self.__clear_files()

    def __init_params(self):
        self.__var_dict = {  # 日志变量字典
            'asctime': '',
            'moduleName': '',
            'functionName': '',
            'className': '',
            'levelName': '',
            'lineNum': '',
            'message': '',
            'scriptName': '',
        }
        self.__var_dict.update(self.__kwargs)
        self.__exclude_funcs = {}  # 存储 __find_caller 中忽略的函数
        self.__exclude_funcs.update(self.__class__.__dict__)
        for item in self.__exclude_funcs_list:
            self.__exclude_funcs[item] = ''
        self.__current_size = 0
        self.__current_day = datetime.today().date()
        self.__isNewFile = True
        self.__level_color_dict = {
            _LogLevel.DEBUG: (_TxtColor.LIGHTGREEN, '', False, False),
            _LogLevel.INFO: (_TxtColor.BLUE, '', False, False),
            _LogLevel.WARNING: (_TxtColor.LIGHTYELLOW, '', True, False),
            _LogLevel.ERROR: (_TxtColor.WHITE, _BgColor.LIGHTRED, True, False),
            _LogLevel.CRITICAL: (_TxtColor.LIGHTYELLOW, _BgColor.RED, True, True),
        }
        self.__log_level_dict = {
            _LogLevel.DEBUG: 10,
            _LogLevel.INFO: 20,
            _LogLevel.WARNING: 30,
            _LogLevel.ERROR: 40,
            _LogLevel.CRITICAL: 50,
        }

    def __set_log_file_path(self):
        """ 设置日志文件路径 """
        # 支持的字符 {}[];'',.!~@#$%^&()_+-=
        if not hasattr(self, '_Logger__log_file_path'):  # 初始化, 创建属性
            self.__start_time = datetime.now()
            self.__start_time_format = self.__start_time.strftime("%Y%m%d_%H'%M'%S")
            if not os.path.exists(os.path.join(self.__log_path, self.__log_sub_folder_name)):
                os.makedirs(os.path.join(self.__log_path, self.__log_sub_folder_name))
            self.__log_file_path = os.path.join(self.__log_path, self.__log_sub_folder_name, f'{self.__log_name}-[{self.__start_time_format}]--0.log')
        else:
            file_name = os.path.splitext(os.path.basename(self.__log_file_path))[0]
            str_list = file_name.split('--')
            self.__log_file_path = os.path.join(self.__log_path, self.__log_sub_folder_name, f'{str_list[0]}--{int(str_list[-1]) + 1}.log')

    def __call__(self, *args, **kwargs) -> None:
        call_dict = {
            _LogLevel.DEBUG: self.debug,
            _LogLevel.INFO: self.info,
            _LogLevel.WARNING: self.warning,
            _LogLevel.ERROR: self.error,
            _LogLevel.CRITICAL: self.critical,
        }
        if self.__default_level in call_dict:
            call_dict[self.__default_level](*args, **kwargs)
        else:
            raise TypeError("'module' object is not callable. Please use Logger.debug/info/warning/error/critical to log.")

    def __setattr__(self, name: str, value) -> None:
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
        if (not isinstance(self.__count_limit, int) and self.__count_limit < 0) or (not isinstance(self.__days_limit, int) and self.__days_limit <= 0):
            return
        current_folder_path = os.path.join(self.__log_path, self.__log_sub_folder_name)
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

    def __find_caller(self):
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
            if fn.function not in self.__exclude_funcs and f'_Logger__{unprefix_variable}' not in self.__exclude_funcs:  # 不在排除列表中, 同时也排除当前类中的私有方法
                caller_name = fn.function
                class_name = fn.frame.f_locals.get('self', None).__class__.__name__ if 'self' in fn.frame.f_locals else ''
                linenum = fn.lineno
                module_name = os.path.splitext(os.path.basename(fn.filename))[0]
                script_name = os.path.basename(fn.filename)
                func = fn
                break
        return {
            'caller': func,
            'caller_name': caller_name,
            'class_name': class_name,
            'line_num': linenum,
            'module_name': module_name,
            'script_name': script_name,
            'script_path': func.filename,
        }

    def __color(self, message: str, *args, **kwargs):
        """ 颜色样式渲染 """
        if self.__highlight_type is None:
            return message
        if self.__highlight_type == _HighlightType.ASNI:
            return asni_ct(text=message, *args, **kwargs)
        return message

    def __format(self, log_level: str, *args):
        """ 格式化日志信息 """
        msg = ' '.join(str(arg) for arg in args)
        caller_info = self.__find_caller()
        self.__var_dict['asctime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.__var_dict['moduleName'] = caller_info['module_name']
        self.__var_dict['scriptName'] = caller_info['script_name']
        self.__var_dict['scriptPath'] = caller_info['script_path']
        self.__var_dict['functionName'] = caller_info['caller_name']
        self.__var_dict['className'] = caller_info['class_name']
        self.__var_dict['levelName'] = log_level
        self.__var_dict['lineNum'] = caller_info['line_num']
        self.__var_dict['message'] = msg
        pattern = r'%\((.*?)\)(\.\d+)?([sdfxXobeEgGc%])'
        used_var_names = re.findall(pattern, self.__message_format)
        # 普通消息
        used_vars = {name[0]: self.__var_dict[name[0]] for name in used_var_names if name[0] in self.__var_dict}
        text = self.__message_format % used_vars + '\n'
        # 高亮消息
        if log_level in self.__level_color_dict:
            self.__var_dict['levelName'] = self.__color(
                log_level,
                txt_color=self.__level_color_dict[log_level][0],
                bg_color=self.__level_color_dict[log_level][1],
                bold=self.__level_color_dict[log_level][2],
                blink=self.__level_color_dict[log_level][3])
        used_vars = {name[0]: self.__var_dict[name[0]] for name in used_var_names if name[0] in self.__var_dict}
        text_with_color = self.__message_format % used_vars + '\n'
        return text_with_color, text

    def __printf(self, message: str):
        """ 打印日志信息 """
        if not self.__doConsoleOutput:
            return
        sys.stdout.write(message)

    def __write(self, message: str):
        """ 写入日志信息 """
        if not self.__doFileOutput:
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
# <file time> This log file is created at\t {file_time}.
# <start time> This Program is started at\t {start_time}.
{'#'*66}\n\n{message}"""
            self.__current_size = len(message.encode('utf-8'))

        with open(self.__log_file_path, 'a', encoding='utf-8') as f:
            f.write(message)

    def __output(self, level, *args, **kwargs):
        txs, tx = self.__format(level, *args)
        self.__write(tx)
        self.__printf(txs)

    def debug(self, *args, **kwargs):
        """ 打印调试信息 """
        if self.__log_level_dict[self.__log_level] > self.__log_level_dict[_LogLevel.DEBUG]:
            return
        self.__output(_LogLevel.DEBUG, *args, **kwargs)

    def info(self, *args, **kwargs):
        """ 打印信息 """
        if self.__log_level_dict[self.__log_level] > self.__log_level_dict[_LogLevel.INFO]:
            return
        self.__output(_LogLevel.INFO, *args, **kwargs)

    def warning(self, *args, **kwargs):
        """ 打印警告信息 """
        if self.__log_level_dict[self.__log_level] > self.__log_level_dict[_LogLevel.WARNING]:
            return
        self.__output(_LogLevel.WARNING, *args, **kwargs)

    def error(self, *args, **kwargs):
        """ 打印错误信息 """
        if self.__log_level_dict[self.__log_level] > self.__log_level_dict[_LogLevel.ERROR]:
            return
        self.__output(_LogLevel.ERROR, *args, **kwargs)

    def exception(self, *args, **kwargs):
        """ 打印异常信息 """
        exception_str = traceback.format_exc()
        if exception_str == f'{type(None).__name__}: {None}\n':
            return
        self.error(exception_str, *args, **kwargs)

    def critical(self, *args, **kwargs):
        """ 打印严重错误信息 """
        if self.__log_level_dict[self.__log_level] > self.__log_level_dict[_LogLevel.CRITICAL]:
            return
        self.__output(_LogLevel.CRITICAL, *args, **kwargs)
