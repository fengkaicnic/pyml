import matplotlib.pyplot as plt

sales = [(99, 91), (85, 54), (25, 10), (15, 6), (16, 3), (25, 16), (7, 2), (25, 19), (12, 2), \
         (5, 5), (4, 1), (9, 7), (4, 4), (2, 1), (18, 7)]

x = [i for i in range(len(sales))]

y = [float(item[1])/item[0] for item in sales]

plt.plot(x, y)

plt.show()
