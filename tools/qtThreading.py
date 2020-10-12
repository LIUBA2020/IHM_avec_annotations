from PyQt5.QtCore import *

import traceback
import sys

"""

    This class allow to set up every necessary signal calling during or after the end of a running thread.
    finished : do something when a thread ends.
    error : do something when a thread raise an error.
    result : do something with a returned object.
    progress : do something with a callback.

        """


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
    update = pyqtSignal()


"""

    This class allow to launch a thread and set up the signal contained in WorkerSignals.

        """


class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        if kwargs.get('progress_callback') is True:
            self.kwargs['progress_callback'] = self.signals.progress
        if kwargs.get('update_callback') is True:
            self.kwargs['update_callback'] = self.signals.update

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            exc_type, value = sys.exc_info()[:2]
            self.signals.error.emit((exc_type, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
