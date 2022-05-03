"""
Based on Jarrod Blinch's 2014 blog tutorial on Cousineau-Morey confidence intervals,
I coded this Python implementation to aid my own learning on the topic.
"""
__author__ = "Link Swanson"

from math import sqrt

import argparse
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

# Blinch's example tutorial:
url = "https://motorbehaviour.wordpress.com/2014/10/31/confidence-intervals-in-within-participant-design-a-tutorial-on-the-cousineau-morey-method/"
print(f"Read the tutorial: \n{url}")

# Allow example data to be overridden with data from a CSV file.
parser = argparse.ArgumentParser(
    description="Calculates and plots Cousineau-Morey confidence intervals for a given data set."
)
parser.add_argument(
    "--datafile",
    type=str,
    help="Path to custom data in .tsv or .csv format. See example data for format requirements.",
)
parser.add_argument(
    "--ylabel",
    type=str,
    help="String to use to label the y axis of given data set.",
)
args = parser.parse_args()

if args.datafile:
    # Import the CSV data file into a pandas DataFrame.
    # Refer to the table in the blog entry to understand 
    # the required data format when using custom data files.
    sep = ","
    if args.datafile.endswith(".tsv"):
        sep = "\t"
    df = pd.read_csv(
        args.datafile,
        sep=sep,
        index_col=0,
    )
    ylabel = f"{args.ylabel if args.ylabel else 'measurement'}"
else:
    # We use the example data from the tutorial if no file path provided.
    ylabel = "Reaction time (ms)"
    example_data = {
        1: {"A1": 241, "A2": 178, "B1": 253, "B2": 215},
        2: {"A1": 209, "A2": 236, "B1": 306, "B2": 344},
        3: {"A1": 211, "A2": 170, "B1": 462, "B2": 521},
        4: {"A1": 167, "A2": 155, "B1": 204, "B2": 204},
        5: {"A1": 190, "A2": 166, "B1": 225, "B2": 271},
        6: {"A1": 207, "A2": 189, "B1": 276, "B2": 281},
        7: {"A1": 163, "A2": 157, "B1": 231, "B2": 266},
        8: {"A1": 172, "A2": 149, "B1": 284, "B2": 251},
        9: {"A1": 171, "A2": 174, "B1": 199, "B2": 263},
        10: {"A1": 187, "A2": 196, "B1": 196, "B2": 207},
        11: {"A1": 181, "A2": 204, "B1": 192, "B2": 244},
        12: {"A1": 164, "A2": 171, "B1": 250, "B2": 268},
        13: {"A1": 139, "A2": 139, "B1": 181, "B2": 191},
        14: {"A1": 153, "A2": 138, "B1": 175, "B2": 198},
        15: {"A1": 165, "A2": 169, "B1": 209, "B2": 245},
        16: {"A1": 158, "A2": 174, "B1": 204, "B2": 229},
        17: {"A1": 199, "A2": 207, "B1": 294, "B2": 292},
        18: {"A1": 180, "A2": 188, "B1": 215, "B2": 262},
    }
    df = pd.DataFrame(example_data).T

# Add a mean column to the dataframe.
df["participant_mean"] = df.mean(axis=1)
# Show the data.
print("Example dataset from the tutorial:")
print(df)
# Calculate mean and sd for each column in the dataframe.
df_totals = df.describe()
print(df_totals.loc[["mean", "std"]].round(2))

# Calculate the 95% confidence interval for the grand mean
# using the 'typical' formula:
# CI = Mean +/- t(1-alpha/2, n-1) * SD / sqrt(n)
# ==============================================
n = len(df.index)
print(f"n = {n}")
# calculate tα/2 (a t-score corresponding to right-tailed area of α/2).
t_a2 = stats.t.ppf(1 - 0.05 / 2, n - 1)
print(f"tα/2 = {t_a2}")
# get the Mean from pandas.
grand_mean = df_totals.at["mean", "participant_mean"]
print(f"grand_mean = {grand_mean}")
# get the SD from pandas.
sd = df_totals.at["std", "participant_mean"]
print(f"sd = {sd}")
# calculate square root of n.
print(f"sqrt_n = {sqrt(n)}")
# calculate the confidence interval.
ci = t_a2 * sd / sqrt(n)
print(f"ci = {ci}")
print(
    "95% confidence intervals for the grand mean using the typical formula: \nCI = Mean +/- t(1-alpha/2, n-1) * SD / sqrt(n)"
)
# Show the +/- ci pair for the grand mean.
print([grand_mean - ci, grand_mean + ci])

# Calculate the typical 95% confidence intervals for the four conditions.
# The conditions in the 2×2 experiment are simply labeled A1, A2, B1, and B2.
# These typical confidence intervals will include the between- and within-participant variance.
# =======================================================================

print("Typical 95% CI pairs for each condition:")


def getTypicalCi(row: pd.Series) -> float:
    """Calculates typical 95% confidence interval."""
    t_a2 = stats.t.ppf(1 - 0.05 / 2, n - 1)
    ci = t_a2 * row["std"] / sqrt(n)

    # Show typical CI for each condition.
    print(f"{row.name}: {[row['mean'] - ci, row['mean'] + ci]}")

    return ci


# Get a df.describe() with transposed index and columns (T is for 'transposed').
df_stats = df.drop(["participant_mean"], axis=1).describe().T[["mean", "std"]]
# Add a column for the 'typical' 95% confidence interval, using our function.
df_stats["typical_ci"] = df_stats.apply(getTypicalCi, axis=1)
print(df_stats)

# Create a set of plots
fig, axes = plt.subplots(2, 2, figsize=(18, 10))
df_stats.drop(["std"], axis=1).plot(
    ax=axes[0, 1],
    kind="bar",
    yerr="typical_ci",
    capsize=4,
    title="Means and typical 95% CIs",
    ylabel=ylabel,
    xlabel="condition",
    legend=False,
)

print('"Now the fun begins."')
# Before we do any normalisation, let’s take a look at all the data from the 18 participants.
# Below is a figure of the means in the four conditions (A1, A2, B1, B2) for each participant.
# Notice that some participant have shorter or longer reaction times than others.
# This is between-participant variance, and we are going to remove it to calculate the within-participant confidence intervals.
ax = (
    df.drop(["participant_mean"], axis=1)
    .T.plot(
        ax=axes[0, 0],
        title="Original means",
        ylabel=ylabel,
        xlabel="condition",
        style=".-",
    )
    .legend(bbox_to_anchor=(1, 1), borderaxespad=0)
)

# We can remove the between-participant variance with one simple step.
# Simply subtract each participant’s mean (the last column in the table above)
# from each of the four conditions (A1, A2, B1, B2).
df_normalized = df.subtract(df["participant_mean"], axis=0).drop(
    ["participant_mean"], axis=1
)

# This will balance each participant’s data around 0 ms.
print(f"Normalized data before adding the grand mean ({grand_mean}):")
print(df_normalized)

# We have now removed the between-participant variance and we could go ahead
# with calculating within-participant confidence intervals.
# However, these reaction times no longer make sense. To make the data appropriate
# for the conditions, simply add the grand mean to all the normalised means.

print(f"Normalized data after adding the grand mean ({grand_mean}):")
df_normalized = df_normalized.add(grand_mean, axis=0)
print(df_normalized)

# Show a plot of the normalized mean data.
ax = df_normalized.T.plot(
    ax=axes[1, 0],
    title="Original means - participant means + grand mean",
    ylabel=ylabel,
    xlabel="condition",
    style=".-",
).legend(bbox_to_anchor=(1, 1), borderaxespad=0)

df_stats = df_normalized.describe().T[["mean", "std"]]
print(df_stats.T.round(2))

# We can now calculate within-participant confidence intervals,
# but we need to make one change to the original formula (this is the Morey part of the Cousineau-Morey method).
# CI = Mean +/- t(1-alpha/2, n-1) * SD / sqrt(n) * sqrt(c / (c-1))
# The addition is sqrt(c / (c-1)), where c is the number of within-participant conditions.

c = len(df_stats.index)
print(f"c = {c}")
morey = sqrt(c / (c - 1))
print(f"morey = {morey}")

# In our 2×2 example, there are four conditions. Evaluating sqrt(4 / (4-1)) gives us 1.15,
# so this correction factor is going to make the confidence intervals slightly larger.
# Note that the largest increase in the confidence intervals would be with 2 within-participant conditions
# [sqrt(2 / (2-1)) = 1.41] and that this correction decreases with more conditions.


def getMoreyCi(row: pd.Series) -> float:
    """Calculates Cousineau-Morey 95% confidence interval."""
    t_a2 = stats.t.ppf(1 - 0.05 / 2, n - 1)
    ci = t_a2 * row["std"] / sqrt(n) * sqrt(c / (c - 1))
    print(f"{row.name}: {[row['mean'] - ci, row['mean'] + ci]}")
    return ci


# Let’s calculate the 95% confidence intervals for the normalised data using the CI formula with the correction factor.
# Add a column for the Cousineau-Morey 95% confidence interval, using our function.
df_stats["cm_ci"] = df_stats.apply(getMoreyCi, axis=1)

print(df_stats.round(2))

ax = df_stats.drop(["std"], axis=1).plot(
    ax=axes[1, 1],
    kind="bar",
    yerr="cm_ci",
    capsize=4,
    title="Means and 95% within-participant CIs",
    ylabel=ylabel,
    xlabel="condition",
    legend=False,
)

# Show all plots in one figure.
fig.tight_layout()
plt.show()

# If we are using the example data, we can finish the tutorial.
# If using custom data, we can't make assumptions about the 
# condition names, so we just stop here.
if not args.datafile:
    # Calculate the 95% within-participant confidence intervals for A vs. B
    # =====================================================================
    # We just calculated confidence intervals for the four conditions,
    # which assumes that there was a significant 2×2 interaction.
    # There could be, however, just a main effect of A (A1, A2) vs. B (B1, B2).
    # In this case, we would calculate confidence intervals for just A and B.

    # The process is very similar but you begin by calculating the mean
    # of A1 and A2 to get A and B1 and B2 to get B for each participant.

    df["A"] = df[["A1", "A2"]].mean(axis=1)
    df["B"] = df[["B1", "B2"]].mean(axis=1)
    df = df[["A", "B", "participant_mean"]]

    # Now that you have A and B, you can normalise the data
    # and then calculate the 95% within-participant confidence intervals.

    df_normalized = (
        df.subtract(df["participant_mean"], axis=0)
        .drop(["participant_mean"], axis=1)
        .add(grand_mean, axis=0)
    )

    print(f"Normalized data for A and B means:")
    print(df_normalized)

    df_stats = df_normalized.describe().T[["mean", "std"]]
    print(df_stats.T.round())

    print(f"Calculate confidence interval for A and B means:")
    c = len(df_stats.index)
    print(f"c = {c}")
    morey = sqrt(c / (c - 1))
    print(f"morey = {morey}")

    # Add a column for the Cousineau-Morey 95% confidence interval, using our function.
    df_stats["mc_ci"] = df_stats.apply(getMoreyCi, axis=1)

    print(df_stats.round(2))

print("Done.")