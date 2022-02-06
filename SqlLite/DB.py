from cProfile import run
import sqlite3
import os
from pathlib import Path
from ToolLib.logger import Logger


class DB(object):
    logger = Logger("DB")

    def __init__(self):
                    
        if not Path('C:/runMultipleProgram/runMultipleProgram.db').is_file():
            self.conn = sqlite3.connect("C:/runMultipleProgram/runMultipleProgram.db")
            self.cur = self.conn.cursor()
            self.db_init_table()
        else:
            self.conn = sqlite3.connect("C:/runMultipleProgram/runMultipleProgram.db")
            self.cur = self.conn.cursor()

    def db_init_table(self):    
        self.conn.execute("""
                   CREATE TABLE IF NOT EXISTS run_list (
                        run_id integer primary key autoincrement, /* ID */
                        run_type TEXT,                        /* 파일 or 폴더 */
                        run_path TEXT                         /* 경로 */
                   )
               """)
        self.conn.commit()

    def find_all(self):
        try:
            sql = "SELECT * FROM run_list"

            self.cur.execute(sql)
            rows = self.cur.fetchall()
            
            if (len(rows)) == 0:
                return None
            else:
                return rows

        except Exception as e:
            self.logger.info("DB Error 발생")
            return -1

    def save(self, runType, runPath):
        try:
            sql = "insert into run_list(run_type, run_path) values(?, ?)"
            self.cur.execute(sql, (runType, runPath, ))
            self.conn.commit()
            self.logger.info("DB 저장 : " + runType + " - "+ runPath)
            return 1

        except Exception as e:
            self.logger.info("DB Error 발생")
            return -1

    def delete_by_run_id(self, runId, runType, runPath):
        try:
            sql = "delete from run_list where run_id = ?"
            self.cur.execute(sql, (runId, ))
            self.conn.commit() 
            self.logger.info("DB 삭제 : " + runType + " - "+ runPath)        
            return 1

        except Exception as e:
            self.logger.info("DB Error 발생")
            return -1

    def find_last_run_id(self):
        try:
            sql = "SELECT max(run_id) FROM run_list"

            self.cur.execute(sql)
            row = self.cur.fetchone()            
            if len(row) == 0:
                return None
            else:
                return row

        except Exception as e:
            self.logger.info("DB Error 발생")
            return -1

    def __del__(self):
        self.conn.close()