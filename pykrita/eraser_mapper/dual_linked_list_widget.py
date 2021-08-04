from PyQt5.QtWidgets import (QGroupBox, QHBoxLayout, QListWidget, QPushButton,
                             QSizePolicy, QSpacerItem, QVBoxLayout)

# This object consists of two list widgets as well as a group of buttons which
# allow you to move items back and forth between the two lists.

class DualLinkedListWidget(QHBoxLayout):

    def __init__(self):
        super(QHBoxLayout, self).__init__()
        
        # Create main widgets.
        self.left = QListWidget()
        self.right = QListWidget()
        
        itemLeftButton = QPushButton('<')
        itemRightButton = QPushButton('>')
        allLeftButton = QPushButton('<<')
        allRightButton = QPushButton('>>')
        
        itemLeftButton.clicked.connect(self._itemLeftButtonClicked)
        itemRightButton.clicked.connect(self._itemRightButtonClicked)
        allLeftButton.clicked.connect(self._allLeftButtonClicked)
        allRightButton.clicked.connect(self._allRightButtonClicked)
        
        # Create groups to hold list widgets (for presentation).
        leftGroupLayout = QVBoxLayout()
        leftGroupLayout.addWidget(self.left)
        self.leftGroup = QGroupBox()
        self.leftGroup.setLayout(leftGroupLayout)
        
        rightGroupLayout = QVBoxLayout()
        rightGroupLayout.addWidget(self.right)
        self.rightGroup = QGroupBox()
        self.rightGroup.setLayout(rightGroupLayout)
        
        # Create layout for middle buttons.
        buttonLayout = QVBoxLayout()
        buttonLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Minimum,
            QSizePolicy.Expanding))
        buttonLayout.addWidget(allRightButton)
        buttonLayout.addWidget(itemRightButton)
        buttonLayout.addWidget(itemLeftButton)
        buttonLayout.addWidget(allLeftButton)
        buttonLayout.addItem(QSpacerItem(10, 20, QSizePolicy.Minimum,
            QSizePolicy.Expanding))
        
        # Add everything to final layout.
        self.addWidget(self.leftGroup)
        self.addLayout(buttonLayout)
        self.addWidget(self.rightGroup)
    
    def _allLeftButtonClicked(self):
        while (self.right.count() > 0):
            self.left.addItem(self.right.takeItem(0))
    
    def _allRightButtonClicked(self):
        while (self.left.count() > 0):
            self.right.addItem(self.left.takeItem(0))
    
    def _itemLeftButtonClicked(self):
        self.left.addItem(self.right.takeItem(self.right.currentRow()))
    
    def _itemRightButtonClicked(self):
        self.right.addItem(self.left.takeItem(self.left.currentRow()))
    
    def appendToLeft(self, items):
        for item in items:
            self.left.addItem(item)
    
    def appendToRight(self, items):
        for item in items:
            self.right.addItem(item)
    
    def clearLeft(self):
        self.left.clear()
    
    def clearRight(self):
        self.right.clear()
    
    def getWidgetLeft(self):
        return self.left
    
    def getWidgetRight(self):
        return self.right
    
    def setSortingEnabled(self, sortingEnabled):
        self.left.setSortingEnabled(sortingEnabled)
        self.right.setSortingEnabled(sortingEnabled)
    
    def setTitleLeft(self, title):
        self.leftGroup.setTitle(title)
    
    def setTitleRight(self, title):
        self.rightGroup.setTitle(title)
