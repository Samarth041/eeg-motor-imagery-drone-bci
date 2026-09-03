from pathlib import Path

import matplotlib.pyplot as plt
import mne
from mne.datasets import eegbci

SUBJECT=1
RUNS=[4,8,12]

DATA_DIR = Path("data")

def main():
    files=eegbci.load_data(
        subjects=SUBJECT,
        runs=RUNS,
        path=DATA_DIR
    )

    raw=mne.io.read_raw_edf(
        files[0],
        preload=True,
        verbose=False
    )

    print(raw)

    #show the first 10 seconds

    raw.plot(
        duration=10,
        n_channels=20,
        scalings="auto"
    )

    plt.show()

if __name__=="__main__":
    main()