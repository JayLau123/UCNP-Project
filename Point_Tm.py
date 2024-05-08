
from utils import to_euclidean, e_distance
from EnergyTransfer import *

class Point_tm():
    
    def __init__(self, coor, mol=None, state=None):
        self.p = coor
        self.type = mol
        self.state = state
    
    def __hash__(self):
        return hash(self.p)
    
    def change_state(self, new_state):
        self.state = new_state

    def to_euclidean(self):
        a, b, c = self.p
        return (0.596*a+0.5*0.596*b, 3**(1/2)/2*0.596*b, 0.353*c)

    def to(self, other):
        p1 = self.p
        p2 = other.p
        vec = (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])
        evec = to_euclidean(vec)
        return e_distance(evec)
    
    def deep_copy(self):
        return Point_tm(self.p, self.type, self.state)
    
    def react(self, other, cross_relaxation_Tm, up_conversion_Tm, yb_yb, distance):

        # return rate, new states
        if self.type == 'Yb' and self.state == 1:
            if other.type == 'Yb':
                if other.state == 0:
                    return yb_yb / (distance/10**7)**6
                return None
            else:
                return up_conversion_Tm[other.state].total_probability(distance)
                
        elif self.type == 'Tm' and other.type == 'Tm':

            return cross_relaxation_Tm[self.state][other.state].total_probability(distance)
            
        return None
    
    def get_decay_rates(self, tag):
        ret = []
        for i in range(self.state):
            ret.append(tag[f'E{self.state}E{i}'])
        return ret

    def __str__(self):
        return f'{self.p} {self.type} {self.state}'
    
    def __eq__(self, other):
        if isinstance(other, Point_tm):
            return self.p[0] == other.p[0] and self.p[1] == other.p[1] and self.p[2] == other.p[2]
        return False
