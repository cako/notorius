# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/window.ui'
#
# Created: Sat Mar 24 12:24:59 2012
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1018, 909)
        MainWindow.setAcceptDrops(True)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setAcceptDrops(True)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.controlsWidget = QtGui.QWidget(self.centralwidget)
        self.controlsWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.controlsWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.controlsWidget.setMouseTracking(True)
        self.controlsWidget.setObjectName("controlsWidget")
        self.gridLayout = QtGui.QGridLayout(self.controlsWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.previousPageButton = QtGui.QPushButton(self.controlsWidget)
        self.previousPageButton.setEnabled(False)
        self.previousPageButton.setMinimumSize(QtCore.QSize(35, 28))
        self.previousPageButton.setMaximumSize(QtCore.QSize(35, 28))
        self.previousPageButton.setMouseTracking(True)
        self.previousPageButton.setText("")
        self.previousPageButton.setIconSize(QtCore.QSize(22, 22))
        self.previousPageButton.setFlat(True)
        self.previousPageButton.setObjectName("previousPageButton")
        self.gridLayout.addWidget(self.previousPageButton, 1, 0, 1, 1)
        self.pageSpinBox = QtGui.QSpinBox(self.controlsWidget)
        self.pageSpinBox.setEnabled(False)
        self.pageSpinBox.setMinimumSize(QtCore.QSize(50, 0))
        self.pageSpinBox.setFrame(True)
        self.pageSpinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.pageSpinBox.setAccelerated(False)
        self.pageSpinBox.setMinimum(1)
        self.pageSpinBox.setProperty("value", 1)
        self.pageSpinBox.setObjectName("pageSpinBox")
        self.gridLayout.addWidget(self.pageSpinBox, 1, 1, 1, 1)
        self.nextPageButton = QtGui.QPushButton(self.controlsWidget)
        self.nextPageButton.setEnabled(False)
        self.nextPageButton.setMinimumSize(QtCore.QSize(35, 28))
        self.nextPageButton.setMaximumSize(QtCore.QSize(35, 28))
        self.nextPageButton.setMouseTracking(True)
        self.nextPageButton.setText("")
        self.nextPageButton.setIconSize(QtCore.QSize(22, 22))
        self.nextPageButton.setFlat(True)
        self.nextPageButton.setObjectName("nextPageButton")
        self.gridLayout.addWidget(self.nextPageButton, 1, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(55, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 5, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(54, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 6, 1, 1)
        self.scaleComboBox = QtGui.QComboBox(self.controlsWidget)
        self.scaleComboBox.setEnabled(False)
        self.scaleComboBox.setMinimumSize(QtCore.QSize(102, 0))
        self.scaleComboBox.setMaximumSize(QtCore.QSize(78, 16777215))
        self.scaleComboBox.setObjectName("scaleComboBox")
        self.scaleComboBox.addItem("")
        self.scaleComboBox.addItem("")
        self.scaleComboBox.addItem("")
        self.gridLayout.addWidget(self.scaleComboBox, 1, 7, 1, 1)
        self.scaleSpinBox = QtGui.QDoubleSpinBox(self.controlsWidget)
        self.scaleSpinBox.setEnabled(False)
        self.scaleSpinBox.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.scaleSpinBox.setMinimum(0.0)
        self.scaleSpinBox.setMaximum(100.0)
        self.scaleSpinBox.setSingleStep(0.25)
        self.scaleSpinBox.setProperty("value", 1.0)
        self.scaleSpinBox.setObjectName("scaleSpinBox")
        self.gridLayout.addWidget(self.scaleSpinBox, 1, 8, 1, 1)
        self.offsetCheckBox = QtGui.QCheckBox(self.controlsWidget)
        self.offsetCheckBox.setEnabled(False)
        self.offsetCheckBox.setObjectName("offsetCheckBox")
        self.gridLayout.addWidget(self.offsetCheckBox, 1, 4, 1, 1)
        self.maxPageLabel = QtGui.QLabel(self.controlsWidget)
        self.maxPageLabel.setObjectName("maxPageLabel")
        self.gridLayout.addWidget(self.maxPageLabel, 1, 2, 1, 1)
        self.gridLayout_3.addWidget(self.controlsWidget, 0, 0, 1, 1)
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setMouseTracking(False)
        self.scrollArea.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.scrollArea.setAcceptDrops(True)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 913, 547))
        self.scrollAreaWidgetContents.setAcceptDrops(True)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.scrollArea, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1018, 26))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menuWindows = QtGui.QMenu(self.menubar)
        self.menuWindows.setObjectName("menuWindows")
        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menuPreferences = QtGui.QMenu(self.menubar)
        self.menuPreferences.setObjectName("menuPreferences")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.annotationSourceDockWidget = QtGui.QDockWidget(MainWindow)
        self.annotationSourceDockWidget.setFloating(False)
        self.annotationSourceDockWidget.setObjectName("annotationSourceDockWidget")
        self.dockWidgetContents_5 = QtGui.QWidget()
        self.dockWidgetContents_5.setObjectName("dockWidgetContents_5")
        self.gridLayout_2 = QtGui.QGridLayout(self.dockWidgetContents_5)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.annotationSourceTextEdit = QtGui.QTextEdit(self.dockWidgetContents_5)
        self.annotationSourceTextEdit.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.annotationSourceTextEdit.setObjectName("annotationSourceTextEdit")
        self.gridLayout_2.addWidget(self.annotationSourceTextEdit, 1, 0, 1, 1)
        self.compileButton = QtGui.QPushButton(self.dockWidgetContents_5)
        self.compileButton.setMinimumSize(QtCore.QSize(0, 97))
        self.compileButton.setMaximumSize(QtCore.QSize(20, 16777215))
        self.compileButton.setObjectName("compileButton")
        self.gridLayout_2.addWidget(self.compileButton, 1, 1, 1, 1)
        self.annotationSourceDockWidget.setWidget(self.dockWidgetContents_5)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.annotationSourceDockWidget)
        self.annotationDockWidget = QtGui.QDockWidget(MainWindow)
        self.annotationDockWidget.setMinimumSize(QtCore.QSize(200, 53))
        self.annotationDockWidget.setFloating(False)
        self.annotationDockWidget.setObjectName("annotationDockWidget")
        self.dockWidgetContents_6 = QtGui.QWidget()
        self.dockWidgetContents_6.setObjectName("dockWidgetContents_6")
        self.gridLayoutAnnotationDock = QtGui.QGridLayout(self.dockWidgetContents_6)
        self.gridLayoutAnnotationDock.setObjectName("gridLayoutAnnotationDock")
        self.annotationWidget = QtGui.QWidget(self.dockWidgetContents_6)
        self.annotationWidget.setObjectName("annotationWidget")
        self.gridLayoutAnnotationDock.addWidget(self.annotationWidget, 0, 0, 1, 1)
        self.annotationDockWidget.setWidget(self.dockWidgetContents_6)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.annotationDockWidget)
        self.searchDockWidget = QtGui.QDockWidget(MainWindow)
        self.searchDockWidget.setObjectName("searchDockWidget")
        self.searchDockWidgetContents = QtGui.QWidget()
        self.searchDockWidgetContents.setObjectName("searchDockWidgetContents")
        self.gridLayout_4 = QtGui.QGridLayout(self.searchDockWidgetContents)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.searchWidget = QtGui.QWidget(self.searchDockWidgetContents)
        self.searchWidget.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.searchWidget.setObjectName("searchWidget")
        self.gridLayout_4.addWidget(self.searchWidget, 0, 0, 1, 1)
        self.searchDockWidget.setWidget(self.searchDockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.searchDockWidget)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setIconVisibleInMenu(True)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExport = QtGui.QAction(MainWindow)
        self.actionExport.setEnabled(False)
        self.actionExport.setIconVisibleInMenu(True)
        self.actionExport.setObjectName("actionExport")
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setIconVisibleInMenu(True)
        self.actionQuit.setObjectName("actionQuit")
        self.actionControls = QtGui.QAction(MainWindow)
        self.actionControls.setCheckable(True)
        self.actionControls.setChecked(True)
        self.actionControls.setObjectName("actionControls")
        self.actionAnnotationSource = QtGui.QAction(MainWindow)
        self.actionAnnotationSource.setCheckable(True)
        self.actionAnnotationSource.setChecked(True)
        self.actionAnnotationSource.setObjectName("actionAnnotationSource")
        self.actionAnnotation = QtGui.QAction(MainWindow)
        self.actionAnnotation.setCheckable(True)
        self.actionAnnotation.setChecked(True)
        self.actionAnnotation.setObjectName("actionAnnotation")
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setIconVisibleInMenu(True)
        self.actionAbout.setObjectName("actionAbout")
        self.actionPreambleEditor = QtGui.QAction(MainWindow)
        self.actionPreambleEditor.setIconVisibleInMenu(True)
        self.actionPreambleEditor.setObjectName("actionPreambleEditor")
        self.menu_File.addAction(self.actionOpen)
        self.menu_File.addAction(self.actionExport)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionQuit)
        self.menuWindows.addAction(self.actionControls)
        self.menuWindows.addAction(self.actionAnnotationSource)
        self.menuWindows.addAction(self.actionAnnotation)
        self.menu_Help.addAction(self.actionAbout)
        self.menuPreferences.addAction(self.actionPreambleEditor)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuWindows.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Notorius", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleComboBox.setItemText(0, QtGui.QApplication.translate("MainWindow", "Use scale", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleComboBox.setItemText(1, QtGui.QApplication.translate("MainWindow", "Fit to width", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleComboBox.setItemText(2, QtGui.QApplication.translate("MainWindow", "Fit to height", None, QtGui.QApplication.UnicodeUTF8))
        self.offsetCheckBox.setText(QtGui.QApplication.translate("MainWindow", "Offset", None, QtGui.QApplication.UnicodeUTF8))
        self.maxPageLabel.setText(QtGui.QApplication.translate("MainWindow", "of 1", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuWindows.setTitle(QtGui.QApplication.translate("MainWindow", "&Windows", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Help.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPreferences.setTitle(QtGui.QApplication.translate("MainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.annotationSourceDockWidget.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Welcome Note", None, QtGui.QApplication.UnicodeUTF8))
        self.compileButton.setText(QtGui.QApplication.translate("MainWindow", ">", None, QtGui.QApplication.UnicodeUTF8))
        self.annotationDockWidget.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Welcome Note", None, QtGui.QApplication.UnicodeUTF8))
        self.searchDockWidget.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setText(QtGui.QApplication.translate("MainWindow", "&Export as", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setIconText(QtGui.QApplication.translate("MainWindow", "Export as", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setToolTip(QtGui.QApplication.translate("MainWindow", "Export as", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionControls.setText(QtGui.QApplication.translate("MainWindow", "&Controls", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAnnotationSource.setText(QtGui.QApplication.translate("MainWindow", "Annotation &Source", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAnnotation.setText(QtGui.QApplication.translate("MainWindow", "&Annotation", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreambleEditor.setText(QtGui.QApplication.translate("MainWindow", "Preamble Editor", None, QtGui.QApplication.UnicodeUTF8))

