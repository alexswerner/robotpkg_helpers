import os
import datetime
from .utils import execute

class RobotpkghLogging:

    def __init__ (self,title):
        current_date = datetime.datetime.now()
        str_cur_date = current_date.strftime("%Y_%m_%d")
        str_cur_time = current_date.strftime("%H_%M")
        base_log_file_name = "/tmp/robotpkg_"+ title+ "_" + \
                             str_cur_date +'_'+ \
                             str_cur_time 

        filename=base_log_file_name+".log"
        self.f_stdout = open(filename,"wb")
        filename=base_log_file_name+"_error.log"
        self.f_error = open(filename,"wb")

    def execute(self,bashCmd,lenv,debug):
        outputdata,error,p_status = execute(bashCmd,lenv,debug)
        bashCmdu = bashCmd+'\n'
        self.f_stdout.write(bashCmdu.encode('utf-8'))
        self.f_stdout.write(outputdata)
        self.f_error.write(error)
        self.f_stdout.flush()
        self.f_error.flush()
        return outputdata,error,p_status

    def execute_call(self,bashCmd,lenv,debug):        
        outputdata,error = execute_call(bashCmd,lenv,debug)
        bashCmdu = bashCmd+'\n'
        self.f_stdout.write(bashCmdu.encode('utf-8'))
        self.f_stdout.write(outputdata)
        self.f_error.write(error)
        self.f_stdout.flush()
        self.f_error.flush()
        return outputdata,error

    def print_log(self,msg):
        snd_msg='RPKGH:'+msg
        print(snd_msg)
        self.f_stdout.write(snd_msg.encode('utf-8'))
        self.f_stdout.flush()

    def print_err_log(self,msg):
        snd_msg='RPKGH:'+msg
        print(snd_msg)
        self.f_error.write(snd_msg.encode('utf-8'))
        self.f_error.flush()

    def __del__(self):
        if hasattr(self,'f_stdout'):
            self.f_stdout.close()
        if hasattr(self,'f_error'):
            self.f_error.close()
        
