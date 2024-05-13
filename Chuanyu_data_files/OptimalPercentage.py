import plotly.graph_objects as go

class SinglePowerDensityPlot:
    def __init__(self, data, selected_power_density):
        """Initialize the class with data and a selected power density."""
        self.data = data
        self.selected_power_density = selected_power_density

    def generate_plot(self, output_file=None):
        """
        Generate the single power density plot.
        
        Parameters:
        - output_file (str): Optional, path to save the plot as an HTML file.
        """

        percentages = sorted(self.data.keys())
        
        Red = []
        Green = []

    
        for percentage in percentages:
            if self.selected_power_density in self.data[percentage]:
                red_value = self.data[percentage][self.selected_power_density]['red_avg_pop']
                Red.append(red_value)
                green_value = self.data[percentage][self.selected_power_density]['green_avg_pop']
                Green.append(green_value)


        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=percentages, y=Red, mode='lines+markers', name='Red emission', line=dict(color='red'), marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=percentages, y=Green, mode='lines+markers', name='Green emission', line=dict(color='green'), marker=dict(size=8)
        ))


        fig.update_layout(
            title=f'Brightness vs. Percentage at Power Density {self.selected_power_density} W/cm²',
            xaxis=dict(
                title='Er Percentages',
                type='linear',
                title_font=dict(size=18),
                tickfont=dict(size=18),
                showgrid=True,
                gridcolor='lightgrey'
            ),
            yaxis=dict(
                title='Brightness (pps)',
                type='linear',
                title_font=dict(size=18),
                tickfont=dict(size=18),
                showgrid=True,
                gridcolor='lightgrey'
            ),
            width=1000, height=600,
            title_x=0.5,
            title_y=0.95,
            template='plotly_white'
        )

   
        fig.show()

        # Save the plot if the output file is specified
        if output_file:
            fig.write_html(output_file)

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

#     selected_power_density = 100
#     single_plot = SinglePowerDensityPlot(myC, selected_power_density)
#     single_plot.generate_plot(output_file='single_power_density_plot.html')