## CHECK DISK ON SPACE AND INOD

    Проверка диска linux от '/' на наличие свободного места. 
    Ответ приходит в формате json.
    Для запроса используется GET запрос.
    
## Reqaered 
 
    Python>=3.7
    bottle==0.12.15

## Install
    apt install python3-dev(need in uwsgi)
    python3 -m venv name_dir_package
    source name_dir_package/bin/activate
    cd venv
    git clone .......
    pip install -r requirements.txt
   
## Configuration


#### Network    
    If a need configuration ip or ports, use uwsgi.ini file    
    Example:
    http = 0.0.0.0:5001
    
#### Email and Threshold value
    Set email and threshold value  uses a configuration file settings.py
    The index of the frequency of sending the letter (sec)
    Default POINT_MOUNT = ['/']
    Example:
      CICLE_TIME = 20
      POINT_MOUNT = ['/', '/run/lock']
      
## Systemd 
    Before to start need change uses directory in uwsgi.ini and check_disk.uwsgi.service
    
##### uwsgi.ini
    Change a parametr chdir
        Example: 
          chdir = /opt/Check_disk/
          
##### check_disk.uwsgi.service
     Paths must be absolute
        Example:
          ExecStart = /opt/Check_disk/venv/bin/uwsgi home/user/Check_disk/uwsgi.ini
          
##### Create simlink:
    ln -s /opt/Check_disk/check_disk.uwsgi.service /etc/systemd/system/check_disk.uwsgi.sevice
    
##### Start 
    systemctl enable check_disk.uwsgi.sevice
    systemctl start check_disk.uwsgi.sevice