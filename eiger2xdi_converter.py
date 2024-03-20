import sys
import os
import fabio
from PyQt5.QtWidgets import (QApplication, 
                             QWidget,
                             QLabel,
                             QLineEdit,
                             QPushButton,
                             QListWidget,
                             QFormLayout,
                             QVBoxLayout,
                             QHBoxLayout,
                             QFileDialog,
                             QMessageBox,
                             QProgressBar)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(400,150)

        self.sourcepath = str()
        self.destpath = str()


        layout = QVBoxLayout()

        self.button_source = QPushButton('Choose source HDF5 file')
        self.button_dest = QPushButton('Choose destination')
        
        toplayout = QHBoxLayout()
        toplayout.addWidget(self.button_source)
        toplayout.addWidget(self.button_dest)


        self.lineedit_source = QLineEdit('')
        self.lineedit_dest = QLineEdit('')

        self.lineedit_source.setStyleSheet("border: 1px solid black;\
                                   background-color:#d8fff7")
        self.lineedit_dest.setStyleSheet("border: 1px solid black;\
                                   background-color:#d8fff7")


        form = QFormLayout()
        form.addRow('Source HDF5 file:   ', self.lineedit_source)
        form.addRow('Destination:        ', self.lineedit_dest)

        self.button_go = QPushButton('Go !')
        self.button_clear = QPushButton('Clear all')

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.button_go)
        bottom_layout.addWidget(self.button_clear)

        self.progress_bar = QProgressBar()

        layout.addLayout(toplayout)
        layout.addLayout(form)
        layout.addLayout(bottom_layout)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

        self.button_source.clicked.connect(self.choose_source)
        self.button_dest.clicked.connect(self.choose_dest)
        self.button_go.clicked.connect(self.go)
        self.button_clear.clicked.connect(self.clear_all)

        self.lineedit_source.textChanged.connect(self.update_source)
        self.lineedit_dest.textChanged.connect(self.update_dest)


    def update_source(self, s):
        self.sourcepath = s


    def update_dest(self, s):
        self.destpath = s


    def choose_source(self):
        options = QFileDialog.Options()
        # ! use Native dialog or qt dialog... 
        # ! Must be checked on different platforms !
    #   options |= QFileDialog.DontUseNativeDialog
        self.sourcepath, _ = QFileDialog.getOpenFileName(self,
            "Choose HDF5 file", "","HDF5 file (*.h5)", 
            options=options)        
        
        self.lineedit_source.setText(self.sourcepath)


    def choose_dest(self):

        options = QFileDialog.Options()
        # ! use Native dialog or qt dialog... 
        # ! Must be checked on different platforms !
    #   options |= QFileDialog.DontUseNativeDialog
        self.destpath = QFileDialog.getExistingDirectory(self,
                 'Select Destination', options=options)

        self.lineedit_dest.setText(self.destpath)


    def go(self):
        if self.sourcepath and self.destpath:
            try:
                img = fabio.open(self.sourcepath)
                nframes = img.nframes

                self.progress_bar.setMinimum(0)
                self.progress_bar.setMaximum(nframes)

                for i in range(nframes):
                    frame = img.getframe(i)
                    conv = frame.convert('tifimage')
                    data = conv.data.astype('int32')
                    data[data < 0] = 0
                    conv.data = data
    
                    conv.write(self.destpath + 
                                '/frame_'+ '%04d' % (i+1) + '.tif')
                    
                    self.progress_bar.setValue(i+1)

            except Exception as e:

                QMessageBox.critical(self, 'Error', str(e))
                self.progress_bar.reset()


    def clear_all(self):
        self.sourcepath = str()
        self.destpath = str()
        self.lineedit_source.clear()
        self.lineedit_dest.clear()
        self.progress_bar.reset()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    app.exec()