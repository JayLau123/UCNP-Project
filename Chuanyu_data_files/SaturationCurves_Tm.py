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



        ################################################################################## NIR total

        fig1 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            NIR_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    NIR_values.append(self.data[percentage][power_density]['NIR_avg_pop'])
                else:
                    NIR_values.append(None)

            # Add traces for each color
            fig1.add_trace(go.Scatter(
                x=power_densities, y=NIR_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig1.update_layout(
            title='Saturation Curves(NIR30+NIR62+NIR75)',
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

        # # Save the plot if the output file is specified
        # if output_file:
        #     fig1.write_html(output_file)

        ################################################################################## NIR30

        fig1 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            NIR_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    NIR_values.append(self.data[percentage][power_density]['NIR30_avg_pop'])
                else:
                    NIR_values.append(None)

            # Add traces for each color
            fig1.add_trace(go.Scatter(
                x=power_densities, y=NIR_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig1.update_layout(
            title='Saturation Curves(NIR30)',
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

        # # Save the plot if the output file is specified
        # if output_file:
        #     fig1.write_html(output_file)


        ################################################################################## NIR62

        fig1 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            NIR_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    NIR_values.append(self.data[percentage][power_density]['NIR62_avg_pop'])
                else:
                    NIR_values.append(None)

            # Add traces for each color
            fig1.add_trace(go.Scatter(
                x=power_densities, y=NIR_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig1.update_layout(
            title='Saturation Curves(NIR62)',
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

        # # Save the plot if the output file is specified
        # if output_file:
        #     fig1.write_html(output_file)

        ################################################################################## NIR74

        fig1 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            NIR_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    NIR_values.append(self.data[percentage][power_density]['NIR74_avg_pop'])
                else:
                    NIR_values.append(None)

            # Add traces for each color
            fig1.add_trace(go.Scatter(
                x=power_densities, y=NIR_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig1.update_layout(
            title='Saturation Curves(NIR74)',
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

        # # Save the plot if the output file is specified
        # if output_file:
        #     fig1.write_html(output_file)


        ################################################################################## NIR75

        fig1 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            NIR_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    NIR_values.append(self.data[percentage][power_density]['NIR75_avg_pop'])
                else:
                    NIR_values.append(None)

            # Add traces for each color
            fig1.add_trace(go.Scatter(
                x=power_densities, y=NIR_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig1.update_layout(
            title='Saturation Curves(NIR75)',
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

        # # Save the plot if the output file is specified
        # if output_file:
        #     fig1.write_html(output_file)

        ################################################################################## NIR86

        fig1 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            NIR_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    NIR_values.append(self.data[percentage][power_density]['NIR86_avg_pop'])
                else:
                    NIR_values.append(None)

            # Add traces for each color
            fig1.add_trace(go.Scatter(
                x=power_densities, y=NIR_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig1.update_layout(
            title='Saturation Curves(NIR86)',
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

        # # Save the plot if the output file is specified
        # if output_file:
        #     fig1.write_html(output_file)


        ################################################################################## NIR96

        fig1 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            NIR_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    NIR_values.append(self.data[percentage][power_density]['NIR96_avg_pop'])
                else:
                    NIR_values.append(None)

            # Add traces for each color
            fig1.add_trace(go.Scatter(
                x=power_densities, y=NIR_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig1.update_layout(
            title='Saturation Curves(NIR96)',
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

        # # Save the plot if the output file is specified
        # if output_file:
        #     fig1.write_html(output_file)


        ################################################################################## blue total

        fig2 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            blue_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    blue_values.append(self.data[percentage][power_density]['blue_avg_pop'])
                else:
                    blue_values.append(None)

            # Add traces for each color
            fig2.add_trace(go.Scatter(
                x=power_densities, y=blue_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',

                # keeping blue as the predominant color, update these lines to control the blue and green components
                line=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})'),
                marker=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})', size=8),
            ))

        # Update layout
        fig2.update_layout(
            title='Saturation Curves(blue60+blue71+blue83+blue10_4+blue10_5)',
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
        #     fig2.write_html(output_file)


        ################################################################################## blue60

        fig2 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            blue_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    blue_values.append(self.data[percentage][power_density]['blue60_avg_pop'])
                else:
                    blue_values.append(None)

            # Add traces for each color
            fig2.add_trace(go.Scatter(
                x=power_densities, y=blue_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',

                # keeping blue as the predominant color, update these lines to control the blue and green components
                line=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})'),
                marker=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})', size=8),
            ))

        # Update layout
        fig2.update_layout(
            title='Saturation Curves(blue60)',
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
        #     fig2.write_html(output_file)

        ################################################################################## blue71

        fig2 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            blue_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    blue_values.append(self.data[percentage][power_density]['blue71_avg_pop'])
                else:
                    blue_values.append(None)

            # Add traces for each color
            fig2.add_trace(go.Scatter(
                x=power_densities, y=blue_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',

                # keeping blue as the predominant color, update these lines to control the blue and green components
                line=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})'),
                marker=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})', size=8),
            ))

        # Update layout
        fig2.update_layout(
            title='Saturation Curves(blue71)',
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
        #     fig2.write_html(output_file)

        ################################################################################## blue72

        fig2 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            blue_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    blue_values.append(self.data[percentage][power_density]['blue72_avg_pop'])
                else:
                    blue_values.append(None)

            # Add traces for each color
            fig2.add_trace(go.Scatter(
                x=power_densities, y=blue_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',

                # keeping blue as the predominant color, update these lines to control the blue and green components
                line=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})'),
                marker=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})', size=8),
            ))

        # Update layout
        fig2.update_layout(
            title='Saturation Curves(blue72)',
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
        #     fig2.write_html(output_file)



        ################################################################################## blue83

        fig2 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            blue_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    blue_values.append(self.data[percentage][power_density]['blue83_avg_pop'])
                else:
                    blue_values.append(None)

            # Add traces for each color
            fig2.add_trace(go.Scatter(
                x=power_densities, y=blue_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',

                # keeping blue as the predominant color, update these lines to control the blue and green components
                line=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})'),
                marker=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})', size=8),
            ))

        # Update layout
        fig2.update_layout(
            title='Saturation Curves(blue83)',
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
        #     fig2.write_html(output_file)

        ################################################################################## blue84

        fig2 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            blue_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    blue_values.append(self.data[percentage][power_density]['blue84_avg_pop'])
                else:
                    blue_values.append(None)

            # Add traces for each color
            fig2.add_trace(go.Scatter(
                x=power_densities, y=blue_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',

                # keeping blue as the predominant color, update these lines to control the blue and green components
                line=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})'),
                marker=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})', size=8),
            ))

        # Update layout
        fig2.update_layout(
            title='Saturation Curves(blue84)',
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
        #     fig2.write_html(output_file)

        ################################################################################## blue85

        fig2 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            blue_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    blue_values.append(self.data[percentage][power_density]['blue85_avg_pop'])
                else:
                    blue_values.append(None)

            # Add traces for each color
            fig2.add_trace(go.Scatter(
                x=power_densities, y=blue_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',

                # keeping blue as the predominant color, update these lines to control the blue and green components
                line=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})'),
                marker=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})', size=8),
            ))

        # Update layout
        fig2.update_layout(
            title='Saturation Curves(blue85)',
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
        #     fig2.write_html(output_file)

        ################################################################################## blue93

        fig2 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            blue_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    blue_values.append(self.data[percentage][power_density]['blue93_avg_pop'])
                else:
                    blue_values.append(None)

            # Add traces for each color
            fig2.add_trace(go.Scatter(
                x=power_densities, y=blue_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',

                # keeping blue as the predominant color, update these lines to control the blue and green components
                line=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})'),
                marker=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})', size=8),
            ))

        # Update layout
        fig2.update_layout(
            title='Saturation Curves(blue93)',
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
        #     fig2.write_html(output_file)

        ################################################################################## blue94

        fig2 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            blue_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    blue_values.append(self.data[percentage][power_density]['blue94_avg_pop'])
                else:
                    blue_values.append(None)

            # Add traces for each color
            fig2.add_trace(go.Scatter(
                x=power_densities, y=blue_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',

                # keeping blue as the predominant color, update these lines to control the blue and green components
                line=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})'),
                marker=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})', size=8),
            ))

        # Update layout
        fig2.update_layout(
            title='Saturation Curves(blue94)',
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
        #     fig2.write_html(output_file)

        ################################################################################## blue95

        fig2 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            blue_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    blue_values.append(self.data[percentage][power_density]['blue95_avg_pop'])
                else:
                    blue_values.append(None)

            # Add traces for each color
            fig2.add_trace(go.Scatter(
                x=power_densities, y=blue_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',

                # keeping blue as the predominant color, update these lines to control the blue and green components
                line=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})'),
                marker=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})', size=8),
            ))

        # Update layout
        fig2.update_layout(
            title='Saturation Curves(blue95)',
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
        #     fig2.write_html(output_file)

        ################################################################################## blue10_3

        fig2 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            blue_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    blue_values.append(self.data[percentage][power_density]['blue10_3_avg_pop'])
                else:
                    blue_values.append(None)

            # Add traces for each color
            fig2.add_trace(go.Scatter(
                x=power_densities, y=blue_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',

                # keeping blue as the predominant color, update these lines to control the blue and green components
                line=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})'),
                marker=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})', size=8),
            ))

        # Update layout
        fig2.update_layout(
            title='Saturation Curves(blue10_3)',
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
        #     fig2.write_html(output_file)


        ################################################################################## blue10_4

        fig2 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            blue_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    blue_values.append(self.data[percentage][power_density]['blue10_4_avg_pop'])
                else:
                    blue_values.append(None)

            # Add traces for each color
            fig2.add_trace(go.Scatter(
                x=power_densities, y=blue_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',

                # keeping blue as the predominant color, update these lines to control the blue and green components
                line=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})'),
                marker=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})', size=8),
            ))

        # Update layout
        fig2.update_layout(
            title='Saturation Curves(blue10_4)',
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
        #     fig2.write_html(output_file)



        ################################################################################## blue10_5

        fig2 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            blue_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    blue_values.append(self.data[percentage][power_density]['blue10_5_avg_pop'])
                else:
                    blue_values.append(None)

            # Add traces for each color
            fig2.add_trace(go.Scatter(
                x=power_densities, y=blue_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',

                # keeping blue as the predominant color, update these lines to control the blue and green components
                line=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})'),
                marker=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})', size=8),
            ))

        # Update layout
        fig2.update_layout(
            title='Saturation Curves(blue10_5)',
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
        #     fig2.write_html(output_file)

        ################################################################################## blue11_4

        fig2 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            blue_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    blue_values.append(self.data[percentage][power_density]['blue11_4_avg_pop'])
                else:
                    blue_values.append(None)

            # Add traces for each color
            fig2.add_trace(go.Scatter(
                x=power_densities, y=blue_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',

                # keeping blue as the predominant color, update these lines to control the blue and green components
                line=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})'),
                marker=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})', size=8),
            ))

        # Update layout
        fig2.update_layout(
            title='Saturation Curves(blue11_4)',
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
        #     fig2.write_html(output_file)

        ################################################################################## blue11_5

        fig2 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        for i, percentage in enumerate(percentages):
            blue_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    blue_values.append(self.data[percentage][power_density]['blue11_5_avg_pop'])
                else:
                    blue_values.append(None)

            # Add traces for each color
            fig2.add_trace(go.Scatter(
                x=power_densities, y=blue_values, mode='lines+markers', name=f'Tm={percentage}, Yb={1-percentage}',

                # keeping blue as the predominant color, update these lines to control the blue and green components
                line=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})'),
                marker=dict(color=f'rgb(0, {int((1 - color) * 255)}, {int(color * 255)})', size=8),
            ))

        # Update layout
        fig2.update_layout(
            title='Saturation Curves(blue11_5)',
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
        #     fig2.write_html(output_file)






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