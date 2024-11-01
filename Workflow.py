import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

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

def main():
    try:
        # Load earthquake data
        print("\nLoading earthquake data...")
        data_path = PROJECT_ROOT / 'data' / 'earthquakes.csv'
        
        if not data_path.exists():
            print(f"Error: Data file not found at {data_path}")
            sys.exit(1)
            
        data = pd.read_csv(data_path)

        # 1. Data Statistics Analysis
        print("\n1. Performing Data Statistics Analysis...")
        stats_analyzer = EarthquakeDataStatistics(data)
        stats_report = stats_analyzer.generate_summary_report()
        print("Basic Statistical Measures:")
        print(stats_report['basic_statistics'])
        stats_analyzer.visualize_distributions()

        # 2. Binning Analysis
        print("\n3. Performing Binning Analysis...")
        binning_analyzer = EarthquakeBinningAnalysis(data)
        print("Magnitude Binning Statistics:")
        magnitude_stats = binning_analyzer.magnitude_binning()
        print(magnitude_stats)
        print("\nDepth Binning Statistics:")
        depth_stats = binning_analyzer.depth_binning()
        print(depth_stats)
        binning_analyzer.visualize_binned_data('magnitude')
        binning_analyzer.visualize_binned_data('depth')

        # 3. Normalization Analysis
        print("\n2. Performing Normalization Analysis...")
        normalizer = EarthquakeNormalization(data)
        norm_report = normalizer.generate_summary_report()
        print("Normalization Summary:")
        print(norm_report)
        normalizer.compare_distributions()

        # 4. Pearson Correlation Analysis
        print("\n4. Performing Pearson Correlation Analysis...")
        correlation_analyzer = EarthquakeCorrelationAnalysis(data)
        corr_report = correlation_analyzer.generate_correlation_report()
        print("Strong Correlations:")
        print(corr_report['strong_correlations'])
        correlation_analyzer.visualize_correlation_matrix(corr_report['correlation_matrix'])

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

    except Exception as e:
        print(f"\nAn error occurred during execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # Verify directory structure
    print("\nVerifying directory structure...")
    expected_structure = {
        'earthquake_analysis': [
            'DataStatistics.py',
            'Normalization.py',
            'BinningAnalysis.py',
            'PearsonCorrelation.py',
            'FeatureImportanceAnalysis.py',
            'CorrelationCoefficientAnalysis.py',
            '__init__.py'
        ],
        'data': ['earthquakes.csv']
    }

    for directory, files in expected_structure.items():
        dir_path = PROJECT_ROOT / directory
        if not dir_path.exists():
            print(f"Error: Directory '{directory}' not found!")
            continue
            
        print(f"\nChecking {directory}:")
        existing_files = os.listdir(dir_path)
        for file in files:
            if file in existing_files:
                print(f"✓ Found {file}")
            else:
                print(f"✗ Missing {file}")

    print("\nStarting analysis...")
    main()