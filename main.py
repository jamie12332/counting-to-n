import matplotlib.pyplot as plot
import random

def safe_divide(numerator, divisor):
    if divisor == 0:
        return 0
    return numerator / divisor

def random_subset(l, subset_size):
    out = []
    for i in range(0, subset_size):
        out += [l[int(random.random() * (len(l) - i))]]
    return out

def simulate_capture_recapture(population_size, first_capture_number, second_capture_number):
    population = [{"tagged": False}] * population_size
    for captured in random_subset(population, first_capture_number):
        captured["tagged"] = True
    second_capture_tagged_number = 0
    for captured in random_subset(population, second_capture_number):
        if captured["tagged"]:
            second_capture_tagged_number += 1
    return {
        "lincoln_peterson_estimated_size": safe_divide(first_capture_number * second_capture_number, second_capture_tagged_number),
        "chapman_estimated_size": (first_capture_number + 1) * (second_capture_number + 1) / (second_capture_tagged_number + 1) - 1,
    }

x_coords = list(range(1, 1 * (10**7), 1000000))
results = list(map(lambda p: simulate_capture_recapture(p, int(p/10), int(p/10)), x_coords))
y_coords1 = list(map(lambda r: r["lincoln_peterson_estimated_size"], results))
y_coords2 = list(map(lambda r: r["chapman_estimated_size"], results))

plot.scatter(x_coords, y_coords1, color = "blue")
plot.scatter(x_coords, y_coords2, color = "red")
plot.xlabel("Population size")
plot.ylabel("Estimated population size")
plot.savefig("plot.png", dpi=300)

