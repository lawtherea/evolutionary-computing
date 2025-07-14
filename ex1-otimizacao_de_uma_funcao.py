import random

# gera um cromossomo (indivíduo) com 8 bits aleatórios
def gerar_individuo():
    return ''.join(random.choice('01') for _ in range(8))  # Ex: '01010101'

# calcula a aptidão (fitness) do cromossomo e conta quantas vezes a substring "01" aparece
def calcular_fitness(cromossomo):
    return sum(1 for i in range(len(cromossomo)-1) if cromossomo[i:i+2] == "01")

# seleção por torneio: pega 2 indivíduos e retorna o melhor
def torneio(populacao):
    a, b = random.sample(populacao, 2)  # seleciona dois indivíduos diferentes
    return a if calcular_fitness(a) > calcular_fitness(b) else b

# cruzamento de ponto único entre dois pais
def cruzamento(pai1, pai2):
    ponto = random.randint(1, 7)  # Escolhe ponto de corte (evita ponto 0 ou 8)
    # gera dois filhos combinando partes dos pais
    return pai1[:ponto] + pai2[ponto:], pai2[:ponto] + pai1[ponto:]

# mutação com taxa de 1%
def mutacao(cromossomo, taxa=0.01):
    # para cada bit, muda com 1% de chance
    return ''.join(
        bit if random.random() > taxa else '1' if bit == '0' else '0'
        for bit in cromossomo
    )

# === INÍCIO DO ALGORITMO GENÉTICO ===

# Cria uma população inicial com 10 cromossomos aleatórios
populacao = [gerar_individuo() for _ in range(10)]
geracao = 0  # Contador de gerações

while True:
    # Ordena a população do melhor para o pior baseado no fitness
    populacao = sorted(populacao, key=calcular_fitness, reverse=True)
    melhor = populacao[0]  # Seleciona o melhor indivíduo da geração
    fitness = calcular_fitness(melhor)  # Calcula o fitness do melhor

    # Mostra o melhor da geração atual
    print(f"Geração {geracao} - Melhor: {melhor} (fitness={fitness})")

    # se o fitness for 4 (máximo possível), para
    if fitness >= 4:
        print(f"Solução encontrada: {melhor} -> {int(melhor, 2)}")
        break  # Interrompe o loop

    # Cria nova geração por cruzamento e mutação
    nova_geracao = []
    while len(nova_geracao) < 10:
        # Seleciona dois pais via torneio
        pai1 = torneio(populacao)
        pai2 = torneio(populacao)

        # Realiza cruzamento entre os pais para gerar filhos
        filho1, filho2 = cruzamento(pai1, pai2)

        # Aplica mutação nos filhos
        filho1 = mutacao(filho1)
        filho2 = mutacao(filho2)

        # Adiciona os filhos à nova geração
        nova_geracao.extend([filho1, filho2])

    # Atualiza a população com os primeiros 10 indivíduos da nova geração
    populacao = nova_geracao[:10]
    geracao += 1  # Avança para a próxima geração
