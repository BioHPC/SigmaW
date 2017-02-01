import mysql.connector
import sys
import time

if __name__ == '__main__':
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

  cursor.execute('UPDATE joblist SET finish_time='+str(time.time())+",jobfinished=1 WHERE id='"+sys.argv[1]+"'")
  cnx.commit()

  cursor.close()
  cnx.close()
