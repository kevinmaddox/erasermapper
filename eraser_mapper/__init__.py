from .eraser_mapper import EraserMapper

# And add the extension to Krita's list of extensions:
app = Krita.instance()
# Instantiate your class:
extension = EraserMapper(parent = app)
app.addExtension(extension)
