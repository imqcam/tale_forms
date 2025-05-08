import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial import ConvexHull
import numpy as np


class forms:
    """
    This class retrieves data and generates plots such as convex hull plot and scatter plot from the IMQCAM database.
    """

    def __init__(self, client):
        """
        Initializes the forms class and retrieves the data.
        """
        result = client.get("entry", parameters={"formId": "67d39472366ec49ab59dd4db", "limit": 10000})
        self.df_org = pd.DataFrame([result[i]['data'] for i in range(len(result))])

    def show_data(self):
        """
        This function returns the data in a pandas DataFrame format.
        """
        return self.df_org
    def convex_hull(self):
        """
        This function retrieves and plots the convex hull plot from the IMQCAM database.
        """
        df = self.df_org[(self.df_org.Elongation>0) & (self.df_org.Yield_Str>910) & 
                         (self.df_org.Porosity_percent_infill < 0.1) & 
                         (self.df. Porosity_percent_infill > 0) ]
        
        x='Elongation'
        y='Yield_Str'
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
        

