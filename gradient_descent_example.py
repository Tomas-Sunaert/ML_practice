import numpy as np
import plotly.graph_objects as go


class grad():
    def __init__(self,eta,alpha,rez, xrange,yrange,fun):
        self.eta = eta
        self.alpha = alpha
        self.rez = rez
        self.xrange = xrange
        self.yrange = yrange
        self.fun = fun
        self.data2d = np.array([0,1,2,3,4,7,6,8,9,10,8,9,10.5,6,5,4,2,2,13,1,]).reshape(2,10)
    def gen_terain(self): 
        self.x = np.arange(-self.xrange,self.xrange,self.rez)
        self.y = np.arange(-self.yrange,self.yrange,self.rez)
        X,Y = np.meshgrid(self.x,self.y)
        self.X = X
        self.Y = Y
        self.Z = eval(self.fun)
    def plot_surface(self,grad= -1): #will plot surface and show path of gradient descend
        if type(grad) != int:
            surf = go.Figure()
            for i in range(self.amount_of_points):
                surf.add_trace(go.Surface(x = self.x,y=self.y,z= self.Z,opacity= 0.8))
                surf.add_trace(go.Scatter3d(x = grad[i][:,0],y = grad[i][:,1],z = grad[i][:,2]))
        else:
            surf = go.Figure(go.Surface(x = self.x,y=self.y,z= self.Z))
        surf.show()
    def find_grad(self, p,shift): #calculates the gradiant at point p numericaly, lower values of shift are typicaly better
        X = p[0]
        Y = p[1]
        Z= eval(self.fun)
        X = p[0]+shift
        x_up = eval(self.fun)
        X = p[0]-shift
        x_down = eval(self.fun)
        X = p[0]
        Y = p[1]+shift
        y_up = eval(self.fun)
        Y = p[1]-shift
        y_down = eval(self.fun)
        X_up = (x_up-Z)/-shift
        X_down = (x_down-Z)/shift
        Y_up = (y_up-Z)/-shift
        Y_down = (y_down-Z)/shift
        dx = min([X_up,X_down])
        dy = min([Y_up,Y_down])
        return np.array([dx,dy,Z]) #also returns Z for optimalisation reason later in the program
    def descent(self,shift = 0.0000001, p= -1,amount_of_points = 1):
        self.amount_of_points = amount_of_points
        spoints = []
        for i in range(amount_of_points):
            points = np.array([])
            if type(p) == int or i>0:  #picks random starting point if no starting point was given
                px= np.random.rand()*self.xrange*((-1)**np.random.randint(0,2))
                py= np.random.rand()*self.yrange*((-1)**np.random.randint(0,2))
                p = np.array([px,py])
            for x in range(self.eta):
                a = self.find_grad(p,shift)
                b = np.append(p,a[2])
                points = np.append(points,b)
                p = p + a[:2]*self.alpha
            points= points.reshape(self.eta,3)
            spoints.append(points)
        self.points = spoints
        self.plot_surface(spoints)
    def example_cost_function(self,w,b):
        if np.size(w) == 1: 
            cost = sum(((self.data2d[0,:] -(self.data2d[1,:]*w + b))**2))/len(self.data2d[1,:])
            return cost
        else:
            W = w.flatten()
            B = b.flatten()
            Z = np.array([])
            for x in range(len(W)): #a cookie for someone who can do this without a for loop  
                cost = sum(((self.data2d[0,:] -(self.data2d[1,:]*W[x] + B[x]))**2))/len(self.data2d[1,:])  
                Z = np.append(Z,cost)
            Z = Z.reshape(len(w[0]),len(w[0])) 
            return Z
    def plotgraph(self):  #doesnt work when using multiple starting points 
        x = np.arange(0,10,0.1)
        fig= go.Figure()
        fig.add_trace(go.Scatter(x = self.data2d[0,:],y = self.data2d[1,:], mode = 'markers'))
        for i in range(len(self.points)):
            for j in range(len(self.points[i])):
                y = self.points[i][j,0]*x + self.points[i][j,1]
                fig.add_trace(go.Scatter(x = x, y = y, mode = 'lines',name = 'cost = ' + str(self.points[i][j,2])))
        fig.show()

        

fitting_line = grad(10,0.01,0.1,10,10,'self.example_cost_function(X,Y)') #doesnt like if when you have a different range for x and y 
fitting_line.gen_terain()                                                #still needs to be upgraded to be able to handle that
fitting_line.descent(p = np.array([-8,8]))
fitting_line.plotgraph()

local_min = grad(500,0.003, 0.05,10,10,'(X**2 + Y**2) - 5*np.sin(X**2) + np.cos(Y*(X-4))*10 + 200/((1+(abs(X+Y))))+ 10*Y')
local_min.gen_terain()
local_min.descent(amount_of_points= 5)

high_alpha = grad(20,0.01,0.1,10,10,'(X**2 + Y**2)')
high_alpha.gen_terain()
high_alpha.descent(p = np.array([3,2]))

local = grad(500,0.003, 0.05,10,10,'(X**2 + Y**2) + 200/((1+(abs(X+Y))))+ 10*Y')
local.gen_terain()
local.descent(amount_of_points= 5)