from sys import argv
from typing import List
from os import path

from machine_transformation import *
import s_expression


def obter_nome_arqs(args: List[str]) -> dict:

    # Verifique se há exatamente 5 argumentos:
    # Nome do prog., param. -i, path arq. de entrada, param. -o, path arq. saída
    if (len(args) != 5):
        print("#ERRO: Número incorreto de argumentos!")
        exit(1)

    else:
        dict_nome_arqs = {"path_in": None, "path_out": None}

        # Para cada arg, verifique se é um param. -i ou -o;
        for i in range(1, len(args)):

            # Se o argumento atual for uma flag, E;
            # houver um próximo argumento que NÃO seja uma flag;
            # Pegue este próximo como caminho de um arquivo;
            if args[i].lower() == "-i" and i < (len(args) - 1) and args[i + 1][0] != '-':
                dict_nome_arqs["path_in"] = args[i + 1]

            elif args[i].lower() == "-o" and i < (len(args) - 1) and args[i + 1][0] != '-':
                dict_nome_arqs["path_out"] = args[i + 1]

        if not dict_nome_arqs["path_in"]:
            print("#ERRO: Path do arquivo de entrada ou argumento '-i' não declarado!")
            exit(1)

        elif not dict_nome_arqs["path_out"]:
            print("#ERRO: Path do arquivo de saída ou argumento '-o' não declarado!")
            exit(1)

        return dict_nome_arqs


def arq_sexpression_to_list(path_arq: str) -> List:

    # Se o arquivo de entrada não existir, aborte a execução;
    if not path.exists(path_arq):
        print("#ERRO: Arquivo '%s' não encontrado, verifique o caminho." % path_arq)
        exit(1)

    with open(path_arq, 'r') as arq_in:
        return s_expression.parse_sexp(arq_in.read())

def list_to_arq_sexpression(lista_maquina: List, nome_arq_saida: str):
    #TODO já há método p/ converter de S-Exp. p/ lista, mas há p/ o inverso?
    pass

def main(args: List[str]):

    #---EXEMPLO de conversão de um txt S-EXP MEALY obtido via CLI p/ máquina---#


    # Verifica se os argumentos estão corretos e obtém os paths dos arquivos;
    dict_nome_arqs = obter_nome_arqs(args)

    # Converte a S-Expression do path do arquivo de entrada para lista;
    lista = arq_sexpression_to_list(dict_nome_arqs["path_in"])

    # Converte de lista para máquina (dict) e imprime a máquina;
    show_machine(list_to_machine(lista))

    
    #---FIM EXEMPLO---#

    teste = ['moore', ['symbols-in', 'a', 'b'], ['symbols-out', 0, 1], ['states', 'q0', "q0'", 'q1', 'q2', 'q3', "q3'"],
             ['start', 'q0'], ['finals', 'q3', "q3'"],
             ['trans', ['q0', 'q1', 'a'], ['q0', 'q3', 'b'], ["q0'", "q1", "a"], ["q0'", "q3", "b"], ['q1', "q3'", 'a'],
              ['q1', 'q2', 'b'], ['q2', "q3", 'a'], ['q2', "q3'", 'b'], ['q3', "q3'", 'a'], ['q3', "q0'", 'b'],
              ["q3'", "q3'", 'a'], ["q3'", "q0'", 'b']],
             ['out-fn', ['q0', []], ["q0'", 1], ['q1', 0], ['q2', 1], ['q3', 0], ["q3'", 1]]]
    maquina = list_to_machine(teste)

    try:
        show_machine(maquina)
        # mealy_to_moore(maquina)

    except ValueError as err:
        print(err)
    # show_machine(maquina)
    # moore = mealy_to_moore(maquina)
    # show_machine(moore)
    # mealy = moore_to_mealy(moore)
    # show_machine(mealy)
    # show_machine(mealy_to_moore(mealy))

    return 0


if __name__ == '__main__':
    main(argv)
