from game import *

if __name__ == '__main__':
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='')
    parser.add_argument("algorithm",
                        metavar="algorithm name",
                        help="'baeysian' or 'benchmark'")
    parser.add_argument("--n",
                        metavar="Number of runs",
                        help="An integer, e.g. 5")
    parser.add_argument('--ratio', required=False,
                        metavar="float number",
                        help='Ratio of whites to black tiles, eg. 0.6')
    parser.add_argument('--map', required=False,
                        metavar="map name",
                        help="Name of the map, e.g. classic")
    parser.add_argument('--ghosts', required=False,
                        metavar="number of ghosts",
                        help="Number of Ghosts, e.g. 25")
    parser.add_argument('--colours', required=False,
                        metavar="number of colours",
                        help="Number of Colours, e.g. 3")

    args = parser.parse_args()
    game = None
    ratio = [0.55]
    map = 'classic'
    ghosts = 25
    games = 100
    colours = 2

    if args.algorithm != "benchmark" and args.algorithm != "bayesian":
        raise ValueError('Invalid algorithm.')
    
    if args.n:
        games = int(args.n)

    if args.ratio:
        ratio = args.ratio.split(",")
        ratio = [float(i) for i in ratio]

    if args.colours:
        if args.algorithm == "benchmark" and int(args.colours) > 2:
            raise ValueError('Benchmark algorithm is used in Binary scenarios only')
        colours = int(args.colours)
    
    if args.algorithm == "benchmark" and len(ratio) > 1:
        raise ValueError('Benchmark algorithm is used in Binary scenarios only')
    
    if args.map:
        map = args.map
        
    if args.ghosts:
        ghosts = int(args.ghosts)

    if args.algorithm == "benchmark":
        print("Benchmark algorithm starts")
        game = Game(2, ratio, map, ghosts, games, 2)
        game.run()
    else:
        game = Game(1, ratio, map, ghosts, games, colours)
        game.run()