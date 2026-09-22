import matplotlib.pyplot as plot
import random
import time
import numpy

start = time.time()

def safe_divide(numerator, divisor):
    if divisor == 0:
        return 0
    return numerator / divisor

def insert_sorted(l, e):
    for i, elem in enumerate(l):
        if elem > e:
            return l[:i] + [e] + l[i:]
    return l + [e]

REPEATS = 500
MIN_POPULATION_SIZE = 1
MAX_POPULATION_SIZE = 1000
POPULATION_STEP = 50

def simulate_capture_recapture(population_size, first_capture_number, second_capture_number):
    population = [{"tagged": True}] * first_capture_number + [{"tagged": False}] * (population_size - first_capture_number)
    lincoln_peterson_estimated_sizes = []
    chapman_estimated_sizes = []
    for _ in range(0, REPEATS):
        second_capture_tagged_number = 0
        for captured in random.sample(population, second_capture_number):
            if captured["tagged"]:
                second_capture_tagged_number += 1
        lincoln_peterson_estimated_sizes = insert_sorted(lincoln_peterson_estimated_sizes, safe_divide(first_capture_number * second_capture_number, second_capture_tagged_number))
        chapman_estimated_sizes = insert_sorted(chapman_estimated_sizes, (first_capture_number + 1) * (second_capture_number + 1) / (second_capture_tagged_number + 1) - 1)
    return {
        "lincoln_peterson_estimated_size": numpy.quantile(lincoln_peterson_estimated_sizes, [0, 0.5, 1]),
        "chapman_estimated_size": numpy.quantile(chapman_estimated_sizes, [0, 0.5, 1]),
        "actual": population_size,
    }

x_coords = list(range(MIN_POPULATION_SIZE, MAX_POPULATION_SIZE, POPULATION_STEP))
results = list(map(lambda p: simulate_capture_recapture(p, int(p/5), int(p/5)), x_coords))
lincol_peterson_min = list(map(lambda r: r["lincoln_peterson_estimated_size"][0] / r["actual"], results))
lincol_peterson_median = list(map(lambda r: r["lincoln_peterson_estimated_size"][1] / r["actual"], results))
lincol_peterson_max = list(map(lambda r: r["lincoln_peterson_estimated_size"][2] / r["actual"], results))

chapman_min = list(map(lambda r: r["chapman_estimated_size"][0] / r["actual"], results))
chapman_median = list(map(lambda r: r["chapman_estimated_size"][1] / r["actual"], results))
chapman_max = list(map(lambda r: r["chapman_estimated_size"][2] / r["actual"], results))

print(time.time() - start)

plot.plot(x_coords, lincol_peterson_min, color = "blue", label = "Lincoln Peterson estimator min")
plot.plot(x_coords, lincol_peterson_median, color = "blue", label = "Lincoln Peterson estimator median")
plot.plot(x_coords, lincol_peterson_max, color = "blue", label = "Lincoln Peterson estimator max")

plot.plot(x_coords, chapman_min, color = "red", label = "Chapman estimator min")
plot.plot(x_coords, chapman_median, color = "red", label = "Chapman estimator median")
plot.plot(x_coords, chapman_max, color = "red", label = "Chapman estimator max")

plot.plot([MIN_POPULATION_SIZE, MAX_POPULATION_SIZE], [1, 1], color = "black", label = "Perfect estimator")
plot.xlabel("Population size")
plot.ylabel("Estimated population size / actual population size")
plot.legend()

print(time.time() - start)

plot.savefig("plot.png", dpi=300)

print(time.time() - start)

