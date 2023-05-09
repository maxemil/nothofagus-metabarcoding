from Bio import SeqIO
from collections import defaultdict
import glob
import os
import pandas as pd

seqstats = defaultdict(lambda: {'raw':0, 'filtered':0, 'assembled':0, 
                                'chimera':0, '150bp':0})

for f in glob.glob('envio_01/raw_reads/*R1*'):
    sample = "_".join(os.path.basename(f).split('_')[0:2])
    seqstats[sample]['raw'] = len([rec.id for rec in SeqIO.parse(f, 'fastq')])

for f in glob.glob('envio_01/filtered_reads/*'):
    sample = "_".join(os.path.basename(f).split('_')[1:3])
    seqstats[sample]['filtered'] = len([rec.id for rec in SeqIO.parse(f, 'fastq')])

for f in glob.glob('assembled_reads/*'):
    sample = "_".join(os.path.basename(f).split('_')[0:2])
    seqstats[sample]['assembled'] = len([rec.id for rec in SeqIO.parse(f, 'fastq')])

for f in glob.glob('chimera_filtered/*150*'):
    sample = "_".join(os.path.basename(f).split('_')[0:2])
    seqstats[sample]['150bp'] = len([rec.id for rec in SeqIO.parse(f, 'fasta')])

for f in glob.glob('chimera_filtered/*nochimera*'):
    sample = "_".join(os.path.basename(f).split('_')[0:2])
    seqstats[sample]['chimera'] = len([rec.id for rec in SeqIO.parse(f, 'fasta')])


df = pd.DataFrame.from_dict(seqstats)
df = df.drop('sample_Ctrl-2', axis=1)
