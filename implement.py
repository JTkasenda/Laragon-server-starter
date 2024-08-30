import psutil
import launcher
import subprocess
laragon_path = r"C:\laragon\laragon.exe" 
apache_path = r"C:\laragon\bin\apache\Apache24\bin\httpd.exe"
mysql_path = r"C:\laragon\bin\mysql\MySQL Server 8.0\bin\mysql.exe"
if __name__ == "__main__":
    # Start Laragon
    laragon = launcher.Launcher(laragon_path, "laragon.exe")
    apache = launcher.Launcher(apache_path, "httpd.exe")
    mysql = launcher.Launcher(mysql_path, "mysql.exe")
    # subprocess.Popen([mysql_path, "-u", "root",""])
    # print(laragon.is_process_running())
    while True:
        if(not apache.is_process_running()):
            apache.start_process()
            # mysql.start_process()
        else:
            pass

    # if(apache.is_process_running()):
    #     apache.close_process()
    #     mysql.close_process()
    # else:
    #     pass
        