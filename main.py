from math import sqrt
from sympy import Symbol, lambdify
 
file = open('input.txt')
file = file.read()
lines = file.split('\n')
f1 = lines[0]
l, r = lines[1].split(' ')
l = int(l)
r = int(r)
e = float(lines[2])
method = int(lines[3])
x = Symbol('x')
d1f = lambdify(x, eval(f1).diff())
d2f = lambdify(x, eval(f1).diff().diff())
f = lambdify(x, eval(f1))
 
 
def dichotomy(l, r):
    k = 1
    while r - l >= e:
        m = (l + r) / 2
        if f(l) * f(m) <= 0:
            r = m
        else:
            l = m
        k += 1
    return (l + r) / 2, k, (r - l) / 2
 
 
def hord(l, r):
    k = 1
    m = 0
    while (r - l >= e or abs(f(m)) >= e) and k < 1000:
        m = l - f(l) / (f(r) - f(l)) * (r - l)
        if f(l) * f(m) <= 0:
            r = m
        else:
            l = m
        k += 1
    return m, k, abs(r - l)
 
 
def newton(p0):
    k = 1
    p1 = p0 - f(p0) / d1f(p0)
    while abs(p0 - p1) > e:
        p0 = p1
        p1 = p0 - f(p0) / d1f(p0)
        k += 1
    return p1, k, abs(p1 - p0)


def goldsech(l, r):
    k = 0
    while (abs(r-l) > e):
        lamb = (sqrt(5)+1)/2
        d = l + ((r - l)/lamb)
        c = l + ((r - l)/lamb**2)
        if f(l) * f(d) <= 0:
            r = d
        else:
            l = c
        k += 1
    return (l + r) / 2, k, (r - l) / 2


def phi(x):
    return x-(f(x)/d1f(x))


def iterations(l, r):
    k = 0
    p0 = (l + r) / 2
    while (abs(phi(p0)) >= 1):
        p0 = phi(p0)
        if (k >= 100):
            break
        k += 1
    return p0, k, f(p0)


def combined(l, r):
    k = 0
    while (abs(r-l) > e):
        c = l - (f(l) / (f(r) - f(l)) * (r - l))
        if (f(l) * d2f(l) > 0):
            l = l - f(l) / d1f(l)
            r = c
        if (f(r) * d2f(r) > 0):
            l = c
            r = r - f(r) / d1f(r)
        k += 1
    return (l + r) / 2, k, f((l + r) / 2)

 
_len = len(str(e).split(".")[1])
_format = f'{{:.{_len}e}}'
fx_format = f'{{:.{_len}f}}'
 
file = open('output.txt', 'w')
file.write("f = " + f1)
file.write('\n')
 
if method == 1:
    func = dichotomy(l, r)
    file.write('method = dichotomy')
elif method == 2:
    func = hord(l, r)
    file.write('method = hord')
elif method == 3:
    func = goldsech(l, r)
    file.write("method = goldsech")
elif method == 4:
    func = iterations(l, r)
    file.write("method = iterations")
elif method == 5:
    func = combined(l, r)
    file.write("method = combined")
else:
    func = newton(r)
    file.write('method = newton')
 
file.write('\n')
file.write("x = " + fx_format.format(func[0]) + "\n")
file.write("y = " + fx_format.format(f(func[0])) + "\n")
file.write("iterations = " + str(func[1]) + "\n")
 
file.write("e = " + _format.format(func[2]))
file.close()