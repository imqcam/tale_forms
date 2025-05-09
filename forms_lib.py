import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial import ConvexHull
import numpy as np


import pandas as pd

class forms:
    """
    This class retrieves data and generates plots such as convex hull plot and scatter plot from the IMQCAM database.
    """
    def __init__(self,client):
        result = client.get("entry", parameters={"formId": "67d39472366ec49ab59dd4db", "limit": 10000})
        self.df_org = pd.DataFrame([result[i]['data'] for i in range(len(result))])
        
    def show_data(self):
        """
        This function returns the data in a pandas DataFrame format.
        """
        return self.df_org.head()
    def scatter_plot(self):
        """
        This function retrieves and plots the scatter plot from the IMQCAM database.
        """
        df_temp=self.df_org.copy()
        df = self.df_org[(self.df_org["Elongation_Percent"]>0) & (self.df_org["Yield_Strength_MPa"]>910) & 
                         (self.df_org["Porosity_percent_infill"] < 0.1) & (self.df_org["Porosity_percent_infill"] > 0) ]
        
        x='Elongation_Percent'
        y='Yield_Strength_MPa'
        hue='DOE_ID'
        # Create a scatter plot with convex hulls
        if x is None or y is None or hue is None:
            print("Please select valid x, y, and hue values.")
            return
        else:
            plt.figure(figsize=(10, 6))
            sns.set(style="whitegrid")
            # Create scatter plot
            palette = sns.color_palette('bright'        , as_cmap=False, n_colors=len(hue)+1)
            sns.scatterplot(
                data=df,
                x=x,
                y=y,
                hue=hue,
                palette=palette,
                s=40,
                edgecolor='black',
                linewidth=0.5
            )
            plt.xlabel(x)
            plt.ylabel(y)
            plt.title(f'{x} vs {y} by {hue}')
            plt.legend(title=hue, bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.show()
            #plt.savefig('scatter_plot.png', dpi=300)
            #plt.show()
            #plt.savefig('scatter_plot.png', dpi=300)

    def convex_hull(self):
        """
        This function retrieves and plots the convex hull plot from the IMQCAM database.
        No argument is required.
        """
        df_temp=self.df_org.copy()
        #print(df_temp[df_temp.Elongation_Percent>0].head(10))
        df = self.df_org[(self.df_org["Elongation_Percent"]>0) & (self.df_org["Yield_Strength_MPa"]>910) & 
                        (self.df_org["Porosity_percent_infill"] < 0.1) & (self.df_org["Porosity_percent_infill"] > 0) ]
        
        x='Elongation_Percent'
        y='Yield_Strength_MPa'
        hue='DOE_ID'
        # Create a scatter plot with convex hulls
        if x is None or y is None or hue is None:
            print("Please select valid x, y, and hue values.")
            return
        else:
            plt.figure(figsize=(10, 6))
            sns.set(style="whitegrid")
            # Create scatter plot
            palette = sns.color_palette('bright'        , as_cmap=False, n_colors=len(hue)+1)
            sns.scatterplot(
                data=df,
                x=x,
                y=y,
                hue=hue,
                palette=palette,
                s=40,
                edgecolor='black',
                linewidth=0.5
            )
            # Draw convex hulls for each DOE_ID

            for key, group in df.groupby(hue):
                if len(group) >= 3:  # Need at least 3 points for a hull
                    points = group[[x, y]].values
                    hull = ConvexHull(points)
                    hull_points = points[hull.vertices]
                    plt.fill(hull_points[:, 0], hull_points[:, 1], alpha=0.2, 
                            #label=f"Group {key}", 
                            edgecolor='black')

            plt.xlabel(x)
            plt.ylabel(y)
            #plt.ylim(800,1200)
            plt.title(f'{x} vs {y} by {hue}')
            plt.legend(title=hue, bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.show()
        

