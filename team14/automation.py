import paramiko

'''
host: ip of host
user
key_path
'''
class cloud_automator:
    def __init__(self,conf):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(conf['host'], username=conf['user'], key_filename=conf['key_path'])

    def upload_file(self,source_path,dest_path):
        file_con=self.ssh.open_sftp()
        try:
            x = file_con.put(source_path,dest_path)
            return x
        except:
            return False

   #should modify to manage stdin
    def run_command(self,command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        if not stderr.readlines():
            return stdout
        else:
            return False