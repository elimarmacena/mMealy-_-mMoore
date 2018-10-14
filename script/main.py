from typing import List
from os import path
import argparse

import deus_ex_machina as MT
import s_expression as SE

parser = argparse.ArgumentParser()
parser.add_argument("-i", required=True, dest="filepath_in",
                    help="Flag para indicar o path do arquivo de entrada.")
parser.add_argument("-o", required=True, dest="filepath_out",
                    help="Flag para indicar o path do arquivo de saída.")
parser.add_argument("-a", help="Exemplo de chamada: python3 main.py -i maq_entrada.txt -o maq_saida.txt")

def arq_sexp_para_lista(path_arq: str) -> List:
	"""
	Processa a S-Expression do arquivo do path recebido e converte para uma lista.

	Se o caminho não existe de fato, então a execução é abortada.
	:param path_arq: Caminho do arquivo da S-Expression de entrada.
	:return: Lista obtida a partir da S-Expression (a ser convertida para máquina)
	"""

	# Se o arquivo de entrada não existir ou for uma pasta, aborte a execução;
	if not path.isfile(path_arq):
		print("#ERRO: O path '%s' não corresponde a um arquivo, verifique o caminho." % path_arq)
		exit(1)

	with open(path_arq, 'r') as arq:
		return SE.parse_sexp(arq.read())

def lista_para_arq_sexp(lista_maquina: List, caminho_arq_saida: str):
	"""
	Converte a lista recebida para S-Expression e a escreve no path do arquivo de saída.

	:param lista_maquina: Lista que representa a máquina
	:param nome_arq_saida: Caminho em que o arquivo com a S-Expression será escrito
	"""

	with open(caminho_arq_saida, 'w') as arq:
		arq.write(SE.to_sexp_visual(lista_maquina))

	return 0


def main():

	args = parser.parse_args()
	path_entrada = args.filepath_in
	path_saida = args.filepath_out

	# Converte a S-Expression do path do arquivo de entrada para lista;
	lista = arq_sexp_para_lista(path_entrada)

	# Converte de lista para máquina (dict) e imprime a máquina;
	maquina = MT.list_to_machine(lista)

	nova_maquina = None

	# Se a máquina for de Moore, converta para Mealy;
	if MT.check_kind_machine(maquina) == 1:
		nova_maquina = MT.moore_to_mealy(maquina)

	# Se a máquina for de Mealy, converta para Moore
	elif MT.check_kind_machine(maquina) == 2:
		nova_maquina = MT.mealy_to_moore(maquina)

	else:
		raise ValueError("#ERRO: O tipo da máquina é desconhecido!")

	# Escreva a nova máquina no caminho do arquivo de saída;
	lista_para_arq_sexp(MT.machine_to_list(nova_maquina), path_saida)

	return 0


if __name__ == '__main__':
	main()
