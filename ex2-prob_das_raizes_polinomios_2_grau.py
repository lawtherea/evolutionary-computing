import random

# Converte uma string binária para decimal
def bin_para_decimal(bin_str):
    return int(bin_str, 2)

# Converte um número decimal para binário com padding de 8 bits
def decimal_para_bin(x, bits=8):
    return format(x, f'0{bits}b')

# Calcula o quão perto x1 e x2 estão de serem raízes da equação x² - 5x + 6 = 0
def calcular_fitness(cromossomo):
    x1 = bin_para_decimal(cromossomo[:8])
    x2 = bin_para_decimal(cromossomo[8:])
    
    # Calcula o valor da equação para cada raiz
    f1 = x1**2 - 5*x1 + 6
    f2 = x2**2 - 5*x2 + 6

    # Penaliza se as raízes forem iguais (não queremos isso)
    if x1 == x2:
        return 1000000

    # Quanto menor o resultado, melhor o fitness
    return abs(f1) + abs(f2)

# Faz mutação invertendo alguns bits aleatoriamente
def mutacao(cromossomo, taxa=0.01):
    novo = ''
    for bit in cromossomo:
        if random.random() < taxa:
            novo += '0' if bit == '1' else '1'
        else:
            novo += bit
    return novo

# Cruzamento de ponto único entre dois cromossomos
def cruzamento(pai1, pai2):
    ponto = random.randint(1, 15)  # ponto de corte
    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]
    return filho1, filho2

# Gera um cromossomo binário com duas raízes diferentes (8 bits cada)
def gerar_individuo():
    x1 = decimal_para_bin(random.randint(0, 255))
    x2 = decimal_para_bin(random.randint(0, 255))
    while x1 == x2:
        x2 = decimal_para_bin(random.randint(0, 255))
    return x1 + x2  # 16 bits no total

# Avalia e ordena os cromossomos da população
def avaliar_populacao(pop):
    return sorted(pop, key=calcular_fitness)

# ========================
# Algoritmo Genético
# ========================

# Passo 1 - Inicia a geração
t = 0

# Passo 2 - Cria população inicial com 10 cromossomos
populacao = [gerar_individuo() for _ in range(10)]

# Passo 3 - Avalia a população
while True:
    populacao = avaliar_populacao(populacao)
    melhor = populacao[0]
    fitness = calcular_fitness(melhor)

    print(f"Geração {t} - Melhor: {melhor} | Fitness = {fitness:.6f}")

    # Passo 4 - Verifica critério de parada
    if fitness < 0.00001:
        x1 = bin_para_decimal(melhor[:8])
        x2 = bin_para_decimal(melhor[8:])
        print(f"\nRaízes encontradas: x1 = {x1}, x2 = {x2}")
        break

    # Passo 5 - Incrementa geração
    t += 1

    # Passos 6, 7, 8 - Seleção de pares, cruzamento e mutação
    nova_geracao = []
    for _ in range(len(populacao) // 2):
        pais = random.sample(populacao, 2)
        filho1, filho2 = cruzamento(pais[0], pais[1])
        filho1 = mutacao(filho1)
        filho2 = mutacao(filho2)
        nova_geracao.extend([filho1, filho2])

    # Passo 9 - Junta pais e filhos
    populacao_completa = populacao + nova_geracao

    # Passo 10 - Mantém os 10 melhores
    populacao = avaliar_populacao(populacao_completa)[:10]

# Passo 12 - Mostra população final
print("\nPopulação Final:")
for cromossomo in populacao:
    x1 = bin_para_decimal(cromossomo[:8])
    x2 = bin_para_decimal(cromossomo[8:])
    print(f"{cromossomo} -> x1 = {x1}, x2 = {x2}, fitness = {calcular_fitness(cromossomo):.6f}")
