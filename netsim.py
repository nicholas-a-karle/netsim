
import sys

import random
import time
from sng import social_network

if __name__ == "__main__":
    print("\n\nRunning...\n\n")

    # testing edgelist vs. non-edgelist reciprocity run

    num_nodes = int(sys.argv[1])
    precision = int(sys.argv[2])

    g = social_network()
    g.set_social_parameters()
    g.add_nodes(num_nodes)

    for i in range(precision + 1):
        density = i / precision


        g.randomly_form_edges(density)
        start = time.time()
        g.reciprocate(True)
        elnat = time.time() - start

        g.clear_edges()
        g.randomly_form_edges(density)
        start = time.time()
        g.reciprocate(False)
        amnat = time.time() - start

        g.clear_edges()
        g.randomly_form_edges(density)
        start = time.time()
        g.reciprocate_no_numall(True)
        elnot = time.time() - start

        g.clear_edges()
        g.randomly_form_edges(density)
        start = time.time()
        g.reciprocate_no_numall(False)
        amnot = time.time() - start

        elrpi = (elnat - elnot) / elnat if elnat != 0 else 0.0001
        amrpi = (amnat - amnot) / amnat if amnat != 0 else 0.0001

        print(f"{elnat:.2f} \t{elnot:.2f} \t{elrpi:.2f} \t|\t{amnat:.2f} \t{amnot:.2f} \t{amrpi:.2f}")

        


    print("\n\nDone.\n\n")