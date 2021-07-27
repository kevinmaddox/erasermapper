# BBD's Krita Script Starter Feb 2018

from krita import (Krita, Extension)
from PyQt5.QtCore import (Qt, QSize)
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QGroupBox, QHBoxLayout,
                             QLabel, QListWidget, QListWidgetItem, QPushButton,
                             QVBoxLayout)
from PyQt5.QtGui import (QIcon, QPixmap)
from .dual_linked_list_widget import DualLinkedListWidget

EXTENSION_ID = 'pykrita_eraser_mapper'
MENU_ENTRY = 'Eraser Mapper'


class EraserMapper(Extension):

    def __init__(self, parent):
        # Always initialise the superclass.
        # This is necessary to create the underlying C++ object
        super().__init__(parent)

    def setup(self):
        self.eraserPreset = ''
        self.activePresets = []
        self.readSettings()
    
    def readSettings(self):
        self.eraserPreset = Application.readSetting(
            '', 'eraserMapperEraser', '')
        self.activePresets = Application.readSetting(
            '', 'eraserMapperActivePresets', '').split(',')
    
    def writeSettings(self):
        Application.writeSetting('', 'eraserMapperEraser', self.eraserPreset)
        Application.writeSetting(
            '', 'eraserMapperActivePresets', ','.join(self.activePresets))

    def createActions(self, window):
        action = window.createAction(EXTENSION_ID, MENU_ENTRY, "tools/scripts")
        # parameter 1 = the name that Krita uses to identify the action
        # parameter 2 = the text to be added to the menu entry for this script
        # parameter 3 = location of menu entry
        action.triggered.connect(self.action_triggered)

    def action_triggered(self):
        self.uiEraserMapper = UIEraserMapper(self)


class UIEraserMapper(QDialog):

    def __init__(self, eraserMapper):
        super(UIEraserMapper, self).__init__(Krita.instance().activeWindow()
            .qwindow())
        
        # Keep reference to parent.
        self.eraserMapper = eraserMapper
        
        # Create button & popup to select and show active eraser preset.
        self.eraserButton = QPushButton()
        self.eraserButton.setFixedSize(64, 64)
        self.eraserButton.setIconSize(QSize(64, 64))
        self.eraserButton.clicked.connect(self.openEraserDialog)
        
        self.eraserChooser = QListWidget()
        for name, preset in Application.resources("preset").items():
            item = QListWidgetItem()
            item.setText(name)
            item.setIcon(QIcon(QPixmap.fromImage(preset.image())))
            self.eraserChooser.addItem(item)
        self.eraserChooser.currentRowChanged.connect(self.selectEraser)
        self.eraserChooser.setCurrentRow(self.eraserChooser.row(
            self.eraserChooser.findItems(
            self.eraserMapper.eraserPreset, Qt.MatchExactly)[0]))
        
        eraserChooserGroupLayout = QVBoxLayout()
        eraserChooserGroupLayout.addWidget(self.eraserChooser)
        
        eraserChooserGroup = QGroupBox()
        eraserChooserGroup.setTitle('Select Eraser Preset')
        eraserChooserGroup.setLayout(eraserChooserGroupLayout)
        
        eraserChooserCloseButton = QPushButton('Close')
        eraserChooserCloseButton.clicked.connect(self.closeEraserDialog)
        
        eraserChooserLayout = QVBoxLayout()
        eraserChooserLayout.addWidget(eraserChooserGroup)
        eraserChooserLayout.addWidget(eraserChooserCloseButton)
        
        self.eraserChooserDialog = QDialog(self)
        self.eraserChooserDialog.setWindowFlags(Qt.Popup)
        self.eraserChooserDialog.setLayout(eraserChooserLayout)
        
        # Create and load list of active/inactive brush presets.
        self.presetLists = DualLinkedListWidget()
        self.presetLists.setTitleLeft("Will Toggle Transparency Effect")
        self.presetLists.setTitleRight("Will Toggle Brush Preset")
        self.presetLists.setSortingEnabled(True)
        inactivePresets = []
        activePresets = []
        for name, preset in Application.resources("preset").items():
            item = QListWidgetItem()
            item.setText(name)
            item.setIcon(QIcon(QPixmap.fromImage(preset.image())))
            if name in self.eraserMapper.activePresets:
                activePresets.append(item)
            else:
                inactivePresets.append(item)
        self.presetLists.appendToLeft(inactivePresets)
        self.presetLists.appendToRight(activePresets)
        
        # Add OK/Cancel buttons to the window.
        buttonBox = QDialogButtonBox(self)
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
        # Add everything to the final layout.
        layout = QVBoxLayout()
        layout.addWidget(QLabel(i18n("Eraser Preset")))
        layout.addWidget(self.eraserButton)
        layout.addLayout(self.presetLists)
        layout.addWidget(buttonBox)
        
        # Display window.
        self.setLayout(layout)
        self.setWindowTitle("Eraser Mapper - Krita")
        self.exec_()
    
    def accept(self):
        # Store new settings.
        self.eraserMapper.eraserPreset = self.eraserChooser.currentItem().text()
        
        self.eraserMapper.activePresets.clear()
        right = self.presetLists.getWidgetRight()
        for i in range(right.count()):
            self.eraserMapper.activePresets.append(right.item(i).text())
        
        # Save settings to kritarc.
        self.eraserMapper.writeSettings()
        
        # Close dialog window.
        super(UIEraserMapper, self).accept()
    
    def closeEvent(self, event):
        # Close dialog window.
        event.accept()
    
    def openEraserDialog(self):
        # Open dialog window.
        self.eraserChooserDialog.exec_()
    
    def closeEraserDialog(self):
        # Close eraser pop-up window.
        self.eraserChooserDialog.accept()
    
    def selectEraser(self, currentRow):
        # Get selected eraser and set the button icon to it.
        item = self.eraserChooser.item(currentRow)
        self.eraserButton.setIcon(item.icon())
