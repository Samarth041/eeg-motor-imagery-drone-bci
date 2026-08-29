from pathlib import Path
import mne
from mne.datasets import eegbci

#==========================================
#configuration
#==========================================

SUBJECT=1
RUNS=[4,8,12]

DATA_DIR=Path("data")

#====================================================
#main
#==============================================

def main():
    DATA_DIR.mkdir(exist_ok=True)

    print("=" *60)
    print("EEG Motor Imagery Dataset Downloader")
    print("=" *60)

    print(f"\n Subject:{SUBJECT}")
    print(f"RUNS: {{RUNS}}")

    print("\n Downloading EEG DATA......")
    print("This may take some time on the first run \n")

    files=eegbci.load_data(
        subjects=SUBJECT,
        runs=RUNS,
        path=DATA_DIR
    )

    print("\nDownload complete!")
    print("\nDownloaded files:")

    for file in files:
        print(f"  {file}")

    print("\n Number of files:", len(files))

    print("\n Loading the first EEG recording....")

    raw=mne.io.read_raw_edf(
        files[0],
        preload=False,
        verbose=False
    )

    print("\n EEG information")
    print("="*60)
    
    print("Number of channels:", len(raw.ch_names))
    print("Sampling frequency:", raw.info["sfreq"], "Hz")
    print("Recording duration:", round(raw.times[-1], 2), "seconds")

    print("\nFirst 10 channel names:")
    for channel in raw.ch_names[:10]:
        print(" ", channel)

    print("\nAnnotations:")
    print(raw.annotations)

    print("\nDataset loading test successful!")


if __name__ == "__main__":
    main()