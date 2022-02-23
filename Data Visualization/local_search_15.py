
import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns 



df = pd.read_csv("Dissertation Iterated Local Search 15 mins  - 250a.csv")

#df["Solution Space"] = df["Solution Space"].map(mult)
#plt.figure(figsize=(15,8))
sns.lineplot(x="Solution Space",y="Local Optima",data = df,color ='black').set_title("Fig.6")

plt.savefig('engagement_sentiment_scatter_apparel.png')
#creates a scatterplot of engagement against sentiment with brandCategory apparel only 
"""
plt.clf()
dfn_a = dfn[( dfn.brandCategory=="apparel")] 
sns.scatterplot(x="sentiment",y="engagement",data = dfn_a[['sentiment','engagement','brandCategory']],hue="brandCategory",palette =["green"] ,alpha = 0.3).set_title("Fig.6")
plt.savefig('engagement_sentiment_scatter_apparel.png')

"""