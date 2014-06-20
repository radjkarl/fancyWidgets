# -*- coding: utf-8 -*-
import appbase
import QtRec
from QtRec import QtGui, QtCore
from appbase.widgets import dialogs
#import os
from appbase.widgets.textEditor import MinimalTextEditor


from fancytools.os import userName




class MenuPreferences(QtGui.QWidget):

	def __init__(self, win, parent=None):

		super(MenuPreferences, self).__init__(parent, logparent=win)
		self.setWindowTitle('Preferences')
		self.app = QtGui.QApplication.instance()
		self.app.session.sigSave.connect(self._saveToFile)

		self._iconPath = None

		vlayout = QtGui.QVBoxLayout()
		self.setLayout(vlayout)

		qtrecPrefs = QtGui.QGroupBox("Record Activity")
		qtrecLayout = QtGui.QVBoxLayout()
		qtrecPrefs.setLayout(qtrecLayout)
		vlayout.addWidget(qtrecPrefs)

		b = QtGui.QRadioButton('Save time stamp')
		b.setChecked(QtRec.save_time_stamp)
		b.toggled.connect(QtRec.setSaveTimeStep)
		b.setToolTip(QtRec.setSaveTimeStep.__doc__)

		qtrecLayout.addWidget(b)

		b = QtGui.QRadioButton('Save History')
		b.setChecked(QtRec.save_history)
		b.toggled.connect(QtRec.setSaveHistory)
		b.setToolTip(QtRec.setSaveHistory.__doc__)
		qtrecLayout.addWidget(b)

		self.interval = QtGui.QLabel()
		self.slider = QtGui.QSlider(QtCore.Qt.Orientation(1), self, logname='AutosaveInterval')#1...horizontal
		self.slider.sliderMoved.connect(self._updateInterval)

		qtrecLayout.addWidget(self.interval)
		qtrecLayout.addWidget(self.slider)
		if self.app:
			self.slider.setSliderPosition (self.app.session.autosave_interval)
			self._updateInterval(self.app.session.autosave_interval)
		else:
			self._updateInterval(5)

		file_desc = QtGui.nolog.QGroupBox('File Information')
		layout = QtGui.nolog.QVBoxLayout()

		iconChoose = QtGui.nolog.QComboBox()
		if self.app:
			self._iconPath = self.app.session.tmp_dir_session.join('icon')
			if self._iconPath.exists():
				iconChoose.addItem (QtGui.nolog.QIcon(self._iconPath), 'Recent')
			else:
				self._iconPath = appbase.logo_path
			iconChoose.addItem (QtGui.nolog.QIcon(appbase.logo_path), 'Default')
		else:
			iconChoose.addItem('None')
		iconChoose.addItem('Individual')
		iconChoose.activated[unicode].connect(self._cooseIndividualIcon)

		iconLayout = QtGui.nolog.QHBoxLayout()
		iconLayout.addWidget(QtGui.nolog.QLabel('Icon:'))
		iconLayout.addWidget(iconChoose)
		layout.addLayout(iconLayout)

		#CHOOSE A SCREENSHOT A SHOW IN THE LAUNCHER DETAILS AREA
		self._lastSchreenshotWindow = None
		self._screenshot_from_window = None
		screenshotLayout = QtGui.nolog.QHBoxLayout()
		screenshotLayout.addWidget(QtGui.nolog.QLabel('Screenshot:'))
		self._screenshotChoose = QtGui.nolog.QComboBox()
		self._screenshotChoose.currentIndexChanged.connect(self._chosenScreenshotWindowChanged)
		screenshotLayout.addWidget(self._screenshotChoose)
		layout.addLayout(screenshotLayout)

		#CREATE A DESCRIPTION TEXT
		self.descritionEditior = MinimalTextEditor(self)
		descriptionText = ''
		if self.app:
			descriptionText = self.app.session.getSavedContent('description')
		if descriptionText:
			self.descritionEditior.text.setText(descriptionText)
		else:
			self.descritionEditior.text.setText(self._defaultDescription())
		layout.addWidget(self.descritionEditior)
		file_desc.setLayout(layout)
		vlayout.addWidget(file_desc)


	def _fillScreenshotChoose(self):
		self._screenshotChoose.clear()
		self._name_2_win = {}
		n = 0
		for win in self._availWindows():
				n += 1
				title = unicode(win.windowTitle())
				if not title:
					title = 'Window ' + str(n)
				self._name_2_win[title] = win
				self._screenshotChoose.addItem(title)
		self._screenshot_from_window = self._name_2_win.values()[0]


	def _availWindows(self):
		#must be a visible window but not this one
		return [win for win in self.app.topLevelWidgets()
			if not win.parent() and win.isVisible() and win != self]


	def _chosenScreenshotWindowChanged(self, index):
		self._restoreLastScreenshotWindow()
		title = self._screenshotChoose.itemText(index)
		win = self._name_2_win[unicode(title)]
		p = win.palette()
		self._lastSchreenshotWindow = (win, win.autoFillBackground(), p.color(win.backgroundRole()) )
		win.setAutoFillBackground(True)
		p.setColor(win.backgroundRole(), QtCore.Qt.red)
		win.setPalette(p)
		self._screenshot_from_window = win


	def _restoreLastScreenshotWindow(self):
		if self._lastSchreenshotWindow:
			#restore last
			(win, autoFill, color) = self._lastSchreenshotWindow
			win.setAutoFillBackground(autoFill)
			p = win.palette()
			p.setColor(win.backgroundRole(), color)
			win.setPalette(p)


	def _saveToFile(self, to_path):
		if not self._screenshot_from_window:
			self._screenshot_from_window = self._availWindows()[0]
		pixmap =  QtGui.QPixmap.grabWidget(self._screenshot_from_window)
		pixmap.save(to_path.join('screenshot.png'), 'png')
		if self._iconPath:
			self.app.session.addFileToSave(self._iconPath, 'icon')
		self.app.session.addContentToSave(self.descritionEditior.text.toHtml(), 'description.html')


	def showEvent(self, event):
		self._fillScreenshotChoose()
		super(MenuPreferences, self).showEvent(event)


	def _defaultDescription(self):
		return '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-style:italic; text-decoration: underline;">- no descrition found -</span></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; text-decoration: underline;"><br /></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">create one in <span style=" font-weight:600;">File-&gt;Preferences</span></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt;">Example</span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">Editor:     %s</span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">Project:</span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">State:</span></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;"><br /></p></body></html>
''' %userName()


	def _cooseIndividualIcon(self, text):
		self._iconPath = dialogs.getOpenFileName(directory= appbase.icon_path)


	def _updateInterval(self, time_min):
		if time_min == 0:
			time_min = 0.1
		if time_min == 99:
			self.interval.setText("Autosave: never")
			if self.app:
				self.app.session.timerAutosave.stop()
		else:
			self.interval.setText("Autosave: %s min" %time_min)
		if self.app:
			self.app.session.timerAutosave.setInterval(time_min*60*1000)
			self.app.session.timerAutosave.start()


	def closeEvent(self, evt):
		self._restoreLastScreenshotWindow()
		super(MenuPreferences, self).closeEvent(evt)
