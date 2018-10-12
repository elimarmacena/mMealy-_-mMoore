import random
import string
from s_expression import print_sexp as out_sexp

# CHECK WHAT A KIND OF MACHINE IS
# 1 EQUALS MOORE || 2 EQUALS MEALY || -1 TYPE INVALID
def check_kind_machine(machine : dict) -> int:
	if (machine["type"].lower() == "moore"):
		return 1
	elif (machine["type"].lower() == "mealy"):
		return 0
	else:
		return -1

# VALIDATION OF THE ITENS RECIEVED
def list_validation(lst:list)->bool:
    # THE LIST OF DATE HAVE AN ORDER, CASE THE ORDER BE DIFFERENT WE THROW AN INFORMATION
    try:
        test = 100
        typeMachine = lst[0]
        test = lst[1].index('symbols-in')
        test = lst[2].index('symbols-out')
        test = lst[3].index('states')
        test = lst[4].index('start')
        test = lst[5].index('finals')
        test = lst[6].index('trans')
        if typeMachine.lower() == "moore":
            test = lst[7].index('out-fn')
        return True
    except ValueError:
        return False
    

# TRANSFORM A LIST TO A MACHINE DICTIONARY
def list_to_machine(lst_machine: list)->dict:
    if list_validation(lst_machine):
        machine = {}
        machine["type"] = lst_machine[0]
        machine["symbols_in"] = lst_machine[1][1:]
        machine["symbols_out"] = lst_machine[2][1:]
        machine["states"] = lst_machine[3][1:]
        machine["start"] = lst_machine[4][1:]
        machine["final"] = lst_machine[5][1:]
        machine["trans"] = lst_machine[6][1:]
        if machine["type"].lower() == "moore":
            machine["out_fn"] = lst_machine[7][1:]
        return machine
    else:
        raise ValueError ("A entrada nao segue o padrao necessario para que seja gerado uma maquina.")

# TRANSFORM A MACHINE INTO A LIST
def machine_to_list(machine:dict)->list:
    list_machine=[machine["type"],["symbols-in"],["symbols-out"],["states"],["start"],["finals"],["trans"]]
    list_machine[1].extend(machine["symbols_in"])
    list_machine[2].extend(machine["symbols_out"])
    list_machine[3].extend(machine["states"])
    list_machine[4].extend(machine["start"])
    list_machine[5].extend(machine["final"])
    list_machine[6].extend(machine["trans"])
    if machine["type"].lower() == "moore":
        list_machine.append(["out-fn"])
        list_machine[7].extend(machine["out_fn"])
    return list_machine

# TRANSFORM A LIST INTO A SEXPRESSION
def list_to_sexp(lst : list)->str:
    sexp = out_sexp(lst)
    return sexp

# SHOW THE PARAMETERS OF THE MACHINE
def show_machine(machine: dict):
    print("{0} MACHINE".format(machine["type"].upper()))
    print("INPUT SYMBOLS:")
    for x in machine["symbols_in"]:
        print(x)
    print("OUTPUT SYMBOLS:")
    for x in machine["symbols_out"]:
        print(x)
    print("STATES:")
    for x in machine["states"]:
        print(x)
    print("INITIAL SYMBOL: {0}".format(machine["start"]))
    print("FINAL STATE: {0}".format(machine["final"]))
    print("TRASATIONS")
    for x in machine["trans"]:
        print(x)
    if machine["type"].lower() == "moore":
        print("STATES AND OUTPUTS:")
        for x in machine["out_fn"]:
            print(x)
    print()

# CHEK IF THE MOORE MACHINE IS IMPOSSIPLE TO CONVERT TO A MEALY MACHINE
def moore_intransitive(moore: dict)->bool:
    starts = moore["start"]
    for y in moore["out_fn"]:
        # IF THE INITIAL STATE HAVE A OUTPUT SYMBOL WE CAN'T CONVERT INTO A MEALY MACHINE
        if y[0] in starts and y[1] != []:
            return True
    return False

# TRANSFORM THE OUTPUT IN THE STATE IN A OUTPUT IN THE TRANSATION
def treat_transaction_moore(mealy: dict, moore: dict):
    mealy_transacion = []
    # FOR EVERY TRANSACTION IN THE MOORE MACHINE WE PUT THE OUTPUT SYBOML OF THE STATE THAT TRANSATION ARE GOING
    for transactions in moore["trans"]:
        for output in moore["out_fn"]:
            if output[0] == transactions[1]:
                mealy_transacion.append(
                    [transactions[0], transactions[1], transactions[2], output[1]]
                )
    return mealy_transacion


# TRANSFORME A MOORE MACHINE INTO A MEALY MACHINE
def moore_to_mealy(moore_machine: dict)->dict:
    # CHECK OF THE POSSIBLLITY TO TRANSFORM THE MACHINE
	if (check_kind_machine(moore_machine) == 1):
		if (moore_intransitive(moore_machine)):
			raise ValueError(
				"Nao é possivel converver esta marquina para mealy pois possui saidas no seu estado inicial")
		else:
			# IN THIS POINT THE MACHINE WILL BE THE SAME AS THE MOORE MACHINE
			mealy_machine = {}
			mealy_machine["type"] = "mealy"
			mealy_machine["symbols_in"] = moore_machine["symbols_in"][:]
			mealy_machine["symbols_out"] = moore_machine["symbols_out"][:]
			mealy_machine["states"] = moore_machine["states"][:]
			mealy_machine["start"] = moore_machine["start"][:]
			mealy_machine["final"] = moore_machine["final"][:]
			# HERE WE MAKE A TRANSFORMATION FROM A STATE OUTPUT INTO A TRANSATION OUTPUT
			mealy_machine["trans"] = treat_transaction_moore(
				mealy_machine, moore_machine)
			return mealy_machine
	else:
		raise ValueError ( "Não é possivel converter a maquina para Mealy por a maquina informada nao é do tipo Moore" )

# USED TO ESTABLISH THE FINAL STATES IN THE MOORE MACHINE
def treat_final_symbols(new_states: list, finals_mealy: list):
    new_finals_states = []
    # FOR EVERY FINAL STATE THAT WE HAVE, WE CHECK THE DERIVATIVE STATES AND PUT THEM IN A LIST
    for final in finals_mealy:
        for state in new_states:
            if final == state[0]:
                for derivative_state in state[1]:
                    new_finals_states.append(derivative_state[0])
    return new_finals_states


# USED TO CHECK IF A OUTPUT SYMBOL IS ALREADY REGISTRED (ASSIST FUNCTIO TO TREAT_STATES)
def check_output(symbol_output: str, created_output: list)->bool:
    for output in created_output:
        if output[1] == symbol_output:
            return True
    return False

# USED TO CREATE A ITEM TO BE ADD IN THE STRUCT OF THE FUNCTION TREAT_STATES
def states_outfn(state: str, out_fn: list)->list:
    states_outfn = [state, []]
    for data in out_fn:
        states_outfn[1].append(data)
    return states_outfn


# RECIEVE A MEALY MACHINE AND CREATE A LIST WITH THE STATE OF THE MEALY MACHINE AND THE STATES(NEW INCLUDE) AND OUT_FNS
# STRUCT [[MEALY_STATE[[STATE,OUTPUT],....]], [MEALY_STATE[[STATE,OUTPUT],....]]....]
def treat_states(mealy: dict)->list:
    treat = []
    for mealy_state in mealy["states"]:
        outfn_mark = []
        for transaction in mealy["trans"]:
            if transaction[1] == mealy_state and mealy_state == mealy["start"][0]:
                if transaction[3] != [] and not check_output(transaction[3], outfn_mark):
                    outfn_mark.append(
                        [mealy_state+random.choice(string.ascii_uppercase), transaction[3]])
            elif transaction[1] == mealy_state:
                if not check_output(transaction[3], outfn_mark) and len(outfn_mark) > 0:
                    outfn_mark.append(
                        [mealy_state+random.choice(string.ascii_uppercase), transaction[3]])
                elif not check_output(transaction[3], outfn_mark) and len(outfn_mark) == 0:
                    outfn_mark.append([mealy_state, transaction[3]])
        if mealy_state == mealy["start"][0]:
            outfn_mark.append([mealy_state, []])
        treat.append(states_outfn(mealy_state, outfn_mark))
    return treat

# HERE WE CHANGE THE STATE DESTINATION FOR THE NEW STATE WHAT WE HAVE FROM OTHER STEPS
def treat_out_transaction(transaction_mealy: list, new_states: list):
    for state_created in new_states:
        # CASE THE STATE PASSED IS EQUALS THE ATUAL STATE
        if transaction_mealy[1] == state_created[0]:
            # WE WILL SEARCH FOR THE OUTPUTSYMBOL OF THE TRANSACTION
            for state_informations in state_created[1]:
                if transaction_mealy[3] == state_informations[1]:
                    new_destine_state = [
                        transaction_mealy[0], state_informations[0], transaction_mealy[2]]
                    return new_destine_state

# HERE WE CREATE THE TRANSACTIONS FOR THE MOORE MACHINE BASED ON THE NEW STATES CREATED
def transform_transaction_to_moore(transaction: list, new_states: list):
    moore_transactions = []
    for state_created in new_states:
        if transaction[0] == state_created[0]:
            for derivative_states in state_created[1]:
                # HERE WE ARE SETTING THE DERIVATIVE STATES IN THE TRANSATIONS OF THE ORIGINAL STATE
                moore_transactions.append(
                    [derivative_states[0], transaction[1], transaction[2]])
    return moore_transactions

# TRNASFORMATION MEALY MACHINE IN MOORE
def mealy_to_moore(mealy: dict)->dict:
	if (check_kind_machine(mealy) == 2):
		new_states = treat_states(mealy)  # NEW STATES WITH THE STATE ORIGEM
		# BEGIN THE CONSTRUCTION OF THE NEW MACHINE
		moore = {}
		moore["type"] = "moore"
		moore["symbols_in"] = []
		moore["symbols_out"] = []
		moore["states"] = []
		moore["start"] = []
		moore["final"] = []
		moore["trans"] = []
		moore["out_fn"] = []
		# SEETING THE INITAL SYMBOL
		moore["start"] = mealy["start"][:]
		# SETTING THE SYMBOLS_IN
		moore["symbols_in"] = mealy["symbols_in"]
		# SETTING THE SYMBOLS_OUT
		moore["symbols_out"] = mealy["symbols_out"]
		# SETTING THE FINALS SYMBOLS
		moore["final"].extend(treat_final_symbols(new_states, mealy["final"]))
		# SETTING THE NEW STATES AND THE OUT_FN INTO THE MOORE MACHINE
		for state_created in new_states:
			for derivative_state in state_created[1]:
				moore["states"].append(derivative_state[0])
			moore["out_fn"].extend(state_created[1])
		# NOW WE WILL US THE INFORMATION TO CHECK ALL TRANSACTIONS FROM MEALY MACHINE AND REPLACE WITH THE NEW DATA
		for mealy_transacions in mealy["trans"]:
			new_destine_state = treat_out_transaction(
				mealy_transacions, new_states)  # HERE WE WILL CHANGE THE STATE DESTINATION USING THE NEW STATES THAT WE HAVE
			# HERE WE WILL CREATE A LIST WITH THE ALL TRANSACTIONS OF THE STATE AND DERIVATE STATES
			moore_transactions = transform_transaction_to_moore(
				new_destine_state, new_states)
			moore["trans"].extend(moore_transactions)
		return moore
	else:
		raise ValueError("Nao é possive converter a maquina para Moore pois a maquina é do tipo Mealy")
