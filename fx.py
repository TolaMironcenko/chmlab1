from math import sqrt # импорт функции для вычисления квадратного корня 
from sympy import Symbol, lambdify # импорт функций для символа x и для парсинга функций


class fx(): # класс fx

    def __init__(self, file: str) -> None: # функция инициализации класса (на вход подается строка название файла)
        file = open('input.txt') # открываем файл
        file = file.read() # читаем файл
        lines = file.split('\n') # разбиваем файл на строки
        self.f1 = lines[0] # первая строка это функция
        l, r = lines[1].split(' ') # вторая строка это интервал
        x = Symbol('x') # обьявляем символ х
        self.d1f = lambdify(x, eval(self.f1).diff()) # вычисляем первую производную
        self.d2f = lambdify(x, eval(self.f1).diff().diff()) # вычисляем вторую производную
        self.l = int(l) # присваиваем нижний предел
        self.r = int(r) # присваиваем верхний интервал
        self.e = float(lines[2]) # присваиваем погрешность (третья строка файла)
        self.method = int(lines[3]) # присваиваем метод (число номер метода)
        self.f = lambdify(x, eval(self.f1)) # присваиваем функцию
        self._len = len(str(self.e).split(".")[1]) # форматирование вывода
        self._format = f'{{:.{self._len}e}}' # форматирование вывода
        self.fx_format = f'{{:.{self._len}f}}' # форматирование вывода

    def dichotomy(self, l, r): # метод дихтомии
        k = 0 # количество итераций 
        while r - l >= self.e: # пока интервал больше погрешности
            m = (l + r) / 2 # берем середину интервала
            if self.f(l) * self.f(m) <= 0:
                r = m
            else:
                l = m
            k += 1
        return (l + r) / 2, k, (r - l) / 2

    def hord(self, l, r):
        k = 0 # количество итераций
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
        k = 0 # количество итераций
        p1 = p0 - self.f(p0) / self.d1f(p0)
        while abs(p0 - p1) > self.e:
            p0 = p1
            p1 = p0 - self.f(p0) / self.d1f(p0)
            k += 1
        return p1, k, abs(p1 - p0)


    def goldsech(self, l, r):
        k = 0 # количество итераций
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
        k = 0 # количество итераций
        p0 = (l + r) / 2
        while (abs(self.phi(p0)) >= 1):
            p0 = self.phi(p0)
            if (k >= 100):
                break
            k += 1
        return p0, k, self.f(p0)

    def combined(self, l, r):
        k = 0 # количество итераций
        while (abs(r-l) > self.e):
            c = l - (self.f(l) / (self.f(r) - self.f(l)) * (r - l))
            if (self.f(l) * self.d2f(l) > 0):
                l = l - self.f(l) / self.d1f(l)
                r = c
            if (self.f(r) * self.d2f(r) > 0):
                l = c
                r = r - self.f(r) / self.d1f(r)
            k += 1
        return (l + r) / 2, k, self.f((l + r) / 2)

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
        elif self.method == 5:
            func = self.combined(self.l, self.r)
            outfile.write("method = combined")
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