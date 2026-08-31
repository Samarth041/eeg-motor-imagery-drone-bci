from pathlib import Path
import mne 

from mne.datasets import eegbci

SUBJECT=1
RUNS=[4,8,12]

DATA_DIR=Path("data")

def main():
    print("Loading EEG data.....")

    files=eegbci.load_data(
        subjects=SUBJECT,
        runs=RUNS,
        path=DATA_DIR
    )

    for file in files:

        print("\n"+"=" *60)
        print("FILE: ",file)
        print("="*60)

        raw=mne.io.read_raw_edf(
            file,
            preload=False,
            verbose=False
        )

        print("\nAnnotations: ")
        print(raw.annotations)

        print("\nDescription: ")
        print(raw.annotations.description)

        print("\n Number of annotations: ")
        print(len(raw.annotations))


if __name__=="__main__":
    main()
