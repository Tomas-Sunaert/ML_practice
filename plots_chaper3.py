import numpy as np
import plotly.graph_objects as go

p = np.arange(0,1,0.1)
c =2 
gini = np.zeros(len(p))
for x in range(c):
    gini += p*(1-p)
entropy = np.zeros(len(p))
for x in range(c):
    entropy += -p*np.log2(p)

fig = go.Figure()
fig.add_trace(go.Scatter(x= p, y= gini, mode = 'lines'))
fig.add_trace(go.Scatter(x=p,y=entropy,mode  ='lines'))
fig.show()
print(entropy, gini)