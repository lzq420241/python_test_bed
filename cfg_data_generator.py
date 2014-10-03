import socket
import glob
import os
import re

CFG_DATA_FOLDER_NAME = 'CFG_Data'
CFG_PARAMETERS_START_WITH_NAME = ['Framework', 'BTS', 'RNC-SIM', 'UE-SIM', 'WireShark']
SCRIPT_PATH = os.getenv("PEGASUS_SCRIPT_PATH", "")
if SCRIPT_PATH:
    CFG_DIR = os.path.dirname(os.path.dirname(SCRIPT_PATH))

TEST_VALUES = '10.69.195.137 10.69.216.160 "" 1'
# TEST_VALUES = 'SRAC 10.69.216.207 10.69.195.133 1'
#TEST_VALUES = 'SRAC "10.69.216.207\n10.69.216.13" 10.69.195.133 1'

# step 1
def create_Tool_Parameters_CFG_xml_file():
    _remove_CFG_parameter_xml_file()
    data_files_path = _get_CFG_data_files_path()
    data_files_path = _combine_tool_name_with_data_files_path(data_files_path)
    tool_ip_args = get_tool_names_for_get_items_name_value()
    '''
    tool_ip_args like :
    {0: {
    'UE-SIM': ['TM500', '10.1.1.2'],
    'Framework': ['Framework'],
    'RNC-SIM': ['Artiza', '10.1.1.1', 'Slot0'],
    'BTS': ['BTS', '10.141.54.114'],
    'WireShark': ['Wireshark', '10.1.1.3']
    }}
    '''
    for index_i, kw_tool_value_tool_ip in tool_ip_args.items():
        cfg_para_xml_file_name, cfg_xml_file_name = _modify_para_and_xml_file_name(index_i)
        tools_name, items_name_value = _combine_item_name_value_for_tool_names(data_files_path, kw_tool_value_tool_ip)
        property_file_strings = create_CFG_property_items(tools_name, items_name_value)
        _create_CFG_parameter_file(property_file_strings, cfg_para_xml_file_name)
        _create_CFG_xml_file(cfg_para_xml_file_name, cfg_xml_file_name)
        print "*" * 50


def _remove_CFG_parameter_xml_file():
    if SCRIPT_PATH:
        cfg_dir = '%s\\*.xml' % CFG_DIR
    else:
        cfg_dir = '..\*.xml'
    cfg_xml_files = glob.glob(cfg_dir)
    for cfg_xml_file in cfg_xml_files:
        if os.system('del /f %s' % cfg_xml_file):
            raise Exception('Error: delete file %s not success' % cfg_xml_file)


def _get_CFG_data_files_path():
    if SCRIPT_PATH:
        data_dir = '%s\\%s\\*' % (CFG_DIR, CFG_DATA_FOLDER_NAME)
    else:
        data_dir = '..\\%s\\*' % CFG_DATA_FOLDER_NAME
    cfg_tool_files = glob.glob(data_dir)
    return cfg_tool_files


def _combine_tool_name_with_data_files_path(data_files_path):
    data_file_path_dict = {}
    for data_file_path in data_files_path:
        cfg_para_tool_name = [x for x in CFG_PARAMETERS_START_WITH_NAME if x in data_file_path]
        if cfg_para_tool_name:
            data_file_path_dict[cfg_para_tool_name[0]] = data_file_path
    return data_file_path_dict


def _modify_para_and_xml_file_name(index_name):
    cfg_para_xml_file_name = 'Parameters_CFG.xml'
    cfg_xml_file_name = 'LRC_IV3G_TC_COM_CFG.xml'
    if 0 != index_name:
        cfg_para_xml_file_name = cfg_para_xml_file_name.replace('.xml', '_' + str(index_name) + '.xml')
        cfg_xml_file_name = cfg_xml_file_name.replace('.xml', '_' + str(index_name) + '.xml')
    return cfg_para_xml_file_name, cfg_xml_file_name


def _combine_item_name_value_for_tool_names(data_files_path, tool_ip_args):
    tools_name = []
    items_name_value = []
    for tool_name, file_path in data_files_path.items():
        if tool_ip_args[tool_name]:
            tools_name.append(tool_name)
            item_name_value = get_item_name_and_value(file_path, tool_ip_args[tool_name])
            items_name_value.append(item_name_value)
    return tools_name, items_name_value


def _create_CFG_parameter_file(property_file_strings, cfg_para_xml_file_name):
    if SCRIPT_PATH:
        cfg_dir = CFG_DIR
    else:
        cfg_dir = '..'
    para_cfg_path = os.sep.join([os.path.abspath(cfg_dir), cfg_para_xml_file_name])
    with open(para_cfg_path, 'wt') as f_obj:
        f_obj.writelines(property_file_strings)


def _create_CFG_xml_file(cfg_para_xml_file_name, cfg_xml_file_name):
    if SCRIPT_PATH:
        cfg_dir = CFG_DIR
    else:
        cfg_dir = '..'
    cfg_xml_items = _cfg_xml_items(cfg_para_xml_file_name)
    cfg_path = os.sep.join([os.path.abspath(cfg_dir), cfg_xml_file_name])
    with open(cfg_path, 'wt') as f_obj:
        f_obj.write(cfg_xml_items)


def _cfg_xml_items(cfg_para_xml_file_name):
    item_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<systemConfiguration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xi="http://www.w3.org/2001/XInclude">

  <systemUnderTests>
  </systemUnderTests>
  <testEquipments>
  </testEquipments>
  <physicalLinks/>
  
	<properties>
		<xi:include href="/IVLRC3G/Configs/%s"/>  
	</properties>
	
</systemConfiguration>

''' % cfg_para_xml_file_name
    return item_xml


# step 1.1
def get_tool_names_for_get_items_name_value():
    pegasus_args = _get_args_with_string_type_from_pegasus()
    ip_Artiza, ip_Tm500, ip_Wireshark, Artiza_Slot = _split_pegasus_args_2_list_through_spaces(pegasus_args)
    bts_kw = _get_tool_BTS_for_get_items_name_value()
    artiza_kw = _get_tool_Artiza_for_get_items_name_value(ip_Artiza, Artiza_Slot)
    wireshark_kw = _get_tool_Wireshark_for_get_items_name_value(ip_Wireshark)
    ip_Tm500s = _split_tool_Tm500s_ip_addresses(ip_Tm500)
    args_kw_ret = {}
    for i in range(len(ip_Tm500s)):
        tm500_kw = _get_tool_Tm500_for_get_items_name_value(ip_Tm500s[i])
        args_kw = _combine_tool_names_from_pegasus_paras(bts_kw, artiza_kw, tm500_kw, wireshark_kw)
        args_kw_ret[i] = args_kw
    return args_kw_ret


def _get_args_with_string_type_from_pegasus():
    if SCRIPT_PATH:
        pegasus_args = pegasus_script_item.getParameter('_args').getParameterValue()
    else:
        pegasus_args = TEST_VALUES
    return pegasus_args


def _split_pegasus_args_2_list_through_spaces(pegasus_args):
    args_list = pegasus_args.split(' ')
    ip_Artiza, ip_Tm500, ip_Wireshark, Artiza_Slot = args_list
    return ip_Artiza, ip_Tm500, ip_Wireshark, Artiza_Slot


def _get_tool_BTS_for_get_items_name_value():
    ip_BTS = _get_BTS_control_pc_ip_address()
    if _is_matched_with_ip_address_format(ip_BTS):
        return ['BTS', ip_BTS]
    raise Exception('Error: not match ip address-%s-' % ip_BTS)


def _get_BTS_control_pc_ip_address():
    host_ips = socket.gethostbyname_ex(socket.gethostname())[2]
    for host_ip in host_ips:
        if '192.168' not in host_ip:
            return host_ip


def _is_matched_with_ip_address_format(ip_address):
    ip_reg_exp = '\d+\.\d+\.\d+\.\d+'
    if re.match(ip_reg_exp, ip_address):
        return True


def _get_tool_Artiza_for_get_items_name_value(ip_address, slot_num):
    if _is_SRAC(ip_address) or _is_matched_with_ip_address_format(ip_address):
        return ['Artiza', ip_address, 'Slot' + slot_num]
    return None


def _is_SRAC(ip_address):
    return ('srac' in ip_address.lower())


def _get_tool_Tm500_for_get_items_name_value(ip_address):
    if _is_matched_with_ip_address_format(ip_address):
        return ['TM500', ip_address]
    return None


def _split_tool_Tm500s_ip_addresses(ip_address):
    ip_addresses = ip_address.splitlines()
    return ip_addresses


def _get_tool_Wireshark_for_get_items_name_value(ip_address):
    if _is_matched_with_ip_address_format(ip_address):
        return ['Wireshark', ip_address]
    return None


def _combine_tool_names_from_pegasus_paras(bts_kw, artiza_kw, tm500_kw, wireshark_kw):
    args_kw_for_find_items_from_data = {}
    args_kw_for_find_items_from_data.update({'BTS': bts_kw})
    args_kw_for_find_items_from_data.update({'RNC-SIM': artiza_kw})
    args_kw_for_find_items_from_data.update({'UE-SIM': tm500_kw})
    args_kw_for_find_items_from_data.update({'WireShark': wireshark_kw})
    args_kw_for_find_items_from_data.update({'Framework': ['Framework']})
    return args_kw_for_find_items_from_data


# step 4
def create_CFG_property_items(tool_names, items_name_value):
    item_head = _create_CFG_property_items_head()
    item_body = _create_CFG_property_items_body(tool_names, items_name_value)
    item_end = _create_CFG_property_items_end()
    item_property = item_head + item_body + item_end
    property_file_strings = '\n'.join(item_property)
    return property_file_strings


def _create_CFG_property_items_head():
    item_head = '''<?xml version="1.0" encoding="UTF-8"?>
<properties>'''
    return [item_head]


def _create_CFG_property_items_body(tool_names, items_name_value):
    item_body = []
    for i in range(len(tool_names)):
        tool_item_body = _create_CFG_property_items_body_with_tool(tool_names[i], items_name_value[i])
        item_body += tool_item_body
    return item_body


def _create_CFG_property_items_end():
    item_end = '</properties>'
    return [item_end]


def _create_CFG_property_items_body_with_tool(tool_name, tool_items_name_value):
    item_body = _create_CFG_property_items_comments(tool_name)
    item_body += _create_CFG_property_item_body(tool_items_name_value)
    return item_body


def _create_CFG_property_items_comments(tool_name):
    item_comments = '<!-- %s configuration -->' % tool_name
    print '\n' + item_comments
    return [item_comments]


def _create_CFG_property_item_body(items_name_value):
    items_property = []
    for item_name, item_value in items_name_value.items():
        item_name = item_name.strip()
        item_value = item_value.strip()
        item_property = _create_CFG_property_item(item_name, item_value)
        items_property.append(item_property)
        if item_name in ['CFG_Artiza_ControlPCAddress', 'CFG_Wireshark_PCAddress', 'CFG_TM500_ControlPCAddress',
                         'CFG_MT_ServerIP']:
            print item_name + ': ' + item_value
    return items_property


def _create_CFG_property_item(item_name, item_value):
    item_property = '''
    <property>
        <name>%s</name>
        <value>%s</value>
    </property>
    ''' % (item_name, item_value)
    return item_property


# step - 3
def get_item_name_and_value(data_file_path, args):
    f_read = _read_item_name_and_value_from_data_file(data_file_path)
    kw_with_ip, kw_nexe_item_with_ip = _get_keywords_for_cut_item_name_and_value(args)
    item_name_and_value = _cut_item_name_and_value_with_keywords(f_read, kw_with_ip, kw_nexe_item_with_ip)
    items = _find_all_item_name_and_value(item_name_and_value)
    _check_tool_data_files_are_matched_for_every_ne(data_file_path, f_read, kw_nexe_item_with_ip, items, args)
    return items


def _check_tool_data_files_are_matched_for_every_ne(data_file_path, f_read, kw_ne, items_name_value, args):
    f_read_list = f_read.split(kw_ne)[1:]
    f_read_string_list = []
    key_ne = kw_ne
    if 'Artiza' in str(args):
        if _is_SRAC(str(args)):
            key_ne = '_'.join([kw_ne, args[1]])
            f_read_list = f_read.split(kw_ne)
            for f_read_strings in f_read_list:
                if _is_SRAC(f_read_strings):
                    f_read_string_list.append(kw_ne + f_read_strings)
        else:
            for f_read_strings in f_read_list:
                if not _is_SRAC(f_read_strings):
                    f_read_string_list.append(kw_ne + f_read_strings)
    else:
        f_read_string_list = f_read_list
    data_file_name = os.path.basename(data_file_path)
    len_ne = f_read.count(key_ne)
    flag_error_items_name_more = False
    flag_error_items_name_less = False
    for item_name, item_value in items_name_value.items():
        for f_read_str in f_read_string_list:
            len_item_name = f_read_str.count(item_name + '=')
            if len_item_name > 1:
                flag_error_items_name_more = True
                print 'Error_more: -file "%s" -ne "%s" -parameter "%s" is more than 1 in 1 ne.' % (
                    data_file_name, f_read_str.split('\n')[0], item_name)
            elif len_item_name == 0:
                flag_error_items_name_less = True
                print 'Error_less: -file "%s" -ne "%s" -parameter "%s" is 0 in 1 ne.' % (
                    data_file_name, f_read_str.split('\n')[0], item_name)
    if flag_error_items_name_more or flag_error_items_name_less:
        raise Exception('Error_Result: so python will not create the xml files.')


def _read_item_name_and_value_from_data_file(data_file_path):
    with open(data_file_path, 'r') as f_obj:
        f_read = f_obj.read()
    f_read = f_read.replace(' =', '=').replace('= ', '=')
    return f_read


def _get_keywords_for_cut_item_name_and_value(args):
    kw_args = '_'.join(args)
    kw_with_ip = '[%s]' % kw_args
    kw_nexe_item_with_ip = '[%s' % args[0]
    return kw_with_ip, kw_nexe_item_with_ip


def _cut_item_name_and_value_with_keywords(f_read, kw_with_ip, kw_nexe_item_with_ip):
    items_with_ip = f_read.split(kw_with_ip)
    _is_only_one_kw_with_ip_in_data_file(len(items_with_ip))
    item_with_ip = items_with_ip[-1]
    item_name_and_value = item_with_ip.split(kw_nexe_item_with_ip)
    item_name_and_value = [x for x in item_name_and_value if x != '']
    item_name_and_value = item_name_and_value[0]
    return item_name_and_value


def _is_only_one_kw_with_ip_in_data_file(len_items_with_ip):
    assert (len_items_with_ip <= 2)


def _find_all_item_name_and_value(item_name_and_value):
    item_name_and_value = _move_empty_line(item_name_and_value)
    items = _find_all_item_name_and_value_through_reg(item_name_and_value)
    return items


def _move_empty_line(item_name_and_value):
    return item_name_and_value.replace('\n+', '\n')


def _find_all_item_name_and_value_through_reg(item_name_and_value):
    find_reg = '(.*?)=(.*?\n)'
    findall_group = re.findall(find_reg, item_name_and_value)
    return dict(findall_group)


if __name__ == '__main__':
    if SCRIPT_PATH:
        try:
            create_Tool_Parameters_CFG_xml_file()
            pegasus_script_item.passed("Result: Pass")
        except:
            pegasus_script_item.passed("Result: Fail")
    else:
        create_Tool_Parameters_CFG_xml_file()
