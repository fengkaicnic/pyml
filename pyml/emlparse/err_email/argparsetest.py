import argparse
parser = argparse.ArgumentParser()

parser.add_argument('squre', help='suqare the num')
args = parser.parse_args()

print type(args.squre)
print int(args.squre) ** 2