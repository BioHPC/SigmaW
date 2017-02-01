#A py file for generating Sigma config files

def make_cfg(data, file_data, uid):
  cfg = '''#################################
##### Parameters for SIGMA #####
#################################

#-----------------------------#
# Program selectiton and path #
#-----------------------------#
[Program_Info]

# Provide bowtie2 and samtools software directory path.
# If you don't know the exact path, just comment the below line with #.
# Then SIGMA will search the programs automatically from env path.
Bowtie_Directory=software/bowtie2
Samtools_Directory=software/samtools

#-------------------------#
# Data directory and path #
#-------------------------#
[Data_Info]

# Reference genome directory
#   - required database hierarchy:
#   [database directory] - [genome directory] - [fasta file] 
#                        - [genome directory] - [fasta file] 
#                                             - [fasta file] 
#                        - [genome directory] - [fasta file] 
#                                             - [fasta file] 
#                             ...
Reference_Genome_Directory=120DB

# Provide metagenome NGS read(s) path using comma separathm files.
# You should select only one: paired-end read(s) OR single end read(s).
# You should comment the unselected option
'''
  
  if data.get("read_type", "") == "single":
    cfg += '''# 
# For paired-end reads
#Paired_End_Reads_1=
#Paired_End_Reads_2=
#
# For single-end reads
Single_End_Reads={0}
'''.format(uid+"/"+file_data["single_file"].name.rstrip('.bz2').rstrip('.gz'))
  else:
    cfg += '''# 
# For paired-end reads
Paired_End_Reads_1={0}
Paired_End_Reads_2={1}
#
# For single-end reads
# Single_End_Reads=
'''.format(uid+"/"+file_data["paired_file1"].name.rstrip('.bz2').rstrip('.gz'),uid+"/"+file_data["paired_file2"].name.rstrip('.bz2').rstrip('.gz'))
  
  cfg += '''#------------------------------------------#
# Parameters for bowtie search and options #
#------------------------------------------#
[Bowtie_Search]
# Preset option of Bowtie2 --end-to-end mode
# sensitive (default preset of Bowtie2), very-sensitive, only-mismatch
Bowtie2_Preset={12}

# Maximum count of mismatches for one read alignment. (Default: 3)
Maximum_Mismatch_Count={0}

# The minimum fragment length (insert-size) for valid paired-end alignments. (Default: 0) 
Minimum_Fragment_Length={1}

# The maximum fragment length (insert-size) for valid paired-end alignments. (Default: 500) 
Maximum_Fragment_Length={2}

# Number of threads for running one bowtie task. (Default: 1)
Bowtie_Threads_Number=4

#----------------------------------#
# Parameters for model probability #
#----------------------------------#
[Model_Probability]

# Mismatch probability for one base pair. (Default: 0.05 equals 5%)
Mismatch_Probability={3}

# Minimum relative abundance rate (%) to report (Default: 0.01)
Minimum_Relative_Abundance ={4}

#---------------------------#
# Parameters for statistics #
#---------------------------#
[Statistics]

# Number of iterations for bootstrapping. (Default: 100)
Bootstrap_Iteration_Number={5}

#--------------------------------------#
# Parameters for genome reconstruction #
#--------------------------------------#
[Genome_Reconstruction]

# Select 1: Reconstruct all genomes above the cuff-off abundance
# Select 2: Reconstruct specific genome
Reconstruction_Selection={6}

# If a genome has lower relative abundance rate (%) than cut-off value, 
# then the genome is not considered to be reconstructed by SIGMA. (Default: 1.0)
Reconstruction_Cutoff_Abundance={7}

# Reconstruct specific genome
Reconstruction_Genome_Name={8}

# Minumum coverage length (bp) by reads (Default: 100)
Minumum_Coverage_Length={9}

# Minumum coverate depth (aveage) by reads (Default: 3)
Minimum_Average_Coverage_Depth={10}


#---------------------------------#
# Parameters for variants calling #
#---------------------------------#
[Variants_Calling]
Filtering_Genome_Name={11}
'''.format(
  data.get("max_mismatch_count", "ERROR"),
  data.get("min_fragment_length", "ERROR"),
  data.get("max_fragment_length", "ERROR"),
  data.get("mismatch_probability", "ERROR"),
  data.get("minimum_abundance", "ERROR"),
  data.get("bootstrap_iterations", "ERROR"),
  data.get("reconstruction_mode", "ERROR"),
  data.get("cutoff_abundance", "ERROR"),
  data.get("reconstruction_name", "ERROR"),
  data.get("min_coverage_length", "ERROR"),
  data.get("min_coverage_depth", "ERROR"),
  data.get("filter_name", "ERROR"),
  data.get("bowtie_mode", "ERROR")
)
  
  return cfg
  
def make_cfg_old(data, file_data, uid):
  cfg = ""
  cfg += "Bowtie_Directory=" + "sigma/bowtie2" + "\n"
  cfg += "Samtool_Directory=" + "sigma/samtools" + "\n"
  cfg += "Reference_Genome_Directory=database\n\n"
  
  if (data.get("read_type", "") == "single"):
    cfg += "Single_End_Reads=" + uid + "/" + file_data.get("single_file", "ERROR").name + "\n\n"
  else:
    cfg += "Paired_End_Reads_1=" + uid + "/" + file_data.get("paired_file1", "ERROR").name + "\n"
    cfg += "Paired_End_Reads_2=" + uid + "/" + file_data.get("paired_file2", "ERROR").name + "\n\n"
  
  cfg += "#Note everything below this point has a default value\n"
  cfg += "Maximum_Mismatch_Count=" + data.get("max_mismatch_count", "ERROR") + "\n"
  cfg += "Minimum_Fragment_Length=" + data.get("min_fragment_length", "ERROR") + "\n"
  cfg += "Maximum_Fragment_Length=" + data.get("max_fragment_length", "ERROR") + "\n"
  cfg += "Bowtie_Threads_Number=8" + "\n\n"
  
  cfg += "Mismatch_Probability=" + data.get("mismatch_probability", "ERROR") + "\n"
  cfg += "Minimum_Relative_Abundance=" + data.get("minimum_abundance", "ERROR") + "\n\n"
  
  cfg += "Bootstrap_Iteration_Number=" + data.get("bootstrap_iterations", "ERROR") + "\n\n"
  
  cfg += "Reconstruction_Selection=" + data.get("reconstruction_mode", "ERROR") + "\n"
  cfg += "Reconstruction_Cutoff_Abundance=" + data.get("cutoff_abundance", "ERROR") + "\n"
  cfg += "#Recostruction_Genome_Name=" + data.get("reconstruction_name", "ERROR") + "\n"
  cfg += "Minimum_Coverage_Length=" + data.get("min_coverage_length", "ERROR") + "\n"
  cfg += "Minimum_Average_Coverage_Depth=" + data.get("min_coverage_depth", "ERROR") + "\n\n"
  
  cfg += "#Filtering_Genome_Name=" + data.get("filter_name", "ERROR")
  
  return cfg
  
if __name__ == '__main__':
  pass
