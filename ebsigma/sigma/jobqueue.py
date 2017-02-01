#a queue for running jobs
import os
import mysql.connector
from time import sleep, time
import subprocess

from threading import Thread

def debug_call(uid):
  with open('sig_log.txt', 'w') as f1, open('sig_err.txt', 'w') as f2:
    subprocess.Popen(['sh','/opt/python/current/app/do_job.sh', uid], stdout=f1, stderr=f2)


if __name__ == '__main__':
  with open('queue.log', 'a') as f:
    f.write('Starting...\n')  
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'YOUR DB NAME',
        'USER': 'YOUR USER NAME',
        'PASSWORD': 'YOUR DB PASSWORD',
        'HOST': 'YOUR DB HOSTNAME',
        'PORT': 'YOUR DB PORT',
    }
  }

  cnx = mysql.connector.connect(user=DATABASES['default']['USER'],password=DATABASES['default']['PASSWORD'],database=DATABASES['default']['NAME'], host=DATABASES['default']['HOST'], port=DATABASES['default']['PORT'])
  cursor = cnx.cursor()
  
  with open('queue.log', 'a') as f:
    f.write('Connected to DB...\n')
  
  #this should run always
  while True:
  
    #check if log file is too big:
    if os.stat('queue.log').st_size > 250000000:
      with open('queue.log','w') as f:
        f.write('File wiped at... ' + str(time()) + '\n')
    #cleanup old jobs from testing days    
    cursor.execute('DELETE FROM joblist WHERE submit_time<1479227887.32')
    cnx.commit()
    cursor.execute('SELECT * FROM joblist WHERE jobfinished=1 AND finish_time<'+str(time() - 2592000))
    for entry in cursor:
      subprocess.Popen(['aws','s3','rm','--recursive','s3://YOUR DB NAME/'+entry[1]])
    #throaway jobs completed more than 30 days ago
    cursor.execute('DELETE FROM joblist WHERE jobfinished=1 AND finish_time<'+str(time() - 2592000))
    cnx.commit()
    
    cursor.execute('SELECT * FROM joblist WHERE jobstarted=1 AND jobfinished=0')
    count=0
    for entry in cursor: count+=1
    if count >= 10:
      pass
    else:
      cursor.execute('SELECT * FROM joblist WHERE jobstarted=0')
      with open('queue.log', 'a') as f:
        f.write('Fecthed all entries...\n')
      jobs = []
      for entry in cursor:
        jobs.append(entry)
        
      jobs = list(map(list,jobs))
      jobs = list(map((lambda x: x[0:2] + [float(x[2])] + x[3:]), jobs))
      jobs = sorted(jobs, key=lambda entry: entry[2])
        
      #jobs is now sorted by timestamp
      #subprocess.Popen(['sh','/opt/python/current/app/do_job.sh',jobs[0][1]])
      
      with open('queue.log', 'a') as f:
        f.write('Entry count: ' + str(len(jobs)) + '\n')
      
      with open('queue.log', 'a') as f:
        for j in jobs:
          f.write('\t'.join([str(x) for x in j]) + '\n')
      
      if len(jobs) > 0:
        curr = jobs[0]
        uid = curr[1]
        
        cursor.execute('UPDATE joblist SET jobstarted=1 WHERE id="' + uid + '"')
        cnx.commit()
        
        #subprocess.Popen(['sudo','sh','/opt/python/current/app/do_job.sh', uid])
        with open('queue.log', 'a') as f:
          f.write('Starting job ' + uid + '\n')
        Thread(target=debug_call, args=(uid,)).start()
      
    sleep(300)
    #break