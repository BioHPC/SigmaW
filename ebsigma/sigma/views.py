from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage

from tasks import run_sigma
from make_cfg import make_cfg
from generate_id import generate_id
from threading import Thread

import os
import mysql.connector
import subprocess
import time

def debug_call(uid):
  with open('sig_log.txt', 'w') as f1, open('sig_err.txt', 'w') as f2:
    subprocess.Popen(['sh','/opt/python/current/app/do_job.sh', uid], stdout=f1, stderr=f2)

# Create your views here.
def index(request):
  if request.method == 'POST':    
    if 'RDS_HOSTNAME' in os.environ:
          DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.environ['RDS_DB_NAME'],
                'USER': os.environ['RDS_USERNAME'],
                'PASSWORD': os.environ['RDS_PASSWORD'],
                'HOST': os.environ['RDS_HOSTNAME'],
                'PORT': os.environ['RDS_PORT'],
            }
          }

          cnx = mysql.connector.connect(user=DATABASES['default']['USER'],password=DATABASES['default']['PASSWORD'],database=DATABASES['default']['NAME'], host=DATABASES['default']['HOST'], port=DATABASES['default']['PORT'])
          cursor = cnx.cursor()
            
          #Begin Database Work
          try: #this is to make a table
            cursor.execute('DROP TABLE jobs')
            cursor.execute('CREATE TABLE IF NOT EXISTS joblist (email VARCHAR(100), id VARCHAR(200), submit_time VARCHAR(200), jobstarted BOOLEAN, finish_time VARCHAR(200), jobfinished BOOLEAN);')
            cnx.commit()
          except:
           pass
          #End Database Work
          
          uid = str(generate_id())
          
          cursor.execute("INSERT INTO joblist (email,id,submit_time,jobstarted,finish_time,jobfinished) VALUES ('" + request.POST.get('email', '') + "','" + uid + "','" + str(time.time()) + "',FALSE,null,FALSE);")
          cnx.commit()
          
          cursor.execute("SELECT * FROM joblist")
          
          res = ''
          for entry in cursor:
            res += str(entry) + '<br>'
          
          cursor.close()
          cnx.close()
          
          sigma_cfg = make_cfg(request.POST, request.FILES, uid)
          
          if (request.POST.get("read_type", "ERROR") == "single"):
            f = default_storage.open(uid+'/'+request.FILES["single_file"].name, 'wb')
            f.write(request.FILES["single_file"].read())
            f.close()
          else:
            f = default_storage.open(uid+'/'+request.FILES["paired_file1"].name, 'wb')
            f.write(request.FILES["paired_file1"].read())
            f.close()
            
            f = default_storage.open(uid+'/'+request.FILES["paired_file2"].name, 'wb')
            f.write(request.FILES["paired_file2"].read())
            f.close()
          
          f = default_storage.open(uid+'/sigma_config.cfg', 'w')
          f.write(sigma_cfg)
          f.close()
          
          #Thread(target=debug_call, args=(uid,)).start()
          
          #subprocess.Popen(['sh','/opt/python/current/app/run_job.sh', uid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
          
          return HttpResponse('Your job is now in the queue.<br><br>Your unique id for this job is: ' + str(uid) + '<br><br>If you did not enter your email SAVE THIS LINK: YOUR SITE DOMAIN/results/' + str(uid))
          
    return HttpResponse('DB Error!')
    
  else:
    return render(request, 'sigma.html')

def results(request, uid='-1'):
  return render(request, 'results.html', {'uid':uid})