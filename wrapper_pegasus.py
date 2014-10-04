# -*- coding: utf-8 -*-
#!/bin/python
import os
import sys

# get script path when it runs with pegasus script.
SCRIPT_PATH = os.getenv("PEGASUS_SCRIPT_PATH", "")


def set_pythonpath():
    # Add LIB into PYTHONPATH
    if not SCRIPT_PATH:
        LRC_HOME = os.path.abspath(os.path.dirname(__file__))
    elif '__main__' == __name__:
        LRC_HOME = os.path.dirname(SCRIPT_PATH)
    elif os.path.dirname(__name__.replace(r'.', os.sep)) in map(lambda x: os.path.basename(x), sys.path):
        LRC_HOME = None
    else:
        raise Exception('The lrclib.runkeyword is not import the Needed lib')
    if LRC_HOME:
        SRC_HOME = os.path.dirname(LRC_HOME)
        # Add LRC_HOME into PYTHONPATH
        if LRC_HOME in sys.path:
            sys.path.remove(LRC_HOME)
        sys.path.insert(0, LRC_HOME)
        # Add SRC_HOME into PYTHONPATH
        if SRC_HOME in sys.path:
            sys.path.remove(SRC_HOME)
        sys.path.insert(0, SRC_HOME)
        # Add ext_lib into PYTHONPATH
        EXT_LIB_HOME = os.path.join(LRC_HOME, 'tools', 'ext_lib')
        for e in os.listdir(EXT_LIB_HOME):
            if e.endswith('.egg'):
                sys.path.insert(0, os.path.join(EXT_LIB_HOME, e))
set_pythonpath()


from tools import *
from base.errors import LrcValidateException, LrcException
from settings.logger import log_setting


def main(args=None):
    if sys.version_info < (2, 6, 0) or sys.version_info >= (3, 0, 0):
        raise LrcValidateException('Lrc lib requires python at least 2.6.')
    if SCRIPT_PATH:
        args = pegasus_script_item.getParameter('_args').getParameterValue()
        args = args.strip().split('\n')
    elif args is None:
        def _map_args(arg):
            arg = arg.strip()
            if arg == 'NULL':
                return ''
            return arg
        argv = map(_map_args, sys.argv)
        args = argv[1:]

    if not args or [''] == args:
        raise LrcValidateException('Please check the input args, it is None.')
    args = map(lambda x: str(x.strip()), args)
    kw_name = args[0]
    kw_args = args[1:]
    kw_args = _covert_type_2_list_or_dict(kw_args)
    try:
        logging.info("K[%s] Parameters: %s" % (kw_name, args[1:]))
        kw_result = getattr(sys.modules[__name__], kw_name)(*kw_args)
    except Exception, e:
        import traceback
        traceback.print_exc()
        console_err = '\n' + traceback.format_exc() + '-' * 30 + '\n'
        logging.error("%sK[%s] Failed\n%s" % (console_err, kw_name, '-' * 30))
        raise e
    else:
        return _parse_result(kw_name, kw_result)


def _covert_type_2_list_or_dict(kw_args):
    kw_args_eval = []
    for kw_arg in kw_args:
        if (kw_arg.startswith('\{') and kw_arg.endswith('\}')
            ) or (kw_arg.startswith('{') and kw_arg.endswith('}')
            ) or (kw_arg.startswith('[') and kw_arg.endswith(']')):
            kw_arg = eval(kw_arg.replace('\{', '{').replace('\}', '}'))
        kw_args_eval.append(kw_arg)
    return kw_args_eval


def _parse_result(kw_name, kw_result):
    if bool == type(kw_result) and not kw_result:
        logging.error("K[%s] Failed" % kw_name)
        raise LrcException("K[%s]: Failed" % kw_name)
    elif SCRIPT_PATH:
        if isinstance(kw_result, tuple) or isinstance(kw_result, dict) or isinstance(kw_result, str) or isinstance(kw_result, int):
            paramters = pegasus_script_item.getParameter('Output_Param').getParameterValue().split(',')
            if isinstance(kw_result, tuple):
                if len(kw_result) > len(paramters):
                    raise LrcException("K[%s]: Failed real return param num > pegasus support" % kw_name)
                for i in xrange(len(kw_result)):
                    tmp = str(kw_result[i]).replace('{', '\{').replace('}', '\}')
                    pegasus_script_item.getParameter(paramters[i]).setParameterValue(tmp)
            else:
                tmp = str(kw_result).replace('{', '\{').replace('}', '\}')
                pegasus_script_item.getParameter(paramters[0]).setParameterValue(tmp)
        pegasus_script_item.passed("K[%s]: Pass" % kw_name)
    logging.info("K[%s] Pass" % kw_name)


if __name__ == '__main__':
    logging.root = logging.getLogger("lrc")
    log_setting()
    #main(['facom_api_power_on_off','10.69.6.21','4001','1','power_off'])
    main(['sdata_restore_to_bts','192.168.128.1','21','D:\CI_Report\logs\\20140924100900'])
    #main(['log_path_creation', 'AAA'])



# MMT/ 
