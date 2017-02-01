import urllib

AWS_ACCESS_KEY_ID = 'YOUR AWK KEY'
AWS_SECRET_ACCESS_KEY = 'YOUR AWS SECRET KEY'

BROKER_BACKEND="SQS"
BROKER_URL = 'sqs://'
BROKER_TRANSPORT_OPTIONS = { 'region':'us-west-2', 'polling_interval':3, 'visibility_timeout':3600,}
BROKER_TRANSPORT_OPTIONS['queue_name_prefix'] = 'sigma-sqs-'