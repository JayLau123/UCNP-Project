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



    #   red40 = 0
    #             red71 = 0
    #             red81 = 0
    #             red91 = 0
    #             red10_2 = 0
    #             red11_2 = 0
    #             red11_3 = 0
    #             red12_3 = 0
    #             red13_3 = 0
    #             red14_3 = 0
    #             red15_4 = 0


    #             green50 = 0
    #             green60 = 0
    #             green10_1 = 0
    #             green11_1 = 0
    #             green12_2 = 0
    #             green13_2 = 0
    #             green14_2 = 0
    #             green15_3 = 0


################################ green total

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
            title='Saturation Curves(green total)',
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


############################### green50

        
        fig2 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            green_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    green_values.append(self.data[percentage][power_density]['green50_avg_pop'])
                else:
                    green_values.append(None)

            # Add traces for each color
            fig2.add_trace(go.Scatter(
                x=power_densities, y=green_values, mode='lines+markers', name=f'Green {percentage}',
                line=dict(color=f'rgb(0, {int(color * 255)}, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb(0, {int(color * 255)}, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig2.update_layout(
            title='Saturation Curves(green50)',
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


############################### green60


        # green total
        fig3 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            green_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    green_values.append(self.data[percentage][power_density]['green60_avg_pop'])
                else:
                    green_values.append(None)

            # Add traces for each color
            fig3.add_trace(go.Scatter(
                x=power_densities, y=green_values, mode='lines+markers', name=f'Green {percentage}',
                line=dict(color=f'rgb(0, {int(color * 255)}, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb(0, {int(color * 255)}, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig3.update_layout(
            title='Saturation Curves(green60)',
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

        fig3.show()


############################### green10_1


        # green total
        fig4 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            green_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    green_values.append(self.data[percentage][power_density]['green10_1_avg_pop'])
                else:
                    green_values.append(None)

            # Add traces for each color
            fig4.add_trace(go.Scatter(
                x=power_densities, y=green_values, mode='lines+markers', name=f'Green {percentage}',
                line=dict(color=f'rgb(0, {int(color * 255)}, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb(0, {int(color * 255)}, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig4.update_layout(
            title='Saturation Curves(green10_1)',
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

        fig4.show()


############################### green11_1


        # green total
        fig5 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            green_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    green_values.append(self.data[percentage][power_density]['green11_1_avg_pop'])
                else:
                    green_values.append(None)

            # Add traces for each color
            fig5.add_trace(go.Scatter(
                x=power_densities, y=green_values, mode='lines+markers', name=f'Green {percentage}',
                line=dict(color=f'rgb(0, {int(color * 255)}, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb(0, {int(color * 255)}, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig5.update_layout(
            title='Saturation Curves(green60)',
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

        fig5.show()



############################### green12_2


        # green total
        fig6 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            green_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    green_values.append(self.data[percentage][power_density]['green12_2_avg_pop'])
                else:
                    green_values.append(None)

            # Add traces for each color
            fig6.add_trace(go.Scatter(
                x=power_densities, y=green_values, mode='lines+markers', name=f'Green {percentage}',
                line=dict(color=f'rgb(0, {int(color * 255)}, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb(0, {int(color * 255)}, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig6.update_layout(
            title='Saturation Curves(green12_2)',
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

        fig6.show()


############################### green13_2


        # green total
        fig7 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            green_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    green_values.append(self.data[percentage][power_density]['green13_2_avg_pop'])
                else:
                    green_values.append(None)

            # Add traces for each color
            fig7.add_trace(go.Scatter(
                x=power_densities, y=green_values, mode='lines+markers', name=f'Green {percentage}',
                line=dict(color=f'rgb(0, {int(color * 255)}, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb(0, {int(color * 255)}, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig7.update_layout(
            title='Saturation Curves(green13_2)',
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

        fig7.show()



############################### green14_2


        # green total
        fig8 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            green_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    green_values.append(self.data[percentage][power_density]['green14_2_avg_pop'])
                else:
                    green_values.append(None)

            # Add traces for each color
            fig8.add_trace(go.Scatter(
                x=power_densities, y=green_values, mode='lines+markers', name=f'Green {percentage}',
                line=dict(color=f'rgb(0, {int(color * 255)}, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb(0, {int(color * 255)}, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig8.update_layout(
            title='Saturation Curves(green14_2)',
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

        fig8.show()


############################### green15_3


        # green total
        fig9 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            green_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    green_values.append(self.data[percentage][power_density]['green15_3_avg_pop'])
                else:
                    green_values.append(None)

            # Add traces for each color
            fig9.add_trace(go.Scatter(
                x=power_densities, y=green_values, mode='lines+markers', name=f'Green {percentage}',
                line=dict(color=f'rgb(0, {int(color * 255)}, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb(0, {int(color * 255)}, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig9.update_layout(
            title='Saturation Curves(green15_3)',
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

        fig9.show()




############################### red total


        fig10 = go.Figure()
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
            fig10.add_trace(go.Scatter(
                x=power_densities, y=red_values, mode='lines+markers', name=f'Red {percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig10.update_layout(
            title='Saturation Curves(red total)',
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

        fig10.show()


############################### red40


        fig11 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            red_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    red_values.append(self.data[percentage][power_density]['red40_avg_pop'])
                else:
                    red_values.append(None)

            # Add traces for each color
            fig11.add_trace(go.Scatter(
                x=power_densities, y=red_values, mode='lines+markers', name=f'Red {percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig11.update_layout(
            title='Saturation Curves(red40)',
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

        fig11.show()

############################### red71


        fig12 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            red_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    red_values.append(self.data[percentage][power_density]['red71_avg_pop'])
                else:
                    red_values.append(None)

            # Add traces for each color
            fig12.add_trace(go.Scatter(
                x=power_densities, y=red_values, mode='lines+markers', name=f'Red {percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig12.update_layout(
            title='Saturation Curves(red71)',
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

        fig12.show()

        ############################### red81


        fig13 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            red_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    red_values.append(self.data[percentage][power_density]['red81_avg_pop'])
                else:
                    red_values.append(None)

            # Add traces for each color
            fig13.add_trace(go.Scatter(
                x=power_densities, y=red_values, mode='lines+markers', name=f'Red {percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig13.update_layout(
            title='Saturation Curves(red81)',
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

        fig13.show()

        ############################### red91


        fig14 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            red_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    red_values.append(self.data[percentage][power_density]['red91_avg_pop'])
                else:
                    red_values.append(None)

            # Add traces for each color
            fig14.add_trace(go.Scatter(
                x=power_densities, y=red_values, mode='lines+markers', name=f'Red {percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig14.update_layout(
            title='Saturation Curves(red91)',
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

        fig14.show()


        ############################### red10_2


        fig15 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            red_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    red_values.append(self.data[percentage][power_density]['red10_2_avg_pop'])
                else:
                    red_values.append(None)

            # Add traces for each color
            fig15.add_trace(go.Scatter(
                x=power_densities, y=red_values, mode='lines+markers', name=f'Red {percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig15.update_layout(
            title='Saturation Curves(red10_2)',
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

        fig15.show()

        ############################### red11_2


        fig16 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            red_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    red_values.append(self.data[percentage][power_density]['red11_2_avg_pop'])
                else:
                    red_values.append(None)

            # Add traces for each color
            fig16.add_trace(go.Scatter(
                x=power_densities, y=red_values, mode='lines+markers', name=f'Red {percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig16.update_layout(
            title='Saturation Curves(red11_2)',
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

        fig16.show()

        ############################### red11_3


        fig17 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            red_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    red_values.append(self.data[percentage][power_density]['red11_3_avg_pop'])
                else:
                    red_values.append(None)

            # Add traces for each color
            fig17.add_trace(go.Scatter(
                x=power_densities, y=red_values, mode='lines+markers', name=f'Red {percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig17.update_layout(
            title='Saturation Curves(red11_3)',
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

        fig17.show()

        ############################### red12_3


        fig18 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            red_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    red_values.append(self.data[percentage][power_density]['red12_3_avg_pop'])
                else:
                    red_values.append(None)

            # Add traces for each color
            fig18.add_trace(go.Scatter(
                x=power_densities, y=red_values, mode='lines+markers', name=f'Red {percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig18.update_layout(
            title='Saturation Curves(red12_3)',
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

        fig18.show()

        ############################### red13_3


        fig19 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            red_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    red_values.append(self.data[percentage][power_density]['red13_3_avg_pop'])
                else:
                    red_values.append(None)

            # Add traces for each color
            fig19.add_trace(go.Scatter(
                x=power_densities, y=red_values, mode='lines+markers', name=f'Red {percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig19.update_layout(
            title='Saturation Curves(red13_3)',
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

        fig19.show()


        ############################### red14_3


        fig20 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            red_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    red_values.append(self.data[percentage][power_density]['red14_3_avg_pop'])
                else:
                    red_values.append(None)

            # Add traces for each color
            fig20.add_trace(go.Scatter(
                x=power_densities, y=red_values, mode='lines+markers', name=f'Red {percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig20.update_layout(
            title='Saturation Curves(14_3)',
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

        fig20.show()

        ############################### red15_4


        fig21 = go.Figure()
        colors = np.linspace(0, 1, len(self.data))

        # Iterate through each percentage to add traces to the plot
        for i, percentage in enumerate(percentages):
            red_values = []
            color = colors[i]
            for power_density in power_densities:
                if power_density in self.data[percentage]:
                    red_values.append(self.data[percentage][power_density]['red15_4_avg_pop'])
                else:
                    red_values.append(None)

            # Add traces for each color
            fig21.add_trace(go.Scatter(
                x=power_densities, y=red_values, mode='lines+markers', name=f'Red {percentage}',
                line=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})'),
                marker=dict(color=f'rgb({int(color * 255)}, 0, {int((1 - color) * 255)})', size=8),
            ))

        # Update layout
        fig21.update_layout(
            title='Saturation Curves(15_4)',
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

        fig21.show()










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