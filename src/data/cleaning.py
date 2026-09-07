import pandas as pd
import numpy as np

def clean_users(users: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate the users dataset.
    """

    df = users.copy()

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    # Remove duplicate user IDs while keeping the first record
    df = df.drop_duplicates(
        subset=["user_id"],
        keep="first"
    )

    # Standardize text columns
    df["country"] = (
        df["country"]
        .astype("string")
        .str.strip()
    )

    df["age_group"] = (
        df["age_group"]
        .astype("string")
        .str.strip()
    )

    # Ensure following count cannot be negative
    df["following_count"] = (
        pd.to_numeric(
            df["following_count"],
            errors="coerce"
        )
        .clip(lower=0)
    )

    # Standardize creator flag
    df["creator_flag"] = (
        df["creator_flag"]
        .fillna(False)
        .astype(bool)
    )

    # Remove records without a user ID
    df = df.dropna(
        subset=["user_id"]
    )

    return df


def clean_creators(creators: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate the creators dataset.
    """

    df = creators.copy()

    df = df.drop_duplicates()

    df = df.drop_duplicates(
        subset=["creator_id"],
        keep="first"
    )

    df["creator_name"] = (
        df["creator_name"]
        .astype("string")
        .str.strip()
    )

    df["creator_type"] = (
        df["creator_type"]
        .astype("string")
        .str.strip()
    )

    df["followers"] = (
        pd.to_numeric(
            df["followers"],
            errors="coerce"
        )
        .clip(lower=0)
    )

    df = df.dropna(
        subset=["creator_id"]
    )

    return df


def clean_content(content: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate the content dataset.
    """

    df = content.copy()

    df = df.drop_duplicates()

    df = df.drop_duplicates(
        subset=["content_id"],
        keep="first"
    )

    # Standardize categorical columns
    df["content_type"] = (
        df["content_type"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    df["genre"] = (
        df["genre"]
        .astype("string")
        .str.strip()
    )

    # Convert duration to numeric
    df["duration"] = pd.to_numeric(
        df["duration"],
        errors="coerce"
    )

    # Invalid duration becomes missing
    df.loc[
        df["duration"] <= 0,
        "duration"
    ] = np.nan

    # Use median duration by content type
    df["duration"] = (
        df.groupby("content_type")["duration"]
        .transform(
            lambda x: x.fillna(x.median())
        )
    )

    # Final fallback in case an entire category is missing
    df["duration"] = (
        df["duration"]
        .fillna(df["duration"].median())
    )

    df = df.dropna(
        subset=["content_id", "creator_id"]
    )

    return df


def clean_interactions(
    interactions: pd.DataFrame,
    users: pd.DataFrame,
    creators: pd.DataFrame,
    content: pd.DataFrame
) -> pd.DataFrame:
    """
    Clean and validate interaction events.
    """

    df = interactions.copy()

    # Remove exact duplicates
    df = df.drop_duplicates()

    # Convert numeric columns
    numeric_columns = [
        "duration",
        "watch_time",
        "completion_rate"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Binary interaction columns
    binary_columns = [
        "impression",
        "clicked",
        "liked",
        "saved",
        "shared",
        "commented",
        "recreated",
        "meaningful_engagement"
    ]

    for column in binary_columns:
        if column in df.columns:
            df[column] = (
                pd.to_numeric(
                    df[column],
                    errors="coerce"
                )
                .fillna(0)
                .clip(0, 1)
                .astype(int)
            )

    # Watch time cannot be negative
    df["watch_time"] = (
        df["watch_time"]
        .clip(lower=0)
    )

    # Watch time cannot exceed content duration
    df["watch_time"] = np.minimum(
        df["watch_time"],
        df["duration"]
    )

    # Recalculate completion rate
    df["completion_rate"] = np.where(
        df["duration"] > 0,
        df["watch_time"] / df["duration"],
        0
    )

    df["completion_rate"] = (
        df["completion_rate"]
        .clip(0, 1)
    )

    # Engagement actions should require a click
    engagement_columns = [
        "liked",
        "saved",
        "shared",
        "commented",
        "recreated"
    ]

    for column in engagement_columns:
        if column in df.columns:
            df.loc[
                df["clicked"] == 0,
                column
            ] = 0

    # Meaningful engagement requires a click
    if "meaningful_engagement" in df.columns:
        df.loc[
            df["clicked"] == 0,
            "meaningful_engagement"
        ] = 0

    # Referential integrity
    df = df[
        df["user_id"].isin(users["user_id"])
    ]

    df = df[
        df["creator_id"].isin(creators["creator_id"])
    ]

    df = df[
        df["content_id"].isin(content["content_id"])
    ]

    # Remove rows without essential identifiers/timestamp
    df = df.dropna(
        subset=[
            "user_id",
            "content_id",
            "creator_id",
            "timestamp"
        ]
    )

    return df


def validate_interactions(
    interactions: pd.DataFrame
) -> dict:
    """
    Return key quality checks for the cleaned
    interaction dataset.
    """

    checks = {
        "duplicate_rows": int(
            interactions.duplicated().sum()
        ),
        "negative_watch_time": int(
            (interactions["watch_time"] < 0).sum()
        ),
        "completion_rate_out_of_range": int(
            (
                (interactions["completion_rate"] < 0)
                |
                (interactions["completion_rate"] > 1)
            ).sum()
        ),
        "watch_time_exceeds_duration": int(
            (
                interactions["watch_time"]
                > interactions["duration"]
            ).sum()
        )
    }

    return checks


