from .eraser_mapper import EraserMapper

# And add the extension to Krita's list of extensions:
app = Krita.instance()
# Instantiate your class:
extension = EraserMapper(parent = app)
app.addExtension(extension)



class noti(krita.Notifier):

    def __init__(self, parent):
        super(noti, self).__init__(parent)

        self.viewClosed.connect(self.close)

    def close(self):
        extension.writeSettings()

noti(Application)