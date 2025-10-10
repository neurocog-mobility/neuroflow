import pandas as pd
from pathlib import Path
from neuroflow.metrics.nimbalwear import summarize_steps
from neuroflow.metrics.bittium import summarize_hrv


def summarymetrics2csv(file_data, detector, output_file=None):
    df = pd.read_csv(file_data)
    df["time"] = pd.to_datetime(df["time"])
    df.attrs["label"] = file_data

    match detector:
        case "nimbalwear-ankles":
            df_summary = summarize_steps(df)
        case "pan-tompkins":
            df_summary = summarize_hrv(df)

    if output_file is None:
        output_file = (
            Path(file_data).parent / f"{file_data.stem}_summary_gait_{detector}.csv"
        )
    df_summary.to_csv(output_file, index=False)

    return output_file
