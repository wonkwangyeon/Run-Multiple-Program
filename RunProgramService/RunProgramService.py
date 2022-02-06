import subprocess
from SqlLite.DB import DB
from ToolLib.logger import Logger


class RunProgramService(object):
    logger = Logger("RunProgramService")
    
    def __init__(self):
        self.db = DB()

    def get_all_run_list(self): 
        rows = self.db.find_all()
        if rows is None:
            return None

        return rows

    def set_run_path(self, runType, runPath):
        result = self.db.save(runType, runPath)
        if result != 1:
            return "DB Error 발생"
                
        return result

    def delete_run_path(self, runId, runType, runPath):
        result = self.db.delete_by_run_id(runId, runType, runPath)     
        if result != 1:
            return "DB Error 발생"

        return result
    
    def get_last_run_id(self): 
        row = self.db.find_last_run_id()
        if row is None:
            return ""
        elif row == -1:
            return "DB Error 발생"

        return row[0]

    def run_multiple_program(self, runType, runPath):
        try:
            if runType == 'Folder':
                #subprocess.Popen('cd ' + runPath + '& start .', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, stdin=subprocess.DEVNULL)
                subprocess.Popen(f'explorer {runPath}')
                self.logger.info("Folder 실행 : " + runPath)
            else:
                subprocess.Popen(runPath, shell=True)
                self.logger.info("File 실행 : " + runPath)
        except Exception as e:
            self.logger.debug(e)