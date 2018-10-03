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

#OUTPUTS FROM THE RECEIVER STATE
def out_trans_receive(state: str, mealy: dict)->list:
    trans_to_state = []
    for x in mealy["trans"]:
        if(x[1] == state):
            trans_to_state.append(x)
    return trans_to_state

#COPY THE TRANSACTION OF A STATE X TO A STATE Y
def copy_trans_to_new_state(new_state: str, old_state: str, machine: dict)->list:
    trans = []
    for x in machine["trans"]:
        if x[0] == old_state:
            trans.append([new_state, x[1], x[2]])
        # END IF
    # END FOR
    return trans

#COPY THE TRANSACTION OF THE INITIAL STATE
def copy_trans_initial_state(machine: dict)->list:
    trans = []
    initial_state = machine["start"][0]
    for x in machine["trans"]:
        if x[0] == initial_state:
            trans.append(x[:3])
        # END IF
    # END FOR
    return trans

#TREAT THE TRANSACTION OF A MEALY MACHINE REMOVING THE MULTIPLE OUTPUT IN A UNIQUE STATE
def treat_trans(state: str, machine_mealy: dict, machine_moore:dict)->dict:
    out_symbols = []
    count_diferent_symbols = 0
    treated_state = {}
    treated_state["final"] = []
    treated_state["trans"] = []
    treated_state["states"] = []
    treated_state["out_fn"] = []
    checked = False
    for transaction in machine_mealy["trans"]:
        if transaction[1] == state and machine_mealy["start"][0] not in transaction[0]: #BECAUSE THE TRANSACTIONS OF THE INITIAL STATE IS ALREADY TREATED
            if transaction[3] not in out_symbols:
                #PUT THE REGISTRE OF THE FIRST TYPE OF OUTPUT FROM THE STATE
                if count_diferent_symbols < 1:
                    count_diferent_symbols += 1
                    out_symbols.append(transaction[3])
                    treated_state["trans"].append(transaction[:3])
                    treated_state["out_fn"].append([transaction[1], transaction[3]])
                # END IF
                #WORKING WITH THE OTHERS OUTPUTS FROM THE SAME STATE
                else:
                    count_diferent_symbols += 1
                    out_symbols.append(transaction[3])
                    new_trans = []
                    new_trans.append(transaction[0])
                    #RENAME THE STATE WITH A RANDOM SYMBOL
                    new_trans.append(transaction[1]+random.choice(string.punctuation))
                    new_trans.append(transaction[2])
                    #ADDING THE NEW STATE INTO THE DICTIONARY
                    treated_state["states"].append(new_trans[1])
                    #ADDING THE NEW TRANSATION INTO THE DICTIONARY
                    treated_state["trans"].append(new_trans)
                    #ADDING THE OUTPUT OF THE STATE INTO THE DICTIONARY
                    treated_state["out_fn"].append([new_trans[1], transaction[3]])
                    #COPYING THE TRANSACTION OF THE ORIGINAL STATE INTO THE NEW ONE
                    new_state_trans = copy_trans_to_new_state(
                        new_trans[1], state, machine_mealy)  # CREATE THE TRANS FOR THE NEW STATE
                    treated_state["trans"].extend(new_state_trans)
                    #CHECKING IF THE STATE IS A FINAL STATE, SO THEN THE NEW STATE WILL BE A FINAL STATE TOO
                    if state in machine_mealy["final"]:
                        treated_state["final"].append(new_trans[1])

                # END ELSE
            # END IF
            #IF THE OUTPUT IS ALREADY REGISTERED WE JUST NEED TO CHANGE THE TRANSACTION OF THE STATE HOW USED THE OLD STATE
            else:
                for out_fn in treated_state["out_fn"]:
                    if out_fn[1] == transaction[3]:
                        new_trans = []
                        new_trans.append(transaction[0])
                        new_trans.append(out_fn[0])
                        new_trans.append(transaction[2])
                        treated_state["trans"].append(new_trans)
                    # END IF
                # END FOR
            # END ELSE
        # END IF
        elif (transaction[1] == state) and ( transaction[1] not in machine_moore["out_fn"]): #ADDING JUST THE STATE AND YOUR OUTPUT BECAUSE THE TRANSACTION IS ALREADY RESGISTRED
            treated_state["out_fn"].append([transaction[1], transaction[3]])
            count_diferent_symbols += 1
            out_symbols.append(transaction[3])


            
    # END FOR
    return treated_state

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


#TRANSFORME A MEALY MACHINE INTO A MOORE MACHINE
def mealy_to_moore(mealy_machine: dict)->dict:
    moore_machine = {}
    moore_machine["type"] = "moore"
    moore_machine["symbols_in"] = mealy_machine["symbols_in"][:]
    moore_machine["symbols_out"] = mealy_machine["symbols_out"][:]
    moore_machine["states"] = mealy_machine["states"][:]
    moore_machine["start"] = mealy_machine["start"][:]
    moore_machine["final"] = mealy_machine["final"][:]
    trans_initial_state = copy_trans_initial_state(mealy_machine)
    moore_machine["trans"] = []
    moore_machine["trans"].extend(trans_initial_state)
    moore_machine["out_fn"] = []

    # CHECK IF THE START STATE RECEIVE A TRANSATION WITH OUTPUT
    trans_to_initial = out_trans_receive(
        mealy_machine["start"][0], mealy_machine)
    if(trans_to_initial != []):
        out_symbols = []
        for x in trans_to_initial:
            new_trans = []
            if(x[3] in out_symbols):  # CHECKING IF EXIST A STATE FOR THE OUTPUT SYMBOL
                for y in moore_machine["out_fn"]:
                    new_trans.append(x[0])
                    new_trans.append(y[0])
                    new_trans.append(x[2])
                    moore_machine["trans"].append(new_trans)
            # END IF
            else:
                new_trans.append(x[0])
                #CREATING A NEW STATE USING A RANDOM SYMBOL 
                new_trans.append(x[1]+random.choice(string.punctuation))
                new_trans.append(x[2])
                #ADDING THE SYMBOL INTO A LIST WHERE WE CAN CHECK THE OUTPUTS ALREADY REGISTERED
                out_symbols.append(x[3])
                #INFORMING THE OUTPUT OF THE SYMBOL
                out_fn = [new_trans[1], x[3]]
                moore_machine["states"].append(new_trans[1])
                # RETIRECT THE STATES TO THE NEW STATE CREATE
                moore_machine["trans"].append(new_trans)
                new_state_trans = copy_trans_to_new_state(
                    new_trans[1], mealy_machine["start"][0], mealy_machine)  # CREATE THE TRANS FOR THE NEW STATE
                moore_machine["trans"].extend(new_state_trans)
                moore_machine["out_fn"].append(out_fn)
            # END ELSE
        # END FOR
        moore_machine["out_fn"].append([mealy_machine["start"][0], []])
    # END IF
    for x in mealy_machine["states"]:
        if x != mealy_machine["start"][0]:
            #CHECK IF THE STATE HAVE 2 TYPES OF OUTPUT IN A UNIQUE STATE
            trans_treated = treat_trans(x, mealy_machine,moore_machine)
            #AFTER TREAT A STATE WE PUT THE PARAMETERS INTO THE NEW MACHINE
            for y in trans_treated.keys():
                moore_machine[y].extend(trans_treated[y])
            # END FOR
        # END IF
    # END FOR
    return moore_machine


def main():
    teste = ['mealy', ['symbols-in', 'a', 'b'], ['symbols-out', 0, 1], ['states', 'q0', 'q1', 'q2', 'q3'], ['start', 'q0'], ['finals', 'q3'], ['trans', ['q0', 'q1',
                                                                                                                                                         'a', 0], ['q0', 'q3', 'b', 0], ['q1', 'q2', 'b', 1], ['q1', 'q3', 'a', 1], ['q2', 'q3', 'a', 0], ['q2', 'q3', 'b', 1], ['q3', 'q0', 'b', 1], ['q3', 'q3', 'a', 1]]]
    #['moore', ['symbols-in', 'a', 'b'], ['symbols-out', 0, 1], ['states', 'q0', "q0'", 'q1', 'q2', 'q3', "q3'"], ['start', 'q0'], ['finals', 'q3',"q3'"], ['trans', ['q0', 'q1', 'a'], ['q0', 'q3', 'b'],["q0'","q1","a"],["q0'","q3","b"], ['q1', "q3'", 'a'], ['q1', 'q2', 'b'], ['q2', "q3", 'a'], ['q2', "q3'", 'b'], ['q3', "q3'", 'a'], ['q3', "q0'", 'b'], ["q3'", "q3'", 'a'], ["q3'", "q0'",'b']], ['out-fn', ['q0', []], ["q0'", 1], ['q1', 0], ['q2', 1], ['q3', 0], ["q3'", 1]]]
    maquina = list_to_machine(teste)
    show_machine(maquina)
    moore=mealy_to_moore(maquina)
    show_machine(moore)
    mealy = moore_to_mealy(moore)
    show_machine(mealy)
    #show_machine (moore_to_mealy(maquina))
    # print (maquina["type"])
    # try:
    #     for x in maquina["trans"]:
    #         print(x)
    #     for y in maquina["out_fn"]:
    #         print(y)
    # except Exception as err:
    #     print("")
    return 0


if __name__ == '__main__':
    main()
