import sys
import os
import os.path
import errno
import platform
import logging
import logging.handlers

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap, QSurfaceFormat
import appdirs

from ui import Ui_MainWindow

# the display timer could be made faster when the processing
# power allows it, firing down to every 10 ms
FAST_TIMER_DUR = 10  # miliseconds

# the slow timer is used for text refresh
# Text has to be refreshed slowly in order to be readable.
# (and text painting is costly)
SLOW_TIMER_DUR = 1000  # miliseconds


class SoundAnnotator(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.logger = logging.getLogger(__name__)

        # set up UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # connect actions and buttons
        self.ui.play_button.clicked.connect(self.play)
        self.ui.save_button.clicked.connect(self.save)
        self.ui.next_button.clicked.connect(self.next_)
        self.ui.prev_button.clicked.connect(self.prev)
        self.ui.action_play.triggered.connect(self.play)
        self.ui.action_save.triggered.connect(self.save)
        self.ui.action_next.triggered.connect(self.next_)
        self.ui.action_prev.triggered.connect(self.prev)
        self.ui.action_open.triggered.connect(self.open)

        # init backend audio stuff

        # display as fast as possible
        self.display_timer = QtCore.QTimer()
        self.display_timer.setInterval(FAST_TIMER_DUR)

        # slow timer
        self.slow_timer = QtCore.QTimer()
        self.slow_timer.setInterval(SLOW_TIMER_DUR)

    def open(self):
        logger.info('open')

    def play(self):
        logger.info('play')

    def save(self):
        logger.info('save')

    def next_(self):
        logger.info('next')

    def prev(self):
        logger.info('prev')

    def quit(self):
        logger.info('quit')

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
    dirs = appdirs.AppDirs('SoundAnnotator', '')
    log_dir = dirs.user_data_dir
    try:
        os.makedirs(log_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    log_fp = os.path.join(log_dir, log_filename)

    # log to file
    file_handler = logging.handlers.RotatingFileHandler(log_fp, maxBytes=100000, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)
    rootLogger.addHandler(file_handler)

    if hasattr(sys, 'frozen'):
        # redirect stdout and stderr to the logger if this is a py2app or pyinstaller bundle
        sys.stdout = StreamToLogger(logging.getLogger('STDOUT'), logging.INFO)
        sys.stderr = StreamToLogger(logging.getLogger('STDERR'), logging.ERROR)
    else:
        # log to console if this is not a py2app or pyinstaller bundle
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        rootLogger.addHandler(console)

    # make Qt logs go to logger
    QtCore.qInstallMessageHandler(qt_message_handler)

    logger = logging.getLogger(__name__)

    logger.info('SoundAnnotator %s starting on %s (%s)', '0.0.0.0', platform.system(), sys.platform)

    # make sure Qt loads the desktop OpenGL stack, rather than OpenGL ES or a software OpenGL
    # only the former option is compatible with the use of PyOpenGL
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseDesktopOpenGL)

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

    app = QApplication(sys.argv)

    if platform.system() == 'Darwin':
        logger.info('Applying Mac OS-specific setup')
        # # help the py2app-packaged application find the Qt plugins (imageformats and platforms)
        # pluginsPath = os.path.normpath(os.path.join(QApplication.applicationDirPath(), os.path.pardir, 'PlugIns'))
        # logger.info('Adding the following to the Library paths: %s', pluginsPath)
        # QApplication.addLibraryPath(pluginsPath)

        # # on macOS, OpenGL 2.1 does not work well
        # # request a 3.2 Core context instead
        # format = QSurfaceFormat()
        # format.setDepthBufferSize(24)
        # format.setStencilBufferSize(8)
        # format.setVersion(3, 2)
        # format.setProfile(QSurfaceFormat.CoreProfile)
        # QSurfaceFormat.setDefaultFormat(format)

    # # Splash screen
    # pixmap = QPixmap(':/images/splash.png')
    # splash = QSplashScreen(pixmap)
    # splash.show()
    # splash.showMessage('Initializing the audio subsystem')
    # app.processEvents()

    window = SoundAnnotator()
    window.show()
    # splash.finish(window)

    return_code = app.exec_()

    # explicitly delete the main windows instead of waiting for the interpreter shutdown
    # tentative to prevent errors on exit on macos
    del window
    sys.exit(return_code)