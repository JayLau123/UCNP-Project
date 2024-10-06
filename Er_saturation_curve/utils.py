def to_euclidean(vec):
   a, b, c = vec
   return (0.596*a+0.5*0.596*b, 3**(1/2)/2*0.596*b, 0.353*c)

def e_distance(vec):
   return (vec[0]**2+vec[1]**2+vec[2]**2)**(1/2)