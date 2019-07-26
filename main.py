import sys
import os
from os import path
import errno
import platform
import logging
import logging.handlers

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
import appdirs

from annotator import Annotator



def qt_message_handler(mode, context, message):
    logger = logging.getLogger(__name__)
    if mode == QtCore.QtInfoMsg:
        logger.info(message)
    elif mode == QtCore.QtWarningMsg:
        logger.warning(message)
    elif mode == QtCore.QtCriticalMsg:
        logger.error(message)
    elif mode == QtCore.QtFatalMsg:
        logger.critical(message)
    else:
        logger.debug(message)


if __name__ == '__main__':
    # make the Python warnings go to logger
    logging.captureWarnings(True)
    log_format = '%(asctime)s %(levelname)s %(name)s: %(message)s'
    formatter = logging.Formatter(log_format)
    log_filename = 'log.txt'
    dirs = appdirs.AppDirs('Annotator', '')
    log_dir = dirs.user_data_dir
    try:
        os.makedirs(log_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    log_fp = path.join(log_dir, log_filename)

    # log to file
    file_handler = logging.handlers.RotatingFileHandler(log_fp, maxBytes=100000, backupCount=5)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)
    rootLogger.addHandler(file_handler)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    rootLogger.addHandler(console)

    # make Qt logs go to logger
    QtCore.qInstallMessageHandler(qt_message_handler)
    logger = logging.getLogger(__name__)
    logger.info('Annotator %s starting on %s (%s)', '0.0.0.0', platform.system(), sys.platform)

    if platform.system() == 'Windows':
        logger.info('Applying Windows-specific setup')

        # enable automatic scaling for high-DPI screens
        os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

        # set the App ID for Windows 7 to properly display the icon in the
        # taskbar.
        import ctypes
        myappid = '??????'  # arbitrary string
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            logger.error('Could not set the app model ID. If the plaftorm is older than Windows 7, this is normal.')

    elif platform.system() == 'Darwin':
        pass
        # logger.info('Applying Mac OS-specific setup')

    app = QApplication(sys.argv)
    window = Annotator()
    window.show()
    return_code = app.exec_()
    del window  # prevent mac errors
    sys.exit(return_code)
