import json
import inspect
import os


os.chdir(os.path.dirname(__file__))
WORKSPACE_PATH = os.getcwd()

WORD_GET = '获取'
WORD_ARGS = '参数'
WORD_RETURNS = '返回值'

WORD_GET = 'Get'
WORD_ARGS = '- Args'
WORD_RETURNS = '- Returns'


def find_module_path(module_name):
    module_list = module_name.split('.')
    try:
        module = __import__(module_name)
        init_file_path = inspect.getfile(module)
        module_root_path = os.path.dirname(init_file_path)
        return os.path.join(module_root_path, *module_list[1:])
    except (ImportError, TypeError):
        print(f"Module {module_name} is not found or cannot be inspected.")
        return ''


def find_schemas_folder_path(module_name):
    module_list = module_name.split('.')
    try:
        module = __import__(module_name)
        init_file_path = inspect.getfile(module)
        module_root_path = os.path.dirname(init_file_path)
        return os.path.join(module_root_path, *module_list[1:], 'schemas')
    except (ImportError, TypeError):
        print(f"Module {module_name} is not found or cannot be inspected.")
        return ''


def find_schema_path_list(module_name):
    temp = []
    if os.path.exists(find_schemas_folder_path(module_name)):
        for fn in os.listdir(find_schemas_folder_path(module_name)):
            temp.append(os.path.join(find_schemas_folder_path(module_name), fn))
    return temp


class ScriptGenerator(object):
    def __init__(self, version):
        self.version = version
        if version == '201' or version == 201:
            from ocpp.v201 import call_result, call, enums
            self.lib_enums = enums
            self.import_str = 'V2_0_1'
            self.ocpp_version = 'ocpp.v201'
        elif version == '16' or version == 16:
            from ocpp.v16 import call_result, call, enums
            self.lib_enums = enums
            self.import_str = 'V1_6'
            self.ocpp_version = 'ocpp.v16'
        else:
            raise ValueError('重新输入版本, 可供候选: 201 16')
        self.var_type_dict = {
            'integer': 'int',
            'string': 'str',
            'boolean': 'bool',
            'number': 'int | float',
            'array': 'list',
            'object': 'dict'
        }
        self.special_cases_201_dict = {
            'ChargingProfileStatusType': 'ChargingProfileStatus',
            'MonitoringBaseType': 'MonitorBaseType'
        }
        self.special_cases_16_dict = {
            'BootNotificationResponse': 'RegistrationStatus',
            'ChangeAvailabilityRequest': 'AvailabilityType',
            'ChangeAvailabilityResponse': 'AvailabilityStatus',
            'ChangeConfigurationResponse': 'ConfigurationStatus',
            'ClearChargingProfileRequest': 'ChargingProfilePurposeType',
            'DiagnosticsStatusNotificationRequest': 'DiagnosticsStatus',
            'FirmwareStatusNotificationRequest': 'FirmwareStatus',
            'GetCompositeScheduleRequest': 'ChargingRateUnitType',
            'MeterValuesRequest_context': 'ReadingContext',
            'MeterValuesRequest_format': 'ValueFormat',
            'MeterValuesRequest_measurand': 'Measurand',
            'MeterValuesRequest_phase': 'Phase',
            'MeterValuesRequest_location': 'Location',
            'MeterValuesRequest_unit': 'UnitOfMeasure',
            'RemoteStartTransactionResponse': 'RemoteStartStopStatus',
            'RemoteStopTransactionResponse': 'RemoteStartStopStatus',
            'ReserveNowResponse': 'ReservationStatus',
            'SendLocalListRequest_status': 'AuthorizationStatus',
            'SendLocalListRequest_updateType': 'UpdateType',
            'SendLocalListResponse': 'UpdateStatus',
            'SetChargingProfileResponse': 'ChargingProfileStatus',
            'StatusNotificationRequest_errorCode': 'ChargePointErrorCode',
            'StatusNotificationRequest_status': 'ChargePointStatus',
            'StopTransactionRequest_reason': 'Reason',
            'StopTransactionRequest_context': 'ReadingContext',
            'StopTransactionRequest_format': 'ValueFormat',
            'StopTransactionRequest_measurand': 'Measurand',
            'StopTransactionRequest_phase': 'Phase',
            'StopTransactionRequest_location': 'Location',
            'StopTransactionRequest_unit': 'UnitOfMeasure',
            'TriggerMessageRequest': 'MessageTrigger',
            'UnlockConnectorResponse': 'UnlockStatus'
        }
        self.replace_dict = {
            '&lt;': '<',
            '&gt;': '>',
            '&amp;': '&',
            '&quot;': '"',
            '&apos;': "'",
            '’': "'",
            '‘': "'",

        }
        self.schema_list = find_schema_path_list(self.ocpp_version)
        self.run()

    def __camel_to_snake_file_name(self, name):
        result = []
        for char in name:
            char: str
            if char.isupper():
                if result:
                    result.append('_')
                result.append(char.lower())
            else:
                result.append(char)
        result_str = ''.join(result)
        return result_str.replace('_e_v_', '_ev_')

    def __snake_to_camel_string(self, snake_str):
        if not isinstance(snake_str, str):
            raise ValueError("Input must be a string")
        snake_str = snake_str.replace("soc_limit_reached", "SOCLimitReached")
        snake_str = snake_str.replace("ocpp_csms", "ocppCSMS")
        snake_str = snake_str.replace("_v2x", "V2X").replace("_v2g", "V2G").replace("_url", "URL")
        snake_str = snake_str.replace("soc", "SoC").replace("_socket", "Socket")
        components = snake_str.split("_")
        camel_case = components[0] + "".join(x.capitalize() for x in components[1:])
        return camel_case

    def __camel_to_snake_string(self, camel_str):
        if not isinstance(camel_str, str):
            raise ValueError("Input must be a string")
        camel_str = camel_str.replace("SOCLimitReached", "soc_limit_reached")
        camel_str = camel_str.replace("ocppCSMS", "ocpp_csms")
        camel_str = camel_str.replace("V2X", "_v2x").replace("V2G", "_v2g").replace("URL", "_url")
        camel_str = camel_str.replace("SoC", "soc").replace("Socket", "_socket")
        snake_case = []
        for idx, char in enumerate(camel_str):
            if char.isupper():
                if snake_case and camel_str[idx - 1].islower():
                    snake_case.append('_')
                snake_case.append(char.lower())
            else:
                snake_case.append(char)
        return "".join(snake_case)

    def __read_ref(self, data: dict, link_path: str):
        if link_path == '':
            return ''
        link_list = link_path.split('/')
        for link_item in link_list:
            if link_item == '#':
                continue
            data = data[link_item]
        return data

    def get_type(self, root_dict: dict, data: dict, dataclass_name_py=''):
        def sort_properties() -> list:
            sorted_properties_list = []
            unrequired_properties = []
            for property_item in properties_dict.keys():
                if property_item == 'customData':
                    continue
                if property_item in required_properties:
                    sorted_properties_list.append(property_item)
                else:
                    unrequired_properties.append(property_item)
            sorted_properties_list.extend(unrequired_properties)
            if 'customData' in properties_dict.keys():
                sorted_properties_list.append('customData')
            return sorted_properties_list

        def get_description(data: dict):
            content: str = ''
            description: str = data.get('description', None)
            if description:
                description = description.replace('\r\n\r\n', '\r\n')
                for old_str, new_str in self.replace_dict.items():
                    description = description.replace(old_str, new_str)
                if '\r\n' in description:
                    description = ' '.join(item for item in description.split('\r\n') if 'uid:' not in item)
                content += """
                - """ + description if description else ''
            return content

        def get_limit(data: dict, type_str: str):
            content = ''
            if type_str in ['int', 'float']:
                minimum = data.get('minimum', 1)
                maximum = data.get('maximum', None)
                if maximum:
                    content += f"""
                - length limit: [{minimum}, {maximum}]"""
            elif type_str == 'str':
                minLength = data.get('minLength', 1)
                maxLength = data.get('maxLength', None)
                format_str = data.get('format', None)
                if maxLength:
                    content += f"""
                - length limit: [{minLength}, {maxLength}]"""
                if format_str:
                    content += f"""
                - format: {format_str}"""
            elif type_str == 'list':
                minItems = data.get('minItems', 1)
                maxItems = data.get('maxItems', None)
                if maxItems:
                    content += f"""
                - length limit: [{minItems}, {maxItems}]"""
            elif type_str == 'dict':
                pass
            return content

        def get_enum(ref_data: dict, property_item, root_dict):
            """ 
            参数：
                ref_data (dict): 实际的字典内容
                property_item (dict): 
                root_dict (dict): 
            返回：
                str
            """
            if 'enum' not in ref_data:
                return ''
            enum_str: str = ref_data.get('javaType', '').replace('Enum', 'Type')
            if self.import_str == 'V2_0_1':
                if enum_str in self.special_cases_201_dict:
                    enum_str = self.special_cases_201_dict[enum_str]
                return enum_str
            # 针对 V16 的处理
            if '$ref' in property_item:  # 链接
                enum_str_from_key: str = property_item['$ref'].split('/')[-1].replace('EnumType', 'Type')
            else:
                enum_str_from_key: str = property_item.replace('EnumType', 'Type')
            if 'title' in root_dict:
                identity = root_dict['title']
            elif '$id' in root_dict:
                identity = root_dict['$id'].split(':')[-1].split('.')[0]
            else:
                identity = enum_str_from_key
            if not enum_str or not hasattr(self.lib_enums, enum_str):
                if hasattr(self.lib_enums, enum_str_from_key):
                    enum_str = enum_str_from_key
                elif hasattr(self.lib_enums, enum_str_from_key.replace('Type', '')):
                    enum_str = enum_str_from_key.replace('Type', '')
                elif hasattr(self.lib_enums, enum_str_from_key.replace('Type', '').replace('Install', '')):
                    enum_str = enum_str_from_key.replace('Type', '').replace('Install', '')
                elif hasattr(self.lib_enums, identity.replace('Response', 'Status')):
                    enum_str = identity.replace('Response', 'Status')
                elif hasattr(self.lib_enums, identity.replace('Request', 'Type')):
                    enum_str = identity.replace('Request', 'Type')

            if not enum_str:
                if 'title' in root_dict:
                    identity = root_dict['title']
                elif '$id' in root_dict:
                    identity = root_dict['$id'].split(':')[-1].split('.')[0]
                else:
                    identity = enum_str_from_key
                enum_str = self.special_cases_16_dict.get(identity, '')
                if enum_str and hasattr(self.lib_enums, enum_str):
                    return enum_str
                else:
                    identity = f'{identity}_{enum_str_from_key}'
                    enum_str = self.special_cases_16_dict.get(identity, '')
            return enum_str

        def get_commentary_enum(data: dict, var_type: str):
            content = ''
            enum_list = data.get('enum', [])
            enum_str = '`' + '`, `'.join(enum_list) + '`'
            enum_class_str: str = data.get('javaType', None)
            if not enum_class_str and '|' in var_type:
                enum_class_str = var_type.split('|')[1]
            if enum_class_str and self.import_str == 'V2_0_1':
                enum_class_str = enum_class_str.replace('Enum', 'Type')
                if enum_class_str in self.special_cases_201_dict:
                    enum_class_str = self.special_cases_201_dict[enum_class_str]
            if enum_list:
                content += f"""
                - Enum: {enum_str}
                - Or use EnumClass (Recommended): `{enum_class_str}`. e.g. `{enum_class_str}.{self.__camel_to_snake_string(enum_list[0])}`"""
            return content

        def get_commentary(var_type_str: str, root_dict, property_item):
            if var_type_str:
                if self.import_str == 'V2_0_1':
                    var_type_str = ''.join(item for item in var_type_str.split(' ') if 'Type' not in item)  # 过滤掉包含 'Type' 的项
                else:
                    var_type_str = ''.join(var_type_str.split(' '))  # 过滤掉包含 'Type' 的项
                if var_type_str.endswith('|'):  # 如果类型以 '|' 结尾，去掉最后一个 '|'
                    var_type_str = var_type_str[:-1]
            var_type_format = f"({var_type_str.replace(' ', '')})" if var_type_str else ''
            content = ''
            if 'dict' in var_type_format:
                # object 类型
                if '$ref' in property_item:
                    ref_data = self.__read_ref(root_dict, property_item['$ref'])
                    content += get_description(ref_data)
                    content += get_limit(ref_data, 'dict')
                content += """
                - """ + f'recommended to use `get_{py_attr}()` to set element'
            elif 'list' in var_type_format:
                # array 类型
                if '$ref' in property_item['items']:
                    ref_data = self.__read_ref(root_dict, property_item['items']['$ref'])
                    content += get_description(ref_data)
                    content += get_limit(property_item, 'list')
                content += """
                - """ + f'recommended to use `get_{py_attr}()` to set element or to build a custom list.'
            elif 'str' in var_type_format:
                # string 类型
                if '$ref' in property_item:
                    ref_data = self.__read_ref(root_dict, property_item['$ref'])
                    content += get_description(ref_data)
                    if 'enum' in ref_data:
                        content += get_commentary_enum(ref_data, var_type_str)
                    content += get_limit(ref_data, 'str')
                else:
                    content += get_description(property_item)
                    if 'enum' in property_item:
                        content += get_commentary_enum(property_item, var_type_str)
                    content += get_limit(property_item, 'str')
            elif 'float' in var_type_format:
                # number 类型
                if '$ref' in property_item:
                    ref_data = self.__read_ref(root_dict, property_item['$ref'])
                    content += get_description(ref_data)
                    content += get_limit(ref_data, 'float')
                else:
                    content += get_description(property_item)
                    content += get_limit(property_item, 'float')
            else:
                # integer 类型, 当前jsonschema中没有其他类型, 如：boolean, null
                if '$ref' in property_item:
                    ref_data = self.__read_ref(root_dict, property_item['$ref'])
                    content += get_description(ref_data)
                    content += get_limit(ref_data, 'int')
                else:
                    content += get_description(property_item)
                    content += get_limit(property_item, 'int')
            return content, var_type_format

        varis = '''
        '''
        commentary = """
            """
        return_dataclass = ''
        func_body = """
        """
        temp_dict_str = """
            """
        return_dict = ''
        if 'properties' not in data:
            return varis.strip(), return_dict, commentary.strip(), func_body.strip(), return_dataclass
        properties_dict: dict = data['properties']
        required_properties = data.get('required', [])
        sorted_properties_list = sort_properties()

        for json_attr in sorted_properties_list:
            if varis != '''
        ''':
                varis += ''',
        '''
            if commentary != """
            """:
                commentary += """
            """
            if return_dataclass != '':
                return_dataclass += """,
            """
            if func_body != """
        """:
                func_body += """
        """
            if return_dict != '':
                return_dict += """,
            """
            py_attr = self.__camel_to_snake_string(json_attr)
            property_item: dict = properties_dict[json_attr]
            if '$ref' in property_item:
                ref_data = self.__read_ref(root_dict, property_item['$ref'])
                var_type = ref_data.get('type', '')
                if var_type == 'string':
                    enum_str = get_enum(ref_data, property_item, root_dict=root_dict)
                    var_type = f'str | {enum_str}' if enum_str else f'{var_type}'
            else:
                var_type: str = property_item.get('type', '')
                if var_type == 'string':
                    enum_str = get_enum(property_item, json_attr, root_dict=root_dict)
                    var_type = f'str | {enum_str}' if enum_str else f'{var_type}'
            var_type_str: str = self.var_type_dict.get(var_type, None) if not var_type.startswith('str | ') else var_type
            # 变量注解
            if json_attr in required_properties:  # 必须属性
                varis += f'{py_attr}: {var_type_str}'
                # 函数体
                if temp_dict_str != """
            """:
                    temp_dict_str += """,
            """
                temp_dict_str += f"'{json_attr}': {py_attr}"
                # 函数返回值
                return_dict += f"{py_attr} = dict_data['{json_attr}']"
            else:   # 非必须属性
                if var_type:
                    sign = ': '
                    none_str = f' | None'
                    var_type_str = f'{var_type_str}{none_str}'
                func_body += f"""if {py_attr} is not None:
            temp_dict['{json_attr}'] = {py_attr}"""
                varis += f'{py_attr}{sign}{var_type_str} = None'
                # 函数返回值
                return_dict += f"{py_attr} = dict_data.get('{json_attr}', None)"
            # 注释
            content, var_type_format = get_commentary(var_type_str=var_type_str, root_dict=root_dict, property_item=property_item)
            commentary += f'- {py_attr}{var_type_format}: {content}'
            return_dataclass += f'{py_attr} = {py_attr}'
        temp_dict_str = f"""
        temp_dict:dict = {{{temp_dict_str}
        }}"""
        func_body = temp_dict_str + func_body
        return varis, return_dict, commentary, func_body, return_dataclass

    def __gen_main_generation_code(self, name: str, data: dict, code_text=''):
        dataclass_name_json = name
        dataclass_name_py = self.__camel_to_snake_file_name(dataclass_name_json)
        if dataclass_name_json.endswith('Response'):
            tmp = dataclass_name_json+'.file'
            std_dataclass_name = tmp.replace('Response.file', '')
            call_struct_import = 'call_result'
            data_class_name = f'call_result.{std_dataclass_name}'
        else:
            std_dataclass_name = dataclass_name_json
            if dataclass_name_json.endswith('Request'):
                tmp = dataclass_name_json+'.file'
            std_dataclass_name = tmp.replace('Request.file', '')
            call_struct_import = 'call'
            data_class_name = f'call.{std_dataclass_name}'
        varis, return_dict, commentary, func_body, return_dataclass = self.get_type(data, data, name)
        code_text += f'''from {self.ocpp_version}.enums import *
from {self.ocpp_version} import {call_struct_import}
from ._Base import *


class {dataclass_name_py}(Base_OCPP_Struct_{self.import_str}):

    @staticmethod
    def generate({varis}
    ) -> {data_class_name}:
        """
        Generate {dataclass_name_json}

        {WORD_ARGS}: {commentary}

        {WORD_RETURNS}:
            - {data_class_name}
        """
        return {data_class_name}(
            {return_dataclass}
        )

    @staticmethod
    def load_dict(dict_data: dict) -> {data_class_name}:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        {WORD_ARGS}:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        {WORD_RETURNS}:
            - {data_class_name}
        """
        return {data_class_name}(
            {return_dict}
        )

'''
        return code_text

    def __gen_sub_generation_code(self, name: str, root_dict: dict, data: dict, json_attr, code_text=''):
        if '$ref' in data:
            sub_data = self.__read_ref(root_dict, data['$ref'])
        else:
            sub_data = data
        if 'properties' not in sub_data:
            return code_text
        for sub_json_attr, value_dict in sub_data['properties'].items():
            if sub_json_attr == 'customData':
                continue
            if '$ref' in value_dict and 'type' not in value_dict:  # 排除 array
                ref_data = self.__read_ref(root_dict, value_dict['$ref'])
                if ref_data.get('type', None) == 'object':
                    code_text = self.__gen_sub_generation_code(name, root_dict, value_dict, sub_json_attr, code_text)
            elif 'type' in value_dict and value_dict['type'] in ['array']:
                code_text = self.__gen_sub_generation_code(name, root_dict, value_dict['items'], sub_json_attr, code_text)
            elif 'properties' in value_dict:
                code_text = self.__gen_sub_generation_code(name, root_dict, value_dict, sub_json_attr, code_text)
        varis, return_dict, commentary, func_body, return_dataclass = self.get_type(root_dict, sub_data, name)
        data_class_name = self.var_type_dict.get(sub_data['type'], '')
        if data_class_name:
            data_class_name = f' -> {data_class_name}'
        func_name = f'get_{self.__camel_to_snake_string(json_attr)}'
        code_text += f'''
    @staticmethod
    def {func_name}({varis}
    ){data_class_name}:
        """
        Get {func_name.replace('get_', '').replace('_', ' ')}

        {WORD_ARGS}: {commentary}

        {WORD_RETURNS}:
            - temp_dict(dict)
        """
        {func_body.strip()}
        return temp_dict

'''

        return code_text

    def gen_code(self, name: str, data: dict, code_text=''):
        if data.get('$schema', None):
            code_text = self.__gen_main_generation_code(name, data, code_text)
            if 'properties' not in data:
                return code_text
            for json_attr, value_dict in data['properties'].items():
                if json_attr == 'customData':
                    continue
                if '$ref' in value_dict and 'type' not in value_dict:  # 排除 array
                    ref_data = self.__read_ref(data, value_dict['$ref'])
                    if ref_data.get('type', None) == 'object':
                        code_text = self.__gen_sub_generation_code(name, data, value_dict, json_attr, code_text)
                elif 'type' in value_dict and value_dict['type'] in ['array']:
                    code_text = self.__gen_sub_generation_code(name, data, value_dict['items'], json_attr, code_text)
                    pass
        return code_text

    def run(self):
        for fp in self.schema_list:
            with open(fp, 'r', encoding='utf-8') as f:
                data = json.load(f)
            file_name: str = os.path.splitext(os.path.basename(fp))[0]
            if not file_name.endswith('Response') and not file_name.endswith('Request'):
                file_name += 'Request'
            py_file_name = f'_{file_name}.py'
            py_file_path = os.path.join(WORKSPACE_PATH, py_file_name)
            text = self.gen_code(file_name, data)
            with open(py_file_path, 'w', encoding='utf-8') as f:
                f.write(text)


a = ScriptGenerator('201')
