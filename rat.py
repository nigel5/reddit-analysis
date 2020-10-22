import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()

df = pd.read_csv('pics_dump.csv')

df.info()

# Create a visualization
# sns.relplot(
#     data=tips,
#     x="total_bill", y="tip", col="time",
#     hue="smoker", style="smoker", size="size",
# )

# plt.show()