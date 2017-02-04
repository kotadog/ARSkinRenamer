import argparse
import codecs


def unescaped_str(arg_str):
    return codecs.decode(arg_str, 'unicode_escape')


parser = argparse.ArgumentParser(
    description='Rename skins and generate Skin String for Wiki.')
parser.add_argument('-l', dest='lancer',
                    help='Name of Freelancer',
                    required=True)
parser.add_argument('-s', dest='skin_dir',
                    help='Directory where Fan Site Kit skins are located. (use forward slashes (/) instead of backslashes (\\)',
                    default=None)
parser.add_argument('-c', dest='config',
                    help='Location of config file containing skin mappings. (use forward slashes (/) instead of backslashes (\\)')

def parse():
    args = parser.parse_args()
    return args
