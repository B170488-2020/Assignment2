# !/usr/bin/python
import subprocess
import os
# The first step of the detailed task
# Input the protein family name and taxonomic group name
pro_fam_name = input("Please type the aim protein family name, such like 'glucose-6-phosphatase' (the quotation marks is necessary) \n")+'[Protein name]'
tax_gro_name = input("Please type the aim taxonomic group name, such like 'Aves' (the quotation mark is necessary) \n")+'[Organism name]'
# Transform the input names into the search format of NCBI
search_name = pro_fam_name + ' AND ' + tax_gro_name
# Get the results of esearch in NCBI
os.system("esearch -db protein -query \"%s\" | efetch -format fasta > pro_seq.fasta" %(search_name))
# Control the number of sequences
seqs_number = os.system("grep -c '>' pro_seq.fasta")
while seqs_number > 1000:
	X1 = input('The number of sequences is over 1000, do you need show all? Y or N')
	if X1 == 'N' :
		exit()
	elif X1 == 'Y' :
		X2 = input('Are you sure? y or n?')
		if X2 == 'y' :
			break
		else :
			exit()
	else :
		continue

#tax_group 
import re
from collections import Counter

tax_group_open = open('pro_seq.fasta')
tax_group_read = tax_group_open.read()

tmp = tax_group_read

tax_group_names = re.findall('\[(.*?)\]', tmp)

tmp = Counter(tax_group_names)

tax_number = len(tmp)

with open('tax_names.txt', 'w') as n:
        n.write(str(tax_group_names))

print(tax_number)

answer = input('the number of taxonomic group is the below number, do you want to continue or read the detail?\ny or detail? Another words take the same value as y \n(all input with quotation marks, nacessary! please) \n')

if answer == 'detail':
        os.system('cat tax_names.txt')
        answer2 = input('\nWould you like to continue? y or n? \n')
        if answer2 == 'n':
                os.system('nano 1.py                   need refresh here!            ')


# The 2nd step of the detailed task
os.system('clustalo -i pro_seq.fasta -o align.fasta')
# 
os.system('cons align.fasta cons_seq.fasta')
#
os.system('makeblastdb -in pro_seq.fasta -input_type fasta -dbtype prot -title pro_db -out pro_db')
#
os.system('blastp -db pro_db -query cons_seq.fasta -out high_sim_seqs.blastp.out -max_target_seqs 250')
#
sim_seq_open = open('high_sim_seqs.blastp.out')
sim_seq_read = sim_seq_open.readlines()

sim_seq_list = []
sim_seq_name = []

for i in sim_seq_read:
	list = i.strip()
	sim_seq_list.append(list.split())
if seqs_number > 250:
	for k in range(279):
		if k >=29:
			sim_seq_name.append(sim_seq_list[k][0])
else :
	for k in range(seqs_number+29):
		if k >=29:
			sim_seq_name.append(sim_seq_list[k][0])

with open('names.txt', 'w') as n:
	n.write(str(sim_seq_name))
#pullseq
subprocess.call('./pullseq/pullseq -i pro_seq.fasta -n names.txt > final_seqs.fasta', shell=True)

#3
sim_seq_open = open('high_sim_seqs.blastp.out')
sim_seq_read = sim_seq_open.readlines()

sim_seq_list = []
sim_seq_name = []

if seqs_number > 250:
	for k in range(279):
		if k >=29:
			sim_seq_name.append(sim_seq_list[k][0])
else :
	for k in range(seqs_number+29):
		if k >=29:
			sim_seq_name.append(sim_seq_list[k][0])

with open('names.txt', 'w') as n:
	n.write(str(sim_seq_name))

subprocess.call('./pullseq/pullseq -i pro_seq.fasta -n names.txt > seqs_motif_base.fasta', shell=True)
os.system('patmatmotifs seqs_motif_base.fasta seqs_motif_process')

with open('seqs_motif_process', 'r') as s:
	tmp = s.readlines()

seqs_motif = []
for l in tmp:
	if 'Motif' in l:
		seqs_motif.append(l.strip())

motifs.loc[sim_seq_name, 'motif'] = str(seqs_motif)
motifs.to_csv('motifs.csv')

#4
os.system(pepstats pro_seq.fasta extra_information)







	



