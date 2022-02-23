from game import *

if __name__ == '__main__':
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='')
    parser.add_argument("algorithm",
                        metavar="algorithm name",
                        help="'baeysian' or 'benchmark'")
    parser.add_argument('--ratio', required=False,
                        metavar="float number",
                        help='Ratio of whites to black tiles, eg. 0.6')
    args = parser.parse_args()
    game = None
    ratio = 0.6

    if args.algorithm != "benchmark" and args.algorithm != "bayesian":
        raise ValueError('Invalid algorithm.')    
    if args.ratio:
        ratio = float(args.ratio)

    if args.algorithm == "benchmark":
        print("Benchmark algorithm starts")
        game = Game(2, ratio)
    else:
        print("Bayesian algorithm starts")
        game = Game(1, ratio)

    game.run()
