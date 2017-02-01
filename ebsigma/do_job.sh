#Create our new instance
#chmod 777 SigmaInternal.pem

export AWS_ACCESS_KEY_ID="YOUR AWK KEY"
export AWS_SECRET_ACCESS_KEY="YOUR AWS SECRET KEY"      

#need to switch to m3.2xlarge
outp=$(aws ec2 run-instances --block-device-mappings file:///opt/python/current/app/mapping.json --instance-initiated-shutdown-behavior terminate --instance-type m3.2xlarge --image-id ami-7172b611 --count 1 --key-name SigmaInternal --security-groups awseb-e-gq8wxdgf3a-stack-AWSEBSecurityGroup-10A84Q28M3X11 rds-launch-wizard-1 --region us-west-2)
id=$(echo $outp | grep -o '"InstanceId": "[^"]*"' | grep -o 'i-[^"]*')

echo $id

#Check server and wait until it is ready to run
while true
do
  output=$(aws ec2 describe-instance-status --region us-west-2 --instance-ids $id)
  code=$(echo $output | grep -o '"Code": [^,]*' | grep -o '[0-9]*')
  
  if [ "$code" == "16" ]; then
    break
  fi
  
  sleep 2  
done

echo "Server in ready state"

#Fetch DNS address
dns=$(aws ec2 describe-instances --instance-ids $id --region us-west-2 | grep -o '"PublicDnsName": "[^"]*"' | grep -o -m 1 'ec2-[^"]*')

#Special case
scp -i /opt/python/current/app/SigmaInternal.pem -o StrictHostKeyChecking=no /opt/python/current/app/run.sh ec2-user@$dns:/home/ec2-user
while [ $? -ne 0 ] 
do
  sleep 30
  scp -i /opt/python/current/app/SigmaInternal.pem -o StrictHostKeyChecking=no /opt/python/current/app/run.sh ec2-user@$dns:/home/ec2-user
done 

scp -i /opt/python/current/app/SigmaInternal.pem -o StrictHostKeyChecking=no /opt/python/current/app/env.sh ec2-user@$dns:/home/ec2-user
scp -i /opt/python/current/app/SigmaInternal.pem -o StrictHostKeyChecking=no /opt/python/current/app/requirements.txt ec2-user@$dns:/home/ec2-user
scp -i /opt/python/current/app/SigmaInternal.pem -o StrictHostKeyChecking=no /opt/python/current/app/updatedb.py ec2-user@$dns:/home/ec2-user

echo "Files transfered to server"

#tag instance for readability
aws ec2 create-tags --resources $id --tags Key=Name,Value=$1 --region=us-west-2

ssh -i /opt/python/current/app/SigmaInternal.pem -o StrictHostKeyChecking=no -t -t ec2-user@$dns "sh run.sh $1"
