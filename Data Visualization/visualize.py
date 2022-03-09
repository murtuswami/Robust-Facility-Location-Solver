
import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns 
from matplotlib import rc 

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)


df = pd.read_csv("Dissertation Iterated Local Search 15 mins  - 250a.csv")

"""
sns.lineplot(x="Solution Space",y="Local Optima",data = df,color ='black').set_title("Fig.6")

plt.savefig('local_search_15')
plt.clf()


dfn_a = dfn[( dfn.brandCategory=="apparel")] 
sns.scatterplot(x="sentiment",y="engagement",data = dfn_a[['sentiment','engagement','brandCategory']],hue="brandCategory",palette =["green"] ,alpha = 0.3).set_title("Fig.6")
plt.savefig('engagement_sentiment_scatter_apparel.png')

"""
df = pd.read_csv("Dissertation 111EuclS worst case realizations -  5.csv")
lp = sns.scatterplot(data = df)
lp.set(ylim=(96116, 114000))
plt.savefig("wc_5")

plt.clf()
df = pd.read_csv("Dissertation 111EuclS worst case realizations -  50.csv")
lp = sns.scatterplot(data = df)
lp.set(ylim=(96116, 273228.697))
plt.savefig("wc_50")

