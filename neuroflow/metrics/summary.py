import pandas as pd
from pathlib import Path
from neuroflow.metrics.nimbalwear import summarize_steps
from neuroflow.metrics.bittium import summarize_hrv
from neuroflow.metrics.paradigma import summarize_armswing


def summarymetrics2csv(file_data, detector, output_file=None):
    df = pd.read_csv(file_data)
    df["time"] = pd.to_datetime(df["time"])
    df.attrs["label"] = file_data

    match detector:
        case "nimbalwear-ankles":
            df_summary = summarize_steps(df)
        case "paradigma-wrists":
            df_summary = summarize_armswing(df)
        case "pan-tompkins":
            df_summary = summarize_hrv(df)

    if output_file is None:
        if detector in file_data.stem:
            output_filename = f"{file_data.stem}_summary.csv"
        else:
            output_filename = f"{file_data.stem}_summary-gait_detector-{detector}.csv"
        output_file = (
            Path(file_data).parent / output_filename
        )
    df_summary.to_csv(output_file, index=False)

    return output_file
