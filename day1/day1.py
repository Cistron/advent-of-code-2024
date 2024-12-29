# PART 1
#%%
import pandas as pd
# %%
df = pd.read_csv('input.csv', header=None, sep="   ")
# %%
for col in df.columns:
    df[col]=sorted(df[col])
# %%
df["difference"] = abs(df[1] - df[0])
# %%
df["difference"].sum()
# 2196996

# PART 2
# %%
count_lookup = df[1].value_counts().to_dict()
# the score for value from df[0] that does not appear in df[1] is 0
# %%
df["smiliarity_score"] = df[0].apply(lambda x: x*count_lookup.get(x, 0))
# %%
df["smiliarity_score"].sum()
# 23655822
