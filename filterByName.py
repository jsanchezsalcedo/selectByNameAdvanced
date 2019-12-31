from PySide2 import QtCore, QtWidgets
import maya.cmds as cmds
from maya import OpenMayaUI as omui
import shiboken2 as shiboken

mainWindow = None
__title__ = 'Select by Name (Advanced)'
__version__ = 'v1.0.0'

print ' '
print ' > You just openned {} {} successfully.'.format(__title__,__version__)
print ' '

def getMainWindow():
    ptr = omui.MQtUtil.mainWindow()
    mainWindow = shiboken.wrapInstance(long(ptr), QtWidgets.QMainWindow)
    return mainWindow

class filtered(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(filtered, self).__init__(parent)
        self.setWindowTitle('{}'.format(__title__))
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setFixedWidth(230)
        self.buildUI()

    def getTypes(self):
        Types = ['All',
                  'NURBS',
                  'Polygons',
                  'Lights',
                  'Cameras']

        return Types

    def buildUI(self):
        Types = self.getTypes()
        self.mainWidget = QtWidgets.QWidget()
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)

        TypesLyt = QtWidgets.QHBoxLayout()
        TypesLyt.setAlignment(QtCore.Qt.AlignTop)
        self.TypeCbb = QtWidgets.QComboBox()
        self.TypeCbb.addItems(Types)
        self.TypeCbb.setFixedWidth(200)
        TypesLyt.addWidget(self.TypeCbb)

        NameLyt = QtWidgets.QHBoxLayout()
        NameLyt.setAlignment(QtCore.Qt.AlignTop)
        NameLbl = QtWidgets.QLabel('Name')
        NameLbl.setFixedWidth(50)
        NameLyt.addWidget(NameLbl)
        self.NameLe = QtWidgets.QLineEdit('name')
        self.NameLe.setFixedWidth(145)
        NameLyt.addWidget(self.NameLe)

        ActionLyt = QtWidgets.QHBoxLayout()
        SelectBtn = QtWidgets.QPushButton('Select')
        ActionLyt.addWidget(SelectBtn)
        CancelBtn = QtWidgets.QPushButton('Cancel')
        ActionLyt.addWidget(CancelBtn)

        self.mainLayout.addLayout(TypesLyt)
        self.mainLayout.addLayout(NameLyt)
        self.mainLayout.addLayout(ActionLyt)

        self.setLayout(self.mainLayout)

        SelectBtn.clicked.connect(self.selectFiltered)
        CancelBtn.clicked.connect(self.cancel)

    def filterAllByName(self):
        NameValue = (str(self.NameLe.text())).lower()
        selected = cmds.listRelatives(cmds.ls(an=True), p=True)
        filtered = []
        for i in selected:
            if NameValue in i.lower():
                filtered.append(i)
        return filtered

    def filterNurbsByName(self):
        NameValue = (str(self.NameLe.text())).lower()
        selected = cmds.listRelatives(cmds.ls(typ='nurbsSurface'), p=True)
        filtered = []
        for i in selected:
            if NameValue in i.lower():
                filtered.append(i)
        return filtered

    def filterPolygonsByName(self):
        NameValue = (str(self.NameLe.text())).lower()
        selected = cmds.listRelatives(cmds.ls(typ='mesh'), p=True)
        filtered = []
        for i in selected:
            if NameValue in i.lower():
                filtered.append(i)
        return filtered

    def filterLightsByName(self):
        NameValue = (str(self.NameLe.text())).lower()
        selected = cmds.listRelatives(cmds.ls(lt=True), p=True)
        filtered = []
        for i in selected:
            if NameValue in i.lower():
                filtered.append(i)
        return filtered

    def filterCamerasByName(self):
        NameValue = (str(self.NameLe.text())).lower()
        selected = cmds.listRelatives(cmds.ls(ca=True), p=True)
        filtered = []
        for i in selected:
            if NameValue in i.lower():
                filtered.append(i)
        return filtered

    def selectFiltered(self):
        if str(self.TypeCbb.currentText()) == 'NURBS':
            filtered = self.filterNurbsByName()
            cmds.select(filtered)

        elif str(self.TypeCbb.currentText()) == 'Polygons':
            filtered = self.filterPolygonsByName()
            cmds.select(filtered)

        elif str(self.TypeCbb.currentText()) == 'Lights':
            filtered = self.filterLightsByName()
            cmds.select(filtered)

        elif str(self.TypeCbb.currentText()) == 'Cameras':
            filtered = self.filterCamerasByName()
            cmds.select(filtered)

        else:
            filtered = self.filterAllByName()
            cmds.select(filtered)

    def cancel(self):
        self.close()

def run():
    global mainWindow

    if not mainWindow or not cmds.window(mainWindow, q=True, e=True):
        mainWindow = filtered(parent=getMainWindow())

    mainWindow.show()
    mainWindow.raise_()