import random
import numpy


# Gold Costs
base_cost = 4800

costs = {
    "grace" : 120,
    "blessing" : 480,
    "protection": 900
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
    "grace" : 0.1,
    "blessing": 0.2,
    "protection" : 0.58
}


def get_values(dictionary, graces, blessings, protections):
    return dictionary['grace'] * graces + dictionary['blessing'] * blessings + dictionary['protection'] * protections

def sim(base_cost, base_percent, artisan_base, pity, graces=0, blessings=0, protections=0):

    enchanted = False 
    total_cost = 0

    success_chance = base_percent

    current_artisans = 0

    for i in range(100):

        if current_artisans >= 100:
            return total_cost + base_cost

        success_chance = success_chance + get_values(increase, graces, blessings, protections)
        total_cost = total_cost + base_cost + get_values(costs, graces, blessings, protections)
        #print(success_chance, current_artisans, total_cost)

        attempt = random.random()
        if attempt < success_chance:
            return total_cost

        current_artisans = current_artisans + artisan_base + get_values(artisan_increase, graces, blessings, protections)

        #print(attempt, success_chance, current_artisans, total_cost)


trials = [
    [0,0,0], # No solars
    [24,0,0], # all graces
    [24.,0,3], # all grace, all protection
    [24,12,3] #everything
]

sim_number = 100000

for t in trials:
    print(t, numpy.average([sim(base_cost, base_percent,  artisans, pity, t[0], t[1], t[2]) for x in range(sim_number)]))

