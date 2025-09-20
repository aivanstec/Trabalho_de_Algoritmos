import os

#------- Classe Cidade -------
class Cidade:
    def __init__(self, codigo, descricao, estado):
        self.codCidade = codigo
        self.descricao = descricao
        self.estado = estado
    def __str__(self):
        return f"Código: {self.codCidade}, Descrição: {self.descricao}, Estado: {self.estado}"

#------- Classe Aluno -------#
class Aluno:
    def __init__(self, codigo, nome, dataNascimento, peso, altura, cidade):
        self.codAluno = codigo
        self.nome = nome
        self.data = dataNascimento
        self.peso = peso
        self.altura = altura
        self.cidade = cidade

    def __str__(self):
        return (f"Código do Aluno: {self.codAluno}"
                f"\nNome: {self.nome}, Data de Nascimento: {self.data} "
                f"\nPeso: {self.peso} kg, Altura: {self.altura} "
                f"\nCidade: {self.cidade.descricao} {self.cidade.estado}")

    def calcular_imc(self):
        if self.altura > 0:
            return self.peso / (self.altura ** 2)
        return 0

    def diagnostico_imc(self):
        imc = self.calcular_imc()
        if imc == 0:
            return "Não foi possível calcular (altura inválida)."
        elif imc < 18.5:
            return "Abaixo do peso"
        elif imc < 25:
            return "Peso normal"
        elif imc < 30:
            return "Sobrepeso"
        else:
            return "Obesidade"

#------- Classe Professor -------
class Professor:
    def __init__(self, codigo, nome, endereco, telefone, cidade):
        self.codProfessor = codigo
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.cidade = cidade

    def __str__(self):
        return (f"Código do Professor: {self.codProfessor}, "
                f"\nNome: {self.nome},  Telefone: {self.telefone}"
                f"\nEndereço: {self.endereco} Cidade: {self.cidade.descricao} {self.cidade.estado}")

#------- Classe Modalidade -------
class Modalidade:
    def __init__(self, codigo, descricao, professor, valorAula, limiteAlunos, totaAlunos):
        self.cod_modalidade = codigo
        self.desc_Modalidade = descricao
        self.cod_professor = professor
        self.valorAula = valorAula
        self.limiteAlunos = limiteAlunos
        self.totaAlunos = totaAlunos

    def __str__(self):
        return (f"Código da Modalidade: {self.cod_modalidade}, Descrição da Modalidade: {self.desc_Modalidade}"
                f"\nCódigo do Professor: {self.cod_professor.nome}, Valor da Aula: {self.valorAula}, Limite de Alunos: {self.limiteAlunos}, Total de Alunos: {self.totaAlunos} ")

#------- Classe Matrícila -------
class Matricula:
    def __init__(self, codigo, aluno, modalidade, qtdeAulas):
        self.cod_Matricula = codigo
        self.cod_aluno = aluno
        self.cod_modalidade = modalidade
        self.qtdeAulas = qtdeAulas

    def __str__(self):
        return (f"Código da Matrícula: {self.cod_Matricula}, Código do Aluno: {self.cod_aluno.nome}, Código da Modalidade: {self.cod_modalidade.desc_Modalidade}, Quantidade de Aulas: {self.qtdeAulas}")

#------- Classe Indece -------
class Indece:
    def __init__(self, codigo, dado_obj):
        self.codigo = codigo
        self.dado = dado_obj
        self.esquerda = None
        self.direita = None

#------- Árvore Binaria -------
class ArvoreBinaria:
    def __init__(self):
        self.raiz = None

    def inserir(self, codigo, dado_obj):
        if self.raiz is None:
            self.raiz = Indece(codigo, dado_obj)
        else:
            self.inserir_indece(self.raiz, codigo, dado_obj)

    def inserir_indece(self, indece_atual, codigo, dado_obj):
        if codigo < indece_atual.codigo:
            if indece_atual.esquerda is None:
                indece_atual.esquerda = Indece(codigo, dado_obj)
            else:
                self.inserir_indece(indece_atual.esquerda, codigo, dado_obj)
        else:
            if indece_atual.direita is None:
                indece_atual.direita = Indece(codigo, dado_obj)
            else:
                self.inserir_indece(indece_atual.direita, codigo, dado_obj)

    def buscar(self, codigo):
        return self.buscar_indece(self.raiz, codigo)

    def buscar_indece(self, indece_atual, codigo):
        if indece_atual is None or indece_atual.codigo == codigo:
            return indece_atual.end if indece_atual else None
        if codigo < indece_atual.codigo:
            return self.buscar_indece(indece_atual.esquerda, codigo)
        else:
            return self.buscar_indece(indece_atual.direita, codigo)

    def salvar(self, arquivo, formatador_arquivo):
        try:
            with open(arquivo, "w", encoding= 'utf-8') as arq:
                self.salvar_arquivo(self.raiz, arq, formatador_arquivo)
            print(f"\nArquivo '{arquivo}' salvo com sucesso!")
        except Exception as e:
            print(f"\nErro falha ao salvar o arquivo '{e}'")

    def salvar_arquivo(self, indece_atual, arquivo, formatador_arquivo):
        if indece_atual is not None:
            self.salvar_arquivo(indece_atual.esquerda, arquivo, formatador_arquivo)
            objeto = indece_atual.dado
            linha = formatador_arquivo(objeto)
            arquivo.write(linha)

            self.salvar_arquivo(indece_atual.direita, arquivo, formatador_arquivo)

def carregar_dados(arquivo, arvore, construtor_arq, **carregar):
    try:
        with open(arquivo, "r", encoding = 'utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    dados = [d.strip() for d in linha.split(',')]
                    arq = construtor_arq(dados, **carregar)
                    if arq:
                        codigo_arq = getattr(arq, list(arq.__dict__.keys())[0])
                        arvore.inserir(codigo_arq, arq)
        print(f"Dados do '{arquivo}' carregados com sucesso!")
    except FileNotFoundError:
        print(f"Arquivo '{arquivo}' não encontrado!")
    except Exception as e:
        print(f"Erro ao carregar '{arquivo}': {e}")

def construtor_cidade(data, **carregar):
    return Cidade(int(data[0]), data[1], data[2])

def incluir_cidade(arvore_cidade):
    try:
        cod_cidade = int(input("Digite o codigo da cidade: "))
        if arvore_cidade.buscar(cod_cidade) is not None:
            print("\nErro: Já existe cidade com esse código.")
            return
        descricao = input("Digite o Nome: ")
        estado = input("Digite o Estado (UF): ")

        nova_cidade = Cidade(cod_cidade, descricao, estado)
        arvore_cidade.inserir(cod_cidade, nova_cidade)

        formato = lambda cid: f"{cid.codCidade}, {cid.descricao}, {cid.estado}"
        arvore_cidade.salvar("Dados/cidades.txt", formato)

        print("\nCidade incluída com sucesso!")

    except ValueError:
        print("\nCódigo inválido. Digite um numero inteiro.")

def incluir_aluno(arvore_aluno, lista_aluno, arvore_cidade, lista_cidade):
    try:
        cod_aluno = int(input("Digite o codigo do Aluno: "))
        nome = input("Digite o Nome: ")
        data = input("Digite a data de nascimento: ")
        peso = float(input("Digite o peso: "))
        altura = float (input("Digite a altura: "))
        cod_cidade = int(input("Digite o Código da Cidade: "))

        endereco_cidade = arvore_cidade.buscar(cod_cidade)
        if endereco_cidade is None:
            print("\nCidade não encontrada. Digite novamente.")
            return

        cidade = lista_cidade[endereco_cidade]
        novo_aluno = Aluno(cod_aluno, nome, data, peso, altura, cidade)

        lista_aluno.append(novo_aluno)
        novo_endereco = len(lista_aluno) - 1
        arvore_aluno.inserir(cod_aluno, novo_endereco)
        print("\nAluno incluído com sucesso!")
        print("-" * 30)
    except ValueError:
        print("\nCódigo inválido. Digite um numero inteiro.")

def consultar_aluno(arvore_alunos, lista_alunos):
    if not lista_alunos:
        print("\nNenhum aluno cadastrado.")
        return

    try:
        codigo = int(input("Digite o código do aluno que deseja consultar: "))
        endereco_aluno = arvore_alunos.buscar(codigo)

        if endereco_aluno is None:
            print("\nAluno não encontrado com este código.")
            return

        aluno_encontrado = lista_alunos[endereco_aluno]
        print("\n--- Ficha do Aluno ---")
        print(aluno_encontrado)
        imc = aluno_encontrado.calcular_imc()
        diagnostico = aluno_encontrado.diagnostico_imc()

        print(f"IMC: {imc:.2f} - Diagnóstico: {diagnostico}")
        print("----------------------")

    except ValueError:
        print("\nEntrada inválida. O código deve ser um número.")

def incluir_professor(arvore_professor, lista_professor, arvore_cidade, lista_cidade):
    try:
        cod_professor = int(input("Digite o codigo do Professor: "))
        nome = input("Digite o Nome do Professor: ")
        endereco = input("Digite o Endereco do Professor: ")
        telefone = input("Digite o Telefone do Professor: ")
        cod_cidade = int(input("Digite o Cidade do Professor: "))

        endereco_cidade = arvore_cidade.buscar(cod_cidade)
        if endereco_cidade is None:
            print("\nCidade não encontrada. Digite novamente.")
            return

        cidade = lista_cidade[endereco_cidade]

        novo_professor = Professor(cod_professor, nome, endereco, telefone, cidade)
        lista_professor.append(novo_professor)

        novo_endereco = len(lista_professor) - 1
        arvore_professor.inserir(cod_professor, novo_endereco)

        print("\nProfessor incluído com sucesso!")
        print("-" * 30)

    except ValueError:
        print("\nCódigo inválido. Digite um numero inteiro.")

def incluir_modalidade(arvore_modalidade, lista_modalidade, arvore_professor, lista_professor):
    try:
        cod_modalidade = int(input("Digite o codigo do Professor: "))
        desc_modalidade = input("Digite o descricao do modalidade: ")
        valor = input("Digite o valor da aula: ")
        limite = input("Digite o limite de alunos: ")
        total = input("Digite o total de alunos: ")
        cod_professor = int(input("Digite o Cidade do Professor: "))

        endereco_professor = arvore_professor.buscar(cod_professor)
        if endereco_professor is None:
            print("\nCidade não encontrada. Digite novamente.")
            return

        professor = lista_professor[endereco_professor]
        nova_modalidade = Modalidade(cod_modalidade, desc_modalidade, valor, limite, total, professor)
        lista_modalidade.append(nova_modalidade)

        novo_endereco = len(lista_modalidade) - 1
        arvore_modalidade.inserir(cod_modalidade, novo_endereco)

        print("\nModalidade incluída com sucesso!")
        print("-" * 30)

    except ValueError:
        print("\nCódigo inválido. Digite um numero inteiro.")

def incluir_matricula(arvore_matricula, lista_matricula, arvore_aluno, lista_aluno, arvore_modalidade, lista_modalidade):
    try:
        cod_matricula = int(input("Digite o codigo do Matricula: "))
        cod_aluno = int(input("Digite o codigo do Aluno: "))
        cod_modalidade = int(input("Digite o codigo do Modalidade: "))
        quantidade = input("Digite o quantidade de aulas: ")

        endereco_aluno = arvore_aluno.buscar(cod_aluno)
        if endereco_aluno is None:
            print("\nAluno não encontrado. Digite novamente.")
            return

        endereco_modalidade = arvore_modalidade.buscar(cod_modalidade)
        if endereco_modalidade is None:
            print("\nModalidade não encontrada. Digite novamente.")
            return

        aluno = lista_aluno[endereco_aluno]
        modalidade = lista_modalidade[endereco_modalidade]

        nova_matricula = Matricula(cod_matricula, aluno, modalidade, quantidade)
        lista_matricula.append(nova_matricula)

        novo_endereco = len(lista_matricula) - 1
        arvore_matricula.inserir(cod_matricula, novo_endereco)

        print("\nMatrícula feita com sucesso!")
        print("-" * 30)

    except ValueError:
        print("\nCódigo inválido. Digite um numero inteiro.")

if __name__ == "__main__":
    os.makedirs("Dados", exist_ok=True)

    arvore_cidade = ArvoreBinaria()
    arvore_aluno = ArvoreBinaria()

    carregar_dados("Dados/cidades.txt", arvore_cidade, construtor_cidade)

    while True:
        print("\n------ MENU PRINCIPAL ------")
        print("1. Incluir Cidade")
        print("2. Incluir Aluno")
        print("3. Consultar Aluno")
        print("0. Sair")

        opcao = input("Digite sua opcao: ")

        if opcao == '1':
            incluir_cidade(arvore_cidade)
        elif opcao == '2':
            incluir_aluno(arvore_aluno, arvore_cidade)
        elif opcao == '3':
            consultar_aluno(arvore_aluno)
        elif opcao == '0':
            print("Encerrando o programa!")
            break
        else:
            print("Opção inválida.")