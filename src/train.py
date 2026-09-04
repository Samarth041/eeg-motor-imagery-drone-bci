from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import mne
import numpy as np

from mne.datasets import eegbci
from mne.decoding import CSP

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    ConfusionMatrixDisplay,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


# ============================================================
# Configuration
# ============================================================

SUBJECT = 1
RUNS = [4, 8, 12]

DATA_DIR = Path("data")
MODEL_DIR = Path("models")

LOW_FREQ = 8.0
HIGH_FREQ = 30.0

TMIN = 0.0
TMAX = 3.0

N_COMPONENTS = 4


# ============================================================
# Load and preprocess EEG
# ============================================================

def load_data():

    files = eegbci.load_data(
        subjects=SUBJECT,
        runs=RUNS,
        path=DATA_DIR,
    )

    all_epochs = []

    for file in files:

        print(f"\nLoading: {file}")

        raw = mne.io.read_raw_edf(
            file,
            preload=True,
            verbose=False,
        )

        # Filter EEG
        raw.filter(
            l_freq=LOW_FREQ,
            h_freq=HIGH_FREQ,
            verbose=False,
        )

        # Find annotations/events
        events, event_id = mne.events_from_annotations(
            raw,
            verbose=False,
        )

        print("Event dictionary:", event_id)

        # Select only T1 and T2
        selected_event_id = {
            "LEFT": event_id["T1"],
            "RIGHT": event_id["T2"],
        }

        epochs = mne.Epochs(
            raw,
            events,
            event_id=selected_event_id,
            tmin=TMIN,
            tmax=TMAX,
            baseline=None,
            preload=True,
            reject_by_annotation=True,
            verbose=False,
        )

        all_epochs.append(epochs)

    # Combine all runs
    combined_epochs = mne.concatenate_epochs(
        all_epochs
    )

    # EEG data
    X = combined_epochs.get_data()

    # Numerical event labels
    event_labels = combined_epochs.events[:, -1]

    # Convert event IDs to LEFT=0, RIGHT=1
    left_id = selected_event_id["LEFT"]
    right_id = selected_event_id["RIGHT"]

    y = np.where(
        event_labels == left_id,
        0,
        1,
    )

    return X, y


# ============================================================
# Main training
# ============================================================

def main():

    print("=" * 60)
    print("CSP + LOGISTIC REGRESSION")
    print("=" * 60)

    X, y = load_data()

    print("\nRaw EEG shape:")
    print(X.shape)

    print("\nLabels shape:")
    print(y.shape)

    print("\nClass counts:")
    print("LEFT :", np.sum(y == 0))
    print("RIGHT:", np.sum(y == 1))

    # --------------------------------------------------------
    # Train/test split
    # --------------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    print("\nTrain shape:", X_train.shape)
    print("Test shape :", X_test.shape)

    # --------------------------------------------------------
    # CSP + Logistic Regression pipeline
    # --------------------------------------------------------

    csp = CSP(
        n_components=N_COMPONENTS,
        reg=None,
        log=True,
        norm_trace=False,
    )

    classifier = LogisticRegression(
        max_iter=1000,
    )

    pipeline = Pipeline([
        ("csp", csp),
        ("classifier", classifier),
    ])

    print("\nTraining model...")

    pipeline.fit(X_train, y_train)

    print("Training complete!")

    # --------------------------------------------------------
    # Evaluate
    # --------------------------------------------------------

    y_pred = pipeline.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        y_pred,
    )

    print("\n" + "=" * 60)
    print("EVALUATION")
    print("=" * 60)

    print("\nAccuracy:")
    print(f"{accuracy:.4f}")

    print("\nClassification report:")

    print(
        classification_report(
            y_test,
            y_pred,
            target_names=["LEFT", "RIGHT"],
        )
    )

    print("\nConfusion matrix:")

    cm = confusion_matrix(
        y_test,
        y_pred,
    )

    print(cm)

    # --------------------------------------------------------
    # Save model
    # --------------------------------------------------------

    MODEL_DIR.mkdir(exist_ok=True)

    model_path = MODEL_DIR / "csp_logistic.pkl"

    joblib.dump(
        pipeline,
        model_path,
    )

    print("\nModel saved to:")
    print(model_path)

    # --------------------------------------------------------
    # Plot confusion matrix
    # --------------------------------------------------------

    ConfusionMatrixDisplay.from_predictions(
        y_test,
        y_pred,
        display_labels=["LEFT", "RIGHT"],
    )

    plt.title("CSP + Logistic Regression")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()