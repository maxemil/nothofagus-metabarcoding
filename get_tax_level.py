import ete3
import glob
import os
import pandas as pd
from collections import defaultdict, Counter
# from skbio.diversity.alpha import shannon
import math 

ncbi = ete3.NCBITaxa()

tax_level = 'genus'
min_reads = 10

rhizophagus_tax = 'NCBI; cellular organisms; Eukaryota; Opisthokonta; Fungi; Fungi incertae sedis; Mucoromycota; Glomeromycotina; Glomeromycetes; Glomerales; Glomeraceae; Rhizophagus;'
def parse_tax_c2c(file):
    taxa = Counter()
    for line in open(file):
        line = line.strip().split('\t')
        if 'Rhizophagus' in line[0]:
            line[0] = rhizophagus_tax
        for t in line[0].split('; '):
            t = t.strip(';')
            try:
                tid = ncbi.get_name_translator([t])[t]
                if ncbi.get_rank(tid)[tid[0]] == tax_level:
                    taxa[t] += int(float(line[1]))
            except:
                pass
    return taxa

sample2counts = {}
for f in glob.glob("maltout/*.c2c"):
    sample = os.path.basename(f).split('_')[1]
    sample2counts[sample] = parse_tax_c2c(f)

taxdf = pd.DataFrame.from_dict(sample2counts).fillna(0)
taxdf = taxdf.sort_index(axis=1)
taxdf = taxdf.loc[taxdf.sum(axis=1).sort_values(ascending=False).index]
taxdf.to_csv("Nothofagus_all_counts_{}.csv".format(tax_level), sep='\t', index_label='plot')

# get summary stats for tax_level
(taxdf > 0).sum(axis=0).describe()

sdf = pd.read_csv('sample_ids.csv', sep='\t', header=None, index_col=0)
sdf.columns = ['plot']

taxdf.columns = pd.Series(taxdf.columns).apply(lambda x: "sample_{}".format(x))

# sdf.index = sdf['sample']
# sdf.drop('sample', axis=1)

taxdf_group = taxdf.groupby(sdf['plot'],axis=1).sum()
# get summary stats for tax_level
(taxdf_group > 0).sum(axis=0).describe()
taxdf_group.to_csv("Nothofagus_plots_counts_{}.csv".format(tax_level), sep='\t', index_label='plot')

# 
# p_tab = {}
# for p in plots:
#     fsample = [f for f in fallopia if p in f][0]
#     bsample = [f for f in begleit if p in f][0]
#     # print(fsample, bsample)
#     frich = (taxdf[fsample] >= min_reads).sum()
#     brich = (taxdf[bsample] >= min_reads).sum()
#     overlap = ((taxdf[bsample] >= min_reads) & (taxdf[fsample] >= min_reads)).sum()
#     fdiv = shannon(taxdf.loc[(taxdf[fsample] >= min_reads), fsample], base=math.e)
#     bdiv = shannon(taxdf.loc[(taxdf[bsample] >= min_reads), bsample], base=math.e)
#     p_tab[p] = {'Fallopia richness':frich, 'Begleit richmess':brich, 
#                 'Overlap':overlap, 'Fallopia shannon':fdiv, 
#                 'Begleit shannon':bdiv}
# 
# p_tab = pd.DataFrame.from_dict(p_tab).T
# p_tab.to_csv('Fallopia_tax_results_{}_min{}.tsv'.format(tax_level, min_reads), 
#             sep='\t', index_label='plot')    
# 
# clean_orders = defaultdict(int)
# for k, v in orders.items():
#     if v > 20:
#         clean_orders[k] = v
# len(clean_orders)
