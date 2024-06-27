
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

    print(f"Density\t  EL T\t  AM T\t Diff\tRPI\tWinner")
    for i in range(precision + 1):
        density = i / precision
        g.randomly_form_edges(density)

        start = time.time()
        g.reciprocate(True)
        tel = time.time() - start

        start = time.time()
        g.reciprocate(False)
        tam = time.time() - start

        diff = abs(tam - tel)
        rpi = diff / max(tam, tel)
        win = "EL" if (tel < tam) else "AM"

        print(f"{density:.2f} \t| {tel:.2f} \t| {tam:.2f} | {diff:.2f} | {rpi:.2f} |  {win}")


    print("\n\nDone.\n\n")