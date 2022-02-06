import sys
import time
from PyQt5.QtWidgets import *
from RunProgramService.RunProgramService import RunProgramService
from ToolLib.logger import Logger


class RunMultipleProgram(QWidget):
    logger = Logger("RunMultipleProgram")

    def __init__(self):
        super().__init__()
        self.runProgram = RunProgramService()
        self.initUI()
        self.logger.info("Start Run Multiple Program") 

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.cb = QComboBox(self)
        self.cb.addItem('File')
        self.cb.addItem('Folder')

        self.pathEdit = QLineEdit()
        grid.addWidget(self.cb, 0, 0)
        grid.addWidget(self.pathEdit, 0, 1, 1,4)

        btnAdd = QPushButton('ADD')
        btnAdd.clicked.connect(self.btnAdd_clicked)

        btnDelete = QPushButton('DELETE')
        btnDelete.clicked.connect(self.btnDelete_clicked)
        grid.addWidget(btnDelete, 1, 3)
        grid.addWidget(btnAdd, 1, 4)

        self.tableWidget = QTableWidget()        
        self.tableWidget.setColumnCount(3)
        columnHeaders = ['ID', 'Type', 'Path']                
        self.tableWidget.setHorizontalHeaderLabels(columnHeaders)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)        
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        grid.addWidget(self.tableWidget, 2, 0, 1, 5)

        btnRun = QPushButton('RUN')
        btnRun.clicked.connect(self.btnRun_clicked)
        grid.addWidget(btnRun, 3, 4)

        self.setWindowTitle('Run Multiple Program')
        self.resize(600, 450)
        self.center()
        self.table_setting()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def table_setting(self):
        runList=self.runProgram.get_all_run_list()    

        if runList is None:
            self.tableWidget.setRowCount(0)
        else:
            self.tableWidget.setRowCount(len(runList))

            for idx, list in enumerate(runList):            
                self.tableWidget.setItem(idx, 0, QTableWidgetItem(str(list[0])))
                self.tableWidget.setItem(idx, 1, QTableWidgetItem(list[1]))
                self.tableWidget.setItem(idx, 2, QTableWidgetItem(list[2]))
  
    def btnAdd_clicked(self):        
        result = self.runProgram.set_run_path(self.cb.currentText(), self.pathEdit.text())
        if result == 1:            
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(rowCount+1)
            lastRunId = self.runProgram.get_last_run_id()
            if lastRunId != -1:
                self.tableWidget.setItem(rowCount, 0, QTableWidgetItem(str(lastRunId)))
                self.tableWidget.setItem(rowCount, 1, QTableWidgetItem(self.cb.currentText()))
                self.tableWidget.setItem(rowCount, 2, QTableWidgetItem(self.pathEdit.text()))
                self.pathEdit.clear()
                QMessageBox.question(self, 'Message', '추가되었습니다.',
                                        QMessageBox.Yes)
            else:
                QMessageBox.question(self, 'Message', result,
                                    QMessageBox.Yes)
        else:
             QMessageBox.question(self, 'Message', result,
                                    QMessageBox.Yes)

    def btnDelete_clicked(self): 
        currentRow = self.tableWidget.currentRow()
        if currentRow != -1:
            runId = self.tableWidget.item(currentRow, 0).text()
            runType = self.tableWidget.item(currentRow, 1).text()
            runPath = self.tableWidget.item(currentRow, 2).text()
            result = self.runProgram.delete_run_path(runId, runType, runPath)
            if result == 1:
                self.tableWidget.removeRow(self.tableWidget.currentRow())
                QMessageBox.question(self, 'Message', '삭제되었습니다.',
                                    QMessageBox.Yes) 
            else:
                QMessageBox.question(self, 'Message', result,
                                    QMessageBox.Yes)
        else :
            QMessageBox.question(self, 'Message', '행을 선택해주세요.',
                                    QMessageBox.Yes)            
    
    def btnRun_clicked(self):
        try:
            rowCount = self.tableWidget.rowCount()
            for i in range(0, rowCount):
                runType = self.tableWidget.item(i, 1).text()
                runPath = self.tableWidget.item(i, 2).text()
                self.runProgram.run_multiple_program(runType, runPath)
                time.sleep(0.3)
        except Exception as e:
            self.logger.debug(e)
            QMessageBox.question(self, 'Message', '프로그램에 문제가 발생하였습니다.',
                                    QMessageBox.Yes)          

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = RunMultipleProgram()
   sys.exit(app.exec_())