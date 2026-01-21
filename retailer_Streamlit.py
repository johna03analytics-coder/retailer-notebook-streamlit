
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


retail_df= pd.read_csv("retail_sales_dataset.csv") # importing dataset
st.title("Welcome to Retailer Details!", text_alignment="center")


# setting all details ahead of time to avoid contingency errors
retail_df["Date"] = pd.to_datetime(retail_df.Date, format='%Y-%m-%d')
retail_df.set_index("Transaction ID", inplace=True)


# time to see some actually useful info
# lets see what age shops the most overrall at this retailer
st.subheader("Range of ages that shop at This Retailer")
st.dataframe(retail_df.Age.value_counts().head(10), width=300) # the dataset shows that the age group that buys most frequently mostly is between 50s ands 60s

# lets find out the top ten best selling days for this retailer in this dataset
top_ten_rev = retail_df.groupby("Date").agg({
    "Total Amount" : "sum"
}).sort_values(by="Total Amount", ascending=False).head(10)
st.write("These are the top ten best selling days recorded")
st.dataframe(top_ten_rev, width=400)


# okay lets do some visualization
# first lets see the sales over the recorded dataset
st.header("Let's see the recorded sales over the past year below: ")
fig, ax = plt.subplots(figsize=(12, 8))
sns.lineplot(x="Date", y="Total Amount", data=retail_df, color="black")

plt.xlabel("Date")
plt.ylabel("Total Amount")
plt.title("Total Amount over Time")
st.pyplot(fig)



st.write("We can see that this retailer's sales suggest that this retailer has a continous cycle of low sales and high values with outliers skewed toward the lower end.\nHowever, I'd like to prove that next below")

fig, ax = plt.subplots(figsize=(12, 8))
sales_distribution = sns.kdeplot(x="Total Amount", data=retail_df, fill=True, color="green", cut=0)
plt.ylim(bottom=0)

plt.xlabel("Total Amount")
plt.ylabel("Count")
plt.title("Total Amount Distribution")
st.pyplot(fig)

st.write("""As we can see, the distribution of sales leans heavily toward the lower end of the total amount. 
We can conclude that this retailer's sales rely on high quantity, low price over high price, low quantity.\n 
This leads me to believe that it should focus on advertising its cheaper options creating more revenue.""")

st.subheader("Lets see which category has the most quantity sold below:")
product_quant = retail_df.groupby("Product Category").agg({
"Quantity" : "sum"
}).sort_values(by="Quantity", ascending=False)
st.dataframe(product_quant)
st.write("As expected, clothing dominates but surprisingly electronics isn't far behind with beauty contributing least.\n"
         "Let's visualize that though.")
fig, ax = plt.subplots(figsize=(8, 6))
category_graph = sns.barplot(x=product_quant.index, y="Quantity", data=product_quant, hue="Product Category", ax=ax)
for container in ax.containers:
    ax.bar_label(container)
plt.xlabel("Product Category")
plt.ylabel("Quantity")
plt.title("Product Quantity Count versus Product Category")
st.pyplot(fig)
st.write("Clothing leads the way with Beauty being the least.\n This retailer's highest selling product remains its clothing")

st.write("Let's find out which gender spends more in each category on average.")

total_avg_gend = retail_df.groupby(["Product Category", "Gender"]).agg({
    "Total Amount" : "mean"
}).round(2)
st.dataframe(total_avg_gend, width=700)
st.write("Men spend more on average for beauty items."
         "Women spend far more on average on clothing while men take the lead once again in electronics.")

# lets visualize that.
total_avg_gend.reset_index(inplace=True) # to make data manipulation easier

fig, ax = plt.subplots(figsize=(12, 8)) # setting the size
color_list = ["#fc5a03", "#fc0341"] # getting a list of colors for the palette

category_avg = sns.barplot(x="Product Category", y="Total Amount", data=total_avg_gend, hue="Gender", ax=ax, palette=color_list)
for container in ax.containers:
    ax.bar_label(container) # to set labels efficiently and increase graph transparency
plt.xlabel("Product Category")
plt.ylabel("Total Amount")
plt.title("Total Amount on Average per Gender")
st.pyplot(fig)
st.write("Men and women share an equal standing in expenses with each gender showing towards particular product category as opposed to a single skewed view.")

st.subheader("In conclusion: ")
st.write("""
This retailer's sales fluctuate regularly but their highest selling quantities remain in their cheap items. These cheap items are often bought in bulk allowing for a higher return on investment.
Despite clothing being a large seller, they have electronics to support their sales targets with enough of a male and female demographic to continue successfully. 
""")