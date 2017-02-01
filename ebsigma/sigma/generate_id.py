import os
import hashlib

def generate_id():
  #generates a unique ID
  seed = os.urandom(160/8)
  return hashlib.sha1(seed).hexdigest()

if __name__ == '__main__':
  print generate_id()
