from mpi4py import MPI
from mpi_master_slave import Master, Slave
from mpi_master_slave import WorkQueue
import time
from worker import MySlave
import os
import subprocess
from pathlib import Path


class MyApp(object):
    """
    This is my application that has a lot of work to do so it gives work to do
    to its slaves until all the work is done
    """


    def __init__(self, slaves):
        # when creating the Master we tell it what slaves it can handle
        #init en variables
        self.master = Master(slaves)
        # WorkQueue is a convenient class that run slaves on a tasks queue
        self.work_queue = WorkQueue(self.master)

    def terminate_slaves(self):
        """
        Call this to make all slaves exit their run loop
        """
        self.master.terminate_slaves()

    def run(self,tasks=2):
        """
        This is the core of my application, keep starting slaves
        as long as there is work to do
        """
        #
        # let's prepare our work queue. This can be built at initialization time
        # but it can also be added later as more work become available
        #
        path_input_1 = os.path.join(os.environ['GENERAL_PATH'],"input-files/OCR_inputs")
        path_input_2 = os.path.join(os.environ['GENERAL_PATH'],"input-files/OCR_inputs")
        # 'data' will be passed to the slave and can be anything
        # 'data' will be passed to the slave and can be anything
        self.work_queue.add_work(data=('Do OCR task',1,path_input_1))
        self.work_queue.add_work(data=('Do OCR task',2,path_input_2))

       
        #
        # Keeep starting slaves as long as there is work to do
        #
        while not self.work_queue.done():

            #
            # give more work to do to each idle worker (if any)
            #
            self.work_queue.do_work()

            #
            # reclaim returned data from completed slaves
            #
            for slave_return_data in self.work_queue.get_completed_work():
                done, message = slave_return_data
                if done:
                    print('Master: worker finished is task and says "%s"' % message)

            # sleep some time
            time.sleep(0.3)


if __name__ == "__main__":
    start = time.time()
    name = MPI.Get_processor_name()
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()

    print('I am  %s rank %d (total %d)' % (name, rank, size) )
    
    if rank == 0: # Master
        app = MyApp(slaves=range(1, size))
        app.run()
        app.terminate_slaves()
    else: # Any slave
        MySlave().run()

    print('Task completed (rank %d)' % (rank) )
    end = time.time()
    print(f"Runtime of the program is {end - start}")
    print('Finish!')