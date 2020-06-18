import pandas as pd
import altair as alt
from scipy.signal import savgol_filter
from math import sqrt
def averageUncertainty(X,ΔX):
    n = len(X)
    Average = sum(X)/n
    Uncertainty = sqrt(sum([(Xk-Average)**2 for Xk in X])/n/(n-1) +  ΔX**2/3)
    return (Average,Uncertainty)

def averageUncertaintyPrint(X,ΔX):
    print("The average is %s, and the unvertainty is %s"%averageUncertainty(X,ΔX))

def linearRegression(X,Y):
    n = len(X)
    x = sum(X) / n
    y = sum(Y) / n
    Sxx = sum([(xi - x)**2 for xi in X])
    Sxy = sum([(xi - x)*(yi - y) for (xi,yi) in zip(X,Y)])
    Syy = sum([(yi - y)**2 for yi in Y])
    k = Sxy/Sxx #斜率k
    b = y - k * x #截距b
    Uk = sqrt((Syy/Sxx - k**2)/(n-2))
    Ub = Uk*sqrt(sum([xi**2 for xi in X])/n)
    r = Sxy/sqrt(Sxx*Syy)#相关系数r
    return (k,b,Uk,Ub,r)
def linearRegressionPrint(X,Y):
    print("k = %s, b = %s, Uk = %s, Ub = %s, r = %s"%linearRegression(X,Y))
    
def pointGraph(X,Y,Xname="X",Yname="Y",color="#000000"):
    df = pd.DataFrame({
    Xname:X,
    Yname:Y,
    })
    Graph = alt.Chart(df).mark_circle(color=color).encode(
        alt.X(Xname),
        alt.Y(Yname),
        tooltip=[Xname,Yname],
    ).interactive()
    return Graph
def lineGraph(X,Y,Xname="X",Yname="Y",color="#66ccff"):
    df = pd.DataFrame({
        Xname:X,
        Yname:Y,
    })
    Graph = alt.Chart(df).mark_line(color=color).encode(
        alt.X(Xname),
        alt.Y(Yname),
        tooltip = [Xname,Yname]
    ).interactive()
    return Graph
def curveGraph(X,Y,Xname="X",Yname="Y",color="#66ccff",part=3,polynomialOrder=2):
    newY = savgol_filter(Y, int(len(Y)/part), polynomialOrder)
    return lineGraph(X,newY,Xname=Xname,Yname=Yname,color=color)
def linearRegressionGraph(X,Y,Xname="X",Yname="Y",color="#66ccff"):
    (k,b,Uk,Ub,r)=linearRegression(X,Y)
    f = lambda x:k*x+b
    X=sorted(X)
    left = X[0] + X[0] - X[1]
    right = X[-1] + X[-1] - X[-2]
    newX = [left,right]
    newY = [f(left),f(right)]
    return lineGraph(newX,newY,Xname=Xname,Yname=Yname,color=color)

aU = averageUncertainty
aUP = averageUncertaintyPrint
lR = linearRegression
lRP = linearRegressionPrint
pG = pointGraph
lG = lineGraph
cG = curveGraph
lRG = linearRegressionGraph
