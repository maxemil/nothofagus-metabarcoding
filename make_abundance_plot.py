import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm

tax_level = 'order'

df = pd.read_csv("Nothofagus_plots_counts_{}.csv".format(tax_level), 
                sep='\t', index_col=0)

df = df/df.sum()
df_min = df[(df.sum(axis=1) > 0.1)]
df_min.loc['Other'] = df[(df.sum(axis=1) <= 0.1)].sum()
df_min = df_min*100

df_min.to_excel('Fungal_orders_Nothofagus.xlsx', header=True, index=True)

colors = sns.color_palette("hls", df_min.shape[0]-1)
colors.append('gray')
ccolors = cm.colors.ListedColormap(colors)


fig, ax = plt.subplots(figsize=(12,8))
df_min.T.plot(ax=ax, kind='bar', stacked=True, cmap=ccolors)
ax.set_ylabel("Relative abundance [%]")
ax.set_xlabel("Plots")
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.tight_layout()
# plt.show()
plt.savefig('Fungal_orders_Nothofagus.pdf')
