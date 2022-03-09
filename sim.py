import random
import numpy


# Gold Costs
base_cost = 3600

costs = {
    "grace" : 100,
    "blessing" : 365,
    "protection": 790
}


#% increase : 1% = 0.01
increase = {
    "grace": 0.0021,
    "blessing": .0042,
    "protection": .0125
}

base_percent = 0.15

pity = 0.015

#artisans pities at 100
artisans = 6.97

artisan_increase = {
    "grace" : 0.105,
    "blessing": 0.21,
    "protection" : 0.58
}


def get_values(dictionary, graces, blessings, protections):
    return dictionary['grace'] * graces + dictionary['blessing'] * blessings + dictionary['protection'] * protections

def sim(base_cost, base_percent, artisan_base, pity, graces=0, blessings=0, protections=0):
    total_cost = 0

    success_chance = base_percent

    current_artisans = 0

    while True:

        if current_artisans >= 100:
            return total_cost + base_cost

        next_artisans = current_artisans + artisan_base + get_values(artisan_increase, graces, blessings, protections)

        while next_artisans > 100:
            if blessings > 0 and (next_artisans - artisan_increase["blessing"] > 100):
                blessings = blessings - 1
                next_artisans = next_artisans - artisan_increase["blessing"]
            else:
                if protections > 0 and (next_artisans - artisan_increase["protection"] > 100):
                    blessings = blessings - 1
                    next_artisans = next_artisans - artisan_increase["protection"]
                else:
                    if protections > 0 and (next_artisans - artisan_increase["grace"] > 100):
                        graces = graces - 1
                        next_artisans = next_artisans - artisan_increase["grace"]
                    else:
                        break


        current_artisans = current_artisans + artisan_base + get_values(artisan_increase, graces, blessings, protections)

        success_chance = success_chance + get_values(increase, graces, blessings, protections)
        total_cost = total_cost + base_cost + get_values(costs, graces, blessings, protections)
        #print(success_chance, current_artisans, total_cost)

        attempt = random.random()
        if attempt < success_chance:
            return total_cost


        #print(attempt, success_chance, current_artisans, total_cost)


trials = [
    [0,0,0], # No solars
    [24,0,0], # all graces
    [24.,0,3], # all grace, all protection
    [24,12,3] #everything
]

sim_number = 10000

for t in trials:
    trial = [sim(base_cost, base_percent, artisans, pity, t[0], t[1], t[2]) for x in range(sim_number)]
    print(t, numpy.average(trial), numpy.median(trial))

print("----")
l_mean, l_median = 0, 0
for i in range(25):
    trial = [sim(base_cost, base_percent, artisans, pity, i, 0, 0) for x in range(sim_number)]
    mean = numpy.average(trial)
    median = numpy.median(trial)
    print(i, mean, median, mean - l_mean, median - l_median)
    l_mean = mean
    l_median = median
