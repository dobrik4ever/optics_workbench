import numpy as np
from matplotlib import pyplot as plt
from colorama import Fore, Style

class Bench:

    def __init__(self):
        self.elements = []
        self.length = 0
        self.add(Components.space(0))

    def add(self, component):
        if type(component) == Components.space:
            d = component.M[0,1]
            self.length += d
        component.pos = self.length
        self.elements.append(component)
    
    def compile(self, at = 0):  
        self.elements.reverse()          
        res = self.elements[at].M
        for i in range(at+1, len(self.elements)):
            M = self.elements[i].M
            res = np.dot(res, M)

        self.elements.reverse()
        return res            

    def get_at(self, h0, t0, at, arg = 'full'):
        Xp = np.array([[h0],[t0]])
        at = len(self.elements) - at-1
        res = self.compile(at)
        res = np.dot(res, Xp)
        if arg == 'full': return res
        if arg == 'height': return res[0,0]
        if arg == 'angle': return res[0,1]
        else: raise ValueError('Not a right arg entry')

    def render(self, height, angle = 0, rays_number = 10, point_source = False, color = 'red'):
        if point_source:
            if rays_number == 1:
                rays = [angle]
            elif rays_number == 2:
                rays = [angle, -angle]
            else:
                rays = np.linspace(angle, -angle, rays_number)

        else:
            if rays_number == 1:
                rays = [height]
            elif rays_number == 2:
                rays = [height, -height]
            else:
                rays = np.linspace(height, 0, rays_number)

        x = []
        plt.axhline(0, c='k')
        for ix, ray in enumerate(rays):
            y = []
            for i, el in enumerate(self.elements):
                if point_source:h = self.get_at(height, ray, i, 'height')
                else:           h = self.get_at(ray, angle, i, 'height')
                y.append(h)
                if abs(el.height) < abs(h): el.height = h
                if ix == 0: x.append(el.pos)
                        
            plt.axis('equal')
            plt.plot(x, y, c=color)
        
        for i, el in enumerate(self.elements):
            if type(el) == Components.lens:
                plt.plot([el.pos, el.pos], [-el.height, el.height], c='b')
                plt.text(el.pos, -el.height, f'\n f:{el.f} h:{el.height:.3}')
            else:
                plt.text(el.pos, 0, f'\n {i}')

        plt.arrow(0, 0, 0, height, fc='g', ec='g')

    def show(self):
        plt.minorticks_on()

        plt.grid(which='major', linestyle='-', linewidth='0.5',)
        # Customize the minor grid
        plt.grid(which='minor', linestyle=':', linewidth='0.5',)
        plt.show()
    
    def __str__(self):
        string = ''
        for i, v in enumerate(self.elements):
            string += f'{i}:\t{v}\n'
        return string


class Components:

    class lens:
        def __init__(self, f):
            self.f = f
            self.M = np.float64([[1, 0], [-1.0/f, 1]])
            self.pos = 0
            self.height = 0.0
        
        def __str__(self):
            s = f'{Fore.BLUE}Lens  {Style.RESET_ALL}' + \
                f'f:{self.f}\t' + \
                f'x:{self.pos}\th:{self.height:.3}'
            return s

    class space:
        def __init__(self, d):
            self.d = d
            self.M = np.float64([[1, d], [0, 1]])
            self.pos = 0
            self.height = 0

        def __str__(self):
            s = f'{Fore.GREEN}Space {Style.RESET_ALL}' + \
                f'd:{self.d}\t' + \
                f'x:{self.pos}\th:{self.height:.3}'
            return s

if __name__=='__main__':
    Mt = 0.325
    f1 = 20
    f2 = 30
    f3 = Mt * f2
    h0 = 12.0
    t0 = 0.0

    lens  = Components.lens
    space = Components.space
    bench = Bench()
    bench.add(space(5))
    bench.add(lens(f1))
    bench.add(space(f1)); bench.add(space(f2));
    bench.add(lens(f2))
    bench.add(space(5))
    bench.add(lens(f3))
    bench.add(space(f3))

    h = 6
    t = np.pi/6
    bench.render(height = h, angle = t, rays_number=10)
    print(bench)
    h0 = bench.get_at(h, t, at=3, arg='height')
    hp = bench.get_at(h, t, at=8, arg='height')
    MT = hp/h0
    print('MT = ',MT)
