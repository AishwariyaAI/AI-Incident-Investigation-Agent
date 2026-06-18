import numpy as np

# Local imports
from score_normalizer import normalize_scores
from fusion_logic import fuse_modalities
from threshold import compute_threshold, predict_anomalies

from metrics import compute_classification_metrics
from visualization import plot_roc_curve

from severity import get_severity
from root_cause import root_cause_analysis
from incident_report import generate_incident_report


class AnomalyDetector:
    """
    End-to-end anomaly detector:

    Sensor + Image + Log
            ↓
       Normalization
            ↓
          Fusion
            ↓
       Thresholding
            ↓
      Anomaly Detection
            ↓
      Severity Analysis
            ↓
      Root Cause Analysis
            ↓
      Incident Reports
    """

    def __init__(
        self,
        fusion_method="weighted",
        fusion_weights=(0.4, 0.4, 0.2),
        normalization="zscore",
        threshold_method="percentile",
        threshold_value=95,
    ):
        self.fusion_method = fusion_method
        self.fusion_weights = fusion_weights
        self.normalization = normalization
        self.threshold_method = threshold_method
        self.threshold_value = threshold_value

    # Step 1: Normalize modality scores
    def normalize(self, sensor_scores, image_scores, log_scores):

        sensor_n = normalize_scores(
            sensor_scores,
            self.normalization
        )

        image_n = normalize_scores(
            image_scores,
            self.normalization
        )

        log_n = normalize_scores(
            log_scores,
            self.normalization
        )

        return sensor_n, image_n, log_n

    # Step 2: Fuse normalized scores
    def fuse(
        self,
        sensor_n,
        image_n,
        log_n
    ):

        fused_scores = fuse_modalities(
            sensor_n,
            image_n,
            log_n,
            method=self.fusion_method,
            weights=self.fusion_weights,
        )

        return fused_scores

    # Step 3: Thresholding
    def threshold(self, fused_scores):

        threshold = compute_threshold(
            fused_scores,
            method=self.threshold_method,
            value=self.threshold_value,
        )

        return threshold

    # Step 4: Predict anomalies
    def predict(
        self,
        fused_scores,
        threshold
    ):

        predictions = predict_anomalies(
            fused_scores,
            threshold
        )

        return predictions

    # Step 5: Full pipeline
    def run(
        self,
        sensor_scores,
        image_scores,
        log_scores,
        y_true=None
    ):

        # Normalize
        sensor_n, image_n, log_n = self.normalize(
            sensor_scores,
            image_scores,
            log_scores
        )

        # Fuse
        fused_scores = self.fuse(
            sensor_n,
            image_n,
            log_n
        )

        # Threshold
        threshold = self.threshold(
            fused_scores
        )

        # Predict
        predictions = self.predict(
            fused_scores,
            threshold
        )

        # Severity Analysis
        severity_levels = [
            get_severity(score)
            for score in fused_scores
        ]

        # Root Cause Analysis
        root_causes = []

        for i in range(len(fused_scores)):

            root_cause = root_cause_analysis(
                sensor_n[i],
                image_n[i],
                log_n[i]
            )

            root_causes.append(root_cause)

        # Incident Reports
        incident_reports = []

        for i in range(len(fused_scores)):

            report = generate_incident_report(
                sensor_n[i],
                image_n[i],
                log_n[i]
            )

            incident_reports.append(report)

        results = {
            "fused_scores": fused_scores,
            "threshold": threshold,
            "predictions": predictions,
            "severity": severity_levels,
            "root_causes": root_causes,
            "incident_reports": incident_reports
        }

        # Optional evaluation
        if y_true is not None:

            metrics = compute_classification_metrics(
                y_true,
                predictions
            )

            plot_roc_curve(
                y_true,
                fused_scores
            )

            results["metrics"] = metrics

        return results


# --------------------------------------------------
# Testing
# --------------------------------------------------

if __name__ == "__main__":

    print("Running AI Incident Investigation Agent...")

    # Dummy Scores
    sensor_scores = np.random.rand(100)
    image_scores = np.random.rand(100)
    log_scores = np.random.rand(100)

    # Dummy Labels
    y_true = np.random.randint(
        0,
        2,
        size=100
    )

    detector = AnomalyDetector()

    outputs = detector.run(
        sensor_scores=sensor_scores,
        image_scores=image_scores,
        log_scores=log_scores,
        y_true=y_true,
    )

    print("\nThreshold:")
    print(outputs["threshold"])

    print("\nSample Predictions:")
    print(outputs["predictions"][:10])

    print("\nSample Severity:")
    print(outputs["severity"][:5])

    print("\nSample Root Cause:")
    print(outputs["root_causes"][0])

    print("\nSample Incident Report:")
    print(outputs["incident_reports"][0])

    print("\nMetrics:")
    print(outputs.get("metrics"))