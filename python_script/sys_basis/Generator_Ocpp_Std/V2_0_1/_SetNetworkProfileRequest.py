from ocpp.v201.enums import *
from ocpp.v201 import call
from ._Base import *


class set_network_profile_request(Base_OCPP_Struct_V2_0_1):

    @staticmethod
    def generate(
        configuration_slot: int,
        connection_data: dict,
        custom_data: dict | None = None
    ) -> call.SetNetworkProfile:
        """
        Generate SetNetworkProfileRequest

        - Args: 
            - configuration_slot(int): 
                - Slot in which the configuration should be stored. 
            - connection_data(dict): 
                - Communication_ Function The NetworkConnectionProfile defines the functional and technical parameters of a communication link. 
                - recommended to use `get_connection_data()` to set element
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - call.SetNetworkProfile
        """
        return call.SetNetworkProfile(
            configuration_slot = configuration_slot,
            connection_data = connection_data,
            custom_data = custom_data
        )

    @staticmethod
    def load_dict(dict_data: dict) -> call.SetNetworkProfile:
        """
        Load dictionary data and convert the dictionary into the ocpp dataclass.

        - Args:
            - dict_data(dict): data of dictionary. It should comply with the OCPP message format (JSON).

        - Returns:
            - call.SetNetworkProfile
        """
        return call.SetNetworkProfile(
            configuration_slot = dict_data['configurationSlot'],
            connection_data = dict_data['connectionData'],
            custom_data = dict_data.get('customData', None)
        )


    @staticmethod
    def get_apn(
        apn: str,
        apn_authentication: str | APNAuthenticationType,
        apn_user_name: str | None = None,
        apn_password: str | None = None,
        sim_pin: int | None = None,
        preferred_network: str | None = None,
        use_only_preferred_network: bool | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get apn

        - Args: 
            - apn(str): 
                - APN. APN. URI The Access Point Name as an URL. 
                - length limit: [1, 512]
            - apn_authentication(str): 
                - APN. APN_ Authentication. APN_ Authentication_ Code Authentication method. 
                - Enum: `CHAP`, `NONE`, `PAP`, `AUTO`
                - Or use EnumClass (Recommended): `APNAuthenticationType`. e.g. `APNAuthenticationType.chap`
            - apn_user_name(str|None): 
                - APN. APN. User_ Name APN username. 
                - length limit: [1, 20]
            - apn_password(str|None): 
                - APN. APN. Password APN Password. 
                - length limit: [1, 20]
            - sim_pin(int|None): 
                - APN. SIMPIN. PIN_ Code SIM card pin code. 
            - preferred_network(str|None): 
                - APN. Preferred_ Network. Mobile_ Network_ ID Preferred network, written as MCC and MNC concatenated. See note. 
                - length limit: [1, 6]
            - use_only_preferred_network(bool|None): 
                - APN. Use_ Only_ Preferred_ Network. Indicator Default: false. Use only the preferred Network, do not dial in when not available. See Note. 
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'apn': apn,
            'apnAuthentication': apn_authentication
        }
        if apn_user_name is not None:
            temp_dict['apnUserName'] = apn_user_name
        if apn_password is not None:
            temp_dict['apnPassword'] = apn_password
        if sim_pin is not None:
            temp_dict['simPin'] = sim_pin
        if preferred_network is not None:
            temp_dict['preferredNetwork'] = preferred_network
        if use_only_preferred_network is not None:
            temp_dict['useOnlyPreferredNetwork'] = use_only_preferred_network
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict


    @staticmethod
    def get_vpn(
        server: str,
        user: str,
        password: str,
        key: str,
        type: str | VPNType,
        group: str | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get vpn

        - Args: 
            - server(str): 
                - VPN. Server. URI VPN Server Address 
                - length limit: [1, 512]
            - user(str): 
                - VPN. User. User_ Name VPN User 
                - length limit: [1, 20]
            - password(str): 
                - VPN. Password. Password VPN Password. 
                - length limit: [1, 20]
            - key(str): 
                - VPN. Key. VPN_ Key VPN shared secret. 
                - length limit: [1, 255]
            - type(str): 
                - VPN. Type. VPN_ Code Type of VPN 
                - Enum: `IKEv2`, `IPSec`, `L2TP`, `PPTP`
                - Or use EnumClass (Recommended): `VPNType`. e.g. `VPNType.ikev2`
            - group(str|None): 
                - VPN. Group. Group_ Name VPN group. 
                - length limit: [1, 20]
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'server': server,
            'user': user,
            'password': password,
            'key': key,
            'type': type
        }
        if group is not None:
            temp_dict['group'] = group
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict


    @staticmethod
    def get_connection_data(
        ocpp_version: str | OCPPVersionType,
        ocpp_transport: str | OCPPTransportType,
        ocpp_csms_url: str,
        message_timeout: int,
        security_profile: int,
        ocpp_interface: str | OCPPInterfaceType,
        apn: dict | None = None,
        vpn: dict | None = None,
        custom_data: dict | None = None
    ) -> dict:
        """
        Get connection data

        - Args: 
            - ocpp_version(str): 
                - Communication_ Function. OCPP_ Version. OCPP_ Version_ Code Defines the OCPP version used for this communication function. 
                - Enum: `OCPP12`, `OCPP15`, `OCPP16`, `OCPP20`
                - Or use EnumClass (Recommended): `OCPPVersionType`. e.g. `OCPPVersionType.ocpp12`
            - ocpp_transport(str): 
                - Communication_ Function. OCPP_ Transport. OCPP_ Transport_ Code Defines the transport protocol (e.g. SOAP or JSON). Note: SOAP is not supported in OCPP 2.0, but is supported by other versions of OCPP. 
                - Enum: `JSON`, `SOAP`
                - Or use EnumClass (Recommended): `OCPPTransportType`. e.g. `OCPPTransportType.json`
            - ocpp_csms_url(str): 
                - Communication_ Function. OCPP_ Central_ System_ URL. URI URL of the CSMS(s) that this Charging Station  communicates with. 
                - length limit: [1, 512]
            - message_timeout(int): 
                - Duration in seconds before a message send by the Charging Station via this network connection times-out. The best setting depends on the underlying network and response times of the CSMS. If you are looking for a some guideline: use 30 seconds as a starting point. 
            - security_profile(int): 
                - This field specifies the security profile used when connecting to the CSMS with this NetworkConnectionProfile. 
            - ocpp_interface(str): 
                - Applicable Network Interface. 
                - Enum: `Wired0`, `Wired1`, `Wired2`, `Wired3`, `Wireless0`, `Wireless1`, `Wireless2`, `Wireless3`
                - Or use EnumClass (Recommended): `OCPPInterfaceType`. e.g. `OCPPInterfaceType.wired0`
            - apn(dict|None): 
                - APN Collection of configuration data needed to make a data-connection over a cellular network. NOTE: When asking a GSM modem to dial in, it is possible to specify which mobile operator should be used. This can be done with the mobile country code (MCC) in combination with a mobile network code (MNC). Example: If your preferred network is Vodafone Netherlands, the MCC=204 and the MNC=04 which means the key PreferredNetwork = 20404 Some modems allows to specify a preferred network, which means, if this network is not available, a different network is used. If you specify UseOnlyPreferredNetwork and this network is not available, the modem will not dial in. 
                - recommended to use `get_apn()` to set element
            - vpn(dict|None): 
                - VPN VPN Configuration settings 
                - recommended to use `get_vpn()` to set element
            - custom_data(dict|None): 
                - This class does not get 'AdditionalProperties = false' in the schema generation, so it can be extended with arbitrary JSON properties to allow adding custom data.
                - recommended to use `get_custom_data()` to set element

        - Returns:
            - temp_dict(dict)
        """
        temp_dict:dict = {
            'ocppVersion': ocpp_version,
            'ocppTransport': ocpp_transport,
            'ocppCsmsUrl': ocpp_csms_url,
            'messageTimeout': message_timeout,
            'securityProfile': security_profile,
            'ocppInterface': ocpp_interface
        }
        if apn is not None:
            temp_dict['apn'] = apn
        if vpn is not None:
            temp_dict['vpn'] = vpn
        if custom_data is not None:
            temp_dict['customData'] = custom_data
        return temp_dict

