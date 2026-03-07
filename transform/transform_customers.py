import pandas as pd

def formating_is_active(df:pd.DataFrame):
    # Standardize mixed yes/no and 1/0 variants into Pandas nullable booleans.
    mapping = {
        "yes": True,
        "true": True,
        "1": True,
        1: True,
        "no": False,
        "false": False,
        "0": False,
        0: False
    }

    df["is_active"] = (
        df["is_active"]
        .astype(str)
        .str.lower()
        .map(mapping)
        .astype("boolean")
    )
    return df

def formating_total_spent(df:pd.DataFrame):
    # Strip non-numeric characters so totals can be cast safely to decimals.
    df["total_spent"] = (
        df["total_spent"]
        .str.replace(r"[^\d.]", "", regex=True)
        .replace("", pd.NA)
        .pipe(pd.to_numeric, errors="coerce")
        .round(2)
    )

    return df

def formating_created_at(df:pd.DataFrame):
    # Accept multiple timestamp formats and convert them into a single datetime dtype.
    df["created_at"] = df["created_at"].str.replace("/","-")
    df["created_at"] = pd.to_datetime(df["created_at"],format="mixed",errors="coerce").dt.strftime("%d/%m/%Y %H:%M:%S")
    df["created_at"] = pd.to_datetime(df["created_at"],format="mixed",errors="coerce")
    return df

def formating_birth_date(df:pd.DataFrame):
    # Parse inconsistent date formats while preserving day-first inputs.
    df["birth_date"] = df["birth_date"].str.replace("/","-")
    df["birth_date"] = pd.to_datetime(df["birth_date"],format="mixed",dayfirst=True,errors="coerce").dt.strftime("%d/%m/%Y")
    df["birth_date"] = pd.to_datetime(df["birth_date"],format="mixed",dayfirst=True,errors="coerce")
    return df
def formating_country(df:pd.DataFrame):
    # Expand shorthand country values to the canonical name used in the target table.
    df.loc[df["country"] == "col", "country"] = "colombia"
    return df

def clean_numbers(df:pd.DataFrame):
    # Keep only Colombian-style 10 digit phone numbers after removing punctuation and prefixes.
    df["phone"] = df["phone"].str.replace(r"\D","",regex=True)
    df["phone"] = df["phone"].str.replace(r"^57","",regex=True)
    df.loc[df["phone"].str.len() != 10, "phone"] = None

    return df

def clean_repeated_rows(df:pd.DataFrame):
    # Deduplicate repeated customer names before the load step.
    df.drop_duplicates(subset=["full_name"],inplace=True)
    return df

def clean_email(df:pd.DataFrame):
    # Null out malformed email values so they can be handled by downstream constraints.
    email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    df.loc[~df["email"].str.match(email_regex, na=False), "email"] = pd.NA

    return df

def clean_null(df:pd.DataFrame):
    # Treat placeholder empty values as nulls and drop rows missing mandatory fields.
    df.replace(
        ["NaN", ""],
        pd.NA,
        inplace=True
    )
    df.dropna(subset=["full_name", "email", "birth_date"], inplace=True)
    return df

def clean_text(df:pd.DataFrame):
    # Normalize string columns to lowercase, trimmed text with collapsed inner spaces.
    df = df.apply(lambda col: col.str.lower().str.strip().str.replace(r"\s+"," ",regex=True) if col.dtype == "str" else col)
    return df

def transform_customers(df:pd.DataFrame):
    # Run the customer dataset through the full cleaning pipeline before loading.
    string_cols = ["full_name", "email", "phone", "city", "country"]
    df = (
        df
        .pipe(clean_null)
        .pipe(clean_text)
        .pipe(clean_repeated_rows)
        .pipe(clean_email)
        .pipe(clean_numbers)
        .pipe(formating_country)
        .pipe(formating_birth_date)
        .pipe(formating_created_at)
        .pipe(formating_total_spent)
        .pipe(formating_is_active)
    )
    df[string_cols] = df[string_cols].astype("string")

    return df
