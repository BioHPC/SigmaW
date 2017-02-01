#script for doing full run on AWS instance

source ./env.sh

#aws s3 cp s3://YOUR DB NAME-db/database.tar.bz2 database.tar.bz2
aws s3 cp s3://YOUR DB NAME-db/software.tar.bz2 software.tar.bz2
aws s3 cp s3://YOUR DB NAME-db/database2.tar.bz2 database2.tar.bz2
aws s3 cp s3://YOUR DB NAME-db/120DB.tar.bz2 120DB.tar.bz2

#tar jxvf database.tar.bz2
tar jxvf software.tar.bz2
tar jxvf database2.tar.bz2

mkdir 120DB
tar jxvf 120DB.tar.bz2 -C 120DB

sudo yum -y install ncurses-devel ncurses
sudo yum -y install gcc
sudo yum -y install zlib-devel

cd software/samtools
make
cd 

#gcc software/3test.c -o software/3test.out

aws s3 sync s3://YOUR DB NAME/$1 $1


#check compression
cd $1
for f in *; do
  if [[ $f == *bz2 ]]; then
    bzip2 -dk $f
  fi
  if [[ $f == *gz ]]; then
    gunzip $f
  fi
done

cd ..

software/SigmaW/bin/sigma-index-genomes -c $1/sigma_config.cfg >> $1/log.txt 2>&1
software/SigmaW/bin/sigma-align-reads -c $1/sigma_config.cfg -w $1 -p 2 >> $1/log.txt 2>&1
software/SigmaW/bin/sigma -c $1/sigma_config.cfg -w $1 -t 8 >> $1/log.txt 2>&1

mv sigma_out* $1

python software/sigToHtml.py -ti $1/sigma_out.gvector.txt -kp software/KronaTools-2.7/scripts/ImportText.pl -tp software/a.out -pp software/phylo_tree.txt

cd $1
tar cvjf small.tar.bz2 sigma_config.cfg sigma_out.gvector.txt sigma_out.gvector.txt_krona1.html sigma_out.gvector.txt_krona2.html sigma_out.html log.txt
cd ..
tar cvSjf big.tar.bz2 $1
mv big.tar.bz2 $1/big.tar.bz2

aws s3 sync $1 s3://YOUR DB NAME/$1

#some stuff for the database management
sudo pip install -r requirements.txt

python updatedb.py $1
python software/send_mail.py YOUR USER NAME@YOUR EMAIL DOMAIN $1

#Comment this out if testing problems
sudo shutdown -h now
