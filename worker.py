from mpi4py import MPI
from mpi_master_slave import Slave
from pdf2image import convert_from_path
from pdf2image.exceptions import (
 PDFPageCountError
)
import pytesseract
import os
from file_managment import file_managment
from multiprocessing import Process

class MySlave(Slave,file_managment):
    """
    A slave process extends Slave class, overrides the 'do_work' method
    and calls 'Slave.run'. The Master will do the rest
    """

    def __init__(self):
        super(MySlave, self).__init__()
        
    def do_work(self, data):
        rank = MPI.COMM_WORLD.Get_rank()
        name = MPI.Get_processor_name()
        task, task_arg,list_folder = data
        self.teseeractOCR(task_arg,list_folder)
        print('  Slave %s rank %d executing "%s" task_id "%d" ' % (name, rank, task, task_arg) )
        return (True, 'I completed my task (%d)' % task_arg)
    
    
    def teseeractOCR(self,count,path_test_train):
        try:
            entries = self.readFiles(count,path_test_train)
            fileTemp = ""
            for entry in entries[0]:
                if "pdf" in entry.lower():
                    print("Files procesing: ", entry)
                    isExist = self.filesExist(entry + ".txt", count,path_test_train)
                    if isExist == False:
                        pages = convert_from_path(entries[1] + "/" + entry, dpi=700, last_page=100, thread_count=2)
                        text = []
                        path_2 = "/Users/luistoribio/Documents/curso_python_avanzado/sesion_7_python_avanzado/master-worker" + "/output-files/"
                        for pageNum, imgBlob in enumerate(pages):
                             text.append(pytesseract.image_to_string(imgBlob, lang='eng'))
                        with open(f'{path_2}{entry}.txt', 'w') as the_file:
                            the_file.write('-'.join(text))
                        print("Files Processed: ", entry, " count: ", count)
                    else:
                        print("already exists: ", entry)
                else:
                    print("other image")
                    
            print("Complete")
        except PDFPageCountError as ex:
            print("Method failed with status code :" + str(ex))