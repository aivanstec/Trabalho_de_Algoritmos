import os

# DEFINIÇÃO DOS NOMES DOS ARQUIVOS (DENTRO DA PASTA DADOS)

NOME_PASTA = "Dados"
ARQUIVO_CIDADES = os.path.join(NOME_PASTA, "Dados_Cidade.txt")
ARQUIVO_ALUNOS = os.path.join(NOME_PASTA, "Dados_Aluno.txt")
ARQUIVO_PROFESSORES = os.path.join(NOME_PASTA, "Dados_Professor.txt")
ARQUIVO_MODALIDADES = os.path.join(NOME_PASTA, "Dados_Modalidade.txt")
ARQUIVO_MATRICULAS = os.path.join(NOME_PASTA, "Dados_Matricula.txt")



# PARTE 1: DEFINIÇÃO DE TODAS AS CLASSES

class Cidade:
    def __init__(self, codigo, descricao, estado):
        self.codCidade = int(codigo)
        self.descricao = descricao
        self.estado = estado

    def __str__(self):
        return f"Código: {self.codCidade}, Descrição: {self.descricao}, Estado: {self.estado}"


class Aluno:
    def __init__(self, codigo, nome, dataNascimento, peso, altura, cidade):
        self.codAluno = int(codigo)
        self.nome = nome
        self.data = dataNascimento
        self.peso = float(peso)
        self.altura = float(altura)
        self.cidade = cidade

    def __str__(self):
        return (f"Código do Aluno: {self.codAluno}"
                f"\nNome: {self.nome}, Data de Nascimento: {self.data} "
                f"\nPeso: {self.peso} kg, Altura: {self.altura}m"
                f"\nCidade: {self.cidade.descricao} ({self.cidade.estado})")

    def calcular_imc(self):
        if self.altura > 0: return self.peso / (self.altura ** 2)
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


class Professor:
    def __init__(self, codigo, nome, endereco, telefone, cidade):
        self.codProfessor = int(codigo)
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.cidade = cidade

    def __str__(self):
        return (f"Código: {self.codProfessor}, Nome: {self.nome}\n"
                f"Telefone: {self.telefone}, Endereço: {self.endereco}\n"
                f"Cidade: {self.cidade.descricao} ({self.cidade.estado})")


class Modalidade:
    def __init__(self, codigo, descricao, professor, valorAula, limiteAlunos, totaAlunos):
        self.cod_modalidade = int(codigo)
        self.desc_Modalidade = descricao
        self.cod_professor = professor
        self.valorAula = float(valorAula)
        self.limiteAlunos = int(limiteAlunos)
        self.totaAlunos = int(totaAlunos)

    def __str__(self):
        return (f"Código: {self.cod_modalidade}, Descrição: {self.desc_Modalidade}\n"
                f"Professor: {self.cod_professor.nome}\n"
                f"Valor da Aula: R${self.valorAula:.2f}, Limite: {self.limiteAlunos}, Matriculados: {self.totaAlunos}")


class Matricula:
    def __init__(self, codigo, aluno, modalidade, qtdeAulas):
        self.cod_Matricula = int(codigo)
        self.cod_aluno = aluno
        self.cod_modalidade = modalidade
        self.qtdeAulas = int(qtdeAulas)

    def __str__(self):
        return (
            f"Cód. Matrícula: {self.cod_Matricula}, Aluno: {self.cod_aluno.nome}, Modalidade: {self.cod_modalidade.desc_Modalidade}, Aulas: {self.qtdeAulas}")


class Indece:
    def __init__(self, codigo, end):
        self.codigo = codigo
        self.end = end
        self.esquerda = None
        self.direita = None


class ArvoreBinaria:
    def __init__(self):
        self.raiz = None

    def inserir(self, codigo, end):
        if self.raiz is None:
            self.raiz = Indece(codigo, end)
        else:
            self.inserir_indece(self.raiz, codigo, end)

    def inserir_indece(self, indece_atual, codigo, endereco):
        if codigo < indece_atual.codigo:
            if indece_atual.esquerda is None:
                indece_atual.esquerda = Indece(codigo, endereco)
            else:
                self.inserir_indece(indece_atual.esquerda, codigo, endereco)
        else:
            if indece_atual.direita is None:
                indece_atual.direita = Indece(codigo, endereco)
            else:
                self.inserir_indece(indece_atual.direita, codigo, endereco)

    def buscar(self, codigo):
        return self.buscar_indece(self.raiz, codigo)

    def buscar_indece(self, indece_atual, codigo):
        if indece_atual is None or indece_atual.codigo == codigo: return indece_atual.end if indece_atual else None
        if codigo < indece_atual.codigo:
            return self.buscar_indece(indece_atual.esquerda, codigo)
        else:
            return self.buscar_indece(indece_atual.direita, codigo)

# PARTE 2: FUNÇÕES DE PERSISTÊNCIA E MANIPULAÇÃO DE DADOS

def carregar_dados(app_data):
    print("--- Carregando dados da última sessão ---")
    if os.path.exists(ARQUIVO_CIDADES):
        with open(ARQUIVO_CIDADES, "r", encoding='utf-8') as arq:
            for linha in arq:
                dados = linha.strip().split(';')
                if len(dados) == 3:
                    nova_cidade = Cidade(*dados)
                    app_data["lista_cidade"].append(nova_cidade)
                    app_data["arvore_cidade"].inserir(nova_cidade.codCidade, len(app_data["lista_cidade"]) - 1)
        print("Cidades carregadas.")

    if os.path.exists(ARQUIVO_PROFESSORES):
        with open(ARQUIVO_PROFESSORES, "r", encoding='utf-8') as arq:
            for linha in arq:
                dados = linha.strip().split(';')
                if len(dados) == 5:
                    cod, nome, end, tel, cod_cid = dados
                    end_cid = app_data["arvore_cidade"].buscar(int(cod_cid))
                    if end_cid is not None:
                        cid_obj = app_data["lista_cidade"][end_cid]
                        novo_prof = Professor(cod, nome, end, tel, cid_obj)
                        app_data["lista_professor"].append(novo_prof)
                        app_data["arvore_professor"].inserir(novo_prof.codProfessor,
                                                             len(app_data["lista_professor"]) - 1)
        print("Professores carregados.")

    if os.path.exists(ARQUIVO_ALUNOS):
        with open(ARQUIVO_ALUNOS, "r", encoding='utf-8') as arq:
            for linha in arq:
                dados = linha.strip().split(';')
                if len(dados) == 6:
                    cod, nome, data, peso, alt, cod_cid = dados
                    end_cid = app_data["arvore_cidade"].buscar(int(cod_cid))
                    if end_cid is not None:
                        cid_obj = app_data["lista_cidade"][end_cid]
                        novo_aluno = Aluno(cod, nome, data, peso, alt, cid_obj)
                        app_data["lista_aluno"].append(novo_aluno)
                        app_data["arvore_aluno"].inserir(novo_aluno.codAluno, len(app_data["lista_aluno"]) - 1)
        print("Alunos carregados.")

    if os.path.exists(ARQUIVO_MODALIDADES):
        with open(ARQUIVO_MODALIDADES, "r", encoding='utf-8') as arq:
            for linha in arq:
                dados = linha.strip().split(';')
                if len(dados) == 6:
                    cod, desc, cod_prof, valor, lim, total = dados
                    end_prof = app_data["arvore_professor"].buscar(int(cod_prof))
                    if end_prof is not None:
                        prof_obj = app_data["lista_professor"][end_prof]
                        nova_mod = Modalidade(cod, desc, prof_obj, valor, lim, total)
                        app_data["lista_modalidade"].append(nova_mod)
                        app_data["arvore_modalidade"].inserir(nova_mod.cod_modalidade,
                                                              len(app_data["lista_modalidade"]) - 1)
        print("Modalidades carregadas.")

    if os.path.exists(ARQUIVO_MATRICULAS):
        with open(ARQUIVO_MATRICULAS, "r", encoding='utf-8') as arq:
            for linha in arq:
                dados = linha.strip().split(';')
                if len(dados) == 4:
                    cod, cod_aluno, cod_mod, qtd = dados
                    end_aluno = app_data["arvore_aluno"].buscar(int(cod_aluno))
                    end_mod = app_data["arvore_modalidade"].buscar(int(cod_mod))
                    if end_aluno is not None and end_mod is not None:
                        aluno_obj = app_data["lista_aluno"][end_aluno]
                        mod_obj = app_data["lista_modalidade"][end_mod]
                        nova_mat = Matricula(cod, aluno_obj, mod_obj, qtd)
                        app_data["lista_matricula"].append(nova_mat)
                        app_data["arvore_matricula"].inserir(nova_mat.cod_Matricula,
                                                             len(app_data["lista_matricula"]) - 1)
        print("Matrículas carregadas.")


def salvar_dados(app_data):
    with open(ARQUIVO_CIDADES, "w", encoding='utf-8') as arq:
        for cid in app_data["lista_cidade"]: arq.write(f"{cid.codCidade};{cid.descricao};{cid.estado}\n")
    with open(ARQUIVO_ALUNOS, "w", encoding='utf-8') as arq:
        for al in app_data["lista_aluno"]: arq.write(
            f"{al.codAluno};{al.nome};{al.data};{al.peso};{al.altura};{al.cidade.codCidade}\n")
    with open(ARQUIVO_PROFESSORES, "w", encoding='utf-8') as arq:
        for prof in app_data["lista_professor"]: arq.write(
            f"{prof.codProfessor};{prof.nome};{prof.endereco};{prof.telefone};{prof.cidade.codCidade}\n")
    with open(ARQUIVO_MODALIDADES, "w", encoding='utf-8') as arq:
        for mod in app_data["lista_modalidade"]: arq.write(
            f"{mod.cod_modalidade};{mod.desc_Modalidade};{mod.cod_professor.codProfessor};{mod.valorAula};{mod.limiteAlunos};{mod.totaAlunos}\n")
    with open(ARQUIVO_MATRICULAS, "w", encoding='utf-8') as arq:
        for mat in app_data["lista_matricula"]: arq.write(
            f"{mat.cod_Matricula};{mat.cod_aluno.codAluno};{mat.cod_modalidade.cod_modalidade};{mat.qtdeAulas}\n")
    print("\nTodos os dados foram salvos com sucesso!")


def incluir_cidade(app_data):
    try:
        cod = int(input("Digite o código da cidade: "))
        if app_data["arvore_cidade"].buscar(cod) is not None:
            print("\nErro: Já existe uma cidade com este código.")
            return
        desc = input("Digite o Nome: ")
        est = input("Digite o Estado (UF): ")
        obj = Cidade(cod, desc, est)
        app_data["lista_cidade"].append(obj)
        app_data["arvore_cidade"].inserir(cod, len(app_data["lista_cidade"]) - 1)
        print("\nCidade incluída com sucesso!")
    except ValueError:
        print("\nCódigo inválido. Digite um número inteiro.")


def incluir_aluno(app_data):
    try:
        cod = int(input("Digite o código do Aluno: "))
        if app_data["arvore_aluno"].buscar(cod) is not None:
            print("\nErro: Já existe um aluno com este código.")
            return
        nome = input("Digite o Nome: ")
        data = input("Digite a data de nascimento: ")
        peso = float(input("Digite o peso (ex: 70.5): "))
        altura = float(input("Digite a altura (ex: 1.75): "))
        cod_cid = int(input("Digite o Código da Cidade: "))
        end_cid = app_data["arvore_cidade"].buscar(cod_cid)
        if end_cid is None:
            print("\nCidade não encontrada.")
            return
        cid = app_data["lista_cidade"][end_cid]
        obj = Aluno(cod, nome, data, peso, altura, cid)
        app_data["lista_aluno"].append(obj)
        app_data["arvore_aluno"].inserir(cod, len(app_data["lista_aluno"]) - 1)
        print("\nAluno incluído com sucesso!")
    except ValueError:
        print("\nDados inválidos. Verifique os números digitados.")


def incluir_professor(app_data):
    try:
        cod = int(input("Digite o código do Professor: "))
        if app_data["arvore_professor"].buscar(cod) is not None:
            print("\nErro: Já existe um professor com este código.")
            return
        nome = input("Digite o Nome: ")
        end = input("Digite o Endereço: ")
        tel = input("Digite o Telefone: ")
        cod_cid = int(input("Digite o Código da Cidade: "))
        end_cid = app_data["arvore_cidade"].buscar(cod_cid)
        if end_cid is None:
            print("\nCidade não encontrada.")
            return
        cid = app_data["lista_cidade"][end_cid]
        obj = Professor(cod, nome, end, tel, cid)
        app_data["lista_professor"].append(obj)
        app_data["arvore_professor"].inserir(cod, len(app_data["lista_professor"]) - 1)
        print("\nProfessor incluído com sucesso!")
    except ValueError:
        print("\nDados inválidos. Verifique os números digitados.")


def incluir_modalidade(app_data):
    try:
        cod = int(input("Digite o código da Modalidade: "))
        if app_data["arvore_modalidade"].buscar(cod) is not None:
            print("\nErro: Já existe uma modalidade com este código.")
            return
        desc = input("Digite a Descrição: ")
        cod_prof = int(input("Digite o Código do Professor: "))
        end_prof = app_data["arvore_professor"].buscar(cod_prof)
        if end_prof is None:
            print("\nProfessor não encontrado.")
            return
        prof = app_data["lista_professor"][end_prof]
        valor = float(input("Digite o valor da aula: "))
        limite = int(input("Digite o limite de alunos: "))
        obj = Modalidade(cod, desc, prof, valor, limite, 0)
        app_data["lista_modalidade"].append(obj)
        app_data["arvore_modalidade"].inserir(cod, len(app_data["lista_modalidade"]) - 1)
        print("\nModalidade incluída com sucesso!")
    except ValueError:
        print("\nDados inválidos. Verifique os números digitados.")


def incluir_matricula(app_data):
    try:
        cod = int(input("Digite o código da Matrícula: "))
        if app_data["arvore_matricula"].buscar(cod) is not None:
            print("\nErro: Já existe uma matrícula com este código.")
            return
        cod_aluno = int(input("Digite o código do Aluno: "))
        end_aluno = app_data["arvore_aluno"].buscar(cod_aluno)
        if end_aluno is None:
            print("\nAluno não encontrado.")
            return
        cod_mod = int(input("Digite o código da Modalidade: "))
        end_mod = app_data["arvore_modalidade"].buscar(cod_mod)
        if end_mod is None:
            print("\nModalidade não encontrada.")
            return
        aluno = app_data["lista_aluno"][end_aluno]
        mod = app_data["lista_modalidade"][end_mod]
        qtd = int(input("Digite a quantidade de aulas: "))
        obj = Matricula(cod, aluno, mod, qtd)
        app_data["lista_matricula"].append(obj)
        app_data["arvore_matricula"].inserir(cod, len(app_data["lista_matricula"]) - 1)
        print("\nMatrícula incluída com sucesso!")
    except ValueError:
        print("\nDados inválidos. Verifique os números digitados.")


def consultar_aluno(app_data):
    try:
        cod = int(input("Digite o código do aluno a consultar: "))
        end = app_data["arvore_aluno"].buscar(cod)
        if end is None:
            print("\nAluno não encontrado.")
            return
        aluno = app_data["lista_aluno"][end]
        print("\n--- Ficha do Aluno ---")
        print(aluno)
        imc = aluno.calcular_imc()
        diag = aluno.diagnostico_imc()
        print(f"IMC: {imc:.2f} - Diagnóstico: {diag}")
    except ValueError:
        print("\nCódigo inválido.")

# PARTE 3: EXECUÇÃO PRINCIPAL DO PROGRAMA

if __name__ == "__main__":
    if not os.path.exists(NOME_PASTA):
        os.makedirs(NOME_PASTA)
        print(f"Pasta '{NOME_PASTA}' criada com sucesso.")

    app_data = {
        "lista_cidade": [], "arvore_cidade": ArvoreBinaria(),
        "lista_aluno": [], "arvore_aluno": ArvoreBinaria(),
        "lista_professor": [], "arvore_professor": ArvoreBinaria(),
        "lista_modalidade": [], "arvore_modalidade": ArvoreBinaria(),
        "lista_matricula": [], "arvore_matricula": ArvoreBinaria(),
    }
    carregar_dados(app_data)

    while True:
        print("\n------ MENU PRINCIPAL  ------")
        print("1. Incluir Cidade")
        print("2. Incluir Professor")
        print("3. Incluir Aluno")
        print("4. Incluir Modalidade")
        print("5. Realizar Matrícula")

        print("6. Consultar Aluno")
        print("0. Salvar e Sair")

        opcao = input("Digite sua opção: ")

        if opcao == '1':
            incluir_cidade(app_data)
        elif opcao == '2':
            incluir_professor(app_data)
        elif opcao == '3':
            incluir_aluno(app_data)
        elif opcao == '4':
            incluir_modalidade(app_data)
        elif opcao == '5':
            incluir_matricula(app_data)
        elif opcao == '6':
            consultar_aluno(app_data)
        elif opcao == '0':
            salvar_dados(app_data)
            print("Encerrando o programa!")
            break
        else:
            print("Opção inválida.")

