# -*- coding: utf-8 -*-
import appbase
from QtRec import QtGui, QtCore
import appbase.widgets.dialogs
import os
from appbase.widgets.textEditor import MinimalTextEditor


from fancytools.os import userName




class MenuAbout(QtGui.QWidget):
#TODO: erstellen
	def __init__(self, parent=None):
		self.app = QtGui.QApplication.instance()

		super(MenuAbout, self).__init__(parent, logparent=self.app)
		self.setWindowTitle('Preferences')

		self._iconPath = None


		vlayout = QtGui.QVBoxLayout()
		self.interval = QtGui.QLabel()
		self.slider = QtGui.QSlider(QtCore.Qt.Orientation(1), self, logname='AutosaveInterval')#1...horizontal
		self.slider.sliderMoved.connect(self._updateInterval)

		vlayout.addWidget(self.interval)
		vlayout.addWidget(self.slider)
		self.setLayout(vlayout)
	#	if self.app:
		self.slider.setSliderPosition (self.app.session.autosave_interval)
		self._updateInterval(self.app.session.autosave_interval)
		#else:
		self._updateInterval(5)

		file_desc = QtGui.nolog.QGroupBox('File Information')
		layout = QtGui.nolog.QVBoxLayout()


		iconText =  QtGui.nolog.QLabel('Icon:')
		iconChoose = QtGui.nolog.QComboBox()

		#if self.app:
		iconPath = self.app.session.tmp_dir_session.join('icon')
		if iconPath.exists():
			iconChoose.addItem (QtGui.nolog.QIcon(iconPath), 'Recent')
		iconChoose.addItem (QtGui.nolog.QIcon(appbase.logo_path), 'Default')
		#else:
		#	iconChoose.addItem('None')
		iconChoose.addItem('Individual')
		iconChoose.activated[unicode].connect(self._cooseIndividualIcon)

		iconLayout = QtGui.nolog.QHBoxLayout()
		iconLayout.addWidget(iconText)
		iconLayout.addWidget(iconChoose)


		layout.addLayout(iconLayout)
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


	#	vlayout.addWidget(QtGui.QLabel('Launcher Representation'))
		#TODO: inser scrreshotlist

	def _cooseIndividualIcon(self, text):
		self._iconPath = dialogs.getOpenFileName(directory= os.path.join(appBase.__path__[0],'media','icons'))

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
		if self.app:
			if self._iconPath:
				self.app.session.addFileToSave(self._iconPath, 'icon')
	
			self.app.session.addContentToSave(self.descritionEditior.text.toHtml(), 'description.html')

		super(MenuAbout, self).closeEvent(evt)
