
import random
import time
from sng import social_network

if __name__ == "__main__":

    print("Running...")

    rand_n_range = (100, 1000)
    num_iterates = 5
    num_runs = 2


    rem = 0.1
    add = 0.1
    start = time.time()

    for _ in range(num_iterates):
        g = social_network()
        g.set_social_parameters(random_additions=add, random_removals=rem)
        num = random.randint(rand_n_range[0], rand_n_range[1])
        g.add_nodes(num)
        for _ in range(num_runs):
            g.random_actions()

    end = time.time()

    time_0 = end - start


    start = time.time()

    for _ in range(num_iterates):
        g = social_network()
        g.set_social_parameters(random_additions=add, random_removals=rem)
        num = random.randint(rand_n_range[0], rand_n_range[1])
        g.add_nodes(num)
        for _ in range(num_runs):
            g.random_actions_1()

    end = time.time()

    time_1 = end - start

    start = time.time()

    for _ in range(num_iterates):
        g = social_network()
        g.set_social_parameters(random_additions=add, random_removals=rem)
        num = random.randint(rand_n_range[0], rand_n_range[1])
        g.add_nodes(num)
        for _ in range(num_runs):
            g.random_actions_2()

    end = time.time()

    time_2 = end - start

    print(f"\nA = {add}, R = {rem}")
    print(f"V0: \t{time_0:.3f} seconds")
    print(f"V1: \t{time_1:.3f} seconds")
    print(f"V2: \t{time_2:.3f} seconds")

    rem = 0.0
    add = 0.1
    start = time.time()

    for _ in range(num_iterates):
        g = social_network()
        g.set_social_parameters(random_additions=add, random_removals=rem)
        num = random.randint(rand_n_range[0], rand_n_range[1])
        g.add_nodes(num)
        for _ in range(num_runs):
            g.random_actions()

    end = time.time()

    time_0 = end - start


    start = time.time()

    for _ in range(num_iterates):
        g = social_network()
        g.set_social_parameters(random_additions=add, random_removals=rem)
        num = random.randint(rand_n_range[0], rand_n_range[1])
        g.add_nodes(num)
        for _ in range(num_runs):
            g.random_actions_1()

    end = time.time()

    time_1 = end - start

    start = time.time()

    for _ in range(num_iterates):
        g = social_network()
        g.set_social_parameters(random_additions=add, random_removals=rem)
        num = random.randint(rand_n_range[0], rand_n_range[1])
        g.add_nodes(num)
        for _ in range(num_runs):
            g.random_actions_2()

    end = time.time()

    time_2 = end - start

    print(f"\nA = {add}, R = {rem}")
    print(f"V0: \t{time_0:.3f} seconds")
    print(f"V1: \t{time_1:.3f} seconds")
    print(f"V2: \t{time_2:.3f} seconds")

    rem = 0.1
    add = 0.0
    start = time.time()

    for _ in range(num_iterates):
        g = social_network()
        g.set_social_parameters(random_additions=add, random_removals=rem)
        num = random.randint(rand_n_range[0], rand_n_range[1])
        g.add_nodes(num)
        for _ in range(num_runs):
            g.random_actions()

    end = time.time()

    time_0 = end - start


    start = time.time()

    for _ in range(num_iterates):
        g = social_network()
        g.set_social_parameters(random_additions=add, random_removals=rem)
        num = random.randint(rand_n_range[0], rand_n_range[1])
        g.add_nodes(num)
        for _ in range(num_runs):
            g.random_actions_1()

    end = time.time()

    time_1 = end - start

    start = time.time()

    for _ in range(num_iterates):
        g = social_network()
        g.set_social_parameters(random_additions=add, random_removals=rem)
        num = random.randint(rand_n_range[0], rand_n_range[1])
        g.add_nodes(num)
        for _ in range(num_runs):
            g.random_actions_2()

    end = time.time()

    time_2 = end - start

    print(f"\nA = {add}, R = {rem}")
    print(f"V0: \t{time_0:.3f} seconds")
    print(f"V1: \t{time_1:.3f} seconds")
    print(f"V2: \t{time_2:.3f} seconds")

    rem = 0.0
    add = 0.0
    start = time.time()

    for _ in range(num_iterates):
        g = social_network()
        g.set_social_parameters(random_additions=add, random_removals=rem)
        num = random.randint(rand_n_range[0], rand_n_range[1])
        g.add_nodes(num)
        for _ in range(num_runs):
            g.random_actions()

    end = time.time()

    time_0 = end - start


    start = time.time()

    for _ in range(num_iterates):
        g = social_network()
        g.set_social_parameters(random_additions=add, random_removals=rem)
        num = random.randint(rand_n_range[0], rand_n_range[1])
        g.add_nodes(num)
        for _ in range(num_runs):
            g.random_actions_1()

    end = time.time()

    time_1 = end - start

    start = time.time()

    for _ in range(num_iterates):
        g = social_network()
        g.set_social_parameters(random_additions=add, random_removals=rem)
        num = random.randint(rand_n_range[0], rand_n_range[1])
        g.add_nodes(num)
        for _ in range(num_runs):
            g.random_actions_2()

    end = time.time()

    time_2 = end - start

    print(f"\nA = {add}, R = {rem}")
    print(f"V0: \t{time_0:.3f} seconds")
    print(f"V1: \t{time_1:.3f} seconds")
    print(f"V2: \t{time_2:.3f} seconds")

    print("\n\nDone")
    