#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools
import os
import multiprocessing
import argparse
import math
import subprocess
from launcherfunc import aco_launcher, brkga_launcher, ils_launcher, acopp_launcher, saashc_launcher

if __name__ == "__main__":

    tsp_base = ["d2103", "d15112", "pla7397", "pla33810", ]
    number_of_items_per_city = [1, 3, 5, 10, ]
    knapsack_type = ["bsc", "unc", "usw", ]
    knapsack_size = [1, 5, 10, ]
    maximum_travel_time = [1, 2, 3, ]
    number_of_runs = 1

    os.system("make clean")
    os.system("make ils")
    os.system("make brkga")
    os.system("make aco")
    os.system("make aco++")
    os.system("make saashc")

    pool = multiprocessing.Pool(processes=max(1, multiprocessing.cpu_count() - 2))
    for _product in itertools.product(tsp_base, number_of_items_per_city, knapsack_type, knapsack_size, maximum_travel_time):
        _tsp_base, _number_of_items_per_city, _knapsack_type, _knapsack_size, _maximum_travel_time = _product
        for repetition in range(number_of_runs):
            pool.apply_async(ils_launcher, args=(_tsp_base, _number_of_items_per_city, _knapsack_type, _knapsack_size, _maximum_travel_time, repetition))
            pool.apply_async(brkga_launcher, args=(_tsp_base, _number_of_items_per_city, _knapsack_type, _knapsack_size, _maximum_travel_time, repetition))
            pool.apply_async(aco_launcher, args=(_tsp_base, _number_of_items_per_city, _knapsack_type, _knapsack_size, _maximum_travel_time, repetition))
            pool.apply_async(acopp_launcher, args=(_tsp_base, _number_of_items_per_city, _knapsack_type, _knapsack_size, _maximum_travel_time, repetition))
            pool.apply_async(saashc_launcher, args=(_tsp_base, _number_of_items_per_city, _knapsack_type, _knapsack_size, _maximum_travel_time, repetition))

    pool.close()
    pool.join()
