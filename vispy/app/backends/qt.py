from vispy.event import MouseEvent
from vispy import app


import vispy
qt_lib = vispy.config['qt_lib']
if qt_lib == 'any':
    try: 
        from PyQt4 import QtGui, QtCore, QtOpenGL
    except ImportError:
        from PySide import QtGui, QtCore, QtOpenGL
elif qt_lib == 'pyqt':
    from PyQt4 import QtGui, QtCore
elif qt_lib == 'pyside':
    from PySide import QtGui, QtCore
else:
    raise Exception("Do not recognize Qt library '%s'. Options are 'pyqt', 'pyside', or 'any' (see vispy.config['qt_lib'])." % str(qt_lib))




class ApplicationBackend(app.ApplicationBackend):
    
    def __init__(self):
        app.ApplicationBackend.__init__(self)
    
    def _vispy_get_backend_name(self):
        return 'Qt' #todo: pyside or PyQt?
    
    def _vispy_process_events(self):
        app = self._vispy_get_native_app()
        app.flush()
        app.processEvents()
    
    def _vispy_run(self):
        app = self._vispy_get_native_app()
        if hasattr(app, '_in_event_loop') and app._in_event_loop:
            pass # Already in event loop
        else:
            return app.exec_()
    
    def _vispy_quit(self):
        return self._vispy_get_native_app().quit()
    
    def _vispy_get_native_app(self):
        # Get native app in save way. Taken from guisupport.py
        app = QtGui.QApplication.instance()
        if app is None:
            app = QtGui.QApplication([''])
        # Store so it won't be deleted, but not on a visvis object,
        # or an application may produce error when closed
        QtGui._qApp = app
        # Return
        return app



class CanvasBackend(QtOpenGL.QGLWidget, app.CanvasBackend):
    """Qt backend for Canvas abstract class."""
    
    def __init__(self, vispy_canvas, *args, **kwargs):
        QtOpenGL.QGLWidget.__init__(self, *args, **kwargs)
        app.CanvasBackend.__init__(self, vispy_canvas)
    
    
    def _vispy_set_current(self):  
        # Make this the current context
        self.makeCurrent()
    
    def _vispy_swap_buffers(self):  
        # Swap front and back buffer
        self.swapBuffers()
    
    def _vispy_set_title(self, title):  
        # Set the window title. Has no effect for widgets
        self.setWindowTitle(title)
    
    def _vispy_set_size(self, w, h):
        # Set size of the widget or window
        self.resize(w, h)
    
    def _vispy_set_location(self, x, y):
        # Set location of the widget or window. May have no effect for widgets
        self.move(x, y)
    
    def _vispy_set_visible(self, visible):
        # Show or hide the window or widget
        if visible:
            self.show()
        else:
            self.hide()
    
    def _vispy_update(self):
        # Invoke a redraw
        self.update()
    
    def _vispy_close(self):
        # Force the window or widget to shut down
        self.close()
    
    def _vispy_get_geometry(self):
        # Should return widget (x, y, w, h)
        g = self.geometry()
        return (g.x(), g.y(), g.width(), g.height())
    
    
    
    def initializeGL(self):
        if self._vispy_canvas is None:
            return
        self._vispy_canvas.events.initialize()
        
    def resizeGL(self, w, h):
        if self._vispy_canvas is None:
            return
        self._vispy_canvas.events.resize(size=(w,h))

    def paintGL(self):
        if self._vispy_canvas is None:
            return
        self._vispy_canvas.events.paint(
            region=(0, 0, self.width(), self.height()))
        
    def mousePressEvent(self, ev):
        if self._vispy_canvas is None:
            return
        self._vispy_canvas.events.mouse_press(
            action='press', 
            qt_event=ev,
            pos=(ev.pos().x(), ev.pos().y()),
            button=int(ev.button()),
            )
            
    def mouseReleaseEvent(self, ev):
        if self._vispy_canvas is None:
            return
        self._vispy_canvas.events.mouse_release(
            action='release', 
            qt_event=ev,
            pos=(ev.pos().x(), ev.pos().y()),
            button=int(ev.button()),
            )

    def mouseMoveEvent(self, ev):
        if self._vispy_canvas is None:
            return
        self._vispy_canvas.events.mouse_move(
            action='move', 
            qt_event=ev,
            pos=(ev.pos().x(), ev.pos().y()),
            )
        
    def wheelEvent(self, ev):
        if self._vispy_canvas is None:
            return
        self._vispy_canvas.events.mouse_wheel(
            action='wheel', 
            qt_event=ev,
            delta=ev.delta(),
            pos=(ev.pos().x(), ev.pos().y()),
            )
    
    
    def keyPressEvent(self, event):      
        key = self._processKey(event)
        text = str(event.text())
        #self.figure._GenerateKeyEvent('keydown', key, text, modifiers(event))
        # todo: modifiers
        self._vispy_canvas.events.key_press(action='press', key=key, text=text)
    
    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return # Skip release auto repeat events
        key = self._processKey(event)
        text = str(event.text())
        self._vispy_canvas.events.key_release(action='release', key=key, text=text)
    
    def _processKey(self,event):
        """ evaluates the keycode of qt, and transform to visvis key.
        """
        key = event.key()
        # special cases for shift control and alt -> map to 17 18 19
        if key in KEYMAP:
            return KEYMAP[key]
        else:
            return key 


class QtMouseEvent(MouseEvent):
    ## special subclass of MouseEvent for propagating acceptance info back to Qt.
    @MouseEvent.handled.setter
    def handled(self, val):
        self._handled = val
        if val:
            self.qt_event.accept()
        else:
            self.qt_event.ignore()


# todo: define constants for vispy
KEYMAP = {}
#             {  QtCore.Qt.Key_Shift: constants.KEY_SHIFT, 
#             QtCore.Qt.Key_Alt: constants.KEY_ALT,
#             QtCore.Qt.Key_Control: constants.KEY_CONTROL,
#             QtCore.Qt.Key_Left: constants.KEY_LEFT,
#             QtCore.Qt.Key_Up: constants.KEY_UP,
#             QtCore.Qt.Key_Right: constants.KEY_RIGHT,
#             QtCore.Qt.Key_Down: constants.KEY_DOWN,
#             QtCore.Qt.Key_PageUp: constants.KEY_PAGEUP,
#             QtCore.Qt.Key_PageDown: constants.KEY_PAGEDOWN,
#             QtCore.Qt.Key_Enter: constants.KEY_ENTER,
#             QtCore.Qt.Key_Return: constants.KEY_ENTER,
#             QtCore.Qt.Key_Escape: constants.KEY_ESCAPE,
#             QtCore.Qt.Key_Delete: constants.KEY_DELETE
#             }


class TimerBackend(app.TimerBackend, QtCore.QTimer):
    def __init__(self, vispy_timer):
        if QtGui.QApplication.instance() is None:
            global QAPP
            QAPP = QtGui.QApplication([])
        app.TimerBackend.__init__(self, vispy_timer)
        QtCore.QTimer.__init__(self)
        self.timeout.connect(self._vispy_timeout)
        
    def _vispy_start(self, interval):
        self.start(interval*1000.)
        
    def _vispy_stop(self):
        self.stop()
        
    def _vispy_timeout(self):
        self._vispy_timer._timeout()
    

