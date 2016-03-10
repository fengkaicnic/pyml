import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--path', default='d:/pop3', help='the path to store result')
parser.add_argument('--num', type=int, default=5, help='the repeat num to terminate the program')
args = parser.parse_args()
print args.path
print args.num