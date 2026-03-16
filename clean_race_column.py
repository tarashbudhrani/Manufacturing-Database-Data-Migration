"""
Strategy to clean the Race/Ethnicity column in employee datasets.

Problems observed in raw data:
  - Inconsistent naming: "Hispanic or Latino/a/x", "Black or African American"
  - Potential whitespace, casing variations
  - Possible null/missing values
  - Redundant suffixes like "/a/x" or long multi-word labels

Cleaning Strategy:
  1. Strip whitespace and normalize casing
  2. Map verbose/inconsistent labels to standardized short categories
  3. Handle nulls and unknown values
  4. Validate that all values map to known categories
"""

import pandas as pd


# Standardized race/ethnicity mapping
# Maps raw variations -> clean, consistent category
RACE_MAPPING = {
    # Hispanic / Latino
    "hispanic or latino/a/x": "Hispanic or Latino",
    "hispanic or latino": "Hispanic or Latino",
    "hispanic": "Hispanic or Latino",
    "latino": "Hispanic or Latino",
    "latina": "Hispanic or Latino",
    "latinx": "Hispanic or Latino",

    # Black / African American
    "black or african american": "Black or African American",
    "black": "Black or African American",
    "african american": "Black or African American",

    # White
    "white": "White",
    "caucasian": "White",

    # Asian
    "asian": "Asian",

    # Native Hawaiian / Pacific Islander
    "native hawaiian or other pacific islander": "Native Hawaiian or Pacific Islander",
    "native hawaiian": "Native Hawaiian or Pacific Islander",
    "pacific islander": "Native Hawaiian or Pacific Islander",

    # American Indian / Alaska Native
    "american indian or alaska native": "American Indian or Alaska Native",
    "american indian": "American Indian or Alaska Native",
    "alaska native": "American Indian or Alaska Native",
    "native american": "American Indian or Alaska Native",

    # Two or More Races
    "two or more races": "Two or More Races",
    "multiracial": "Two or More Races",
    "multi-racial": "Two or More Races",

    # Not Specified
    "not specified": "Not Specified",
    "prefer not to say": "Not Specified",
    "unknown": "Not Specified",
    "n/a": "Not Specified",
}


def clean_race_column(df: pd.DataFrame, column: str = "Race") -> pd.DataFrame:
    """
    Clean and standardize the race/ethnicity column.

    Steps:
      1. Strip whitespace and lowercase for matching
      2. Map to standardized categories via RACE_MAPPING
      3. Flag unmapped values as 'Other' for review
      4. Fill nulls with 'Not Specified'

    Args:
        df: DataFrame with a race/ethnicity column.
        column: Name of the column to clean (default: "Race").

    Returns:
        DataFrame with cleaned column and a report printed to stdout.
    """
    df = df.copy()

    # Count nulls before cleaning
    null_count = df[column].isna().sum()

    # Step 1: Strip and lowercase for lookup
    normalized = df[column].astype(str).str.strip().str.lower()

    # Step 2: Map to standard categories
    df[column] = normalized.map(RACE_MAPPING)

    # Step 3: Values that didn't map -> 'Other'
    unmapped_mask = df[column].isna() & normalized.notna() & (normalized != "nan")
    unmapped_values = normalized[unmapped_mask].unique()
    df.loc[unmapped_mask, column] = "Other"

    # Step 4: Fill remaining nulls
    df[column] = df[column].fillna("Not Specified")

    # Report
    print(f"Race column cleaning report:")
    print(f"  Null/missing values filled: {null_count}")
    print(f"  Unmapped values set to 'Other': {unmapped_mask.sum()}")
    if len(unmapped_values) > 0:
        print(f"  Unmapped raw values: {list(unmapped_values)}")
    print(f"  Final distribution:\n{df[column].value_counts().to_string()}")

    return df


if __name__ == "__main__":
    # Example usage with sample data matching the screenshot
    sample_data = pd.DataFrame({
        "Race": [
            "Hispanic or Latino/a/x",
            "Black or African American",
            "Black or African American",
            "White",
            "Asian",
            " hispanic ",
            "CAUCASIAN",
            None,
            "Two or More Races",
            "Native Hawaiian or Other Pacific Islander",
        ],
        "Sex": ["Male"] * 10,
        "Department": [
            "Seattle Police Department",
            "Seattle Fire Department",
            "Seattle Public Utilities",
            "Seattle Police Department",
            "Seattle IT",
            "Seattle Fire Department",
            "Seattle Public Utilities",
            "Seattle Police Department",
            "Seattle IT",
            "Seattle Fire Department",
        ],
    })

    print("=== BEFORE ===")
    print(sample_data["Race"].value_counts(dropna=False))
    print()

    cleaned = clean_race_column(sample_data, column="Race")

    print()
    print("=== AFTER ===")
    print(cleaned["Race"].value_counts())
