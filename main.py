import awsinstance as awsins
from argparse import ArgumentParser as argp



def parsearguments():
    parser = argp()
    parser.add_argument("--saludar", "-s", help="Imprime un saludo")
    parser.add_argument("--despedir", "-d", help="Imprime una despedida")
    parser.add_argument("--target", "-t", help="Imprime la direccion IP")
    return parser.parse_args()


def run_menu():
    pass

run_menu()