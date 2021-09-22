import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, qApp
from os.path import basename
from DateConverter import DateConverter

def converter(fname):
    dc = DateConverter(fname)
    try:
        dc.processFile()
        dc.writeFile()
    except FileNotFoundError:
        return 'File Not Found'
    except PermissionError:
        return 'Permission Error'
    else:
        return 'OK'

class ConverterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()
    
    def initializeUI(self):
        self.setWindowTitle('Converter')
        self.setFixedHeight(500)
        self.setFixedWidth(350)
        
        openBtn = QPushButton('Open Files', self)
        openBtn.move(20, 20)
        openBtn.clicked.connect(self.showOpenDialog)
        
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setRowCount(0)
        self.table.setGeometry(10, 60, 330, 430)
        self.table.setHorizontalHeaderLabels(['File Name', 'Status'])
        self.table.setColumnWidth(0, 180)
        
        self.show()
    
    def showOpenDialog(self):
        self.fname, _ = QFileDialog.getOpenFileNames()
        
        qApp.processEvents()
        
        if self.fname:
            self.table.setRowCount(len(self.fname))
            for f in enumerate(self.fname):
                self.table.setItem(f[0], 0, QTableWidgetItem(basename(f[1])))
                self.table.setItem(f[0], 1, QTableWidgetItem(''))
        
        qApp.processEvents()
        
        self.processFiles()
    
    def processFiles(self):
        if self.fname:
            for f in enumerate(self.fname):
                self.table.setItem(f[0], 1, QTableWidgetItem(converter(f[1])))
                self.table.scrollToItem(self.table.item(f[0], 0))
                qApp.processEvents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConverterWindow()
    sys.exit(app.exec_())