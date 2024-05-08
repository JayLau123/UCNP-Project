# shape of lattice based on https://www.nature.com/articles/s41598-018-19415-w and
    # https://www.researchgate.net/publication/253240215_Enhancement_of_blue_upconversion_luminescence_in_hexagonal_NaYF_4_YbTm_by_using_K_and_Sc_ions?enrichId=rgreq-ded66b2e7d92246868aa37d5e2ce7db2-XXX&enrichSource=Y292ZXJQYWdlOzI1MzI0MDIxNTtBUzoxMDIwMTIzNzI5MTQxNzlAMTQwMTMzMzA1MzY0Nw%3D%3D&el=1_x_3&_esc=publicationCoverPdf
    # Power-Dependent Optimal Concentrations of Tm3+ and Yb3+ in Upconversion Nanoparticles

    # Simplifying assumptions: in a unit cell, 
    #     xy projection: in the center of triangle formed by Na
    #     z projection: height is the middle point between 2 layers of Na

    # Some ignored details: probabilistic occupation of nodes, P\bar{6}2m, P\bar{6}, P6_3m
    #    https://www.researchgate.net/profile/Sameera-Perera-2/publication/318604006_Average_and_Local_Crystal_Structure_of_b-ErYbNaYF_4_Upconverting_Nanocrystals_Probed_by_X-ray_Total_Scattering/links/62f94e40b8dc8b4403e1987c/Average-and-Local-Crystal-Structure-of-b-ErYbNaYF-4-Upconverting-Nanocrystals-Probed-by-X-ray-Total-Scattering.pdf


import numpy as np
import math

from Point_Tm import *
from utils import *

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from tqdm import tqdm
from scipy.integrate import odeint

class Lattice_tm():
    
    def __init__(self, Yb_conc, Tm_conc, d, r, seed = None):

        if seed is not None:
            np.random.seed(seed)

        # Create the lattice
        l_r = int(d/2/0.596)
        l_z = int(d/2/0.353)
        na_points = [Point_tm((i, j, k), mol = 'Na') for i in range(-l_r, l_r+1) for j in range(-l_r, l_r+1) for k in range(-l_z, l_z+1)]
        y_coords = [Point_tm((na.p[0]+1/3, na.p[1]+1/3, na.p[2]+1/2)) for na in na_points]
        y_coords = y_coords + [Point_tm((na.p[0]-1/3, na.p[1]-1/3, na.p[2]+1/2)) for na in na_points]
        na_points = self.in_diameter(d, na_points)
        y_coords = self.in_diameter(d, y_coords)
        n_points = int(len(y_coords) * 3/4)  # 3/4 probability for Y/Yb/Tm

        # Assign molecules to the lattice points 
        n_Yb = int(Yb_conc * n_points)
        n_Tm = int(Tm_conc * n_points)
        types = ['Na'] * (len(y_coords) - n_points) + ['Yb'] * n_Yb + ['Tm'] * n_Tm + ['Y'] * (n_points - n_Yb - n_Tm)

        np.random.shuffle(types)
        for p, t in zip(y_coords, types):
            p.type = t
            if t == 'Yb':
                p.state = np.random.choice([0, 1], p=[0.85, 0.15])
                ### here, because of absorbation rate of Yb, set the rate manually as 0.85 and 0.15
            else:
                p.state = 0

        y_points = [p for p in y_coords if p.type != 'Na'] 
        na_points = na_points + [p for p in y_coords if p.type == 'Na']
        
        self.Yb_conc = Yb_conc
        self.Tm_conc = Tm_conc
        self.Yb_num = n_Yb
        self.Tm_num = n_Tm
        self.d = d
        self.r = r

        self.na_points = na_points
        self.y_points = y_points # Y/Yb/Tm points
        self.points = [p for p in self.y_points if p.type != 'Y'] # rare earth doping points, Yb/Tm
        self.n_points = len(self.points) # number of Yb/Tm points

        self.get_neighbors(r)

        self.excited = [p for p in self.points if p.state != 0]
        self.ground_Yb = [p for p in self.points if p.type == 'Yb'  and p.state == 0]
    
    def get_neighbors(self, r):
        # Get all neighbors (within distance r) of every point 
        ret = {p:[] for p in self.points}
        for i in tqdm(range(self.n_points)):
            i_nei = []
            for j in range(self.n_points):
                if i == j :
                    continue
                dist = self.points[i].to(self.points[j])
                if dist <= r:
                    i_nei.append((self.points[j], dist))
            ret[self.points[i]] = i_nei

        self.neighbors = ret

    def in_diameter(self, d, points):
        origin = Point_tm((0,0,0))
        ret = []
        for point in points:
            if point.to(origin) < d/2:
                ret.append(point)
        return ret
    

    def collect_stats(self):
            
            Yb_1 = len([i for i in self.points if i.type == 'Yb' and i.state == 1])
            Yb_0 = len([i for i in self.points if i.type == 'Yb' and i.state == 0])

            Tm_0 = len([i for i in self.points if i.type == 'Tm' and i.state == 0])
            Tm_1 = len([i for i in self.points if i.type == 'Tm' and i.state == 1])
            Tm_2 = len([i for i in self.points if i.type == 'Tm' and i.state == 2])
            Tm_3 = len([i for i in self.points if i.type == 'Tm' and i.state == 3])
            Tm_4 = len([i for i in self.points if i.type == 'Tm' and i.state == 4])
            Tm_5 = len([i for i in self.points if i.type == 'Tm' and i.state == 5])
            Tm_6 = len([i for i in self.points if i.type == 'Tm' and i.state == 6])
            Tm_7 = len([i for i in self.points if i.type == 'Tm' and i.state == 7])

            return [Yb_0, Yb_1], [Tm_0, Tm_1, Tm_2, Tm_3, Tm_4, Tm_5, Tm_6, Tm_7]


    def deep_copy(self):
        # Create deep copy of lattice so that we can perform experiments with the same initial state
        # ALERT: na_points is not deep copied

        # print(np.random.get_state())
        cp = Lattice_tm(self.Yb_conc, self.Tm_conc, self.d, self.r)
        cp.Yb_conc = self.Yb_conc
        cp.Tm_conc = self.Tm_conc 
        cp.d = self.d
        cp.r = self.r

        cp.na_points = self.na_points
        cp.y_points = [p.deep_copy() for p in self.points]
        cp.points = [p for p in cp.y_points if p.type != 'Y']
        cp.n_points = self.n_points
        cp.get_neighbors(cp.r)
        cp.excited = [p for p in cp.points if p.state != 0]
        cp.ground_Yb = [p for p in cp.points if p.type == 'Yb'  and p.state == 0]

        return cp
    







'''

    def plot_distributions(self):
        points = self.points
        # once we input the configurations, then we can get the total information of the system

        # Create a list of all types and values for easier plotting
        all_types = [point.type for point in points]
        all_values_A = [point.state for point in points if point.type == 'Yb']
        all_values_B = [point.state for point in points if point.type == 'Er']

        plt.figure(figsize=(15, 5))

        # Plotting distribution of A, B, C using bar plot

        # 1 row, 3 columns, 1st plot
        plt.subplot(1, 3, 1)
        labels, counts = np.unique(all_types, return_counts=True)
        counts_tmp = dict(zip(labels, counts))
        counts_tmp['Y'] = counts_tmp.setdefault('Y', 0)

        bars = plt.bar(['Yb', 'Er', 'Y'], [counts_tmp['Yb'], counts_tmp['Er'], counts_tmp['Y']], color=['blue', 'pink', 'green'], width=0.4)
        plt.ylabel('Count',fontsize=18)
        plt.title('Distribution of three types',fontsize=18)
        plt.xticks(['Yb', 'Er', 'Y'], ['Sensitizers', 'Emitters', 'Others'],fontsize=16)
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 5, yval, ha='center', va='bottom')

        # Plotting value distribution for type A using histogram
        # 1 row, 3 columns, 2nd plot
        plt.subplot(1, 3, 2)
        counts, bins, patches = plt.hist(all_values_A, bins=[0, 1, 2], align='left', rwidth=0.4, color='blue')
        plt.ylabel('Count',fontsize=18)
        plt.title('Value distribution for sensitizers',fontsize=18)
        plt.xticks([0, 1], ['0(Ground state)', '1(Excited state)'],fontsize=16)
        for count, bin, patch in zip(counts, bins, patches):
            plt.text(bin + 0.01, count + 1, int(count), ha='center', va='bottom')

        # Plotting value distribution for type B using histogram
        # 1 row, 3 columns, 3rd plot
        plt.subplot(1, 3, 3)
        counts, bins, patches = plt.hist(all_values_B, bins=[0, 1, 2, 3, 4, 5, 6, 7], align='left', rwidth=0.4, color='pink')

        plt.ylabel('Count',fontsize=18)
        plt.title('Value distribution for emitters',fontsize=18)
        plt.xticks([0, 1, 2, 3, 4, 5, 6, 7], ['G', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th'],fontsize=16)
        for count, bin, patch in zip(counts, bins, patches):
            plt.text(bin + 0.01, count + 1, int(count), ha='center', va='bottom')

        plt.tight_layout()
        plt.show()
    


    def plot_3d_points_with_plotly(self):
        points = self.points
        # Separate points based on their type (A or B)
        points_A = [point for point in points if point.type == 'Yb']
        points_B = [point for point in points if point.type == 'Er']
        points_Y = [point for point in self.y_points if point.type == 'Y']

        # Extract coordinates and values for points of type A
        euclidean_coords_A = [(point.to_euclidean()) for point in points_A]
        x_A = [point[0] for point in euclidean_coords_A]
        y_A = [point[1] for point in euclidean_coords_A]
        z_A = [point[2] for point in euclidean_coords_A]
        values_A = [point.state for point in points_A]

        # Extract coordinates and values for points of type B
        euclidean_coords_B = [(point.to_euclidean()) for point in points_B]
        x_B = [point[0] for point in euclidean_coords_B]
        y_B = [point[1] for point in euclidean_coords_B]
        z_B = [point[2] for point in euclidean_coords_B]
        values_B = [point.state for point in points_B]

        # Extract coordinates and values for points of type Y
        euclidean_coords_Y = [(point.to_euclidean()) for point in points_Y]
        x_Y = [point[0] for point in euclidean_coords_Y]
        y_Y = [point[1] for point in euclidean_coords_Y]
        z_Y = [point[2] for point in euclidean_coords_Y]

        # Create 3D scatter plots
        trace_A = go.Scatter3d(x=x_A, y=y_A, z=z_A, mode='markers+text',
                            marker=dict(size=6, color='blue', opacity=0.8),
                            text=values_A, textposition='top center',
                            name = 'Yb')

        trace_B = go.Scatter3d(x=x_B, y=y_B, z=z_B, mode='markers+text',
                            marker=dict(size=6, color='pink', opacity=0.8),
                            text=values_B, textposition='top center',
                            name = 'Er')
        
        trace_Y = go.Scatter3d(x=x_Y, y=y_Y, z=z_Y, mode='markers',
                            marker=dict(size=6, color='gray', opacity=0.8),
                            textposition='top center', name = 'Y')

        # Combine plots and set layout
        data = [trace_A, trace_B, trace_Y]
        layout = go.Layout(margin=dict(l=0, r=0, b=0, t=0))
        fig = go.Figure(data=data, layout=layout)
        fig.update_layout(legend=dict(title='Legend'))
        fig.layout.scene.camera.projection.type = "orthographic"

        # Display the figure
        fig.show()
        fig.write_html("small.html")
    
    def plot_3d_points_with_na(self):
        euclidean_coords_na = [(point.to_euclidean()) for point in self.na_points]
        na_x = [point[0] for point in euclidean_coords_na]
        na_y = [point[1] for point in euclidean_coords_na]
        na_z = [point[2] for point in euclidean_coords_na]
        trace_na = go.Scatter3d(x=na_x, y=na_y, z=na_z, mode='markers+text',
                            marker=dict(size=4, color='green', opacity=0.8),
                            text='Na', textposition='top center', name = 'Na')

        points = self.points
        # Separate points based on their type (A or B)
        points_A = [point for point in points if point.type == 'Yb']
        points_B = [point for point in points if point.type == 'Er']
        points_Y = [point for point in self.y_points if point.type == 'Y']

        # Extract coordinates and values for points of type A
        euclidean_coords_A = [(point.to_euclidean()) for point in points_A]
        x_A = [point[0] for point in euclidean_coords_A]
        y_A = [point[1] for point in euclidean_coords_A]
        z_A = [point[2] for point in euclidean_coords_A]
        values_A = [point.state for point in points_A]

        # Extract coordinates and values for points of type B
        euclidean_coords_B = [(point.to_euclidean()) for point in points_B]
        x_B = [point[0] for point in euclidean_coords_B]
        y_B = [point[1] for point in euclidean_coords_B]
        z_B = [point[2] for point in euclidean_coords_B]
        values_B = [point.state for point in points_B]

        # Extract coordinates and values for points of type Y
        euclidean_coords_Y = [(point.to_euclidean()) for point in points_Y]
        x_Y = [point[0] for point in euclidean_coords_Y]
        y_Y = [point[1] for point in euclidean_coords_Y]
        z_Y = [point[2] for point in euclidean_coords_Y]

        trace_Y = go.Scatter3d(x=x_Y, y=y_Y, z=z_Y, mode='markers',
                            marker=dict(size=6, color='gray', opacity=0.8),
                            textposition='top center', name = 'Y')

        # Create 3D scatter plots
        trace_A = go.Scatter3d(x=x_A, y=y_A, z=z_A, mode='markers+text',
                            marker=dict(size=6, color='blue', opacity=0.8),
                            text=values_A, textposition='top center',
                            name = 'Yb')

        trace_B = go.Scatter3d(x=x_B, y=y_B, z=z_B, mode='markers+text',
                            marker=dict(size=6, color='pink', opacity=0.8),
                            text=values_B, textposition='top center',
                            name = 'Er')

        # Combine plots and set layout
        data = [trace_A, trace_B, trace_Y, trace_na]
        layout = go.Layout(margin=dict(l=0, r=0, b=0, t=0))
        fig = go.Figure(data=data, layout=layout)
        fig.layout.scene.camera.projection.type = "orthographic"
        fig.update_layout(legend=dict(title='Legend'))

        # Display the figure
        fig.show()

 
    def ode_distribution(self):
        ## Why ODE and MC doesn't match? presence of c0
        n_yb = int(self.yb_conc*self.n_points)
        n_tm = int(self.tm_conc*self.n_points)

        def system(state, t):

            ns2, n0, n1, n2, n3, n4, n5, n6, n7 = state
            ms2 = tag['laser']*(n_yb-ns2) - tag['Ws']*ns2 - (tag['c1']*n0+tag['c2']*n1+tag['c3']*n3+tag['c1']*n6)*ns2
            m0 = -tag['c1']*n0*ns2                   + tag['W10']*n1 + tag['W20']*n2 + tag['W30']*n3 + tag['W40']*n4 + tag['W50']*n5 + tag['W60']*n6 + tag['W70']*n7 - tag['k31']*n0*n3 - tag['k41']*n0*n6 - tag['k51']*n0*n7
            m1 = -tag['c2']*n1*ns2 + tag['MPR21']*n2 - tag['W10']*n1 + tag['W21']*n2 + tag['W31']*n3 + tag['W41']*n4 + tag['W51']*n5 + tag['W61']*n6 + tag['W71']*n7 + tag['k31']*n0*n3
            m2 = tag['c1']*n0*ns2 - tag['MPR21']*n2  - tag['W20']*n2 - tag['W21']*n2 + tag['W32']*n3 + tag['W42']*n4 + tag['W52']*n5 + tag['W62']*n6 + tag['W72']*n7 + tag['k31']*n0*n3 + tag['k41']*n0*n6
            m3 = tag['c3']*n3*ns2 + tag['MPR43']*n4  - tag['W30']*n3 - tag['W31']*n3 - tag['W32']*n3 + tag['W40']*n4 + tag['W53']*n5 + tag['W63']*n6 + tag['W73']*n7 - tag['k31']*n0*n3 + tag['k41']*n0*n6 + tag['k51']*n0*n7
            m4 = tag['c2']*n1*ns2 - tag['MPR43']*n4  - tag['W40']*n4 - tag['W41']*n4 - tag['W42']*n4 - tag['W43']*n4 + tag['W54']*n5 + tag['W64']*n6 + tag['W74']*n7 
            m5 =                                     - tag['W50']*n5 - tag['W51']*n5 - tag['W52']*n5 - tag['W53']*n5 - tag['W54']*n5 + tag['W65']*n6 + tag['W75']*n7 + tag['k51']*n0*n7
            m6 = tag['c3']*n3*ns2 - tag['c4']*n6*ns2 - tag['W60']*n6 - tag['W61']*n6 - tag['W62']*n6 - tag['W63']*n6 - tag['W64']*n6 - tag['W65']*n6 + tag['W76']*n7 - tag['k41']*n0*n6
            m7 = tag['c4']*n6*ns2                    - tag['W70']*n7 - tag['W71']*n7 - tag['W72']*n7 - tag['W73']*n7 - tag['W74']*n7 - tag['W75']*n7 - tag['W76']*n7 - tag['k51']*n0*n7

            return [ms2, m0, m1, m2, m3, m4, m5, m6, m7]
        
        yb_excited = len([i for i in self.y_points if i.type == 'Yb' and i.state == 1])
        state0 = [yb_excited, n_tm, 0, 0, 0, 0, 0, 0, 0]
        t = np.arange(0.0, 0.001, 0.000001)
        state = odeint(system, state0, t)

        state_f = [state[:, 0][-1], state[:, 1][-1], state[:, 2][-1], state[:, 3][-1], state[:, 4][-1], state[:, 5][-1], state[:, 6][-1], state[:, 7][-1], state[:, 8][-1]]
        
        plt.figure(figsize=(5, 5))
        bars = plt.bar([0, 1, 2, 3, 4, 5, 6, 7], state_f[1:], width=0.4, color='pink')
        plt.ylabel('Count',fontsize=18)
        plt.title('ODE value distribution for emitters',fontsize=18)
        plt.xticks([0, 1, 2, 3, 4, 5, 6, 7], ['G', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th'],fontsize=16)
        for i, bar in enumerate(bars):
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 5, round(state_f[i+1],1), ha='center', va='bottom')

        plt.tight_layout()
        plt.show()

        return state_f
    

'''
