from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import sys 

if __name__ == '__main__':
    try:
        logging.info('Try the logging&Exception')
        x = 1 / 0
    except Exception as e:
        raise NetworkSecurityException(e, sys)