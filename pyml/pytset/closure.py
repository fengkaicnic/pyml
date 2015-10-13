#

def plus(number):
    def plus_in(number_in):
        print str(number_in) + '\r\n'
        return number+number_in
    return plus_in

v1 = plus(2)
print v1(100)