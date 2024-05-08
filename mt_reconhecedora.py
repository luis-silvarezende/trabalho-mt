# GRUPO: 
#        Luis Felipe Silva Rezende-20212079, Aaron Martins Leão Ferreira-202120496,
#        Gabriel Marcos Lope-201910144, Luana Peixoto Borges-202210573

import sys

# Recebe os argumentos da linha de comando

args = sys.argv
desc_mt1 = args[1]
input_string = args[2]
saida_output = args[3]

print(desc_mt1)

class TuringMachine:

    def __init__(self, states, alphabet, transitions, initial_state, final_states): # Construtor
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.current_state = initial_state
        self.final_states = final_states
        self.head_position = 0
        self.tape = ['B'] #Baabb

    def step(self): # Método para fazer a gravação na fita e posicionar a cabeça conforme a as instruções

        # Recebe um simbolo do alfabeto da fita
        current_symbol = self.tape[self.head_position]

        # Se existir o estado atual e um simbolo atual do alfabeto da fita em transitions
        if (self.current_state, current_symbol) in self.transitions:
            next_state, write_symbol, move_direction = self.transitions[(self.current_state, current_symbol)]

            # o array tape recebe o simbolo que vai ser escrito naquela posição
            self.tape[self.head_position] = write_symbol
            
            if move_direction == 'D':
                self.head_position += 1

            elif move_direction == 'E':
                self.head_position = self.head_position - 1 

            self.current_state = next_state

            return True # Retorna verdadeiro se existir a transição
        else:
            return False

    def run(self, input_string): # recebe input da linha de comando
        self.tape += list(input_string) # Cria um array com a palavra e coloca na fita
        self.tape.append('B') # Coloca Branco no final da fita
        while self.current_state not in self.final_states: # Enquanto estado atual nao for estado final fica no loop
            if not self.step(): # Verifica se o metodo retorna verdadeiro ou falso 
                break
            self.output() # chama o método para a escrita no arquivo saida.txt
        return self.current_state in self.final_states # retorna True se o estado atual estiver na lista de estados finais, se não estiver na lista quer dizer que parou em estado não final, rejeita.
    
    # ESCRITA NO ARQUIVO
    def output(self):
        with open(saida_output, 'a') as output_file:
            tape_str = ''.join(self.tape)
            output_file.write(f"{tape_str[:self.head_position]}{{{self.current_state}}}{tape_str[self.head_position:]}\n")

# LEIURA DO ARQUIVO

with open(desc_mt1, 'r') as arquivo:
    lines = arquivo.readlines()

states = lines[1].strip().rstrip(',')
alphabet = lines[2].strip().rstrip(',')

start_index = 4
end_index = 0

# Estrutua para encontrar o tamanho da descricao das transicoes da mt
for i in range(start_index, len(lines)):
    line = lines[i].strip()  # Remove espaços em branco no início e no final da linha

    if line == '},':
        end_index = i
        break
transitions = ''

# Armazena todas as linhas referente a transição da mt removendo os espaços em branco 
for line in range(start_index,end_index):
    transitions += lines[line].strip()

transitions = transitions + '}'

# Caracteres para fazer a troca na string e deixa-la no formato de dicionario
replacements = {
    "->": ":",
    "(": "('",
    ")": "')",
    ",": "', '",
    ")'":")",
    " '(":"("
}

# Faz a troca dos caracteres
for old, new in replacements.items():
    transitions = transitions.replace(old, new)

dicionario = eval(transitions) # Converte toda a string para dicionario

# Armazena as linhas que possuem estado inicial e final 

initial_state = lines[end_index+1].strip().strip(',') 
final_states = lines[end_index+2].strip()

# FIM DA LEITURA DO ARQUIVO

tm = TuringMachine(states, alphabet, dicionario, initial_state, final_states)

result = tm.run(input_string)

# Escreve no final do arquivo se aceita ou não a palavra 

with open(saida_output, 'a') as output_file:
    if result:
        output_file.write("aceita\n")
    else:
        output_file.write("nao aceita\n")