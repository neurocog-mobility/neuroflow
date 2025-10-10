import argparse
from neuroflow.io.load import convert2csv
from neuroflow.io.sync import split2csv
from neuroflow.io.window import window2csv
from neuroflow.processing.gait import gaitevents2csv
from neuroflow.processing.ecg import ecgevents2csv
from neuroflow.metrics.summary import summarymetrics2csv
from pathlib import Path
import json, ast


def get_parser():
    parser = argparse.ArgumentParser(prog="neuroflow")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # convert
    sub_convert = subparsers.add_parser(
        "convert",
        help="""
        Convert raw files to standardized CSV
        """,
    )
    sub_convert.category = "1. Pre-process"
    sub_convert.add_argument(
        "list_data", nargs="+", help="List of raw files to convert"
    )
    sub_convert.add_argument(
        "--device",
        type=str,
        required=True,
        choices=["Axivity (IMU)", "Bittium (ECG)"],
        help="Device name/modality",
    )
    sub_convert.add_argument("--savefile", type=str, help="Output CSV path")

    # sync
    sub_sync = subparsers.add_parser(
        "sync", help="Split continuous data using event timestamps."
    )
    sub_sync.category = "1. Pre-process"
    sub_sync.add_argument("list_data", type=str, help="Path to data file")
    sub_sync.add_argument("file_sync", type=str, help="Path to sync file")
    sub_sync.add_argument(
        "--source",
        type=str,
        required=True,
        choices=["NeuroFlow (CSV)", "Axivity (CWA)", "Bittium (EDF)"],
        help="Device name/modality",
    )
    sub_sync.add_argument("--savedir", type=str, help="Path to output directory")

    # window
    sub_window = subparsers.add_parser(
        "window", help="Split continuous data using event timestamps."
    )
    sub_window.category = "1. Pre-process"
    sub_window.add_argument("list_data", type=str, help="Path to data file")
    sub_window.add_argument("file_times", type=str, help="Path to timestamps file")
    sub_window.add_argument(
        "--source",
        type=str,
        required=True,
        choices=["NeuroFlow (CSV)", "Axivity (CWA)", "Bittium (EDF)"],
        help="Device name/modality",
    )
    sub_window.add_argument(
        "--duration", required=True, type=int, help="Window duration in seconds"
    )
    sub_window.add_argument(
        "--number", required=True, type=int, help="Number of windows (pre/post)"
    )
    sub_window.add_argument("--savedir", type=str, help="Path to output directory")

    # gait
    sub_gait = subparsers.add_parser(
        "gait",
        help="""
        Detect gait events from standardized IMU CSV
        """,
    )
    sub_gait.category = "2. Event detection"
    sub_gait.add_argument("file_data", type=str, help="Path to data file")
    sub_gait.add_argument(
        "--detector",
        type=str,
        required=True,
        choices=["nimbalwear-ankles", "paradigma-wrists"],
        help="Detector name",
    )
    sub_gait.add_argument(
        "--detector_params",
        type=str,
        required=False,
        help="Key-value dictionary (as string) for the detector.",
    )
    sub_gait.add_argument("--savefile", type=str, help="Output CSV path")

    # ecg
    sub_ecg = subparsers.add_parser(
        "ecg",
        help="""
        Detect ECG events from standardized ECG CSV
        """,
    )
    sub_ecg.category = "2. Event detection"
    sub_ecg.add_argument("file_data", type=str, help="Path to data file")
    sub_ecg.add_argument(
        "--detector",
        type=str,
        required=True,
        choices=["pan-tompkins"],
        help="Detector name",
    )
    sub_ecg.add_argument(
        "--detector_params",
        type=str,
        required=False,
        help="Key-value dictionary (as string) for the detector.",
    )
    sub_ecg.add_argument("--savefile", type=str, help="Output CSV path")

    # metrics
    sub_metrics = subparsers.add_parser(
        "metrics",
        help="""
        Summarize event metrics from a processed CSV
        """,
    )
    sub_metrics.category = "3. Feature extraction"
    sub_metrics.add_argument("file_data", type=str, help="Path to data file")
    sub_metrics.add_argument(
        "--detector",
        type=str,
        required=True,
        choices=["nimbalwear-ankles", "pan-tompkins"],
        help="Detector name",
    )
    sub_metrics.add_argument("--savefile", type=str, help="Output CSV path")

    # validate
    sub_validate = subparsers.add_parser("validate", help="Launch validation UI")
    sub_validate.category = "3. Feature extraction"
    sub_validate.add_argument("file", help="Standardized CSV file to validate")

    # # test
    # subparsers.add_parser("test", help="Test function.")

    # add GUI command
    subparsers.add_parser("gui", help="Launch Neuroflow GUI.")

    return parser


def run_command(args):
    match args.command:
        case "convert":
            try:
                file_list = [Path(f) for f in args.list_data.split(", ")]
            except:
                file_list = [Path(f) for f in args.list_data]
            output_file = Path(args.savefile) if args.savefile else None

            result = convert2csv(
                file_list,
                device=args.device,
                output_file=output_file,
            )
            print(f"Conversion complete: {result}")

        case "sync":
            try:
                file_list = [Path(f) for f in args.list_data.split(", ")]
            except:
                file_list = [Path(f) for f in args.list_data]
            file_sync = Path(args.file_sync)
            output = Path(args.savedir) if args.savedir else None

            result = split2csv(
                file_list, file_sync, source=args.source, output_dir=output
            )
            print(f"Sync complete: {result}")

        case "window":
            try:
                file_list = [Path(f) for f in args.list_data.split(", ")]
            except:
                file_list = [Path(f) for f in args.list_data]
            file_times = Path(args.file_times)
            output = Path(args.savedir) if args.savedir else None

            result = window2csv(
                file_list,
                file_times,
                duration_window=args.duration,
                number_window=args.number,
                source=args.source,
                output_dir=output,
            )
            print(f"Sync complete: {result}")

        case "gait":
            file_data = Path(args.file_data)
            output = Path(args.savefile) if args.savefile else None

            try:
                param_dict = (
                    json.loads(args.detector_params) if args.detector_params else {}
                )
            except:
                try:
                    param_dict = (
                        ast.literal_eval(args.detector_params)
                        if args.detector_params
                        else {}
                    )
                except:
                    raise ValueError(
                        "Enter a valid kay-value dictionary string of detector parameters."
                    )

            result = gaitevents2csv(
                file_data, detector=args.detector, detector_params=param_dict
            )
            print(f"Gait event detection complete: {result}")

        case "ecg":
            file_data = Path(args.file_data)
            output = Path(args.savefile) if args.savefile else None

            try:
                param_dict = (
                    json.loads(args.detector_params) if args.detector_params else {}
                )
            except:
                try:
                    param_dict = (
                        ast.literal_eval(args.detector_params)
                        if args.detector_params
                        else {}
                    )
                except:
                    raise ValueError(
                        "Enter a valid kay-value dictionary string of detector parameters."
                    )

            result = ecgevents2csv(
                file_data, detector=args.detector, detector_params=param_dict
            )
            print(f"ECG event detection complete: {result}")

        case "metrics":
            file_data = Path(args.file_data)
            output = Path(args.savefile) if args.savefile else None

            result = summarymetrics2csv(file_data, detector=args.detector)
            print(f"Summary metrics extraction complete: {result}")

        case "validate":
            import subprocess, os

            validate_path = os.path.join(
                os.path.dirname(__file__), "validation", "validate.py"
            )

            subprocess.run(["streamlit", "run", validate_path, "--", args.file])

        case "test":
            print("This is an example command.")

        case "gui":
            from neuroflow.gui import NeuroflowGUI

            app = NeuroflowGUI()
            app.mainloop()
        case _:
            raise ValueError(f"Unknown command: {args.command}")
