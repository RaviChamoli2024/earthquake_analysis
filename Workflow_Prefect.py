import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from prefect import flow, task
from datetime import timedelta

# Get the absolute path of the project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()

# Add the project root to Python path
sys.path.insert(0, str(PROJECT_ROOT))

# Print debugging information
print(f"Project root: {PROJECT_ROOT}")
print(f"Python path: {sys.path}")
print("\nChecking directory contents:")
print("\nProject root contents:", os.listdir(PROJECT_ROOT))

earthquake_analysis_path = PROJECT_ROOT / 'earthquake_analysis'
if earthquake_analysis_path.exists():
    print("\nearthquake_analysis contents:", os.listdir(earthquake_analysis_path))
else:
    print("\nError: 'earthquake_analysis' directory not found.")
    sys.exit(1)

try:
    # Import the modules
    from earthquake_analysis.DataStatistics import EarthquakeDataStatistics
    from earthquake_analysis.Normalization import EarthquakeNormalization
    from earthquake_analysis.BinningAnalysis import EarthquakeBinningAnalysis
    from earthquake_analysis.PearsonCorrelation import EarthquakeCorrelationAnalysis
    from earthquake_analysis.FeatureImportanceAnalysis import EarthquakeFeatureImportance
    from earthquake_analysis.CorrelationCoefficientAnalysis import EarthquakeCorrelationCoefficient
except ImportError as e:
    print(f"\nError importing modules: {e}")
    print("\nPlease ensure all files are in the correct locations:")
    print("- All analysis files should be in the 'earthquake_analysis' directory")
    print("- The data file should be in the 'data' directory")
    sys.exit(1)

@task
def load_data():
    print("\nLoading earthquake data...")
    data_path = PROJECT_ROOT / 'data' / 'earthquakes.csv'
    
    if not data_path.exists():
        print(f"Error: Data file not found at {data_path}")
        sys.exit(1)
        
    return pd.read_csv(data_path)

@task(log_prints=True)
def analyze_data(data):
    # 1. Data Statistics Analysis
    print("\n1. Performing Data Statistics Analysis...")
    stats_analyzer = EarthquakeDataStatistics(data)
    stats_report = stats_analyzer.generate_summary_report()
    print("Basic Statistical Measures:")
    print(stats_report['basic_statistics'])

    # 2. Binning Analysis
    print("\n2. Performing Binning Analysis...")
    binning_analyzer = EarthquakeBinningAnalysis(data)
    print("Magnitude Binning Statistics:")
    magnitude_stats = binning_analyzer.magnitude_binning()
    print(magnitude_stats)
    print("\nDepth Binning Statistics:")
    depth_stats = binning_analyzer.depth_binning()
    print(depth_stats)

    # 3. Normalization Analysis
    print("\n3. Performing Normalization Analysis...")
    normalizer = EarthquakeNormalization(data)
    norm_report = normalizer.generate_summary_report()
    print("Normalization Summary:")
    print(norm_report)

    # 4. Pearson Correlation Analysis
    print("\n4. Performing Pearson Correlation Analysis...")
    correlation_analyzer = EarthquakeCorrelationAnalysis(data)
    corr_report = correlation_analyzer.generate_correlation_report()
    print("Strong Correlations:")
    print(corr_report['strong_correlations'])

    # 5. Correlation Coefficient Analysis
    print("\n5. Performing Correlation Coefficient Analysis...")
    coef_analyzer = EarthquakeCorrelationCoefficient(data)
    coef_report = coef_analyzer.generate_detailed_report()
    print("Correlations with Magnitude:")
    print(coef_report['magnitude']['correlations'])
    print("\nHighly Significant Correlations:")
    print(coef_report['magnitude']['significance_analysis']['highly_significant'])

    # 6. Feature Importance Analysis
    print("\n6. Performing Feature Importance Analysis...")
    importance_analyzer = EarthquakeFeatureImportance(data)
    importance_report = importance_analyzer.generate_importance_report()
    print("Feature Importance for Magnitude Prediction:")
    print(importance_report['magnitude']['feature_importance'])
    print("\nFeature Group Importance:")
    print(importance_report['magnitude']['group_importance'])

    # Show all plots (if any are still pending)
    plt.show()

@flow
def workflow_earthquake_analysis():
    data = load_data()
    analyze_data(data)

# Run the workflow directly or serve it for local testing
if __name__ == "__main__":
    # Use serve for local development
    workflow_earthquake_analysis.serve()