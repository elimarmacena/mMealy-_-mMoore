import random
import string

#TRANSFORM A LIST TO A MACHINE DICTIONARY 
def list_to_machine(lst_machine: list)->dict:
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

#SHOW THE PARAMETERS OF THE MACHINE 
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

#CHEK IF THE MOORE MACHINE IS IMPOSSIPLE TO CONVERT TO A MEALY MACHINE
def moore_intransitive(moore: dict)->bool:
    starts = moore["start"]
    for y in moore["out_fn"]:
        if y[0] in starts and y[1] != []: #IF THE INITIAL STATE HAVE A OUTPUT SYMBOL WE CAN'T CONVERT INTO A MEALY MACHINE
            return True
    return False

#TAKE THE TRANSACTION OF A STATE
def take_trans_state(state: str, machine: dict)->list:
    trans_state = []
    for x in machine["trans"]:
        if state == x[0]:
            trans_state.append(x) #TAKE THE TRANSACTION OF THE STATE AND PUT INTO A LIST
    return trans_state

#TAKE THE OUTPUT FROM THE STATE
def take_out_state(state: str, moore: dict)->str:
    for x in moore["out_fn"]:
        if state == x[0]:
            return x[1] #RETURN THE OUTPUT SYMBOL

#TRANSFORM THE OUTPUT IN THE STATE IN A OUTPUT IN THE TRANSATION
def out_to_trans(mealy: dict, moore: dict)->list:
    trans_with_out = []
    for state_x in moore["states"]:
        state = state_x
        state_out = take_out_state(state, moore)
        trans_state = take_trans_state(state, moore)
        for y in trans_state:
            _temp = y[:] #TAKE THE TRANSACTION WITHOUT THE OUTPUT SYMBOL
            _temp.append(state_out) #ADD THE OUTPUT SYMBOL INTO THE TTRANSACTION
            trans_with_out.append(_temp) #REFESH THE LIST OF TRANSACTION WITH OUTPUT
        # END FOR Y
    # END FOR X
    return trans_with_out

#TRANSFORME A MOORE MACHINE INTO A MEALY MACHINE
def moore_to_mealy(moore_machine: dict)->dict:
    # CHECK OF THE POSSIBLLITY TO TRANSFORM THE MACHINE
    if (moore_intransitive(moore_machine)):
        raise ValueError(
            "Nao é possivel converver esta marquina para mealy pois possui saidas no seu estado inicial")
    else:
        #IN THIS POINT THE MACHINE WILL BE THE SAME AS THE MOORE MACHINE
        mealy_machine = {}
        mealy_machine["type"] = "mayle"
        mealy_machine["symbols_in"] = moore_machine["symbols_in"][:]
        mealy_machine["symbols_out"] = moore_machine["symbols_out"][:]
        mealy_machine["states"] = moore_machine["states"][:]
        mealy_machine["start"] = moore_machine["start"][:]
        mealy_machine["final"] = moore_machine["final"][:]
        #HERE WE MAKE A TRANSFORMATION FROM A STATE OUTPUT INTO A TRANSATION OUTPUT
        mealy_machine["trans"] = out_to_trans(mealy_machine, moore_machine)
        return mealy_machine

#USED TO ESTABLISH THE FINAL STATES IN THE MOORE MACHINE
def treat_final_symbols(new_states:list,finals_mealy:list):
    new_finals_states=[]
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
# STRUCT [[MEALY_STATE[(STATE,OUTPUT),....]], [MEALY_STATE[(STATE,OUTPUT),....]]....]
def treat_states(mealy: dict)->list:
    treat = []
    for mealy_state in mealy["states"]:
        outfn_mark = []
        for transaction in mealy["trans"]:
            if transaction[1] == mealy_state and mealy_state == mealy["start"][0]:
                if transaction[3] != [] and not check_output(transaction[3], outfn_mark):
                    outfn_mark.append(
                        (mealy_state+random.choice(string.ascii_uppercase), transaction[3]))
            elif transaction[1] == mealy_state:
                print(len(outfn_mark))
                if not check_output(transaction[3], outfn_mark) and len(outfn_mark) > 0:
                    outfn_mark.append(
                        (mealy_state+random.choice(string.ascii_uppercase), transaction[3]))
                elif not check_output(transaction[3], outfn_mark) and len(outfn_mark) == 0:
                    outfn_mark.append((mealy_state, transaction[3]))
        if mealy_state == mealy["start"][0]:
            outfn_mark.append((mealy_state, []))
        treat.append(states_outfn(mealy_state, outfn_mark))
    return treat

#HERE WE CHANGE THE STATE DESTINATION FOR THE NEW STATE WHAT WE HAVE FROM OTHER STEPS
def treat_out_transaction(transaction_mealy: list, new_states: list):
    for state_created in new_states:
        if transaction_mealy[1] == state_created[0]: #CASE THE STATE PASSED IS EQUALS THE ATUAL STATE 
            for state_informations in state_created[1]: #WE WILL SEARCH FOR THE OUTPUTSYMBOL OF THE TRANSACTION
                if transaction_mealy[3] == state_informations[1]:
                    new_destine_state = [transaction_mealy[0],state_informations[0], transaction_mealy[2]]
                    return new_destine_state

def transform_transaction_to_moore(transaction:list, new_states:list):
    moore_transactions = []
    for state_created in new_states:
        if transaction[0] == state_created[0]:
            for derivative_states in state_created[1]:
                    moore_transactions.append([derivative_states[0],transaction[1],transaction[2]]) #HERE WE ARE SETTING THE DERIVATIVE STATES IN THE TRANSATIONS OF THE ORIGINAL STATE
    return moore_transactions


def mealy_to_moore(mealy: dict)->dict:
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
    #SEETING THE INITAL SYMBOL
    moore["start"] = mealy["start"][0]
    #SETTING THE SYMBOLS_IN
    moore["symbols_in"] = mealy["symbols_in"]
    #SETTING THE SYMBOLS_OUT
    moore["symbols_out"] = mealy["symbols_out"]
    #SETTING THE FINALS SYMBOLS
    moore["final"].extend(treat_final_symbols(new_states,mealy["final"]))
    # SETTING THE NEW STATES AND THE OUT_FN INTO THE MOORE MACHINE
    for state_created in new_states:
        for derivative_state in state_created[1]:
            moore["states"].append(derivative_state[0])
        moore["out_fn"].extend(state_created[1])
    # NOW WE WILL US THE INFORMATION TO CHECK ALL TRANSACTIONS FROM MEALY MACHINE AND REPLACE WITH THE NEW DATA
    for mealy_transacions in mealy["trans"]:
        new_destine_state = treat_out_transaction(
            mealy_transacions, new_states) #HERE WE WILL CHANGE THE STATE DESTINATION USING THE NEW STATES THAT WE HAVE
        moore_transactions = transform_transaction_to_moore(new_destine_state,new_states) #HERE WE WILL CREATE A LIST WITH THE ALL TRANSACTIONS OF THE STATE AND DERIVATE STATES
        moore["trans"].extend(moore_transactions)
    return moore









def main():
    teste = ['mealy', ['symbols-in', 'a', 'b'], ['symbols-out', 0, 1], ['states', 'q0', 'q1', 'q2', 'q3'], ['start', 'q0'], ['finals', 'q3'], ['trans', ['q0', 'q1',
                                                                                                                                                         'a', 0], ['q0', 'q3', 'b', 0], ['q1', 'q2', 'b', 1], ['q1', 'q3', 'a', 1], ['q2', 'q3', 'a', 0], ['q2', 'q3', 'b', 1], ['q3', 'q0', 'b', 1], ['q3', 'q3', 'a', 1]]]
    #['moore', ['symbols-in', 'a', 'b'], ['symbols-out', 0, 1], ['states', 'q0', "q0'", 'q1', 'q2', 'q3', "q3'"], ['start', 'q0'], ['finals', 'q3',"q3'"], ['trans', ['q0', 'q1', 'a'], ['q0', 'q3', 'b'],["q0'","q1","a"],["q0'","q3","b"], ['q1', "q3'", 'a'], ['q1', 'q2', 'b'], ['q2', "q3", 'a'], ['q2', "q3'", 'b'], ['q3', "q3'", 'a'], ['q3', "q0'", 'b'], ["q3'", "q3'", 'a'], ["q3'", "q0'",'b']], ['out-fn', ['q0', []], ["q0'", 1], ['q1', 0], ['q2', 1], ['q3', 0], ["q3'", 1]]]
    maquina = list_to_machine(teste)
    show_machine(maquina)
    moore = mealy_to_moore(maquina)
    show_machine(moore)
    # mealy = moore_to_mealy(moore)
    # show_machine(mealy)
    return 0


if __name__ == '__main__':
    main()