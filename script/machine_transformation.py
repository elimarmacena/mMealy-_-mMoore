def list_to_machine(lst_machine):
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

def show_machine(machine):
    print("{0} MACHINE".format(machine["type"].upper()))
    print("INPUT SYMBOLS:")
    for x in machine["symbols_in"]:
        print(x)
    print ("OUTPUT SYMBOLS:")
    for x in machine["symbols_out"]:
        print(x)
    print("STATES:")
    for x in machine["states"]:
        print(x)
    print("\nINITIAL SYMBOL: {0}".format(machine["start"]))
    print("\nFINAL STATE: {0}".format(machine["final"]))
    print("\nTRASATIONS")
    for x in machine["trans"]:
        print(x)
    if machine["type"].lower()=="moore":
        print("STATES AND OUTPUTS:")
        for x in machine["out_fn"]:
            print(x)
    print()

def moore_intransitive(moore):
    starts  = moore["start"]
    for y in moore["out_fn"]:
        if y[0] in starts and y[1] != []:
            return True
    return False

def take_trans_state(state,machine):
    trans_state = []
    for x in machine["trans"]:
        if state == x[0]:
            trans_state.append(x)
    return trans_state

def take_out_state(state,moore):
    for x in moore["out_fn"]:
        if state == x[0]:
            return x[1]

def out_to_trans(mealy,moore):
    trans_with_out =[]
    for state_x in moore["states"]:
        state = state_x
        state_out = take_out_state(state,moore)
        trans_state = take_trans_state(state,moore)
        for y in trans_state:
            _temp = y[:]
            _temp.append(state_out)
            trans_with_out.append( _temp )
        #END FOR Y
    #END FOR X
    return trans_with_out


def moore_to_mealy(moore_machine):
    #VERIFICACAO DA POSSIBILIDADE DE TRANSFORMACAO
    if (moore_intransitive(moore_machine)):
        raise ValueError ("Nao é possivel converver esta marquina para mealy pois possui saidas no seu estado inicial")
    else:
        mealy_machine = {}
        mealy_machine["type"] = "mayle"
        mealy_machine["symbols_in"] = moore_machine["symbols_in"][:]
        mealy_machine["symbols_out"] = moore_machine["symbols_out"][:]
        mealy_machine["states"] = moore_machine["states"][:]
        mealy_machine["start"] = moore_machine["start"][:]
        mealy_machine["final"] = moore_machine["final"][:]
        mealy_machine["trans"] = out_to_trans(mealy_machine,moore_machine)
        return mealy_machine


def main():
    teste =  ['moore', ['symbols-in', 'a', 'b'], ['symbols-out', 0, 1], ['states', 'q0', "q0'", 'q1', 'q2', 'q3', "q3'"], ['start', 'q0'], ['finals', 'q3',"q3'"], ['trans', ['q0', 'q1', 'a'], ['q0', 'q3', 'b'], ['q1', "q3'", 'a'], ['q1', 'q2', 'b'], ['q2', "q0'", 'a'], ['q2', "q3'", 'b'], ['q3', "q3'", 'a'], ['q3', "q0'", 'b'], ["q3'", "q3'", 'a'], ["q3'", "q0",'b']], ['out-fn', ['q0', []], ["q0'", 1], ['q1', 0], ['q2', 1], ['q3', 0], ["q3'", 1]]]
    maquina = list_to_machine(teste)
    show_machine(maquina)
    show_machine (moore_to_mealy(maquina))
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

