__author__ = 'liziqiang'
import logging

#logging.warning('Watch out!')


logging.basicConfig(filename='example.log', filemode='w', level=logging.INFO)
logger = logging.getLogger(__name__)
effect_lvl = logger.getEffectiveLevel()
print logging.getLevelName(effect_lvl)

#disable logging
logging.disable(logging.CRITICAL)
logging.critical('This message should not go to the log file')
logging.info('So neither this')

#restore logging
logging.disable(logging.NOTSET)
logging.debug('This message should not go to the log file...')
logging.info('This message should go to the log file')
logging.warning('And this, too')
