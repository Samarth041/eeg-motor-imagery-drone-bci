from pathlib import Path
import mne
from mne.datasets import eegbci


#=====================================================
#configuration
#==============================================

SUBJECT=1
RUNS=[4,8,12]

DATA_DIR=Path("data")

LOW_FREQ=8.0
HIGH_FREQ=30.0

#we want 0 to 3 seconds after the event

TMIN=0.0
TMAX=3.0

#===========================================================
#LOAD EEG
#==========================================================

def load_subject():

    files=eegbci.load_data(
        subjects=SUBJECT,
        runs=RUNS,
        path=DATA_DIR
    )

    raws=[]

    for file in files:

        print(f"\n Laoding :{file}")
        raw=mne.io.read_raw_edf(
            file,
            preload=True,
            verbose=False
        )

        raws.append(raw)

    return raws

#preprocessing one recording


def preprocess_raw(raw):

    print("\n Original sampling frequency : ")
    print(raw.info["sfreq"])

    print("\n Number of channels: ")
    print(len(raw.ch_names))

    #filter EEf

    raw.filter(
        l_freq=LOW_FREQ,
        h_freq=HIGH_FREQ,
        verbose=False
    )

    return raw

#======================================================
#extract epochs
#==========================================================

def create_epochs(raw):

    print("\n finding events.............")

    events,event_id=mne.events_from_annotations(
        raw,
        verbose=False
    )

    print("\n Event dictionary: ")
    print(event_id)

    print("\n Number of events: ")
    print(len(events))

    #select only motor-imagery classes.

    selected_event_id={}

    if "T1" in event_id:
        selected_event_id["LEFT"]=event_id["T1"]  

    if "T2" in event_id:
        selected_event_id["RIGHT"]=event_id["T2"]

    print("\n Selected events: ")
    print(selected_event_id)      

    if len(selected_event_id)!=2:
        raise RuntimeError(
            "Could not find both T1 and T2 events."
        )

    epochs=mne.Epochs(
        raw,
        events,
        event_id=selected_event_id,
        tmin=TMIN,
        tmax=TMAX,
        baseline=None,
        preload=True,
        reject_by_annotation=True,
        verbose=False
    )

    return epochs

#=============================================================
#Main
#=============================================================

def main():
    print("="*60)
    print("EEG PREPROCESSING")
    print("="*60)

    raws=load_subject()

    all_epochs=[]

    for raw in raws:
        raw=preprocess_raw(raw)

        epochs=create_epochs(raw)

        print("\n Epoch information: ")
        print(epochs)

        print("\n Epoch shape: ")
        print(epochs.get_data().shape)

        all_epochs.append(epochs)

    #combine the runs

    combined_epochs=mne.concatenate_epochs(
        all_epochs
    )

    X=combined_epochs.get_data()

    y=combined_epochs.events[;,-1]

    print("\n"+"="*60)
    print("Final data")
    print("="*60)

    print("X_shape",X.shape)
    print("y shape",y.shape)

    print("\nLabels:")
    print(y)

    print("\nPreprocessing complete! ")

if __name__=="__main__":
    main()