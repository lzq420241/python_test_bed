import sys
import os

try:
    import xmlrpc.client as xmlrpclib
except ImportError:
    import xmlrpclib

class Pegasus:
    def __init__(self,serverURL,scriptId):
        self.server = xmlrpclib.ServerProxy(serverURL, verbose=False)
        self.scriptId = scriptId

class PegasusLogger:
    def formatLog(self,message,error):
        if error is None :
            return message
        else:
            return "%s\n%s" % (message, error)

    def __init__(self,logCategory):
        self.logCategory = logCategory
    def fatal(self,message,error=None):
        pegasus.server.pegasus.scripting.handler.IPegasusLogger.fatal(self.logCategory, self.formatLog(message,error))
    def error(self,message,error=None):
        pegasus.server.pegasus.scripting.handler.IPegasusLogger.error(self.logCategory, self.formatLog(message,error))
    def warn(self,message,error=None):
        pegasus.server.pegasus.scripting.handler.IPegasusLogger.warn(self.logCategory, self.formatLog(message,error))
    def log(self,message,error=None):
        pegasus.server.pegasus.scripting.handler.IPegasusLogger.log(self.logCategory, self.formatLog(message,error))
    def info(self,message,error=None):
        pegasus.server.pegasus.scripting.handler.IPegasusLogger.info(self.logCategory, self.formatLog(message,error))
    def debug(self,message,error=None):
        pegasus.server.pegasus.scripting.handler.IPegasusLogger.debug(self.logCategory, self.formatLog(message,error))

class PegasusLoggerFactory:
    def getLogger(self,logCategory):
        return PegasusLogger(logCategory)
        
class PegasusScriptItem:
    def passed(self,message):
        pegasus.server.pegasus.scripting.handler.IPegasusScriptItem.passed(pegasus.scriptId,message)
    def failed(self,message):
        pegasus.server.pegasus.scripting.handler.IPegasusScriptItem.failed(pegasus.scriptId,message)
    def inconclusive(self,message):
        pegasus.server.pegasus.scripting.handler.IPegasusScriptItem.inconclusive(pegasus.scriptId,message)
    def insignificant(self,message):
        pegasus.server.pegasus.scripting.handler.IPegasusScriptItem.insignificant(pegasus.scriptId,message)
    def skipped(self,message):
        pegasus.server.pegasus.scripting.handler.IPegasusScriptItem.skipped(pegasus.scriptId,message)
    def warn(self,message):
        pegasus.server.pegasus.scripting.handler.IPegasusScriptItem.warn(pegasus.scriptId,message)
    def stopTp(self):
        pegasus.server.pegasus.scripting.handler.IPegasusScriptItem.stopTp(pegasus.scriptId)
    def stopTs(self):
        pegasus.server.pegasus.scripting.handler.IPegasusScriptItem.stopTs(pegasus.scriptId)
    def stopTest(self):
        return pegasus.server.pegasus.scripting.handler.IPegasusScriptItem.stopTest(pegasus.scriptId)
    def getParameter(self,name):
        param = pegasus.server.pegasus.scripting.handler.IPegasusScriptItem.getParameter(pegasus.scriptId,name)
        if param is None:
            pegasus.logger.error("Unknown parameter '%s'" % name)
            return None
        else:
            return PegasusParameter(name)
    def getResult(self):
        return PegasusResult(pegasus.server.pegasus.scripting.handler.IPegasusScriptItem.getResult(pegasus.scriptId))

class PegasusResult:
    def __init__(self,result):
        self.result = result
    def getVerdict():
        return self.result['verdict']

class PegasusParameter:
    def __init__(self,name):
        self.name = name
    def getParameterValue(self):
        param=pegasus.server.pegasus.scripting.handler.IPegasusScriptItem.getParameter(pegasus.scriptId,self.name)
        if param['type'] in ['Integer', '   IntegerRange']:
            return int(param['value'])
        if param['type'] in ['Float', 'FloatRange', 'Double', 'DoubleRange']:
            return float(param['value'])
        if param['type'] in ['Long', 'LongRange']:
            return long(param['value'])
        if param['type'] == 'Boolean':
            return param['value'] != 0 and param['value']!='false'
        if param['type'] == 'String':
            return param['value']
        else:
            pegasus.logger.error("Unknown type '%s'" % param['type'])
            return param['value']
    def getStringValue(self):
        return pegasus.server.pegasus.scripting.handler.IPegasusScriptItem.getParameter(pegasus.scriptId,self.name)['value']
    def getUnresolvedValue(self):
        return pegasus.server.pegasus.scripting.handler.IPegasusScriptItem.getParameter(pegasus.scriptId,self.name)['unresoledValue']
    def isResolveable(self):
        return pegasus.server.pegasus.scripting.handler.IPegasusScriptItem.getParameter(pegasus.scriptId,self.name)['isResolveable'] == 'true'
    def setParameterValue(self,value):
        return pegasus.server.pegasus.scripting.handler.IPegasusScriptItem.setParameterValue(pegasus.scriptId,self.name,str(value))

xmlrpcUrl = os.getenv("PEGASUS_XMLRPC", "http://localhost:62288/")
id = os.getenv("PEGASUS_ID", 0)
scrPath = os.getenv("PEGASUS_SCRIPT_PATH", "")
pegasus = Pegasus(xmlrpcUrl,id)
javax_script_filename = scrPath
loggerFactory = PegasusLoggerFactory()
pegasus_script_item = PegasusScriptItem()
pegasus.logger = loggerFactory.getLogger("Script")

# add script's dir to path, so local modules can be used
sys.path.append(os.path.abspath(os.path.dirname(javax_script_filename)))


if sys.version_info<(3,0,0):
    # in python<2.7 compile doesn't handle newlines correctly
    # see http://docs.python.org/library/functions.html#compile
    execfile(javax_script_filename, globals(), locals())
else:
    # in python>=3 execfile is missing
    exec(compile(open(javax_script_filename).read(), javax_script_filename, "exec"), globals(), locals())


