print('Successfully import:')
print()
print('class Er_EnergyLevelDiagram(ion_name, energy_levels)')
print('class Er_EnergyLevelDiagramArrow(ion_name, energy_levels, ED_transitions, MD_transitions)')
print()



import plotly.graph_objects as go

class Er_EnergyLevelDiagram:

    def __init__(self, ion_name, energy_levels):
        """
        Initialize the EnergyLevelDiagram with a dictionary of energy levels.
        
        :param energy_levels: A dictionary with levels as keys and energy values as values.
        """
        self.ion_name = ion_name
        self.energy_levels = energy_levels

    def plot_diagram(self):
        """
        Generate and display the energy level diagram using Plotly.
        """
        # Create the figure
        fig = go.Figure()

        # Add a line for each energy level
        for level, energy in sorted(self.energy_levels.items(), key=lambda item: item[1]):
            fig.add_trace(go.Scatter(
                x=[0, 1],  # Use constant x-values to draw horizontal lines
                y=[energy, energy],  # Start and end y-values for each line
                mode='lines',
                line=dict(color='black', width=2),  # Set line color to black and width
                showlegend=False  # No legend for each line
            ))

        # Update the layout to display energy values on y-axis
        fig.update_layout(
            title=f'{self.ion_name} Energy Level Diagram',
            title_x=0.5,
            title_y=0.95,
            title_font=dict(size=20),
            yaxis_title='Energy (cm⁻¹)',
            yaxis=dict(
                type='linear',
                autorange=True,
                tickmode='array',
                tickvals=list(self.energy_levels.values()),  # Only show ticks at the energy levels
                ticktext=[f"{level}: {energy}" for level, energy in sorted(self.energy_levels.items(), key=lambda item: item[1])],
                tickfont=dict(size=13),
                title_font=dict(size=20)
            ),
            width=1100,  # Set the width of the figure
            height=1100,  # Set the height of the figure
            plot_bgcolor='white',  # Set the background color to white
            xaxis_showgrid=False,  # Remove the x-axis grid
            yaxis_showgrid=False,  # Remove the y-axis grid
            xaxis=dict(
                tickmode='array',
                tickvals=[]  # No tick values on the x-axis
            )
        )

        # Display the figure
        fig.show()





class Er_EnergyLevelDiagramArrow:

    def __init__(self, ion_name, energy_levels, ED_transitions, MD_transitions):
        """
        Initialize the EnergyLevelDiagramArrow with energy levels and transitions and
        automatically generate and display the energy level diagram.
        
        :param energy_levels: A dictionary with levels as keys and energy values as values.
        :param transitions: A nested dictionary with colors as keys and dictionaries of transitions and wavelengths as values.
        """
        self.ion_name = ion_name
        self.energy_levels = energy_levels
        self.transitions_MD = MD_transitions
        self.transitions = ED_transitions
        self.energy_levels_arrow = {key: value + 350 for key, value in self.energy_levels.items()}
        self.fig = go.Figure()

        # mpr start point
        self.x_start_2 = 0.05

        # MD start point
        self.x_start_3 = 0.1
        self.x_step_3 = 0.03

        # ED start point
        self.x_start = 0.4
        self.x_step = 0.03
        
        
        self.add_energy_levels()

        self.add_mpr() # MPR transition

        self.add_MD() # MD transition

        self.add_ED() # ED transition
        
        self.add_legend_traces()
        self.plot()

    def add_energy_levels(self):
        """Add energy level lines to the plot."""
        for level, energy in sorted(self.energy_levels.items(), key=lambda item: item[1]):
            self.fig.add_trace(go.Scatter(
                x=[0, 1],
                y=[energy, energy],
                mode='lines',
                line=dict(color='black', width=2),
                showlegend=False
            ))

    def add_mpr(self):
        """Add arrows for transitions based on the provided transitions dictionary."""

        
        for i, key in enumerate(self.energy_levels):

            if i<15:

                start_level = key
                end_level = list(self.energy_levels.keys())[i+1]
                i+=1

                self.fig.add_annotation(
                        x=self.x_start_2,
                        y=self.energy_levels[start_level],
                        xref="x",
                        yref="y",
                        ax=self.x_start_2,
                        ay=self.energy_levels[end_level],
                        axref="x",
                        ayref="y",
                        showarrow=True,
                        text="",
                        font=dict(size=10, color="orange"),
                        arrowhead=3,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor='orange'
                    )
    
    def add_MD(self):
        """Add arrows for transitions based on the provided MD transitions dictionary."""

        offset = 0

        for i in self.transitions_MD:

            start_level = i[0][0]
            end_level = i[1][0]


            self.fig.add_annotation(
                    x=self.x_start_3 + offset,
                    y=self.energy_levels[start_level],
                    xref="x",
                    yref="y",
                    ax=self.x_start_3 + offset,
                    ay=self.energy_levels[end_level],
                    axref="x",
                    ayref="y",
                    showarrow=True,
                    text="",
                    font=dict(size=10, color="black"),
                    arrowhead=3,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor='black'
                )
            offset += self.x_step_3

    def add_ED(self):
        """Add arrows for transitions based on the provided ED transitions dictionary."""
        offset = 0
        for color, color_transitions in self.transitions.items():
            for transition, wavelength in color_transitions.items():
                end_level, start_level = transition[:transition.find('E', 1)], transition[transition.find('E', 1):]


                # transition_string = "E9(1I6)E6(1G4)"

                # # Find first 'E'
                # first_E_index = transition_string.find('E')  # Returns 0, the index of the first 'E'

                # # Find second 'E'
                # split_index = transition_string.find('E', first_E_index+1)  # Starts looking from index 1, finds 'E' at index 7

                # print("Index of first 'E':", first_E_index)   # Output: 0
                # print("Index of second 'E':", split_index)    # Output: 7

                self.fig.add_annotation(
                        x=self.x_start + offset,
                        y=self.energy_levels[start_level],
                        xref="x",
                        yref="y",
                        ax=self.x_start + offset,
                        ay=self.energy_levels_arrow[end_level],
                        axref="x",
                        ayref="y",
                        showarrow=True,
                        text=f"{round(wavelength)}",
                        font=dict(size=10, color="black"),
                        arrowhead=3,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor=color
                    )
                offset += self.x_step
    


    def add_legend_traces(self):
        """Add invisible traces to the plot for legend purposes."""
        for color in self.transitions:
            self.fig.add_trace(go.Scatter(
                x=[None],
                y=[None],
                mode='lines',
                name=f'{color.capitalize()} emission (Selected ED)',
                line=dict(color=color, width=2)
            ))

        self.fig.add_trace(go.Scatter(
                x=[None],
                y=[None],
                mode='lines',
                name='MPR',
                line=dict(color='orange', width=2)
            ))
        
        self.fig.add_trace(go.Scatter(
                x=[None],
                y=[None],
                mode='lines',
                name='MD',
                line=dict(color='black', width=2)
            ))


    def plot(self):
        """Configure and display the complete figure."""
        self.fig.update_layout(
            title=f'{self.ion_name} Energy Level Diagram',
            title_x=0.4,
            title_y=0.95,
            title_font=dict(size=20),
            yaxis_title='Energy (cm⁻¹)',
            yaxis=dict(
                type='linear',
                autorange=True,
                tickmode='array',
                tickvals=list(self.energy_levels.values()),
                ticktext=[f"{level}: {energy}" for level, energy in sorted(self.energy_levels.items(), key=lambda item: item[1])],
                tickfont=dict(size=13),
                title_font=dict(size=20)
            ),
            width=1500,
            height=1100,
            plot_bgcolor='white',
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            showlegend=True,  # Enable legend
            xaxis=dict(tickmode='array', tickvals=[])
        )
        self.fig.show()


