# -*- coding: utf-8 -*-
import QtRec
from QtRec import QtGui, QtCore


from menupreferences import MenuPreferences
from menuabout import MenuAbout



class MenuBar(QtGui.QMenuBar):
	
	def __init__(self):
		super(MenuBar, self).__init__()
		self.app = QtGui.QApplication.instance()
		#MENU - FILE
		self.menu_file = self.addMenu('&File')

		new_add = self.menu_file.addAction('New - add')
		new_add.setStatusTip('...in new window')
		new_add.setShortcuts(QtGui.QKeySequence.New)

		new_rep = self.menu_file.addAction('New - replace')
		new_rep.setStatusTip('...replace this window')
		key_new_replace = QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_N)
		new_rep.setShortcuts(key_new_replace)

		self.menu_file.addSeparator()

		save = self.menu_file.addAction('Save')
		save.setStatusTip('Override last saved session')
		save.setShortcuts(QtGui.QKeySequence.Save)

		save_as = self.menu_file.addAction('Save As')
		save.setStatusTip('Choose a name')
		save_as.setShortcuts(QtGui.QKeySequence.SaveAs)

		self.menu_file.addSeparator()

		open_add = self.menu_file.addAction('Open - add')
		open_add.setStatusTip('...in new window')
		open_add.setShortcuts(QtGui.QKeySequence.Open)

		open_rep = self.menu_file.addAction('Open - replace')
		open_rep.setStatusTip('...replace this window')
		key_open_replace = QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_O)
		open_rep.setShortcuts(key_open_replace)

		self.menu_file.addSeparator()
		self.file_preferences = MenuPreferences(self)
		#print preferences, preferences.show()
		prefBtn = self.menu_file.addAction('Preferences')
		prefBtn.triggered.connect(self.file_preferences.show)


		#MENU - EDIT
		self.menu_edit = self.addMenu('&Edit')

		undo = self.menu_edit.addAction('Undo')
		#undo.setStatusTip('...')
		undo.triggered.connect(QtRec.undo)
		undo.setShortcuts(QtGui.QKeySequence.Undo)

		redo = self.menu_edit.addAction('Redo')
		#redo.setStatusTip('...')
		redo.triggered.connect(QtRec.redo)
		redo.setShortcuts(QtGui.QKeySequence.Redo)

		#self.menu_edit.addSeparator()

		#cut = self.menu_edit.addAction('Cut')
		##cut.setStatusTip('...')
		#cut.triggered.connect(QtRec.redo)#######################
		#cut.setShortcuts(QtGui.QKeySequence.Cut)

		#copy = self.menu_edit.addAction('Copy')
		##copy.setStatusTip('...')
		#copy.triggered.connect(QtRec.redo)#######################
		#copy.setShortcuts(QtGui.QKeySequence.Copy)

		#paste = self.menu_edit.addAction('Paste')
		##paste.setStatusTip('...')
		#paste.triggered.connect(QtRec.redo)#######################
		#paste.setShortcuts(QtGui.QKeySequence.Paste)

		#self.menu_edit.addSeparator()


		#MENU - VIEW
		self.menu_view = self.addMenu('&View')
		self.ckBox_fullscreen =  QtGui.QAction('Fullscreen', self.menu_view, checkable=True)
		self.menu_view.addAction(self.ckBox_fullscreen)
		self.ckBox_fullscreen.setStatusTip('Toggle between window and fullscreen')
		self.ckBox_fullscreen.triggered.connect(self.toggleFullScreen)
		self.ckBox_fullscreen.setShortcuts(QtGui.QKeySequence('F11'))


		#MENU - HELP
		self.menu_help = self.addMenu('&Help')


		#TODO: hier alle doc pdfs und rts listen - schön mit pdf und rtf logo

		sc = self.menu_help.addAction('Shortcuts')
		sc.setStatusTip('...list all shortcuts')
	
		self.menu_help.addSeparator()

		about = self.menu_help.addAction('About')
		about.setShortcuts(QtGui.QKeySequence('F1'))
		aboutWidget = MenuAbout()
		about.triggered.connect(aboutWidget.show)

		#connecting to app
		#try:
		s = self.app.session
		#i = self.app.identity
		#self.setWindowIcon(QtGui.QIcon(appbase.logo_path))
		new_add.triggered.connect(s.newAdd)
		new_rep.triggered.connect(s.newReplace)
		save.triggered.connect(s.save)
		save_as.triggered.connect(s.saveAs)
		open_add.triggered.connect(s.openAdd)
		open_rep.triggered.connect(s.openReplace)



	def toggleFullScreen(self):
		'''toggle between fullscreen and normal window'''
		if self.isFullScreen():
			self.ckBox_fullscreen.setChecked(False)
			self.showNormal()
		else:
			self.ckBox_fullscreen.setChecked(True)
			self.showFullScreen()