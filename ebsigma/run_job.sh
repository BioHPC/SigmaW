#a shell script for running sigma
echo "Starting Run Job" >> /opt/python/current/app/log.txt
mkdir $1
chmod 777 $1
aws s3 sync s3://YOUR DB NAME/$1 $1

cd $1 #move into the new directory

/opt/python/current/app/sigma/Sigma/bin/sigma-index-genomes -c sigma_config.cfg >> /opt/python/current/app/log.txt 2>&1
/opt/python/current/app/sigma/Sigma/bin/sigma-align-reads -c sigma_config.cfg >> /opt/python/current/app/log.txt 2>&1
/opt/python/current/app/sigma/Sigma/bin/sigma -c sigma_config.cfg >> /opt/python/current/app/log.txt 2>&1

#modify to krona
cp /opt/python/current/app/3test.c .
gcc 3test.c -o 3test.out

python /opt/python/current/app/sigma/sigToHtml.py -ti sigma_out.gvector.txt -kp /opt/python/current/app/sigma/KronaTools-2.7/scripts/ImportText.pl -tp 3test.out

cd .. 

aws s3 sync $1 s3://YOUR DB NAME/$1

echo "Sending email" >> /opt/python/current/app/log.txt
sh email.sh $1

rm -r $1
