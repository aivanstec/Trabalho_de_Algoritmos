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
        elif codigo > indece_atual.codigo:
            if indece_atual.direita is None:
                indece_atual.direita = Indece(codigo, dado_obj)
            else:
                self.inserir_indece(indece_atual.direita, codigo, dado_obj)

    def buscar(self, codigo):
        return self.buscar_indece(self.raiz, codigo)

    def buscar_indece(self, indece_atual, codigo):
        if indece_atual is None or indece_atual.codigo == codigo:
            return indece_atual.dado if indece_atual else None
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
            print(f"\nErro falha ao salvar o arquivo '{arquivo}'. Detalhes: {e}")

    def salvar_arquivo(self, indece_atual, arquivo, formatador_arquivo):
        if indece_atual is not None:
            self.salvar_arquivo(indece_atual.esquerda, arquivo, formatador_arquivo)
            objeto = indece_atual.dado
            linha = formatador_arquivo(objeto)
            arquivo.write(linha)
            self.salvar_arquivo(indece_atual.direita, arquivo, formatador_arquivo)

def carregar_dados(arquivo, arvore, construtor_arq, **carregar):
    try:
        with open(arquivo, "r", encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    dados = [d.strip() for d in linha.split(',')]
                    obj = construtor_arq(dados, **carregar)
                    if obj:
                        codigo_obj = getattr(obj, list(obj.__dict__.keys())[0])
                        arvore.inserir(codigo_obj, obj)
        print(f"Dados de '{arquivo}' carregados.")
    except FileNotFoundError:
        print(f"Arquivo '{arquivo}' não encontrado.")
    except Exception as e:
        print(f"Erro ao carregar '{arquivo}': {e}")

    def remover(self, codigo):
        self.raiz = self.excluir_indece(self.raiz, codigo)

    def encontrar_indece(self, indece_atual):
        while indece_atual and indece_atual.direita is not None:
            indece_atual = indece_atual.direita
        return indece_atual

    def excluir_indece(self, indece_atual, codigo):
        if indece_atual is None:
            return indece_atual

        if codigo < indece_atual.codigo:
            indece_atual.esquerda = self.excluir_indece(indece_atual.esquerda, codigo)
        elif codigo > indece_atual.codigo:
            indece_atual.direita = self.excluir_indece(indece_atual.direita, codigo)
        else:
            if indece_atual.esquerda is None:
                return indece_atual.direita
            elif indece_atual.direita is None:
                return indece_atual.esquerda

            predecessor = self.encontrar_indece(indece_atual.esquerda)

            indece_atual.codigo = predecessor.codigo
            indece_atual.dado = predecessor.dado

            indece_atual.esquerda = self.excluir_indece(indece_atual.esquerda, predecessor.codigo)

        return indece_atual

#------- Área da Cidade -------
def construtor_cidade(data, **carregar):
    return Cidade(int(data[0]), data[1], data[2])

def incluir_cidade(arvore_cidade):
    try:
        cod_cidade = int(input("Digite o codigo da cidade: "))
        if arvore_cidade.buscar(cod_cidade) is not None:
            print("\nErro: Já existe cidade com esse CEP.")
            return
        descricao = input("Digite o Nome: ")
        estado = input("Digite o Estado (UF): ")
        nova_cidade = Cidade(cod_cidade, descricao, estado)
        arvore_cidade.inserir(cod_cidade, nova_cidade)
        formato = lambda cid: f"{cid.codCidade}, {cid.descricao}, {cid.estado}\n"
        arvore_cidade.salvar("Dados/cidades.txt", formato)
        print("\nCidade incluída com sucesso!")
    except ValueError:
        print("\nCódigo inválido. Digite um numero inteiro.")

def consultar_cidade(arvore_cidade):
    try:
        codigo = int(input("Digite o código da cidade que deseja consultar: "))
        cidade_encontrada = arvore_cidade.buscar(codigo)
        if cidade_encontrada is None:
            print("\nCidade não encontrada com este código.")
            return
        print("\n--- Ficha da Cidade ---")
        print(cidade_encontrada)
        print("-----------------------")
    except ValueError:
        print("\nEntrada inválida. O código deve ser um número.")

def excluir_cidade(arvore_cidade, arvore_aluno, arvore_professor):
    try:
        codigo = int(input("Digite o código da cidade a ser excluída: "))
        if arvore_cidade.buscar(codigo) is None:
            print("\nCidade não encontrada com este código.")
            return

        arvore_cidade.remover(codigo)
        formato = lambda cid: f"{cid.codCidade},{cid.descricao},{cid.estado}\n"
        arvore_cidade.salvar("Dados/cidades.txt", formato)
        print("\nCidade excluída com sucesso.")
    except ValueError:
        print("\nEntrada inválida. O código deve ser um número.")

#------- Área da Aluno -------
def construtor_aluno(data, **carregar):
    arvore_cidade = carregar['arvore_cidade']
    cidade = arvore_cidade.buscar(int(data[5]))
    if cidade:
        return Aluno(int(data[0]), data[1], data[2], float(data[3]), float(data[4]), cidade)
    return None

def incluir_aluno(arvore_aluno, arvore_cidade):
    try:
        cod_aluno = int(input("Digite o codigo do Aluno: "))
        if arvore_aluno.buscar(cod_aluno):
            print("\nErro: Já existe aluno com esse ID.")
            return
        nome = input("Digite o Nome: ")
        data = input("Digite a data de nascimento: ")
        peso = float(input("Digite o peso: "))
        altura = float(input("Digite a altura: "))
        cod_cidade = int(input("Digite o Código da Cidade: "))

        cidade = arvore_cidade.buscar(cod_cidade)
        if cidade is None:
            print("\nCidade não encontrada. Cadastre a cidade primeiro.")
            return

        novo_aluno = Aluno(cod_aluno, nome, data, peso, altura, cidade)
        arvore_aluno.inserir(cod_aluno, novo_aluno)
        formato = lambda \
            alu: f"{alu.codAluno}, {alu.nome}, {alu.data}, {alu.peso}, {alu.altura}, {alu.cidade.codCidade}\n"
        arvore_aluno.salvar("Dados/alunos.txt", formato)
        print("\nAluno incluído com sucesso!")
    except (ValueError, IndexError):
        print("\nDados inválidos. Por favor, tente novamente.")

def consultar_aluno(arvore_alunos):
    try:
        codigo = int(input("Digite o código do aluno que deseja consultar: "))
        aluno_encontrado = arvore_alunos.buscar(codigo)

        if aluno_encontrado is None:
            print("\nAluno não encontrado com este código.")
            return
        print("\n--- Ficha do Aluno ---")
        print(aluno_encontrado)
        print(f"IMC: {aluno_encontrado.calcular_imc():.2f} - Diagnóstico: {aluno_encontrado.diagnostico_imc()}")
        print("----------------------")
    except ValueError:
        print("\nEntrada inválida. O código deve ser um número.")

def excluir_aluno(arvore_aluno, arvore_matricula):
    try:
        codigo = int(input("Digite o código do aluno a ser excluído: "))
        if arvore_aluno.buscar(codigo) is None:
            print("\nAluno não encontrado com este código.")
            return

        arvore_aluno.remover(codigo)
        formato = lambda a: f"{a.codAluno},{a.nome},{a.data},{a.peso},{a.altura},{a.cidade.codCidade}\n"
        arvore_aluno.salvar("Dados/alunos.txt", formato)
        print("\nAluno excluído com sucesso.")
    except ValueError:
        print("\nEntrada inválida. O código deve ser um número.")

#------- Área da Professor -------
def construtor_professor(data, **carrega):
    arvore_cidade = carrega['arvore_cidade']
    cidade = arvore_cidade.buscar(int(data[4]))
    if carrega:
        return Professor(int(data[0]), data[1], data[2], data[3], cidade)
    return None

def incluir_professor(arvore_professor, arvore_cidade):
    try:
        cod_professor = int(input("Digite o codigo do Professor: "))
        if arvore_professor.buscar(cod_professor):
            print("\nErro: Já existe professor com esse ID.")
            return
        nome = input("Digite o Nome do Professor: ")
        endereco = input("Digite o Endereço: ")
        telefone = input("Digite o Telefone: ")
        cod_cidade = int(input("Digite o Código da Cidade: "))

        cidade = arvore_cidade.buscar(cod_cidade)
        if cidade is None:
            print("\nCidade não encontrada. Cadastre a cidade primeiro.")
            return

        novo_professor = Professor(cod_professor, nome, endereco, telefone, cidade)
        arvore_professor.inserir(cod_professor, novo_professor)
        formato = lambda \
                prof: f"{prof.codProfessor}, {prof.nome}, {prof.endereco}, {prof.telefone}, {prof.cidade.codCidade}\n"
        arvore_professor.salvar("Dados/professores.txt", formato)
        print("\nProfessor incluído com sucesso!")
    except (ValueError, IndexError):
        print("\nDados inválidos. Por favor, tente novamente.")

def consultar_professor(arvore_professor):
    try:
        codigo = int(input("Digite o código do professor que deseja consultar: "))
        professor_encontrado = arvore_professor.buscar(codigo)
        if professor_encontrado is None:
            print("\nProfessor não encontrado com este código.")
            return
        print("\n--- Ficha do Professor ---")
        print(professor_encontrado)
        print("--------------------------")
    except ValueError:
        print("\nEntrada inválida. O código deve ser um número.")

def excluir_professor(arvore_professor, arvore_modalidade):
    try:
        codigo = int(input("Digite o código do professor a ser excluído: "))
        if arvore_professor.buscar(codigo) is None:
            print("\nProfessor não encontrado com este código.")
            return

        arvore_professor.remover(codigo)
        formato = lambda p: f"{p.codProfessor},{p.nome},{p.endereco},{p.telefone},{p.cidade.codCidade}\n"
        arvore_professor.salvar("Dados/professores.txt", formato)
        print("\nProfessor excluído com sucesso.")
    except ValueError:
        print("\nEntrada inválida. O código deve ser um número.")

#------- Área da Modalidade -------
def construtor_modalidade(data, **carrega):
    arvore_professor = carrega['arvore_professor']
    professor = arvore_professor.buscar(int(data[5]))
    if professor:
        return Modalidade(int(data[0]), data[1], professor, float(data[2]), int(data[3]), int(data[4]))
    return None

def incluir_modalidade(arvore_modalidade, arvore_professor):
    try:
        cod_modalidade = int(input("Digite o codigo da Modalidade: "))
        if arvore_modalidade.buscar(cod_modalidade):
            print("\nErro: Já existe modalidade com esse ID.")
            return
        desc_modalidade = input("Digite a descricao da modalidade: ")
        valor = float(input("Digite o valor da aula: "))
        limite = int(input("Digite o limite de alunos: "))
        total = int(input("Digite o total de alunos atual: "))
        cod_professor = int(input("Digite o código do Professor: "))

        professor = arvore_professor.buscar(cod_professor)
        if professor is None:
            print("\nProfessor não encontrado. Cadastre o professor primeiro.")
            return

        nova_modalidade = Modalidade(cod_modalidade, desc_modalidade, professor, valor, limite, total)
        arvore_modalidade.inserir(cod_modalidade, nova_modalidade)
        formato = lambda mod: f"{mod.cod_modalidade},{mod.desc_Modalidade},{mod.valorAula},{mod.limiteAlunos},{mod.totaAlunos},{mod.cod_professor.codProfessor}\n"
        arvore_modalidade.salvar("Dados/modalidades.txt", formato)
        print("\nModalidade incluída com sucesso!")
    except (ValueError, IndexError):
        print("\nDados inválidos. Por favor, tente novamente.")

def consultar_modalidade(arvore_modalidade):
    try:
        codigo = int(input("Digite o código da modalidade que deseja consultar: "))
        modalidade_encontrada = arvore_modalidade.buscar(codigo)
        if modalidade_encontrada is None:
            print("\nModalidade não encontrada com este código.")
            return
        print("\n--- Ficha da Modalidade ---")
        print(modalidade_encontrada)
        print("---------------------------")
    except ValueError:
        print("\nEntrada inválida. O código deve ser um número.")

def excluir_modalidade(arvore_modalidade, arvore_matricula):
    try:
        codigo = int(input("Digite o código da modalidade a ser excluída: "))
        if arvore_modalidade.buscar(codigo) is None:
            print("\nModalidade não encontrada com este código.")
            return

        arvore_modalidade.remover(codigo)
        formato = lambda \
            m: f"{m.cod_modalidade},{m.desc_Modalidade},{m.valorAula},{m.limiteAlunos},{m.totaAlunos},{m.cod_professor.codProfessor}\n"
        arvore_modalidade.salvar("Dados/modalidades.txt", formato)
        print("\nModalidade excluída com sucesso.")
    except ValueError:
        print("\nEntrada inválida. O código deve ser um número.")

#------- Área da Matricila -------
def construtor_matricula(data, **carrega):
    arvore_aluno = carrega['arvore_aluno']
    arvore_modalidade = carrega['arvore_modalidade']
    aluno = arvore_aluno.buscar(int(data[2]))
    modalidade = arvore_modalidade.buscar(int(data[3]))
    if modalidade and aluno:
        return Matricula(int(data[0]), aluno, modalidade, int(data[1]))
    return None

def incluir_matricula(arvore_matricula, arvore_aluno, arvore_modalidade):
    try:
        cod_matricula = int(input("Digite o codigo da Matrícula: "))
        if arvore_matricula.buscar(cod_matricula):
            print("\nErro: Já existe uma matrícula com este código.")
            return
        cod_aluno = int(input("Digite o codigo do Aluno: "))
        cod_modalidade = int(input("Digite o codigo da Modalidade: "))
        qtde_aulas = int(input("Digite a quantidade de aulas: "))

        aluno = arvore_aluno.buscar(cod_aluno)
        if aluno is None:
            print("\nAluno não encontrado.")
            return

        modalidade = arvore_modalidade.buscar(cod_modalidade)
        if modalidade is None:
            print("\nModalidade não encontrada.")
            return

        nova_matricula = Matricula(cod_matricula, aluno, modalidade, qtde_aulas)
        arvore_matricula.inserir(cod_matricula, nova_matricula)
        formato = lambda matri: f"{matri.cod_Matricula},{matri.qtdeAulas},{matri.cod_aluno.codAluno},{matri.cod_modalidade.cod_modalidade}\n"
        arvore_matricula.salvar("Dados/matriculas.txt", formato)
        print("\nMatrícula feita com sucesso!")
    except (ValueError, IndexError):
        print("\nDados inválidos. Por favor, tente novamente.")

def consultar_matricula(arvore_matricula):
    try:
        codigo = int(input("Digite o código da matrícula que deseja consultar: "))
        matricula_encontrada = arvore_matricula.buscar(codigo)
        if matricula_encontrada is None:
            print("\nMatrícula não encontrada com este código.")
            return
        print("\n--- Ficha da Matrícula ---")
        print(matricula_encontrada)
        print("--------------------------")
    except ValueError:
        print("\nEntrada inválida. O código deve ser um número.")

def excluir_matricula(arvore_matricula):
    try:
        codigo = int(input("Digite o código da matrícula a ser excluída: "))
        if arvore_matricula.buscar(codigo) is None:
            print("\nMatrícula não encontrada com este código.")
            return

        arvore_matricula.remover(codigo)
        formato = lambda m: f"{m.cod_Matricula},{m.qtdeAulas},{m.cod_aluno.codAluno},{m.cod_modalidade.cod_modalidade}\n"
        arvore_matricula.salvar("Dados/matriculas.txt", formato)
        print("\nMatrícula excluída com sucesso.")
    except ValueError:
        print("\nEntrada inválida. O código deve ser um número.")

if __name__ == "__main__":
    os.makedirs("Dados", exist_ok=True)

    arvore_cidade = ArvoreBinaria()
    arvore_aluno = ArvoreBinaria()
    arvore_professor = ArvoreBinaria()
    arvore_modalidade = ArvoreBinaria()
    arvore_matricula = ArvoreBinaria()

    carregar_dados("Dados/cidades.txt", arvore_cidade, construtor_cidade)
    carregar_dados("Dados/alunos.txt", arvore_aluno, construtor_aluno, arvore_cidade = arvore_cidade)
    carregar_dados("Dados/professores.txt", arvore_professor, construtor_professor, arvore_cidade = arvore_cidade)
    carregar_dados("Dados/modalidades.txt", arvore_modalidade, construtor_modalidade, arvore_professor = arvore_professor)
    carregar_dados("Dados/matriculas.txt", arvore_matricula, construtor_matricula, arvore_aluno = arvore_aluno, arvore_modalidade = arvore_modalidade)

    while True:
        print("\n------ MENU PRINCIPAL ------")
        print("1. Incluir Cidade")
        print("2. Incluir Aluno")
        print("3. Incluir Professor")
        print("4. Incluir Modalidade")
        print("5. Fazer Matrícula")
        print("6. Consultar Cidade")
        print("7. Consultar Aluno")
        print("0. Sair")

        opcao = input("Digite sua opcao: ")

        if opcao == '1':
            incluir_cidade(arvore_cidade)
        elif opcao == '2':
            incluir_aluno(arvore_aluno, arvore_cidade)
        elif opcao == '3':
            incluir_professor(arvore_professor, arvore_cidade)
        elif opcao == '4':
            incluir_modalidade(arvore_modalidade, arvore_professor)
        elif opcao == '5':
            incluir_matricula(arvore_matricula, arvore_aluno, arvore_modalidade)
        elif opcao == '6':
            consultar_cidade(arvore_cidade)
        elif opcao == '7':
            consultar_aluno(arvore_aluno)
        elif opcao == '0':
            print("Encerrando o programa!")
            break
        else:
            print("Opção inválida.")