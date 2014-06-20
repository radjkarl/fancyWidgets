# -*- coding: utf-8 -*-

#own
#foreign

from pyqtgraph import ImageView as pgImageView
from pyqtgraph.exporters.ImageExporter import ImageExporter
from pyqtgraph.Qt import QtCore, QtGui




class FwImageView(pgImageView):
	
	def __init__(self, **opts):
		#self.roiClicked = self._pass
		self._show_roi = False
		super(FwImageView, self).__init__(**opts)
		
	#	filterMenu = QtGui.QMenu("Filter Options")
	#	plotItem.ctrlMenu = [filterMenu]
		
		
		
		#Show/Hide in main menu - for histogramm in histogramm menu
		shMenu = self.view.menu.leftMenu.addMenu('Show/Hide')
		shMenu.addAction('Histogramm').triggered.connect(self.toggleHistogramm)
		#hide buttons ad add its func. to the menu:
	#	self.ui.roiBtn.clicked.disconnect()
		self.ui.roiBtn.hide()
		self.ui.normBtn.hide()
		shMenu.addAction('Region Of Interest').triggered.connect(self.toggleROI)
		shMenu.addAction('Normalize').triggered.connect(self.toggleNorm)
		self._origROI_setVisible = self.ui.roiPlot.setVisible
		self.ui.roiPlot.setVisible = self._setVisibleROI

		#self._show_roi = True
	#	self._calcROIPosition()
		#self._show_roi = False
		self.ui.splitter.setSizes([self.height(), 0])
	#	self.ui.splitter.hide()
	#	self.ui.roiPlot.hide()



	def _calcROIPosition(self):
		c = self.view.viewRect().center()
		p0 = self.view.viewRect().topLeft()
		#calc scale as half size:
		sX = self.view.viewRect().width()/2
		sY = self.view.viewRect().height()/2
		self.roi.sigRegionChanged.disconnect()#connect(self.roiChanged)
		#reset angle
		self.roi.setAngle(0)
		#move to the middle of the display
		#if that is not done the ROI gos from 0 to 10 ... that can cause errors
		# on small of high resoluted arrays
		self.roi.setPos((c+p0)/2)
		self.roi.setSize([sX,sY])
		#roi should be selected:
		self.roi.setSelected(True)
		self.roi.sigRegionChanged.connect(self.roiChanged)

		self.roiChanged()


	def _setVisibleROI(self, showRoiPlot):
		if showRoiPlot:
			self._calcROIPosition()
		self._origROI_setVisible(showRoiPlot)


	def roiClicked(self):
		if self._show_roi:
			super(FwImageView, self).roiClicked()


	def toggleROI(self):
		self._show_roi = True
		self.ui.roiBtn.toggle()
		self.roiClicked()
		self._show_roi = False


	def toggleNorm(self):
		self.ui.normBtn.toggle()
		self.normToggled()


	def toggleHistogramm(self):
		if self.ui.histogram.isVisible():
			self.ui.histogram.hide()
		else:
			self.ui.histogram.show()


	def exportImage(self, fName, resX=None,resY=None):
		#zoom the the chosen colorrange:
		r = self.ui.histogram.region.getRegion()
		self.ui.histogram.vb.setYRange(*r)
		#create ImageExpoerters:
		mainExp = ImageExporter(self.view)
		colorAxisExp = ImageExporter(self.ui.histogram.axis)
		colorBarExp = ImageExporter(self.ui.histogram.gradient)


		if resX or resY:
			#get size-x:
			mainW = mainExp.getTargetRect().width()
			colorAxisW = colorAxisExp.getTargetRect().width()
			colorBarW = colorBarExp.getTargetRect().width()
			
			#all parts have the same height:
			mainExp.parameters()['height'] = resY
			colorAxisExp.parameters()['height'] = resY
			colorBarExp.parameters()['height'] = resY
			#size x is proportional:
			sumWidth = mainW + colorAxisW + colorBarW
			mainExp.parameters()['width'] = resX * mainW / sumWidth
			colorAxisExp.parameters()['width'] = resX * colorAxisW / sumWidth
			colorBarExp.parameters()['width'] = resX * colorBarW / sumWidth
		#create QImages:
		main =mainExp.export(toBytes=True)
		colorAxis =colorAxisExp.export(toBytes=True)
		colorBar = colorBarExp.export(toBytes=True)
		#define teh size:
		x = main.width() + colorAxis.width() + colorBar.width()
		y = main.height()
		#to get everything in the same height:
		yOffs = [0,0.5*(y-colorAxis.height()),0.5*(y-colorBar.height())]

		result = QtGui.QImage(x, y ,QtGui.QImage.Format_RGB32)
		#the colorbar is a bit smaller that the rest. to exclude black lines paint all white:
		result.fill(QtCore.Qt.white)

		painter = QtGui.QPainter(result)
		posX = 0
		for img,y in zip((main,colorAxis,colorBar),yOffs):
			#draw every part in different positions:
			painter.drawImage(posX, y, img)
			posX += img.width()
		painter.end()
		#save to file
		result.save(fName)



if __name__ == "__main__":
	import sys

	app = QtGui.QApplication(sys.argv)
	
	#there is a bug on pyqtgraph and win7 64bit, therefore:
	import pyqtgraph
	pyqtgraph.setConfigOptions(useWeave=False)
	
	imv= FwImageView()

	## Create random 3D data set with noisy signals
	import numpy as np
	data = np.random.randint(low=0, high=10, size=(10,100,100))

	
	
	## Display the data and assign each frame a time value from 1.0 to 3.0
	imv.setImage(data)


	imv.show()
	sys.exit(app.exec_())

	#def setImage(self, img, autoRange=True, autoLevels=True, levels=None, axes=None, xvals=None, pos=None, scale=None, transform=None, autoHistogramRange=True)
		####SET COLORLEVEL###
		##bydefault autoLevel (the colorlevel of the merge-dims) == True
		##(calc. by pyqtgraph)
		##thus it only can process array without nan-values the calc. colorlevel
		##is wrong when the real values are boyond the nan-replacement(zero)
		##therefore i calc the colorlevel by my self in case nans arein the array:
		#if anynan and self.fitColorbar:
			#mmin = bn.nanmin(self.merge_extract)
			#mmax = bn.nanmax(self.merge_extract)
			##in case there are only nans:
			#if np.isnan(mmin):
				#mmin,mmax=0,0
			##in case there are only nans and eval values:
			#if mmin == mmax:
				##set min to 0 to see all places where those equal values are =! 0
				#mmin = 0
			#self.plot.setLevels(mmin, mmax)
		#args["autoLevels"]= False
			###the following line dont work with my version of pyQtGraph
			##args["levels"]= [mmin,mmax]#np.nanmin(merge_extract), np.nanmax(merge_extract))
		#self.merge_extract = utils.nanToZeros(self.merge_extract)
		#if self.transpose_axes:
			#self.plot.setImage(self.merge_extract.transpose(),
				#autoRange=self.scale_plot,**args)
		#else:
			#self.plot.setImage(self.merge_extract,
				#autoRange=self.scale_plot,**args)
		#if anynan and self.fitColorbar: # scale the histogramm to the new range
			#self.plot.ui.histogram.vb.setYRange(mmin,mmax)