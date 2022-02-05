#!/bin/sh
### Set the job name (for your reference)
#PBS -N evallen8stride4
### Set the project name, your department code by default
#PBS -P ee
### Request email when job begins and ends
#PBS -m bea
### Low priority for now
#PBS -q standard
### Specify email address to use for notification.
#PBS -M $USER@iitd.ac.in
####
#PBS -lselect=1:ncpus=1
### Specify "wallclock time" required for this job, hhh:mm:ss
#PBS -lwalltime=36:00:00
export OMP_NUM_THREADS=1
# After job starts, must goto working directory. 
# $PBS_O_WORKDIR is the directory from where the job is fired. 
echo "==============================="
echo $PBS_JOBID
cat $PBS_NODEFILE
echo "==============================="
cd $PBS_O_WORKDIR
#job 
#module load apps/anaconda/3
python3 eval.py
