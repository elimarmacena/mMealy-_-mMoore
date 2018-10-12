from sys import argv
from typing import List
from os import path

import script.machine_transformation as MT
import script.s_expression as SE


def obter_nome_arqs(args: List[str]) -> dict:
	"""
	Processa a lista de argumentos e retorna um dicionário com os caminhos dos arq. de entrada e saída.

	Se algum argumento estiver ausente, então a execução é abortada.
	:param args: Lista de argumentos obtidos via linha de comando
	:return: Dicionário contendo os caminhos do arquivo de entrada("path_in") e de saída ("path_out")
	"""

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
		arq.write(SE.print_sexp(lista_maquina))

	return 0


def main(args: List[str]):

	# Verifica se os argumentos estão corretos e obtém os paths dos arquivos;
	dict_nome_arqs = obter_nome_arqs(args)

	# Converte a S-Expression do path do arquivo de entrada para lista;
	lista = arq_sexp_para_lista(dict_nome_arqs["path_in"])

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
	lista_para_arq_sexp(MT.machine_to_list(nova_maquina), dict_nome_arqs["path_out"])

	return 0


if __name__ == '__main__':
	main(argv)
