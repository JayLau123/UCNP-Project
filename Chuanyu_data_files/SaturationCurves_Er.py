import plotly.graph_objects as go
import numpy as np

class SaturationPlot:
    def __init__(self, data):
        """Initialize the class with data."""
        self.data = data

    def generate_plot(self, output_file=None):
        """
        Generate the saturation curves plot.
        
        Parameters:
        - output_file (str): Optional, path to save the plot as an HTML file.
        """
        # Prepare data for plotting
        percentages = sorted(self.data.keys())
        power_densities = sorted({k for subdict in self.data.values() for k in subdict.keys()})





        # sim_stats['red_avg_pop']
        # sim_stats['green_avg_pop'] 
        # sim_stats['green50_avg_pop'] 
        # sim_stats['green60_avg_pop'] 


        # green total
        fig1 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            green_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    green_values.append(self.data[percentage][power_density]['green_avg_pop'])
                else:
                    green_values.append(None)

            # Add traces for each color
            fig1.add_trace(go.Scatter(
                x=power_densities, y=green_values, mode='lines+markers', name=f'Green {percentage}',
                line=dict(color=f'rgb(0, {int(color * 255)}, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb(0, {int(color * 255)}, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig1.update_layout(
            title='Saturation Curves',
            xaxis=dict(
                title='Power Densities (W/cm²)',
                type='log',
                title_font=dict(size=18),
                tickfont=dict(size=18),
                showgrid=True,
                gridcolor='lightgrey'
            ),
            yaxis=dict(
                title='Brightness (pps)',
                type='log',
                title_font=dict(size=18),
                tickfont=dict(size=18),
                showgrid=True,
                gridcolor='lightgrey'
            ),
            legend_title='Percentages',
            width=1000, height=800,
            title_x=0.5,
            title_y=0.95,
            template='plotly_white'
        )

        fig1.show()




        # red total
        fig2 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            red_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    red_values.append(self.data[percentage][power_density]['red_avg_pop'])
                else:
                    red_values.append(None)

            # Add traces for each color
            fig2.add_trace(go.Scatter(
                x=power_densities, y=red_values, mode='lines+markers', name=f'Red {percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig2.update_layout(
            title='Saturation Curves',
            xaxis=dict(
                title='Power Densities (W/cm²)',
                type='log',
                title_font=dict(size=18),
                tickfont=dict(size=18),
                showgrid=True,
                gridcolor='lightgrey'
            ),
            yaxis=dict(
                title='Brightness (pps)',
                type='log',
                title_font=dict(size=18),
                tickfont=dict(size=18),
                showgrid=True,
                gridcolor='lightgrey'
            ),
            legend_title='Percentages',
            width=1000, height=800,
            title_x=0.5,
            title_y=0.95,
            template='plotly_white'
        )

        fig2.show()







        # # Save the plot if the output file is specified
        # if output_file:
        #     fig1.write_html(output_file)


# # Example usage
# if __name__ == "__main__":
#     myC = {
#         1: {
#             10: {'green_avg_pop': 100, 'red_avg_pop': 50},
#             100: {'green_avg_pop': 150, 'red_avg_pop': 75},
#             1000: {'green_avg_pop': 200, 'red_avg_pop': 100}
#         },
#         2: {
#             10: {'green_avg_pop': 120, 'red_avg_pop': 60},
#             100: {'green_avg_pop': 180, 'red_avg_pop': 90},
#             1000: {'green_avg_pop': 250, 'red_avg_pop': 125}
#         },
#         3: {
#             10: {'green_avg_pop': 130, 'red_avg_pop': 65},
#             100: {'green_avg_pop': 190, 'red_avg_pop': 95},
#             1000: {'green_avg_pop': 260, 'red_avg_pop': 130}
#         }
#     }

#     # Generate the saturation curves plot
#     saturation_plot = SaturationPlot(myC)
#     saturation_plot.generate_plot(output_file='saturation_plot.html')