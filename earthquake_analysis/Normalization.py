import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns
import json
from scipy import stats  # Added for QQ plots

class EarthquakeNormalization:
    def __init__(self, data):
        self.data = data
        self.normalized_data = {}
        
    def prepare_columns(self):
        """
        Define columns for different normalization techniques
        """
        return {
            'standard_scaling': [
                'magnitude',    # Requires standard scaling due to normal-like distribution
                'depth',       # Large variations in depth values
                'sig',         # Significance scores with outliers
                'mmi',         # Modified Mercalli Intensity
                'gap',         # Azimuthal gap values
                'rms',         # Root mean square residuals
                'dmin'         # Minimum distance to stations
            ],
            'minmax_scaling': [
                'latitude',    # Bounded geographic coordinates
                'longitude',   # Bounded geographic coordinates
                'cdi',        # Community Decimal Intensity (0-12 scale)
                'felt',       # Number of felt reports (needs bounded scaling)
                'distanceKM'  # Distance measurements (non-negative values)
            ]
        }

    def apply_standard_scaling(self):
        """
        Apply StandardScaler to appropriate columns
        """
        scaler = StandardScaler()
        columns = self.prepare_columns()['standard_scaling']
        
        scaled_data = {}
        original_stats = {}
        scaled_stats = {}
        
        for column in columns:
            # Handle missing values
            data_clean = self.data[column].dropna()
            
            # Original statistics
            original_stats[column] = {
                'mean': float(data_clean.mean()),
                'std': float(data_clean.std()),
                'min': float(data_clean.min()),
                'max': float(data_clean.max())
            }
            
            # Apply scaling
            scaled_values = scaler.fit_transform(data_clean.values.reshape(-1, 1))
            scaled_data[column] = scaled_values.flatten()
            
            # Scaled statistics
            scaled_stats[column] = {
                'mean': float(np.mean(scaled_values)),
                'std': float(np.std(scaled_values)),
                'min': float(np.min(scaled_values)),
                'max': float(np.max(scaled_values))
            }
        
        self.normalized_data['standard_scaled'] = scaled_data
        return original_stats, scaled_stats

    def apply_minmax_scaling(self):
        """
        Apply MinMaxScaler to appropriate columns
        """
        scaler = MinMaxScaler()
        columns = self.prepare_columns()['minmax_scaling']
        
        scaled_data = {}
        original_stats = {}
        scaled_stats = {}
        
        for column in columns:
            # Handle missing values
            data_clean = self.data[column].dropna()
            
            # Original statistics
            original_stats[column] = {
                'min': float(data_clean.min()),
                'max': float(data_clean.max()),
                'range': float(data_clean.max() - data_clean.min())
            }
            
            # Apply scaling
            scaled_values = scaler.fit_transform(data_clean.values.reshape(-1, 1))
            scaled_data[column] = scaled_values.flatten()
            
            # Scaled statistics
            scaled_stats[column] = {
                'min': float(np.min(scaled_values)),
                'max': float(np.max(scaled_values)),
                'range': float(np.max(scaled_values) - np.min(scaled_values))
            }
        
        self.normalized_data['minmax_scaled'] = scaled_data
        return original_stats, scaled_stats

    def visualize_distributions(self, column, original_data, normalized_data, scaling_type):
        """
        Visualize distribution before and after normalization
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Original distribution
        sns.histplot(original_data, ax=ax1, kde=True)
        ax1.set_title(f'Original Distribution of {column}')
        ax1.set_xlabel('Value')
        ax1.set_ylabel('Frequency')
        
        # Normalized distribution
        sns.histplot(normalized_data, ax=ax2, kde=True)
        ax2.set_title(f'Normalized Distribution ({scaling_type})')
        ax2.set_xlabel('Normalized Value')
        ax2.set_ylabel('Frequency')
        
        plt.tight_layout()
        return fig

    def visualize_qq_plots(self, column, original_data, normalized_data):
        """
        Create Q-Q plots for original and normalized data
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Original Q-Q plot
        stats.probplot(original_data, dist="norm", plot=ax1)
        ax1.set_title(f'Q-Q Plot of Original {column}')
        
        # Normalized Q-Q plot
        stats.probplot(normalized_data, dist="norm", plot=ax2)
        ax2.set_title(f'Q-Q Plot of Normalized {column}')
        
        plt.tight_layout()
        return fig

    def compare_distributions(self):
        """
        Compare distributions of all normalized columns
        """
        for scaling_type, columns in self.prepare_columns().items():
            for column in columns:
                original_data = self.data[column].dropna()
                
                if scaling_type == 'standard_scaling':
                    normalized_data = self.normalized_data['standard_scaled'][column]
                else:
                    normalized_data = self.normalized_data['minmax_scaled'][column]
                
                # Distribution plots
                fig_dist = self.visualize_distributions(
                    column, original_data, normalized_data, scaling_type
                )
                
                # Q-Q plots
                fig_qq = self.visualize_qq_plots(
                    column, original_data, normalized_data
                )
                
                plt.show()

    def generate_summary_report(self):
        """
        Generate summary report of normalization results
        """
        standard_orig, standard_scaled = self.apply_standard_scaling()
        minmax_orig, minmax_scaled = self.apply_minmax_scaling()
        
        report = {
            'standard_scaling': {
                'original': standard_orig,
                'normalized': standard_scaled
            },
            'minmax_scaling': {
                'original': minmax_orig,
                'normalized': minmax_scaled
            }
        }
        
        return report

def main():
    # Load earthquake data
    data = pd.read_csv('earthquakes.csv')
    
    # Initialize normalizer
    normalizer = EarthquakeNormalization(data)
    
    # Generate and print summary report
    report = normalizer.generate_summary_report()
    print("Normalization Summary Report:")
    print(json.dumps(report, indent=2))
    
    # Visualize distributions
    normalizer.compare_distributions()

if __name__ == "__main__":
    main()