
import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns 
from matplotlib import rc 


#rc('text', usetex=True)
#sns.set(font="serif")
sns.set_style("whitegrid")
sns.set_style({'font.family':'serif', 'font.serif':['Computer Modern']})



plt.clf()
df = pd.read_csv("Dissertation 111EuclS worst case realizations -  50.csv")
lp = sns.lineplot(data = df,color='black', x ="p" ,y = "wc realization",hue="Type")
plt.tight_layout()
plt.savefig("Fig.11_wcRealizations.png")
plt.clf()



df = pd.read_csv("vary_gamma.csv")
lp = sns.lineplot(data=df,x="gamma",y="robust solution",color='red')
lp.axhline(96116.0,linestyle='--',color='blue')
lp.axhline(113650.13999999997,linestyle='--',color='orange')
plt.tight_layout()
plt.legend(labels=["Varying Gamma","Lower Bound","Upper Bound"])
plt.savefig("Fig.13_varyGamma.png")
plt.clf()


