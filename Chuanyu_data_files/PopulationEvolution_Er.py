import plotly.graph_objects as go

class PopulationEvolutionPlot:
    def __init__(self, data, percentage, power_density):
        """Initialize the class with data, a specific percentage, and power density."""
        self.data = data
        self.percentage = percentage
        self.power_density = power_density

    def generate_plot(self, output_file=None):
        """
        Generate the population evolution plot.
        
        Parameters:
        - output_file (str): Optional, path to save the plot as an HTML file.
        """

        pop_evolution = self.data[self.percentage][self.power_density]['er_distribution']


        total_steps = max(len(values) for values in pop_evolution.values())
        steps = list(range(1, total_steps + 1))


        fig = go.Figure()

        for key, values in pop_evolution.items():
            fig.add_trace(go.Scatter(x=steps, y=values, mode='lines', name=f'Energy level {key}', marker=dict(size=3)))

   
        fig.update_xaxes(
            title_text='Simulation Steps (Real time = step * 1us)',
            title_font=dict(size=20, color='black'),
            tickfont=dict(size=20),
            showgrid=True,
            gridwidth=2,
            gridcolor='white'
        )
        fig.update_yaxes(
            title_text='Population',
            title_font=dict(size=20, color='black'),
            tickfont=dict(size=20),
            showgrid=True,
            gridwidth=2,
            gridcolor='white'
        )
        fig.update_layout(
            title_text=f'Population Evolution of All Energy Levels',
            title_font=dict(size=20, family="Arial, sans-serif", color='black'),
            width=2000,
            height=500,
            title_x=0.5,
            title_y=0.95,
            showlegend=True,
            margin=dict(l=20, r=20, b=20, t=70),
            legend_title='Energy level',
            legend=dict(
                font=dict(
                    size=20,
                    family="Arial, sans-serif"
                )
            )
        )

        fig.show()

        # Save the plot if the output file is specified
        if output_file:
            fig.write_html(output_file)


# # Example usage
# if __name__ == "__main__":
#     myC = {
#         0.02: {
#             3 * 10**4: {
#                 'tm_distribution': {
#                     'Level 1': [0.1, 0.15, 0.2, 0.25, 0.3],
#                     'Level 2': [0.05, 0.07, 0.09, 0.11, 0.13],
#                     'Level 3': [0.02, 0.03, 0.04, 0.05, 0.06]
#                 }
#             }
#         }
#     }

#     percentage = 0.02
#     power_density = 3 * 10**4
#     pop_plot = PopulationEvolutionPlot(myC, percentage, power_density)
#     pop_plot.generate_plot(output_file='population_evolution_plot.html')
