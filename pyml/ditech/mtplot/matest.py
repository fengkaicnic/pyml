#coding:utf8
import matplotlib.pyplot as plt
import sys
import numpy as np
reload(sys)
sys.setdefaultencoding('utf8')

def rect_plot():
    plt.title('gender ratio analysis')

    plt.xlabel(u'gender')
    plt.ylabel(u'num')
    plt.xticks((0, 1), ('male', 'female'))

    rect = plt.bar(left=(0, 1), height=(1, 1), width=0.5, align='center')
    plt.legend((rect,), ('example',))
    plt.show()


def ser_plot():
    x = np.linspace(0, 10, 1000)
    y = np.sin(x)
    z = np.cos(x**2)

    plt.figure(figsize=(10, 5))
    plt.plot(x, y, label="$sin(x)$", color="red", linewidth=2)
    plt.plot(x, z, "b--", label="$cos(x^2)$")
    plt.xlabel("Time(s)")
    plt.ylabel("Volt")
    plt.title("PyPlot First Example")
    plt.ylim(-1.2, 1.2)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    ser_plot()
