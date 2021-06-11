#!/usr/bin/env python
# coding: utf-8

# **Project Goal**
# 
# **Perfom market research based on open source data on restaurant in LOS Angelos in order to commence small cafe with robotic waiters.**

# ## Step 1. Download the data and prepare it for analysis

# In[1]:


import pandas as pd

import datetime as dt
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns


# In[2]:


import sys
import warnings
if not sys.warnoptions:
       warnings.simplefilter("ignore")


# In[3]:


pip install -U seaborn


# In[4]:


rest_la= pd.read_csv('/datasets/rest_data_us.csv')


# In[5]:


rest_la.head(10)


# In[6]:


rest_la.isnull().sum()


# In[7]:


rest_la=rest_la.dropna()


# Missing values can be dropped as they are very small in numbers

# In[8]:


rest_la.info()


# In[9]:


rest_la[rest_la.duplicated()].count()


# No duplicated data

# In[10]:


rest_la= rest_la.dropna()


# In[11]:


rest_la.info()


# While data preparation only 3 missing values are found and there are no duplicated data. So, missing values are dropped.

# ## Step 2. Data analysis

# ### Investigate the proportions of the various types of establishments. Plot a graph. 

# In[12]:


plt.figure(figsize=(12, 8)) # Note! Write this code before you create the graph
#proportion=rest_la.groupby('object_type')['id'].nunique()
proportion= rest_la.groupby('object_type', as_index= False)['id'].count()
proportion= proportion.sort_values('id', ascending= False)
total= proportion['id'].sum()
proportion['id']= proportion['id']/total

ax = sns.barplot(x='object_type', y='id', data=proportion); 
for i in ax.patches:
    # get_x pulls left or right; get_height pushes up or down
    ax.text(i.get_x()+.04, i.get_height()+0.01,             str(round((i.get_height()), 2)), fontsize=11, color='#010fae', rotation=0)
ax.set_title('proportions of the various types of establishments');



# Resturant shares the by far the highest propertion of resturant business as they offer wide varierty of food and provide comfortable
# conditions to sit and meet in groups.

# ### Investigate the proportions of chain and nonchain establishments. Plot a graph. 

# In[13]:


plt.figure(figsize=(12, 8)) # Note! Write this code before you create the graph
proportion1= rest_la.groupby('chain', as_index= False)['id'].count()
proportion= proportion.sort_values('id', ascending= False)
proportion1['id']= proportion1['id']/proportion1['id'].sum()
ax = sns.barplot(x='chain', y='id', data=proportion1); 
for i in ax.patches:
    # get_x pulls left or right; get_height pushes up or down
    ax.text(i.get_x()+.04, i.get_height()+0.01,             str(round((i.get_height()), 2)), fontsize=11, color='#010fae', rotation=0)

ax.set_title('proportions of chain and nonchain establishments'); 


# In[14]:


sns.set(style="darkgrid")
ax= sns.displot(data=rest_la, x="object_type", hue="chain", multiple="stack")
plt.grid()

plt.xticks(rotation = 90)

plt.title('proportions of chain and nonchain establishments');


# In[15]:


#fig = px.bar(rest_la, x='object_type', y='number', color='chain', title='proportions of chain and nonchain establishments')
#fig.update_xaxes(tickangle=45)
#colors = {'True':'red',          'False':'green'}
#fig.show() 


# Bar and resturant chain are in less than  50 % of their type whereas, all Bakeries are in chain. Likewise, Cafe, Pizza resturant and Fast food
# resturants having in chain are in atleast  50 % of their type.

# ### Which type of establishment is typically a chain? 

# In[16]:



plt.figure(figsize=(12, 8)) # Note! Write this code before you create the graph
proportion1= rest_la.groupby(['object_type','chain'], as_index= False)['id'].count()
proportion= proportion.sort_values(['object_type','id'], ascending= [False, False])
proportion1['id']= proportion1['id']/proportion1['id'].sum()
ax = sns.barplot(x='object_type', y='id', hue='chain', data=proportion1); 
for i in ax.patches:
    # get_x pulls left or right; get_height pushes up or down
    ax.text(i.get_x()+.04, i.get_height()+0.01,             str(round((i.get_height()), 2)), fontsize=11, color='#010fae', rotation=0)

ax.set_title('proportions of chain and nonchain establishments'); 
plt.grid();


# Except Bakery all other types of establishment are of both types ( having chain or not having chain). So, backery are typical chain
#  establisment

# ### What characterizes chains: many establishments with a small number of seats or a few establishments with a lot of seats? 

# In[17]:


chains=rest_la[rest_la['chain']==True]
no_chains=rest_la[rest_la['chain']==False]


x_values = pd.Series(range(0, len(chains['chain'])))
x_values1 = pd.Series(range(0, len(no_chains['chain'])))
plt.scatter(x_values, chains['number'], c='red', alpha= 0.3) 
plt.scatter(x_values1, no_chains['number'], c='blue', alpha=0.3) 



plt.xlabel('establishments');
plt.ylabel('no of seats');
plt.title('Number of seats per establishment( blue--> no chain, red--> chains)');


# > Chains are characterized by few establishment with lot of seats

# ### Determine the average number of seats for each type of restaurant. On average, which type of restaurant has the greatest number of seats? Plot graphs.
# 

# In[18]:


seats_avg= rest_la.groupby('object_type', as_index= False)['number'].mean()
seats_avg= seats_avg.sort_values('number', ascending= False)





ax = sns.barplot(x='object_type', y='number', data=seats_avg); 
for i in ax.patches:
    # get_x pulls left or right; get_height pushes up or down
    ax.text(i.get_x()+.04, i.get_height()+1,             str(round((i.get_height()), 2)), fontsize=11, color='#010fae', rotation=0)



ax.set_title('Determine the average number of seats for each type of restaurant');


# > **_Resturants_** have greatest number of seats  on average at about _48_ closely followed by **_bars_** at _45_. Likewise, **_fast food_** and
# **_pizza stores_** have about _32_ and _29_ seats on average, respectively. **_Cafe_** and  **_Bakery_** on the other hand have about _25_ and _22_ seats on average.

# In[19]:


plt.figure(figsize=(12, 8)) # Note! Write this code before you create the graph
seats= rest_la.groupby(['object_type','chain'], as_index= False)['number'].mean()
seats1= seats.sort_values(['number','object_type'], ascending= [False, False])

ax = sns.barplot(x='object_type', y='number', hue='chain', data=seats1); 
for i in ax.patches:
    # get_x pulls left or right; get_height pushes up or down
    ax.text(i.get_x()+.04, i.get_height()+0.01,             str(round((i.get_height()), 2)), fontsize=11, color='#010fae', rotation=0);

ax.set_title('proportions of chain and nonchain establishments'); 
plt.grid();


# Average number of seats on chain and non-chain estalishment vary nominally from average number of seats on average in overall.
# the maximum deviation can be seen in fast food (to about 24 and 38 from about 32.)

# ### Put the data on street names from the address column in a separate column.
# 

# In[20]:





rest_la['street_name'] = rest_la['address'].str.split("#", 1, expand=True)[0]
rest_la['street_name'] = rest_la['street_name'].str.replace('\d+', '')

print(rest_la.sample(5))


# ### Plot a graph of the top ten streets by number of restaurants.
# 

# In[21]:


streets= rest_la.groupby('street_name', as_index= False)['object_name'].count().sort_values('object_name', ascending= False)
top10_streets= streets.iloc[0:10, :]
top10_streets.columns=['street_name', 'resturants_number']
top10_streets.head()


# In[22]:


ax = sns.barplot(x='street_name', y='resturants_number', data=top10_streets); 
for i in ax.patches:
    # get_x pulls left or right; get_height pushes up or down
    ax.text(i.get_x(), i.get_height()+2,             str(i.get_height()), fontsize=11, color='#010fae', rotation=45)



ax.set_title('top ten streets by number of restaurants');
plt.xticks(rotation = 300);
plt.grid();


# W TH ST (323), W SUNSET BLVD (296) and W PICO BLVD (288) are top three streets based on number of resturants. Each of them have almost double resturants compared to 
# other streets on top ten list individually. These street should be major street near the city center where most of shopping malls and
# offices are located.

# ### Find the number of streets that only have one restaurant.
# 

# In[23]:


print('The number of streets that have only one resturant: {}'.format(streets[streets['object_name']== 1]['street_name'].count()))


# This indicates LA have large number of less dense neighbourhood.

# ### For streets with a lot of restaurants, look at the distribution of the number of seats. What trends can you see?
# 

# In[24]:


#cumulativeData = top10_streets.merge(rest_la, on='street_name', how= inner)

cumulativeData = pd.merge(top10_streets, rest_la, left_on='street_name', right_on='street_name')
cumulativeData.head()


# In[25]:


Cafe_street= cumulativeData[cumulativeData['object_type']=='Cafe']
Cafe_street = Cafe_street.rename(columns={'number': 'number_of_ seats'})
ax= sns.barplot(data=Cafe_street, x="street_name", y="number_of_ seats");
for i in ax.patches:
    # get_x pulls left or right; get_height pushes up or down
    ax.text(i.get_x()+0.31, i.get_height()+7,             str((i.get_height()).round()), fontsize=11, color='#010fae', rotation=45);
ax.set_title('Average number of seats in Cafes in popular streets');
plt.xticks(rotation = 90);
plt.grid();


# Among popular street the size of cafe do not vary significantly as can be seen in bar diagram.

# In[26]:



ax= sns.barplot(data=Cafe_street, x="street_name", y="number_of_ seats", hue='chain');
for i in ax.patches:
    # get_x pulls left or right; get_height pushes up or down
    ax.text(i.get_x()+0.31, i.get_height()+7,             str((i.get_height()).round()), fontsize=11, color='#010fae', rotation=45);
ax.set_title('Average number of seats in Cafes in popular streets');
plt.xticks(rotation = 90);
plt.grid();


# In santa monica and Hollywood BlVD the average number of seats are by far highest (at 31 and 30) for chain type and non-chain cafe.

# In[27]:


no_Cafe_streets= Cafe_street.groupby('street_name', as_index= False)['object_type'].count().sort_values('object_type', ascending= False)


# In[28]:


cafe_previous_order = pd.merge(top10_streets, no_Cafe_streets, left_on='street_name', right_on='street_name')
ax= sns.barplot(data=cafe_previous_order, x="street_name", y="object_type");
for i in ax.patches:
    # get_x pulls left or right; get_height pushes up or down
    ax.text(i.get_x()+0.31, i.get_height()+1,             str((i.get_height()).round()), fontsize=11, color='#010fae', rotation=45);
ax.set_title('Average number of Cafes in popular streets');
plt.xticks(rotation = 90);
plt.grid();


# >As W sunset BLVD have highest number of cafes with highest average size. Chain Cafes on that streets are slightly bigger
# indicates their popularity. Introducing new cafe with new service would attract people.
# 
# >santa monica and Hollywood BlVD streets had highest number of seats in (at 31 and 30) for chain type and non-chain cafes respectively but these
# streets have not highest number of cafes. There are some big cafes because of slightly lower number of cafes.
# 

# In[29]:


plt.figure(figsize=(20, 16));
cumulativeData1=cumulativeData[['street_name','object_type', 'number']]
ax = sns.distplot(cumulativeData1['number']) 


# The distribution for number of seats is skewed towards positive side

# In[30]:


plt.figure(figsize=(18, 16));
ax= sns.displot(data=cumulativeData1, x="number", hue="object_type", multiple="stack");


# > Most of establishments less than 50 seats on average. The skewness in earlier figure seems to be due to some large resturants
# with few number of bigger Bars and fast food shop.

# In[31]:


plt.figure(figsize=(12, 8));
sns.scatterplot(data=cumulativeData, x="id", y="number", hue="object_type");


# Mostly, resturants are of bigger size than 50 seats

# In[32]:


bigger_estb= cumulativeData[cumulativeData['number']>50]
plt.figure(figsize=(6, 6));
#ax= sns.displot(data=bigger_estb, x="number", hue="object_type", multiple="stack");

number_estb= bigger_estb.groupby('object_type', as_index= False)['number'].count()
number_estb= number_estb.sort_values('number', ascending= False)





ax = sns.barplot(x='object_type', y='number', data=number_estb); 
plt.xticks(rotation = 90);
for i in ax.patches:
    # get_x pulls left or right; get_height pushes up or down
    ax.text(i.get_x()+.04, i.get_height()+1,             str(round((i.get_height()), 2)), fontsize=11, color='#010fae', rotation=0)



ax.set_title('Number establishment with  seats more than 50');


# This figure illustrates the same fact obtained in previous figures with more clarity. Most of the bigger establishment are resturnts with few fast food and Bar.
# Other type of bigger establishments are very rare. The type of our intrest ('Cafe'), has only one cafe with bigger size.

# **Conclusion**
# Restaurants made up largest share of establishment in Los Angeles (75% ) and they have highest number of average seats.
# More than 2000 restaurants and about 500 fast food belong to chain.
# 
# Fast food shop also have about 32 seats on average.
# 
# 
# Top ten streets based on number of establishment have about 130 to 325 establishments.
# 
# About one third of restaurants belong to chain restaurants. 
# 
# 
# Introducing robot would save huge expenditure as they will replace waiters. No, need of double shift waiters specially when it is small café.
# Existing cafes are small in size (25 seats on average) compared to other types of establishment except bakery. Competition will not be that tough.
# About 40% of cafes do not belong to any chain.
# Only 5 % of establishments are cafes.
# Famous streets are accommodating unto  more than 300 establishment indicates establishment can survive on these streets.
# 

# >Establishing café with robotic waiter on Los Angeles could be good ideas as LA have streets that can accommodate number of cafes. Cafes are very less in numbers and small in size where there are already huge restaurants and bar in very large numbers.
# 

# >As **W sunset BLVD** street have highest number of cafes with highest average size. Chain Cafes on that streets are slightly bigger than non-chain indicates their popularity. Introducing one more chain-cafe with new service on that streetwould attract customers.
# 

# ## Step 3. Preparing a presentation
# 

# Presentation: <https://www.dropbox.com/s/j71ojpmnbszikcq/Restaurant%20market%20research%20on%20Los%20Angelos.pdf?dl=0>

# In[ ]:




