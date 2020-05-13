# Python port of Nicolas' regex searching R script
# Rick Sear, May 2020

import re, csv, datetime
import janitor as j
import pandas as pd
import numpy as np

# List of CSV files to be searched
csv_files = [
    "filepaths to CSV files here"
]

# Terms to search for
regex_find = [
    "Johnson|Neil ((F|Fraser) )?Johnson|Nicol(a|á)s Vel[[:alpha:]]squez|Nicholas ((J|Johnson) )?Restrepo|Rhys Leahy|(Nicholas|Nick) Gabriel|Sara El( |-)?Oud|Minzhang Zheng|Pedro Manrique|Stefan Wuchty|Yon(atan)? Lupu|Richard Sear",
    "online.{,20}competition.{,60}(vaccin|vax)",
    "George Washington University|\\<GWU\\>|\\<GW\\>|IDDP|Data...Democracy...Politics",
    "https://www.nature.com/articles/d41586-020-01423-4",
    "https://www.nature.com/articles/s41586-020-2281-1",
    "https://ieeexplore.ieee.org/document/9091126",
    "https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9091126",
    "https://doi.org/10.1109/ACCESS.2020.2993967",
]

# Terms that indicate false positive
regex_ignore = ["Boris Johnson|Ron Johnson"]


def run_regex_search(csv_file, output_file, regex_true, regex_false):
    df = pd.read_csv(csv_file, encoding="utf8", dtype=str)
    df = j.clean_names(df)

    # Rename some columns
    df = df.rename(columns={"fb_uid": "facebook_id", "created_at": "created"})

    # In R code, here there is a filter function for an "average" line, but I didn't see one in the CSV CrowdTangle export

    # Convert all numbers to 64-bit ints
    df = df.astype("int64", errors="ignore")

    # Reformat creation time
    df["created"] = pd.to_datetime(df["created"])
    df["created"] = df["created"].dt.strftime(r"%Y/%m/%d_%H%M%S")

    # Obtain post ID
    df["post_id"] = df["url"].replace(
        regex="^http.*facebook.com[/][/ -~/]+[/]posts[/]", value=""
    )

    # Note current time of analysis
    df["FHCaptura"] = datetime.datetime.now()

    # Remove duplicate posts
    df = df.drop_duplicates(subset="post_id", keep="first")

    # Ensure final link is actually a link
    df["final_link"] = np.where(df["final_link"].isnull(), df["link"], df["final_link"])

    # There should be no "NaN"s in the final output
    df = df.fillna("")

    df["compiled_text"] = (
        df["message"]
        + " "
        + df["description"]
        + " "
        + df["link_text"]
        + " "
        + df["image_text"]
    )

    # Throw out anything that doesn't contain a term in "regex_true"
    contains_terms = df["compiled_text"].str.contains(regex_true)
    df = df[contains_terms]
    
    # Throw out anything that contains a term in "regex_false"
    false_positives = df["compiled_text"].str.contains(regex_false)
    df = df[~false_positives]

    df = df.sort_values(by=["page_name"])
    df.to_csv(output_file, sep="\t", index=False)


if __name__ == "__main__":
    regex_find_concat = "|".join(regex_find)
    regex_ignore_concat = "|".join(regex_ignore)

    for path in csv_files:
        run_regex_search(
            path, path + ".regex_filter.tsv", regex_find_concat, regex_ignore_concat
        )
