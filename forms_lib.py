import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial import ConvexHull
import numpy as np
import matplotlib.patches as mpatches  # Needed for legend bars

class forms:
    """
    This class retrieves data and generates plots such as convex hull plot and scatter plot from the IMQCAM database.
    """
    def __init__(self, client):
        result = client.get("entry", parameters={"formId": "67d39472366ec49ab59dd4db", "limit": 10000})
        self.df_org = pd.DataFrame([result[i]['data'] for i in range(len(result))])
        
    def show_data(self):
        return self.df_org.head()

    def scatter_plot(self):
        df = self.df_org[(self.df_org["Elongation_Percent"]>0) & (self.df_org["Yield_Strength_MPa"]>910) & 
                         (self.df_org["Porosity_percent_infill"] < 0.1) & (self.df_org["Porosity_percent_infill"] > 0) ]
        x = 'Elongation_Percent'
        y = 'Yield_Strength_MPa'
        hue = 'DOE_ID'
        plt.figure(figsize=(10, 6))
        sns.set(style="whitegrid")
        sns.scatterplot(data=df, x=x, y=y, hue=hue, s=40, edgecolor='black', linewidth=0.5)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(f'{x} vs {y} by {hue}')
        plt.legend(title=hue, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

    def convex_hull(self):
        df = self.df_org[(self.df_org["Elongation_Percent"]>0) & (self.df_org["Yield_Strength_MPa"]>910) & 
                         (self.df_org["Porosity_percent_infill"] < 0.1) & (self.df_org["Porosity_percent_infill"] > 0) ]
        x = 'Elongation_Percent'
        y = 'Yield_Strength_MPa'
        hue = 'DOE_ID'
        plt.figure(figsize=(10, 6))
        sns.set(style="whitegrid")
        sns.scatterplot(data=df, x=x, y=y, hue=hue, s=40, edgecolor='black', linewidth=0.5)
        for key, group in df.groupby(hue):
            if len(group) >= 3:
                points = group[[x, y]].values
                hull = ConvexHull(points)
                hull_points = points[hull.vertices]
                plt.fill(hull_points[:, 0], hull_points[:, 1], alpha=0.2, edgecolor='black')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(f'{x} vs {y} by {hue}')
        plt.legend(title=hue, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

    def plot_porosity_vs_ved(self):  # ← this must have 'self'
        color_map = {
            1: 'purple',
            2: 'green',
            3: 'yellow'
        }
        fig, ax = plt.subplots(figsize=(8, 6))
        for doe_id, color in color_map.items():
            subset = self.df_org[
                (self.df_org['DOE_Code'] == doe_id) & 
                (self.df_org['Porosity_percent_infill'] > 0)
            ]
            ax.scatter(
                subset['VED_J_per_mm3'],
                subset['Porosity_percent_infill'],
                color=color,
                edgecolors='black',
                alpha=0.7
            )
        ax.set_xlabel('Volumetric Energy Density (J/mm³)')
        ax.set_ylabel('Infill Porosity (%)')
        ax.set_title('Porosity vs VED Colored by DOE ID')
        ax.set_ylim(-1, 5)

        # Add legend bar manually
        import matplotlib.patches as mpatches
        bar_ax = fig.add_axes([0.88, 0.25, 0.03, 0.5])
        for i, (doe_id, color) in enumerate(reversed(color_map.items())):
            bar_ax.add_patch(mpatches.Rectangle((0, i), 1, 1, color=color))
            bar_ax.text(1.2, i + 0.5, f'DOE ID {doe_id}', va='center')
        bar_ax.set_xlim(-1, 1)
        bar_ax.set_ylim(-1, len(color_map))
        bar_ax.axis('off')

        plt.tight_layout(rect=[0, 0, 0.85, 1])
        plt.show()

