import math
import numpy


class class_sinus:

    result = 0

    def __init__(self, start_result):
        self.result = start_result

    def sinusx(self, x):
        y = math.sin(x)
        self.result = y

    def logarifm(self, x):
        y = math.log(x, 10)
        self.result = y

    def print_result(self):
        print(self.result)



A = class_sinus(-1)
A.print_result()

A.sinusx(0.5)
A.print_result()


A.logarifm(30)
A.print_result()

