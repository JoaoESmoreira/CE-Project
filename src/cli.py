
import argparse
import sys
import logging
from typing import Optional
from time import perf_counter

from solvers import *

def cli(Problem):
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-file', type=argparse.FileType('w'), default=sys.stderr)
    parser.add_argument('--input-file', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--output-file', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('--generate-data', type=bool, default=False)
    parser.add_argument('--budget', type=int, default=100)
    parser.add_argument('--algorithm',
                        choices=['random', 'rr', 'sea', 'sss'],
                        default='none')
    args = parser.parse_args()

    if args.generate_data:
        from generate_maps import write_maps
        write_maps()

    p = Problem.from_textio(args.input_file)
    #if s is not None:
    if args.algorithm == 'random':
        s = p.empty_solution()
        s = random_construction(s)
    elif args.algorithm == 'rr':
        s = random_restart(p, args.budget)
    elif args.algorithm == 'sss':
        for _ in range(200):
            s = sea(p, args.budget)
            if s is not None:
                print(s.output(), end="", file=args.output_file)
                if s.is_feasible():
                    print(f"Solution is feasible. Fitness: {s.fitness():.3f}")
                else:
                    print(f"Solution not feasible. Fitness: {s.fitness():.3f}")
    elif args.algorithm == 'sea':
        s = sea(p, args.budget)

    if s is not None:
        print(s.output(), end="", file=args.output_file)
        if s.is_feasible():
            print(f"Solution is feasible. Fitness: {s.fitness():.3f}")
        else:
            print(f"Solution not feasible. Fitness: {s.fitness():.3f}")
