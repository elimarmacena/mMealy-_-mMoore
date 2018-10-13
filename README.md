# Autômatos Finitos com Saída - Máquinas de Mealy e de Moore<br>
&nbsp; Repositório destinado para o trabalho ministrado na disciplina de Linguagens Formais e Autômatos

# SUMÁRIO<br>

### 1. Autores<br>
Antônio Carlos D.:  [duraes-antonio](https://github.com/duraes-antonio)<br>
Elimar Macena:      [elimarmacena](https://github.com/elimarmacena)<br>

### 2. Descrição do Código<br>
 &nbsp; O código construído para este trabalho foi construído utilizando a linguagem <i>Python</i>, no qual para os integrantes foi a que mostrou maior facilidade de resolução do problema proposto. O código foi desenvolvido seguindo o paradigma procedural, pois não foi visto uma necessidade de utilizar orientação objeto para a resolução do problema. <br>
 
 &nbsp; Na questão de organização logica e metodologia utilizada para resolver o problema foi trabalhado da seguinte maneira, ao receber a S expression a mesma é convertida numa lista, o que torna mais fácil o procedimento de validação dos dados informados, e então é montado a máquina, no qual é elaborada em cima da estrutura de dicionário do <i>Python</i>.<br>
 
&nbsp; Ao se tratar de equivalência de máquina não houve grande dificuldade de se converter de <i>Moore</i> para <i>Mealy</i>, primeiro o código avalia se a mesma pode ser convertida para <i>Mealy</i>, caso seja então é feito os procedimentos necessários, que neste caso é checado a transição que está sendo feita e colocado o caractere de saída do estado da máquina de Moore na transição.<br> 

&nbsp; A maior dificuldade encontrada foi na questão de resolução da equivalência de <i>Mealy</i> para <i>Moore</i>, mas a o problema proposto foi resolvido da seguinte maneira, o código avalia as transições feitas para cada estado, checa se existe a necessidade de criar um novo estado, faz a ligação do estado com o caractere de saída e também guarda o estado da máquina de <i>Mealy</i> que o mesmo se originou. Após isto é criada as novas transações, copiando as transações e substituindo os estados da máquina de <i>Mealy</i> para os estados derivados utilizados na máquina de <i>Moore</i> e após esse procedimento é removido os caracteres de saída da transação e deixando apenas nos estados.<br>

### 3. Procedimento para compilação do trabalho<br>
&nbsp; Por se tratar de um script python não é necessário a utilização de nenhum procedimento específico, apenas a chamada do script em linha de comando. Exemplo:<br> 
  ```sh
  python3 exemplo_script.py
  ```  
  
### 4. Nome e Modo de Uso do Programa<br>
&nbsp; O nome escolhido para o programa desenvolvido é <i>Machine_Transformation</i>, por que afinal se trata de uma conversão de máquina. Para que seja feito uso do programa é necessário fazer uma chamada via linha de comando, no qual o usuário informa o input e também informar o seu output, para o cenário deste trabalho ambos devem ser um arquivo.<br>
  Exemplo:
```sh
  python3 machine_transformation.py -i arquivoOrigem.txt -o arquivoDestino.txt
```

### 5. Exemplos de maquina<br>
#### 5.1 Moore <br> 
##### 5.1.1 Exemplo 1<br>
```
(moore 
(symbols-in A B C) 
(symbols-out X Y) 
(states q0 q1 q2 q4) 
(start q0) 
(finals q4) 
(trans (q0 q1 A) (q0 q2 B) (q2 q4 C) (q1 q4 C)) 
(out-fn (q0 X) (q1 X) (q2 X) (q4 Y)))
```
[desenho do autômato](https://github.com/elimarmacena/mMealy-_-mMoore/blob/master/automatos/MOORE_IMAGEM/AUTOMATO_01_MOORE__INTRASITIVE.svg)
<br>Não possui conversão pois o seu estado inicial gera saida.

#### 5.1.2 Exemplo 2<br>
```
(moore 
(symbols-in A B C) 
(symbols-out 0 1 2) 
(states q0 q1 q2 q3) 
(start q0) 
(finals q3) 
(trans (q0 q1 A) (q0 q2 B) (q2 q1 B)(q2 q3 C) (q1 q2 A) (q1 q3 C)) 
(out-fn (q0 ()) (q1 0) (q2 1) (q4 2)))
```
[desenho do autômato](https://github.com/elimarmacena/mMealy-_-mMoore/blob/master/automatos/MOORE_IMAGEM/AUTOMATO_02_MOORE.svg)<br>
[desenho da conversão](https://github.com/elimarmacena/mMealy-_-mMoore/blob/master/automatos/MOORE_IMAGEM/AUTOMATO_02_MOORE_CONVERTED.svg)
#### 5.1.3 Exemplo 3<br>
```
(moore 
(symbols-in A B) 
(symbols-out J A P O) 
(states q0 q1 q2 q3 q4) 
(start q0) 
(finals q4) 
(trans (q0 q1 A) (q1 q2 B) (q2 q3 A) (q3 q2 B) (q2 q4 B)) 
(out-fn (q0 ()) (q1 J) (q2 A) (q3 P) (q4 O)))
```
[desenho do autômato](https://github.com/elimarmacena/mMealy-_-mMoore/blob/master/automatos/MOORE_IMAGEM/AUTOMATO_03_MOORE.svg)<br>
[desenho da conversão](https://github.com/elimarmacena/mMealy-_-mMoore/blob/master/automatos/MOORE_IMAGEM/AUTOMATO_03_MOORE_CONVERTED.svg)
#### 5.2 Mealy <br> 
#### 5.2.1 Exemplo 1<br>
```
(mealy 
(symbols-in A B) 
(symbols-out 0 1) 
(states q0 q1 q2 q3 q4) 
(start q0) 
(finals q4) 
(trans (q0 q1 A 0) (q0 q2 B 1) (q2 q3 B 0) (q1 q3 B 1) (q3 q4 B 0)))
```
[desenho do autômato](https://github.com/elimarmacena/mMealy-_-mMoore/blob/master/automatos/MEALY_IMAGEM/AUTOMATO_01_MEALY.svg)<br>
[desenho da conversão](https://github.com/elimarmacena/mMealy-_-mMoore/blob/master/automatos/MEALY_IMAGEM/AUTOMATO_01_MEALY_CONVERTED.svg)

#### 5.2.2 Exemplo 2<br>
```
(mealy 
(symbols-in A B) 
(symbols-out J L S F X U B K Y Q) 
(states q0 q1 q2 q3 q4 q5 q6 q7) 
(start q0) 
(finals q7) 
(trans (q0 q1 A J) (q0 q2 B X) (q1 q3 A L) (q1 q2 B X) (q2 q4 B X) (q3 q5 A S) (q4 q3 A Y) (q4 q6 B U) (q5 q7 A F) (q6 q5 A Q) (q6 q7 B K)))
```
[desenho do autômato](https://github.com/elimarmacena/mMealy-_-mMoore/blob/master/automatos/MEALY_IMAGEM/AUTOMATO_02_MEALY.svg)<br>
[desenho da conversão](https://github.com/elimarmacena/mMealy-_-mMoore/blob/master/automatos/MEALY_IMAGEM/AUTOMATO_02_MEALY_CONVERTED.svg)

#### 5.2.3 Exemplo 3<br>
```
(mealy 
(symbols-in A B C E) 
(symbols-out L F A) 
(states q0 q1 q2 q3 q4 q5 q6 q7 q8 q9) 
(start q0) 
(finals q9) 
(trans (q0 q1 A A) (q0 q5 B L) (q1 q2 A L) (q2 q3 A F) (q2 q4 C F) (q3 q4 A A) (q4 q9 A A) (q5 q0 E F) (q5 q6 B F) (q5 q8 C F) (q5 q9 A F) (q6 q7 C A) (q7 q5 B L) (q7 q8 C L) (q8 q9 C F)))
```
[desenho do autômato](https://github.com/elimarmacena/mMealy-_-mMoore/blob/master/automatos/MEALY_IMAGEM/AUTOMATO_03_MEALY.svg)<br>
[desenho da conversão](https://github.com/elimarmacena/mMealy-_-mMoore/blob/master/automatos/MEALY_IMAGEM/AUTOMATO_03_MEALY_CONVERTED.svg)



### 6. Informacoes Complementares ao Trabalho<br>
&nbsp; Para o desenvolvimento deste trabalho era necessário manusear <i>s_expression</i>, como ambos do grupo não possuíam conhecimento com este formato foi optado por utilizar o código disponibilizado no seguinte link [ROSETTACODE](https://rosettacode.org/wiki/S-Expressions#Python), referência no qual é expressa no arquivo utilizado para a leitura e conversão de <i>s_expression</i>.<br>

&nbsp; Para desenhar os automatos disponiveis no repositorio foi utilizado a ferramenta [Draw.io](https://www.draw.io/)
  
  
   有難う
