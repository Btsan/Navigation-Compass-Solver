import argparse
import numpy as np

"""
python navigation_compass.py \
    --inner 180 \
    --middle 240 \
    --outer 60 \
    --marks-inner 3 \
    --marks-middle 1 \
    --marks-outer 2 \
    --inner-cw \
    --middle-cw \
    -a inner \
    -b middle outer \
    -c inner outer \
"""


def main():
    parser = argparse.ArgumentParser(
                description='solver for navigation compass puzzles',
                epilog='python navigation_compass.py --inner 60 --middle 0 --outer 180 --marks-inner 4 --marks-middle 3 --marks-outer 1 --inner-cw --middle-cw --outer-cw -a inner -b middle outer -c inner outer')
    parser.add_argument('--inner', type=int, required=True, help='degree of inner celestial axis, e.g. 0, 60, 120, 180, 240, 300, 360')
    parser.add_argument('--middle', type=int, required=True, help='degree of middle celestial axis, e.g. 0, 60, 120, 180, 240, 300, 360')
    parser.add_argument('--outer', type=int, required=True, help='degree of outer celestial axis, e.g. 0, 60, 120, 180, 240, 300, 360')
    parser.add_argument('--marks-inner', type=int, required=True, help='number of bright astral marks on inner ring')
    parser.add_argument('--marks-middle', type=int, required=True, help='number of bright astral marks on middle ring')
    parser.add_argument('--marks-outer', type=int, required=True, help='number of bright astral marks on outer ring')
    parser.add_argument('--inner-cw', action='store_true', help='sets to true if inner ring rotates clockwise')
    parser.add_argument('--middle-cw', action='store_true', help='sets to true if middle ring rotates clockwise')
    parser.add_argument('--outer-cw', action='store_true', help='sets to true if outer ring rotates clockwise')
    parser.add_argument('-a', '--group-a', nargs='+', choices=['inner', 'middle', 'outer'], help='group of rings that rotate together, e.g. "middle outer" or "inner outer"')
    parser.add_argument('-b', '--group-b', nargs='+', choices=['inner', 'middle', 'outer'], help='group of rings that rotate together, e.g. "middle outer" or "inner outer"')
    parser.add_argument('-c', '--group-c', nargs='+', choices=['inner', 'middle', 'outer'], help='group of rings that rotate together, e.g. "middle outer" or "inner outer"')
    parser.add_argument('-N', '--maxit', default=100, help='maximum number of brute-force attempts"')
    args = parser.parse_args()
    print(args)

    assert args.inner % 60 == 0, f'inner axis ({args.inner}) must be a degree evenly divisible by 60'
    assert args.middle % 60 == 0, f'middle axis ({args.middle}) must be a degree evenly divisible by 60'
    assert args.outer % 60 == 0, f'outer axis ({args.outer}) must be a degree evenly divisible by 60'

    rot_inner = 360 - args.marks_inner * 60 if args.inner_cw else args.marks_inner * 60
    rot_middle = 360 - args.marks_middle * 60 if args.middle_cw else args.marks_middle * 60
    rot_outer = 360 - args.marks_outer * 60 if args.outer_cw else args.marks_outer * 60

    # convert degrees into positive [0, 360) range
    args.inner = (args.inner % 360 + 360) % 360
    args.middle = (args.middle % 360 + 360) % 360
    args.outer = (args.outer % 360 + 360) % 360

    rot_inner = (rot_inner % 360 + 360) % 360
    rot_middle = (rot_middle % 360 + 360) % 360
    rot_outer = (rot_outer % 360 + 360) % 360

    mat = []
    for rot, ring in zip([rot_inner, rot_middle, rot_outer], ['inner', 'middle', 'outer']):
            mat.append([rot if ring in group else 0 for group in [args.group_a, args.group_b, args.group_c]])
    mat = np.array(mat)
    print(f'A = {mat}')

    pos = np.array([(180 - args.inner + 360) % 360, (180 - args.middle + 360) % 360, (180 - args.outer + 360) % 360])
    print(f'b = {pos}')


    brute = [[360, 0, 0], [0, 360, 0], [0, 0, 360],
            [360, 360, 0], [360, 0, 360], [0, 360, 360],
            [360, 360, 360]]
    brute = list(map(np.array, brute))

    for i in range(args.maxit):
        for j, vec in enumerate(brute):
            ans = np.linalg.solve(mat, pos + i * vec)
            if (ans >= 0).all() and (np.mod(ans, 1) == 0).all():
                print(f'{i * len(brute) + j}: solve {pos} + {i} * {vec} = {pos + i * vec} = {ans}')
                steps = np.mod(ans, 6).astype(int)
                print(f'\t answer = {ans} % 6 = {steps}')
                print(f'\t rotate group A {args.group_a} {steps[0]} times')
                print(f'\t rotate group B {args.group_b} {steps[1]} times')
                print(f'\t rotate group C {args.group_c} {steps[2]} times')
                return i + 1
    return -1

if __name__ == '__main__':
    iterations = main()
    if iterations:
        print(f'Solved in {iterations} brute-force iterations')
    else:
        print(f'No solution found. Either the puzzle was input incorrectly and/or has no solution. Otherwise, try increasing iterations with --maxit (default 100)')