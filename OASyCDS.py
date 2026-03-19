

# ------------------------------------------------
# DESCARGA DE CDS (ANDA)
# ------------------------------------------------

import eikon as ek
import pandas as pd

ek.set_app_key("TU_APP_KEY_NUEVA")

# 1) Buscar el CDS principal
ric_df, err = ek.get_data(["AAPL.O"], ["TR.CDSPrimaryCDSRic"])
print(ric_df)
print(err)

cds_ric = ric_df.loc[0, "Primary CDS RIC"]

# 2) Pedir histórico de spread CDS con get_data, no get_timeseries
cds_df, err = ek.get_data(
    [cds_ric],
    ["TR.CDSType", "TR.PARMIDSPREAD.date", "TR.PARMIDSPREAD"],
    {"SDate": "2015-01-01", "EDate": "2025-01-01", "DateType": "AD", "CURN": "USD"}
)

print(cds_df.head())
print(err)














# ------------------------------------------------
# 2) DESCARGA DE SPREADS (ANDA)
# ------------------------------------------------


import eikon as ek
import pandas as pd

ek.set_app_key("TU_APP_KEY")

bond_rics = ["674599DS1=", "580135BY6=", "02079KAD9="]

# ------------------------------------------------
# 1) OAS histórico mensual
# ------------------------------------------------
oas_frames = []

for ric in bond_rics:
    print(f"\nTesting OAS history for {ric}")
    df, err = ek.get_data(
        [ric],
        ["TR.OPTIONADJUSTEDSPREADBID.date", "TR.OPTIONADJUSTEDSPREADBID"],
        parameters={
            "SDate": "2015-01-01",
            "EDate": "2025-01-01",
            "Frq": "M"
        }
    )
    print(df.head())
    print(err)
    
    if df is not None and len(df) > 0:
        df["source_ric"] = ric
        oas_frames.append(df)

oas_hist = pd.concat(oas_frames, ignore_index=True) if oas_frames else pd.DataFrame()
print("\n=== OAS HIST ALL ===")
print(oas_hist.head(20))


# ------------------------------------------------
# 2) Z-spread histórico mensual
# ------------------------------------------------
z_frames = []

for ric in bond_rics:
    print(f"\nTesting Z-spread history for {ric}")
    df, err = ek.get_data(
        [ric],
        ["TR.ZSPREAD.date", "TR.ZSPREAD"],
        parameters={
            "SDate": "2015-01-01",
            "EDate": "2025-01-01",
            "Frq": "M"
        }
    )
    print(df.head())
    print(err)

    if df is not None and len(df) > 0:
        df["source_ric"] = ric
        z_frames.append(df)

z_hist = pd.concat(z_frames, ignore_index=True) if z_frames else pd.DataFrame()
print("\n=== Z-SPREAD HIST ALL ===")
print(z_hist.head(20))


# ------------------------------------------------
# 3) Limpieza mínima para inspección
# ------------------------------------------------
if not oas_hist.empty:
    oas_hist["Date"] = pd.to_datetime(oas_hist["Date"], errors="coerce")
    oas_hist["Option Adjusted Spread Bid"] = pd.to_numeric(
        oas_hist["Option Adjusted Spread Bid"], errors="coerce"
    )
    print("\n=== OAS COVERAGE ===")
    print(
        oas_hist.groupby("source_ric")
        .agg(
            first_date=("Date", "min"),
            last_date=("Date", "max"),
            n_obs=("Option Adjusted Spread Bid", "count")
        )
        .reset_index()
    )

if not z_hist.empty:
    z_hist["Date"] = pd.to_datetime(z_hist["Date"], errors="coerce")
    z_hist["Z Spread"] = pd.to_numeric(z_hist["Z Spread"], errors="coerce")
    print("\n=== Z-SPREAD COVERAGE ===")
    print(
        z_hist.groupby("source_ric")
        .agg(
            first_date=("Date", "min"),
            last_date=("Date", "max"),
            n_obs=("Z Spread", "count")
        )
        .reset_index()
    )
