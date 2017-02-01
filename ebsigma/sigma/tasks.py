from __future__ import absolute_import
from celery import shared_task

from time import sleep
from .send_mail import send_mail

@shared_task
def test():
  sleep(10)
  return 'Hello'
  
@shared_task
def run_sigma(id): #id is used to fetch config and data
  #TODO: Call sigma and fetch data
  sleep(5)
  send_mail('YOUR USER NAME@YOUR EMAIL DOMAIN', id) #will fetch email from db
  