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

from Point_Er import *
from utils import *
from tqdm import tqdm

import numpy as np
from Point_Er import *
from utils import *
from tqdm import tqdm

class Lattice():
    
    def __init__(self, yb_conc, er_conc, d, r, defects_fraction, thickness_shell, Gd_conc, seed=None):
        if seed is not None:
            np.random.seed(seed)

        # Create the lattice
        l_r = int((d/2) / 0.596)
        l_z = int((d/2) / 0.353)

        # type + coord = points
        na_points = [Point((i, j, k), mol='Na') for i in range(-l_r, l_r+1) for j in range(-l_r, l_r+1) for k in range(-l_z, l_z+1)]

        # only coord
        y_coords = [Point((na.p[0] + 1/3, na.p[1] + 1/3, na.p[2] + 1/2)) for na in na_points] + \
                   [Point((na.p[0] - 1/3, na.p[1] - 1/3, na.p[2] + 1/2)) for na in na_points]
    
        na_points = self.in_core(d, na_points)
        y_coords = self.in_core(d, y_coords)

        # Print total number of Na and Y atoms before replacement
        # print(f"Total Na atoms before replacement: {len(na_points)}")
        # print(f"Total Y atoms before replacement: {len(y_coords)}")
        # print(f"Total Na and Y atoms in {d}nm nanoparticle before replacement: {len(na_points)} + {len(y_coords)} = {len(na_points) + len(y_coords)}")

        # find the coords, and 75% is lanthanides
        Ln_points = int(len(y_coords) * 3 / 4)  # 3/4 probability for Y/Yb/Er, 1/4 for Na
        n_yb = int(yb_conc * Ln_points)
        n_er = int(er_conc * Ln_points)
        # print(f"Total Yb atoms: {yb_conc} * {len(y_coords)} * 0.75 = {n_yb}")
        # print(f"Total Er atoms: {er_conc} * {len(y_coords)} * 0.75 = {n_er}")
        # print(f"Total lanthanide ions (Yb + Er): {n_yb + n_er}")

        # Assign types to the lattice points
        types = ['Na'] * (len(y_coords) - Ln_points) + ['Yb'] * n_yb + ['Er'] * n_er + ['Y'] * (Ln_points - n_yb - n_er)
        np.random.shuffle(types)

        # for each coords, assignthe type
        for p, t in zip(y_coords, types):
            p.type = t
            # then assign the state
            if t == 'Yb':
                p.state = np.random.choice([0, 1], p=[0.99, 0.01])  # Set state based on absorption rate
            else:
                p.state = 0
        
        na_points_tot = na_points + [p for p in y_coords if p.type == 'Na']
        # print(f"New Na atoms from Y atoms (25% Y atoms): {len(y_coords) - Ln_points}")
        # print(f"Total Na atoms (initial Na atoms + 25% Y atoms): {len(na_points)} + {len(na_points_tot) - len(na_points)} = {len(na_points_tot)}")
        
        # y_points = [p for p in y_coords if p.type == 'Y']
        # print(f"Total Y atoms after replacement: {len(y_points)}")

        # remaining is Yb/Er
        y_points = [p for p in y_coords if p.type != 'Na'] 

        
        self.yb_conc = yb_conc
        self.er_conc = er_conc
        self.d = d
        self.r = r
        self.defects_fraction = defects_fraction
        self.thickness_shell = thickness_shell
        self.Gd_conc = Gd_conc

        self.yb_num = n_yb
        self.er_num = n_er
        self.na_points_tot = na_points_tot
        self.y_points = y_points  # Includes Y, Yb, Er
        self.points = [p for p in self.y_points if p.type != 'Y']  # only contain lanthanide
        self.num_Ln_points = len(self.points)  # Number of Yb/Er points

        self.defects_points = [p for p in self.points if p.type in ['Yb', 'Er']]  # Candidates for defects: only consider lanthanides (Yb and Er)
        # self.defects_points = [p for p in self.points if p.type in ['Na','Yb', 'Er']] # Candidates for defects: consider lanthanides and Na from all Y ions (not initial Na) 
        # print(f"Total defects point candidates: {len(self.defects_points)}")

        self.get_neighbors(r)
        self.excited = [p for p in self.points if p.state != 0]
        self.ground_yb = [p for p in self.points if p.type == 'Yb' and p.state == 0]

#################################################### shell

    def introduce_shell(self):
        
        if self.thickness_shell is None or self.Gd_conc is None:
            print("Shell parameters are not defined.")
            return

        d_core_shell = self.d + 2 * self.thickness_shell
        r_total = self.r + self.thickness_shell
        l_r_total = int(r_total / 0.596)
        l_z_total = int(r_total / 0.353)

        na_points_core_shell = [Point((i, j, k), mol='Na') for i in range(-l_r_total, l_r_total+1)
                                for j in range(-l_r_total, l_r_total+1) for k in range(-l_z_total, l_z_total+1)]
        na_points_shell = self.in_layer(self.d, d_core_shell, na_points_core_shell)

        y_coords_shell = [Point((na.p[0] + 1/3, na.p[1] + 1/3, na.p[2] + 1/2)) for na in na_points_shell] + \
                         [Point((na.p[0] - 1/3, na.p[1] - 1/3, na.p[2] + 1/2)) for na in na_points_shell]
        
        y_coords_shell = self.in_layer(self.d, d_core_shell, y_coords_shell)

        n_Gd = int(len(y_coords_shell) * self.Gd_conc)

        types = ['Gd'] * n_Gd + ['Y'] * (len(y_coords_shell) - n_Gd)
        np.random.shuffle(types)

        for p, t in zip(y_coords_shell, types):
            p.type = t
            p.state = 0

        self.shell_points = y_coords_shell

        y_points = [p for p in self.shell_points if p.type == 'Y']
        Gd_points = [p for p in self.shell_points if p.type == 'Gd']

        print(f"Total Y atoms in the shell layer: {len(y_points)}")
        print(f"Total Gd atoms in the shell layer: {len(Gd_points)}")

        

    def in_core(self, d, points):
        origin = Point((0, 0, 0))
        ret = []
        for point in points:
            if point.to(origin) < d / 2:
                ret.append(point)
        return ret

    def in_layer(self, d1, d2, points):
        origin = Point((0, 0, 0))
        ret = []
        for point in points:
            distance = point.to(origin)
            if d1 / 2 < distance < d2 / 2:
                ret.append(point)
        return ret
    


    def introduce_defects(self):
        num_defects = int(self.defects_fraction * len(self.defects_points))
        # print(f"Introducing {num_defects} defect points out of {len(self.defects_points)} candidates, while others are fiexd")
        # print()
        # print('The selected ions from total candidates: ')
        # print()
        defect_indices = np.random.choice(range(len(self.defects_points)), size=num_defects, replace=False)
        for index in defect_indices:
            point = self.defects_points[index]
            delta_x, delta_y, delta_z = np.random.uniform(-0.5, 0.5, 3)
            point.p = (point.p[0] + delta_x, point.p[1] + delta_y, point.p[2] + delta_z)
            # print(f"Ion index: {index}, Defected Point Type: {point.type}, New Coords: {point.p}")

 

    def get_neighbors(self, r):
        """
        Calculate neighbors for each Yb and Er point within a specified distance `r`.
        
        Parameters:
        r (float): The critical distance to consider for neighboring points.
        """
        ret = {}
        for i in tqdm(range(self.num_Ln_points)): # num_Ln_points is a number
            i_nei = [] 
            for j in range(self.num_Ln_points):
                if i == j:
                    continue
                dist = self.points[i].to(self.points[j]) # self.points only contain lanthanide
                if dist <= r:
                    i_nei.append((self.points[j], dist)) # self.points only contain lanthanide
            ret[self.points[i]] = i_nei # the lanthanide is used as the key, while its neighbors is the value
        self.neighbors = ret


    def validate_neighbors(self, num):
        """
        Validate the neighbors of all Yb and Er ions in self.Ln_points.
        """

        print("Validating neighbors for all Yb and Er ions:")
        print()
        neighbors = {}
        for i in tqdm(range(self.num_Ln_points)):
            i_nei = []
            for j in range(self.num_Ln_points):
                if i == j:
                    continue
                dist = self.points[i].to(self.points[j])
                if dist <= self.r:
                    i_nei.append((self.points[j], dist))
            neighbors[i] = i_nei  # Use index as key

        a = 0
        for i, ion in enumerate(self.points):
            neighbors_list = neighbors.get(i, [])
            print(f"Ion {i}: Type: {ion.type}, Coords: {ion.p}, Number of neighbors: {len(neighbors_list)}")
            if a == num-1:
                break
            a+=1

            # for neighbor, dist in neighbors_list:
            #     print(f"  Neighbor: Type: {neighbor.type}, Coords: {neighbor.p}, Distance: {dist:.2f} nm")


    def deep_copy(self):
        # Create deep copy of lattice to perform experiments with the same initial state
        cp = Lattice(self.yb_conc, self.er_conc, self.d, self.r, self.defects_fraction, self.thickness_shell, self.Gd_conc)
        cp.yb_conc = self.yb_conc
        cp.er_conc = self.er_conc
        cp.d = self.d
        cp.r = self.r
        cp.defects_fraction = self.defects_fraction
        cp.thickness_shell = self.thickness_shell
        cp.Gd_conc = self.Gd_conc

        cp.na_points_tot = self.na_points_tot
        cp.y_points = [p.deep_copy() for p in self.points]
        cp.points = [p for p in cp.y_points if p.type != 'Y']
        cp.num_Ln_points = self.num_Ln_points
        cp.get_neighbors(cp.r)
        cp.excited = [p for p in cp.points if p.state != 0]
        cp.ground_yb = [p for p in cp.points if p.type == 'Yb' and p.state == 0]

        return cp



# class Lattice():
    
#     def __init__(self, yb_conc, er_conc, d, r, defects_fraction, seed = None):
#         if seed is not None:
#             np.random.seed(seed)

#         # Create the lattice
#         l_r = int((d/2)/0.596)

#         l_z = int((d/2)/0.353)

#         na_points = [Point((i, j, k), mol = 'Na') for i in range(-l_r, l_r+1) for j in range(-l_r, l_r+1) for k in range(-l_z, l_z+1)]
#         y_coords = [Point((na.p[0]+1/3, na.p[1]+1/3, na.p[2]+1/2)) for na in na_points] + [Point((na.p[0]-1/3, na.p[1]-1/3, na.p[2]+1/2)) for na in na_points]
    
#         na_points = self.in_diameter(d, na_points)
#         y_coords = self.in_diameter(d, y_coords)

#         # Print total number of Na and Y atoms before replacement
#         print(f"Total Na atoms before replacement: {len(na_points)}")
#         print(f"Total Y atoms before replacement: {len(y_coords)}")
#         print(f"Total Na and Y atoms in {d}nm nanoparticle before replacement: {len(na_points)}+{len(y_coords)}={len(na_points)+len(y_coords)}")


#         Ln_points = int(len(y_coords) * 3/4)  # 3/4 probability for Y/Yb/Tm, 1/4 probability for Na

#         # Assign ions to the lattice points 
        

#         n_yb = int(yb_conc*Ln_points)
#         print(f"Toal Yb atoms: {yb_conc}*{len(y_coords)}*{0.75}={n_yb}")

#         n_er = int(er_conc*Ln_points)
#         print(f"Toal Er atoms: {er_conc}*{len(y_coords)}*{0.75}={n_er}")
#         print(f"Total lanthanide ions: {n_yb}+{n_er}={n_yb+n_er}")

#         types = ['Na'] * (len(y_coords) - Ln_points) + ['Yb'] * n_yb + ['Er'] * n_er + ['Y'] * (Ln_points - n_yb - n_er)
#         np.random.shuffle(types)
#         for p, t in zip(y_coords, types):
#             p.type = t
#             if t == 'Yb':
#                 p.state = np.random.choice([0, 1], p=[0.85, 0.15])
#                 ### here, because of absorbation rate of Yb, set the rate manually as 0.85 and 0.15
#             else:
#                 p.state = 0
              

#         print(f"New Na atoms from Y atoms (25% Y atom): {len(y_coords) - Ln_points}")
#         na_points_tot = na_points + [p for p in y_coords if p.type == 'Na']
#         print(f"Total Na atoms (initial Na atoms + 25% Y atom): {len(na_points)}+{len(y_coords) - Ln_points}={len(na_points_tot)}")
#         y_points = [p for p in y_coords if p.type == 'Y'] 
#         print(f"Total Y atoms after replacement: {len(y_points)}")

#         y_points = [p for p in y_coords if p.type != 'Na'] 

#         self.defects_fraction = defects_fraction
#         self.yb_conc = yb_conc
#         self.er_conc = er_conc 
#         self.yb_num = n_yb
#         self.er_num = n_er
#         self.d = d
#         self.r = r
#         self.na_points_tot = na_points_tot
#         self.y_points = y_points # Y/Yb/Tm points
#         self.points = [p for p in self.y_points if p.type != 'Y'] # rare earth doping points, Yb/Tm
#         self.defects_points = [p for p in self.y_points if p.type != 'Y'] + na_points_tot

#         print(f"Total defects point candidates: {len(self.defects_points)}")

#         self.Ln_points = len(self.points) # number of Yb/Tm points
#         self.get_neighbors(r)
#         self.excited = [p for p in self.points if p.state != 0]
#         self.ground_yb = [p for p in self.points if p.type == 'Yb'  and p.state == 0]

#     def introduce_defects(self, defects_fraction):
#         num_defects = int(defects_fraction * len(self.defects_points))
#         print(f'There are total {num_defects} defect points')
#         defect_indices = np.random.choice(range(len(self.defects_points)), size=num_defects, replace=False)
#         for index in defect_indices:
#             point = self.defects_points[index]
#             delta_x, delta_y, delta_z = np.random.uniform(-0.5, 0.5, 3)
#             point.p = (point.p[0] + delta_x, point.p[1] + delta_y, point.p[2] + delta_z)
#             print(f"Defected Point: Type: {point.type}, New Coords: {point.p}")
        
    
#     def get_neighbors(self, r):
#         # Get all neighbors (within distance r) of every point 
#         ret = {p:[] for p in self.points}
#         for i in tqdm(range(self.Ln_points)):
#             i_nei = []
#             for j in range(self.Ln_points):
#                 if i == j :
#                     continue
#                 dist = self.points[i].to(self.points[j])
#                 if dist <= r:
#                     i_nei.append((self.points[j], dist))
#             ret[self.points[i]] = i_nei

#         self.neighbors = ret

#     def in_diameter(self, d, points):
#         origin = Point((0,0,0))
#         ret = []
#         for point in points:
#             if point.to(origin) < d/2:
#                 ret.append(point)
#         return ret

    
#     def deep_copy(self):
#         # Create deep copy of lattice so that we can perform experiments with the same initial state
#         # ALERT: na_points is not deep copied

#         # print(np.random.get_state())
#         cp = Lattice(self.yb_conc, self.er_conc, self.d, self.r)
#         cp.yb_conc = self.yb_conc
#         cp.er_conc = self.er_conc 
#         cp.d = self.d
#         cp.r = self.r

#         cp.na_points = self.na_points_tot
#         cp.y_points = [p.deep_copy() for p in self.points]
#         cp.points = [p for p in cp.y_points if p.type != 'Y']
#         cp.Ln_points = self.Ln_points
#         cp.get_neighbors(cp.r)
#         cp.excited = [p for p in cp.points if p.state != 0]
#         cp.ground_yb = [p for p in cp.points if p.type == 'Yb'  and p.state == 0]

#         return cp
    

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
        n_er = int(self.er_conc*self.n_points)

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
        state0 = [yb_excited, n_er, 0, 0, 0, 0, 0, 0, 0]
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



    # def collect_stats(self):
    #     yb_1 = len([i for i in self.points if i.type == 'Yb' and i.state == 1])
    #     yb_0 = len([i for i in self.points if i.type == 'Yb' and i.state == 0])

    #     er_0 = len([i for i in self.points if i.type == 'Er' and i.state == 0])
    #     er_1 = len([i for i in self.points if i.type == 'Er' and i.state == 1])
    #     er_2 = len([i for i in self.points if i.type == 'Er' and i.state == 2])
    #     er_3 = len([i for i in self.points if i.type == 'Er' and i.state == 3])
    #     er_4 = len([i for i in self.points if i.type == 'Er' and i.state == 4])
    #     er_5 = len([i for i in self.points if i.type == 'Er' and i.state == 5])
    #     er_6 = len([i for i in self.points if i.type == 'Er' and i.state == 6])
    #     er_7 = len([i for i in self.points if i.type == 'Er' and i.state == 7])

    #     return [yb_0, yb_1], [er_0, er_1, er_2, er_3, er_4, er_5, er_6, er_7]
    
'''
