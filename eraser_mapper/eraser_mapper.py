# BBD's Krita Script Starter Feb 2018

from krita import (Extension, Krita)
from PyQt5.QtCore import (qDebug, QSize, Qt)
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
        self.activePresetNames = []
        self.eraserPreset = None
        self.lastBrushPreset = None
        
        self.activePresetNames = Application.readSetting(
            '', 'eraserMapperActivePresetNames', '').split(',')
        eraserPresetName = Application.readSetting(
            '', 'eraserMapperEraserPreset', '')
        lastBrushPresetName = Application.readSetting(
            '', 'eraserMappeLastBrushPreset', '')
        
        self.assignEraserPreset(eraserPresetName)
        self.assignLastBrushPreset(lastBrushPresetName)
    
    def writeSettings(self):
        Application.writeSetting(
            '', 'eraserMapperActivePresetNames', ','.join(self.activePresetNames))
        Application.writeSetting(
            '', 'eraserMapperEraserPreset', self.eraserPreset.name())
        Application.writeSetting(
            '', 'eraserMapperLastBrushPreset', self.lastBrushPreset.name())

    def createActions(self, window):
        # parameter 1 = the name that Krita uses to identify the action
        # parameter 2 = the text to be added to the menu entry for this script
        # parameter 3 = location of menu entry
        
        action = window.createAction(EXTENSION_ID, MENU_ENTRY, "tools/scripts")
        action.triggered.connect(self.action_triggered)
        
        eraserAction = window.createAction(
            'pykrita_eraser_mapper_toggle_eraser', 'Eraser', '')
        eraserAction.triggered.connect(self.handleEraser)
        
        lastBrushAction = window.createAction(
            'pykrita_eraser_mapper_freehand_brush_tool', 'Freehand Brush Tool', '')
        lastBrushAction.triggered.connect(self.handleLastBrush)
        
        #TODO: On preset change in any way, do handleLastBrush
    
    def handleEraser(self):
        window = Application.activeWindow()
        # Switch to brush tool if necessary.
        Application.action("KritaShape/KisToolBrush").trigger()
        # Get currently active preset.
        preset = window.views()[0].currentBrushPreset()
        # Bail out if we're already erasing.
        if preset.name() == self.eraserPreset.name():
            return
        # Check if preset should toggle transparency or brush.
        if preset.name() in self.activePresetNames:
            window.views()[0].activateResource(self.eraserPreset)
            self.lastBrushPreset = preset
        else:
            kritaEraserAction = Application.action("erase_action")
            if not kritaEraserAction.isChecked():
                kritaEraserAction.trigger()
    
    def handleLastBrush(self):
        window = Application.activeWindow()
        # Switch to brush tool if necessary.
        Application.action("KritaShape/KisToolBrush").trigger()
        # Switch to last preset if we're currently using the eraser brush.
        preset = window.views()[0].currentBrushPreset()
        if preset.name() == self.eraserPreset.name():
            window.views()[0].activateResource(self.lastBrushPreset)
        # Disable eraser mask mode if it's active.
        kritaEraserAction = Application.action("erase_action")
        if kritaEraserAction.isChecked():
            kritaEraserAction.trigger()
    
    def assignEraserPreset(self, presetName):
        presets = Application.resources("preset")
        
        # Attempt to find preset by name.
        for name, preset in presets.items():
            if name == presetName:
                self.eraserPreset = preset
                return
        
        # Otherwise, default to first preset.
        self.eraserPreset = list(presets.values())[0]
    
    def assignLastBrushPreset(self, presetName):
        presets = Application.resources("preset")
        
        # Attempt to find preset by name.
        for name, preset in presets.items():
            if name == presetName:
                self.lastBrushPreset = preset
                return
        
        # Otherwise, default to first preset.
        self.lastBrushPreset = list(presets.values())[0]

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
            self.eraserMapper.eraserPreset.name(), Qt.MatchExactly)[0]))
        
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
        inactivePresetList = []
        activePresetList = []
        for name, preset in Application.resources("preset").items():
            item = QListWidgetItem()
            item.setText(name)
            item.setIcon(QIcon(QPixmap.fromImage(preset.image())))
            if name in self.eraserMapper.activePresetNames:
                activePresetList.append(item)
            else:
                inactivePresetList.append(item)
        self.presetLists.appendToLeft(inactivePresetList)
        self.presetLists.appendToRight(activePresetList)
        
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
        self.eraserMapper.assignEraserPreset(self.eraserChooser.currentItem().text())
        
        self.eraserMapper.activePresetNames.clear()
        right = self.presetLists.getWidgetRight()
        for i in range(right.count()):
            self.eraserMapper.activePresetNames.append(right.item(i).text())
        
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
