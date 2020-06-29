import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("res.csv")
df['wmean'] = df.loc[:,'t2':'t10'].mean(axis=1)
df['min'] = df.loc[:,'t2':'t10'].min(axis=1)
df['warmup'] = df.loc[:,'t1':'t10'].max(axis=1)

grouped = df.groupby('library')
groups = [grouped.get_group(x).reset_index(drop=True) for x in grouped.groups]

cupy = groups[0]
dr = groups[1]
numpy = groups[2]

numpy['np_speedup'] = 1.0
dr['np_speedup'] = numpy['wmean'] / dr['wmean']
cupy['np_speedup'] = numpy['wmean'] / cupy['wmean']
dr['cupy_speedup'] = cupy['wmean'] / dr['wmean']

comb = pd.concat([cupy,numpy,dr]).reset_index(drop=True).sort_values(by=['benchmark','library'])

sns.set(palette='colorblind')
ax = sns.barplot(x='benchmark', y='np_speedup', hue='library', data=comb)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45,
    horizontalalignment='right')
plt.savefig('speedup.png')

comb.to_latex('results.tex', columns=['benchmark', 'library', 'wmean', 'np_speedup'],
    index=False, header=['Benchmark', 'Library', 'Mean execution time (s)',
    'Speedup'])

