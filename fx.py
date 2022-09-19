from math import sqrt
from sympy import Symbol, lambdify


class fx():

    def __init__(self, file: str) -> None:
        file = open('input.txt')
        file = file.read()
        lines = file.split('\n')
        self.f1 = lines[0]
        l, r = lines[1].split(' ')
        x = Symbol('x')
        self.d1f = lambdify(x, eval(self.f1).diff())
        self.l = int(l)
        self.r = int(r)
        self.e = float(lines[2])
        self.method = int(lines[3])
        self.f = lambdify(x, eval(self.f1))
        self._len = len(str(self.e).split(".")[1])
        self._format = f'{{:.{self._len}e}}'
        self.fx_format = f'{{:.{self._len}f}}'

    def dichotomy(self, l, r):
        k = 1
        while r - l >= self.e:
            m = (l + r) / 2
            if self.f(l) * self.f(m) <= 0:
                r = m
            else:
                l = m
            k += 1
        return (l + r) / 2, k, (r - l) / 2

    def hord(self, l, r):
        k = 1
        m = 0
        while (r - l >= self.e or abs(self.f(m)) >= self.e) and k < 1000:
            m = l - self.f(l) / (self.f(r) - self.f(l)) * (r - l)
            if self.f(l) * self.f(m) <= 0:
                r = m
            else:
                l = m
            k += 1
        return m, k, abs(r - l)
    
    
    def newton(self, p0):
        k = 1
        p1 = p0 - self.f(p0) / self.d1f(p0)
        while abs(p0 - p1) > self.e:
            p0 = p1
            p1 = p0 - self.f(p0) / self.d1f(p0)
            k += 1
        return p1, k, abs(p1 - p0)


    def goldsech(self, l, r):
        k = 0
        while (abs(r-l) > self.e):
            lamb = (sqrt(5)+1)/2
            d = l + ((r - l)/lamb)
            c = l + ((r - l)/lamb**2)
            if self.f(l) * self.f(d) <= 0:
                r = d
            else:
                l = c
            k += 1
        return (l + r) / 2, k, (r - l) / 2

    def phi(self, x):
        return x-(self.f(x)/self.d1f(x))

    def iterations(self, l, r):
        k = 0
        p0 = (l + r) / 2
        while (abs(self.phi(p0)) >= 1):
            p0 = self.phi(p0)
            if (k >= 100):
                break
            k += 1
        return p0, k, self.f(p0)

    def out(self, filestr: str):
        outfile = open(filestr, 'w')
        outfile.write("f = " + self.f1)
        outfile.write('\n')

        if self.method == 1:
            func = self.dichotomy(self.l, self.r)
            outfile.write('method = dichotomy')
        elif self.method == 2:
            func = self.hord(self.l, self.r)
            outfile.write('method = hord')
        elif self.method == 3:
            func = self.goldsech(self.l, self.r)
            outfile.write("method = goldsech")
        elif self.method == 4:
            func = self.iterations(self.l, self.r)
            outfile.write("method = iterations")
        else:
            func = self.newton(self.r)
            outfile.write('method = newton')

        outfile.write('\n')
        outfile.write("x = " + self.fx_format.format(func[0]) + "\n")
        outfile.write("y = " + self.fx_format.format(self.f(func[0])) + "\n")
        outfile.write("iterations = " + str(func[1]) + "\n")
        
        outfile.write("e = " + self._format.format(func[2]))
        outfile.close()


def main():
    fx1 = fx("input.txt")
    fx1.out(filestr="output.txt")


if __name__ == "__main__":
    main()