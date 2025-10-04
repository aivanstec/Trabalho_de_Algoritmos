import os
import customtkinter as ctk
from tkinter import messagebox

# ------- Classe Cidade -------
class Cidade:
    def __init__(self, codigo, descricao, estado):
        self.codCidade = codigo
        self.descricao = descricao
        self.estado = estado

    def __str__(self):
        return f"Código: {self.codCidade}, Descrição: {self.descricao}, Estado: {self.estado}"

# ------- Classe Aluno -------
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
                f"\nCidade: {self.cidade.descricao} ({self.cidade.estado})")

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

# ------- Classe Professor -------
class Professor:
    def __init__(self, codigo, nome, endereco, telefone, cidade):
        self.codProfessor = codigo
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.cidade = cidade

    def __str__(self):
        return (f"Código do Professor: {self.codProfessor}"
                f"\nNome: {self.nome},  Telefone: {self.telefone}"
                f"\nEndereço: {self.endereco} Cidade: {self.cidade.descricao} ({self.cidade.estado})")

# ------- Classe Modalidade -------
class Modalidade:
    def __init__(self, codigo, descricao, professor, valorAula, limiteAlunos, totaAlunos):
        self.cod_modalidade = codigo
        self.desc_Modalidade = descricao
        self.cod_professor = professor
        self.valorAula = valorAula
        self.limiteAlunos = limiteAlunos
        self.totaAlunos = totaAlunos

    def __str__(self):
        return (f"Código da Modalidade: {self.cod_modalidade}, Descrição: {self.desc_Modalidade}\n"
                f"Professor: {self.cod_professor.nome} (Cidade: {self.cod_professor.cidade.descricao})\n"
                f"Valor da Aula: R${self.valorAula:.2f}, Limite de Alunos: {self.limiteAlunos}, Total de Alunos: {self.totaAlunos}")

# ------- Classe Matrícula -------
class Matricula:
    def __init__(self, codigo, aluno, modalidade, qtdeAulas):
        self.cod_Matricula = codigo
        self.cod_aluno = aluno
        self.cod_modalidade = modalidade
        self.qtdeAulas = qtdeAulas

    def __str__(self):
        return (f"Código da Matrícula: {self.cod_Matricula}\n"
                f"Aluno: {self.cod_aluno.nome} (Cidade: {self.cod_aluno.cidade.descricao})\n"
                f"Modalidade: {self.cod_modalidade.desc_Modalidade}\n"
                f"Quantidade de Aulas: {self.qtdeAulas}\n"
                f"Valor a Pagar: R${self.calcular_valor():.2f}")

    def calcular_valor(self):
        return self.qtdeAulas * self.cod_modalidade.valorAula

# ------- Classe Indece -------
class Indece:
    def __init__(self, codigo, dado_obj):
        self.codigo = codigo
        self.dado = dado_obj
        self.esquerda = None
        self.direita = None

# ------- Árvore Binária -------
class ArvoreBinaria:
    def __init__(self):
        self.raiz = None

    def inserir(self, codigo, dado_obj):
        if self.raiz is None:
            self.raiz = Indece(codigo, dado_obj)
        else:
            self._inserir_indece(self.raiz, codigo, dado_obj)

    def _inserir_indece(self, indece_atual, codigo, dado_obj):
        if codigo < indece_atual.codigo:
            if indece_atual.esquerda is None:
                indece_atual.esquerda = Indece(codigo, dado_obj)
            else:
                self._inserir_indece(indece_atual.esquerda, codigo, dado_obj)
        elif codigo > indece_atual.codigo:
            if indece_atual.direita is None:
                indece_atual.direita = Indece(codigo, dado_obj)
            else:
                self._inserir_indece(indece_atual.direita, codigo, dado_obj)

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
            with open(arquivo, "w", encoding='utf-8') as arq:
                self.salvar_arquivo(self.raiz, arq, formatador_arquivo)
        except Exception as e:
            messagebox.showerror("Erro de Arquivo", f"Falha ao salvar o arquivo '{arquivo}'.\nDetalhes: {e}")

    def salvar_arquivo(self, indece_atual, arquivo, formatador_arquivo):
        if indece_atual is not None:
            self.salvar_arquivo(indece_atual.esquerda, arquivo, formatador_arquivo)
            objeto = indece_atual.dado
            linha = formatador_arquivo(objeto)
            arquivo.write(linha)
            self.salvar_arquivo(indece_atual.direita, arquivo, formatador_arquivo)

    def remover(self, codigo):
        self.raiz = self.excluir_indece(self.raiz, codigo)

    def _encontrar_minimo(self, indece_atual):
        while indece_atual and indece_atual.esquerda is not None:
            indece_atual = indece_atual.esquerda
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
            sucessor = self._encontrar_minimo(indece_atual.direita)
            indece_atual.codigo = sucessor.codigo
            indece_atual.dado = sucessor.dado
            indece_atual.direita = self.excluir_indece(indece_atual.direita, sucessor.codigo)
        return indece_atual

    def percorrer(self):
        dados = []
        self.percorrer_raiz(self.raiz, dados)
        return dados

    def percorrer_raiz(self, indece_atual, dados):
        if indece_atual is not None:
            self.percorrer_raiz(indece_atual.esquerda, dados)
            dados.append(indece_atual.dado)
            self.percorrer_raiz(indece_atual.direita, dados)

def leitura_exaustiva(arvore, nome_tabela):
    print(f"\n--- Leitura Exaustiva de {nome_tabela} ---")
    todos_os_itens = arvore.percorrer()
    if not todos_os_itens:
        print(f"Nenhum registro encontrado em {nome_tabela}.")
        return
    for item in todos_os_itens:
        print(item)
        print("-" * 20)
    print(f"Total de {len(todos_os_itens)} registros.")

# ------- Funções de Carregamento -------
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
        print(f"Arquivo '{arquivo}' não encontrado. Será criado um novo ao salvar.")
    except Exception as e:
        messagebox.showwarning("Erro de Carregamento", f"Erro ao carregar dados de '{arquivo}': {e}")

def construtor_cidade(data, **carregar):
    return Cidade(int(data[0]), data[1], data[2])

def construtor_aluno(data, **carregar):
    arvore_cidade = carregar['arvore_cidade']
    cidade = arvore_cidade.buscar(int(data[5]))
    if cidade:
        return Aluno(int(data[0]), data[1], data[2], float(data[3]), float(data[4]), cidade)
    return None

def construtor_professor(data, **carregar):
    arvore_cidade = carregar['arvore_cidade']
    cidade = arvore_cidade.buscar(int(data[4]))
    if carregar:
        return Professor(int(data[0]), data[1], data[2], data[3], cidade)
    return None

def construtor_modalidade(data, **carregar):
    arvore_professor = carregar['arvore_professor']
    professor = arvore_professor.buscar(int(data[5]))
    if professor:
        return Modalidade(int(data[0]), data[1], professor, float(data[2]), int(data[3]), int(data[4]))
    return None

def construtor_matricula(data, **carregar):
    arvore_aluno = carregar['arvore_aluno']
    arvore_modalidade = carregar['arvore_modalidade']
    aluno = arvore_aluno.buscar(int(data[2]))
    modalidade = arvore_modalidade.buscar(int(data[3]))
    if modalidade and aluno:
        return Matricula(int(data[0]), aluno, modalidade, int(data[1]))
    return None

# ------- Área do Front-end -------
class App(ctk.CTk):
    def __init__(self, arvores):
        super().__init__()
        self.arvores = arvores

        self.title("PowerOn")
        self.geometry("1500x768")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.tab_view = ctk.CTkTabview(self, width=780, height=580)
        self.tab_view.pack(padx=10, pady=10)

        self.tab_view.add("Cadastros")
        self.tab_view.add("Consultas")
        self.tab_view.add("Exclusões")
        self.tab_view.add("Listagens")
        self.tab_view.add("Relatórios")

        self.cadastros()
        self.consultas()
        self.exclusoes()
        self.listagens()
        self.relatorios()

    def cadastros(self):
        cadastros_tab = self.tab_view.tab("Cadastros")

        cadastro_opts = ctk.CTkTabview(cadastros_tab, width=760, height=520)
        cadastro_opts.pack(padx=5, pady=5)

        tabs = ["Cidade", "Aluno", "Professor", "Modalidade", "Matrícula"]
        for tab in tabs:
            cadastro_opts.add(tab)

        cidade = ctk.CTkScrollableFrame(cadastro_opts.tab("Cidade"))
        cidade.pack(fill="both", expand=True)
        ctk.CTkLabel(cidade, text="Código da Cidade:").pack(padx=10, pady=5, anchor="w")
        self.cidade_cod = ctk.CTkEntry(cidade)
        self.cidade_cod.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(cidade, text="Descrição:").pack(padx=10, pady=5, anchor="w")
        self.cidade_desc = ctk.CTkEntry(cidade)
        self.cidade_desc.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(cidade, text="Estado (UF):").pack(padx=10, pady=5, anchor="w")
        self.cidade_uf = ctk.CTkEntry(cidade)
        self.cidade_uf.pack(padx=10, pady=5, fill="x")
        ctk.CTkButton(cidade, text="Incluir Cidade", command=self.incluir_cidade).pack(padx=10, pady=20)

        aluno = ctk.CTkScrollableFrame(cadastro_opts.tab("Aluno"))
        aluno.pack(fill="both", expand=True)
        ctk.CTkLabel(aluno, text="Código do Aluno:").pack(padx=10, pady=5, anchor="w")
        self.aluno_cod = ctk.CTkEntry(aluno)
        self.aluno_cod.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(aluno, text="Nome:").pack(padx=10, pady=5, anchor="w")
        self.aluno_nome = ctk.CTkEntry(aluno)
        self.aluno_nome.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(aluno, text="Data de Nascimento:").pack(padx=10, pady=5, anchor="w")
        self.aluno_data = ctk.CTkEntry(aluno)
        self.aluno_data.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(aluno, text="Peso (kg):").pack(padx=10, pady=5, anchor="w")
        self.aluno_peso = ctk.CTkEntry(aluno)
        self.aluno_peso.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(aluno, text="Altura (m):").pack(padx=10, pady=5, anchor="w")
        self.aluno_altura = ctk.CTkEntry(aluno)
        self.aluno_altura.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(aluno, text="Código da Cidade:").pack(padx=10, pady=5, anchor="w")
        self.aluno_cidade_cod = ctk.CTkEntry(aluno)
        self.aluno_cidade_cod.pack(padx=10, pady=5, fill="x")
        ctk.CTkButton(aluno, text="Incluir Aluno", command=self.incluir_aluno).pack(padx=10, pady=20)

        professor = ctk.CTkScrollableFrame(cadastro_opts.tab("Professor"))
        professor.pack(fill="both", expand=True)
        ctk.CTkLabel(professor, text="Código do Professor:").pack(padx=10, pady=5, anchor="w")
        self.prof_cod = ctk.CTkEntry(professor)
        self.prof_cod.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(professor, text="Nome:").pack(padx=10, pady=5, anchor="w")
        self.prof_nome = ctk.CTkEntry(professor)
        self.prof_nome.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(professor, text="Endereço:").pack(padx=10, pady=5, anchor="w")
        self.prof_end = ctk.CTkEntry(professor)
        self.prof_end.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(professor, text="Telefone:").pack(padx=10, pady=5, anchor="w")
        self.prof_tel = ctk.CTkEntry(professor)
        self.prof_tel.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(professor, text="Código da Cidade:").pack(padx=10, pady=5, anchor="w")
        self.prof_cidade_cod = ctk.CTkEntry(professor)
        self.prof_cidade_cod.pack(padx=10, pady=5, fill="x")
        ctk.CTkButton(professor, text="Incluir Professor", command=self.incluir_professor).pack(padx=10, pady=20)

        mod_frame = ctk.CTkScrollableFrame(cadastro_opts.tab("Modalidade"))
        mod_frame.pack(fill="both", expand=True)
        ctk.CTkLabel(mod_frame, text="Código da Modalidade:").pack(padx=10, pady=5, anchor="w")
        self.mod_cod_entry = ctk.CTkEntry(mod_frame)
        self.mod_cod_entry.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(mod_frame, text="Descrição:").pack(padx=10, pady=5, anchor="w")
        self.mod_desc_entry = ctk.CTkEntry(mod_frame)
        self.mod_desc_entry.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(mod_frame, text="Valor da Aula (R$):").pack(padx=10, pady=5, anchor="w")
        self.mod_valor_entry = ctk.CTkEntry(mod_frame)
        self.mod_valor_entry.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(mod_frame, text="Limite de Alunos:").pack(padx=10, pady=5, anchor="w")
        self.mod_limite_entry = ctk.CTkEntry(mod_frame)
        self.mod_limite_entry.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(mod_frame, text="Código do Professor:").pack(padx=10, pady=5, anchor="w")
        self.mod_prof_cod_entry = ctk.CTkEntry(mod_frame)
        self.mod_prof_cod_entry.pack(padx=10, pady=5, fill="x")
        ctk.CTkButton(mod_frame, text="Incluir Modalidade", command=self.incluir_modalidade).pack(padx=10, pady=20)

        matricula = ctk.CTkScrollableFrame(cadastro_opts.tab("Matrícula"))
        matricula.pack(fill="both", expand=True)
        ctk.CTkLabel(matricula, text="Código da Matrícula:").pack(padx=10, pady=5, anchor="w")
        self.mat_cod = ctk.CTkEntry(matricula)
        self.mat_cod.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(matricula, text="Código do Aluno:").pack(padx=10, pady=5, anchor="w")
        self.mat_aluno_cod = ctk.CTkEntry(matricula)
        self.mat_aluno_cod.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(matricula, text="Código da Modalidade:").pack(padx=10, pady=5, anchor="w")
        self.mat_mod_cod = ctk.CTkEntry(matricula)
        self.mat_mod_cod.pack(padx=10, pady=5, fill="x")
        ctk.CTkLabel(matricula, text="Quantidade de Aulas:").pack(padx=10, pady=5, anchor="w")
        self.mat_aulas = ctk.CTkEntry(matricula)
        self.mat_aulas.pack(padx=10, pady=5, fill="x")
        ctk.CTkButton(matricula, text="Fazer Matrícula", command=self.incluir_matricula).pack(padx=10, pady=20)

    def consultas(self):
        consultas_tab = self.tab_view.tab("Consultas")

        input_frame = ctk.CTkFrame(consultas_tab)
        input_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(input_frame, text="Código:").pack(side="left", padx=5)
        self.consulta_codigo = ctk.CTkEntry(input_frame)
        self.consulta_codigo.pack(side="left", padx=5, expand=True, fill="x")

        button_frame = ctk.CTkScrollableFrame(consultas_tab, orientation="horizontal", height=60)
        button_frame.pack(padx=10, pady=5, fill="x")

        botoes_comandos = {
            "Cidade": self.consultar_cidade, "Aluno": self.consultar_aluno,
            "Professor": self.consultar_professor, "Modalidade": self.consultar_modalidade,
            "Matrícula": self.consultar_matricula,
        }

        for nome, comando in botoes_comandos.items():
            ctk.CTkButton(button_frame, text=f"Consultar {nome}", command=comando).pack(side="left", padx=5, pady=5)

        self.consulta_resultado = ctk.CTkTextbox(consultas_tab, width=760, height=380)
        self.consulta_resultado.pack(padx=10, pady=10, fill="both", expand=True)
        self.consulta_resultado.configure(state="disabled")

    def exclusoes(self):
        exclusoes_tab = self.tab_view.tab("Exclusões")

        input_frame = ctk.CTkFrame(exclusoes_tab)
        input_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(input_frame, text="Código para Excluir:").pack(side="left", padx=5)
        self.exclusao_codigo = ctk.CTkEntry(input_frame)
        self.exclusao_codigo.pack(side="left", padx=5, expand=True, fill="x")

        button_frame = ctk.CTkFrame(exclusoes_tab)
        button_frame.pack(padx=10, pady=20, fill="x")

        botoes_comandos = {
            "Cidade": self.excluir_cidade, "Aluno": self.excluir_aluno,
            "Professor": self.excluir_professor, "Modalidade": self.excluir_modalidade,
            "Matrícula": self.excluir_matricula,
        }

        for i, (nome, comando) in enumerate(botoes_comandos.items()):
            ctk.CTkButton(button_frame, text=f"Excluir {nome}", command=comando, fg_color="firebrick").grid(row=i, column=0, padx=10, pady=5, sticky="ew")

    def listagens(self):
        listagens_tab = self.tab_view.tab("Listagens")

        button_frame = ctk.CTkScrollableFrame(listagens_tab, orientation="horizontal", height=60)
        button_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkButton(button_frame, text="Listar Cidades", command=self.listar_cidades).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(button_frame, text="Listar Alunos", command=self.listar_alunos).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(button_frame, text="Listar Professores", command=self.listar_professores).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(button_frame, text="Listar Modalidades", command=self.listar_modalidades).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(button_frame, text="Listar Matrículas", command=self.listar_matriculas).pack(side="left", padx=5, pady=5)

        self.listagem = ctk.CTkTextbox(listagens_tab, width=760, height=430)
        self.listagem.pack(padx=10, pady=10, fill="both", expand=True)
        self.listagem.configure(state="disabled")

    def leitura_exaustiva(self, tipo_arvore, nome_tabela):
        self.listagem.configure(state="normal")
        self.listagem.delete("1.0", "end")

        todos_os_itens = self.arvores[tipo_arvore].percorrer()
        if not todos_os_itens:
            self.listagem.insert("1.0", f"Nenhum registro encontrado em {nome_tabela}.")
        else:
            texto_final = f"--- Listagem Exaustiva de {nome_tabela} ---\n\n"
            for item in todos_os_itens:
                texto_final += str(item) + "\n"
                texto_final += "-" * 30 + "\n"
            texto_final += f"\nTotal de {len(todos_os_itens)} registros."
            self.listagem.insert("1.0", texto_final)
        self.listagem.configure(state="disabled")

    def relatorios(self):
        relatorio = self.tab_view.tab("Relatórios")
        input_frame = ctk.CTkFrame(relatorio)
        input_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(input_frame, text="Cód. da Modalidade:").pack(side="left", padx=(10, 5), pady=10)
        self.relatorio_cod = ctk.CTkEntry(input_frame, width=150)
        self.relatorio_cod.pack(side="left", padx=5, pady=10)
        ctk.CTkButton(input_frame, text="Faturamento por Modalidade", command=self.relatorio_faturamento).pack(
            side="left", padx=(5, 10), pady=10)
        ctk.CTkButton(input_frame, text="Relatório Geral de Matrículas", command=self.relatorio_geral).pack(side="left", padx=(10, 10), pady=10)
        self.relatorio = ctk.CTkTextbox(relatorio, width=760, height=430)
        self.relatorio.pack(padx=10, pady=10, fill="both", expand=True)
        self.relatorio.configure(state="disabled")

# ------- Área da Cidade -------
    def incluir_cidade(self):
        try:
            cod_cidade = int(self.cidade_cod.get())
            descricao = self.cidade_desc.get()
            estado = self.cidade_uf.get()
            if not all([descricao, estado]):
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
                return
            if self.arvores['cidade'].buscar(cod_cidade):
                messagebox.showerror("Erro", "Já existe uma cidade com este código.")
                return

            nova_cidade = Cidade(cod_cidade, descricao, estado)
            self.arvores['cidade'].inserir(cod_cidade, nova_cidade)
            formato = lambda cid: f"{cid.codCidade},{cid.descricao},{cid.estado}\n"
            self.arvores['cidade'].salvar("Dados/cidades.txt", formato)
            messagebox.showinfo("Sucesso", "Cidade incluída com sucesso!")
            for entry in [self.cidade_cod, self.cidade_desc, self.cidade_uf]:
                entry.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Erro de Entrada", "O código da cidade deve ser um número inteiro.")

    def consultar_cidade(self):
        try:
            codigo_con = self.consulta_codigo.get()
            if not codigo_con:
                messagebox.showwarning("Aviso", "Por favor, digite um código para consultar.")
                return
            codigo = int(codigo_con)
            resultado = self.arvores['cidade'].buscar(codigo)

            self.consulta_resultado.configure(state="normal")
            self.consulta_resultado.delete("1.0", "end")
            if resultado:
                self.consulta_resultado.insert("1.0", str(resultado))
            else:
                self.consulta_resultado.insert("1.0", "Cidade não encontrada com este código.")
            self.consulta_resultado.configure(state="disabled")
        except ValueError:
            messagebox.showerror("Erro de Entrada", "O código deve ser um número inteiro.")

    def excluir_cidade(self):
        try:
            codigo_exc = self.exclusao_codigo.get()
            if not codigo_exc:
                messagebox.showwarning("Aviso", "Digite um código para excluir.")
                return
            codigo = int(codigo_exc)
            if self.arvores['cidade'].buscar(codigo) is None:
                messagebox.showerror("Erro", "Cidade não encontrada com este código.")
                return
            for aluno in self.arvores['aluno'].percorrer():
                if aluno.cidade.codCidade == codigo:
                    messagebox.showerror("Erro de Exclusão",
                                         f"A cidade não pode ser excluída, pois o aluno '{aluno.nome}' está cadastrado nela.")
                    return
            for prof in self.arvores['professor'].percorrer():
                if prof.cidade.codCidade == codigo:
                    messagebox.showerror("Erro de Exclusão",
                                         f"A cidade não pode ser excluída, pois o professor '{prof.nome}' está cadastrado nela.")
                    return
            if messagebox.askyesno("Confirmar Exclusão",
                                   f"Tem certeza que deseja excluir a cidade de código {codigo}?"):
                self.arvores['cidade'].remover(codigo)
                formato = lambda cid: f"{cid.codCidade},{cid.descricao},{cid.estado}\n"
                self.arvores['cidade'].salvar("Dados/cidades.txt", formato)
                messagebox.showinfo("Sucesso", "Cidade excluída com sucesso.")
                self.exclusao_codigo.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Erro de Entrada", "O código deve ser um número.")

    def listar_cidades(self):
        self.leitura_exaustiva("cidade", "Cidades")

# ------- Área do Aluno -------
    def incluir_aluno(self):
        try:
            cod_aluno = int(self.aluno_cod.get())
            nome = self.aluno_nome.get()
            data = self.aluno_data.get()
            peso = float(self.aluno_peso.get())
            altura = float(self.aluno_altura.get())
            cod_cidade = int(self.aluno_cidade_cod.get())

            if not all([nome, data]):
                messagebox.showerror("Erro", "Campos de texto não podem estar vazios.")
                return
            if self.arvores['aluno'].buscar(cod_aluno):
                messagebox.showerror("Erro", "Já existe um aluno com este código.")
                return
            cidade = self.arvores['cidade'].buscar(cod_cidade)
            if not cidade:
                messagebox.showerror("Erro", "Cidade não encontrada. Cadastre a cidade primeiro.")
                return
            novo_aluno = Aluno(cod_aluno, nome, data, peso, altura, cidade)
            self.arvores['aluno'].inserir(cod_aluno, novo_aluno)
            formato = lambda alu: f"{alu.codAluno},{alu.nome},{alu.data},{alu.peso},{alu.altura},{alu.cidade.codCidade}\n"
            self.arvores['aluno'].salvar("Dados/alunos.txt", formato)
            messagebox.showinfo("Sucesso", "Aluno incluído com sucesso!")
            for entry in [self.aluno_cod, self.aluno_nome, self.aluno_data, self.aluno_peso,
                          self.aluno_altura, self.aluno_cidade_cod]:
                entry.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Verifique se os códigos, peso e altura são números válidos.")

    def consultar_aluno(self):
        try:
            codigo_con = self.consulta_codigo.get()
            if not codigo_con:
                messagebox.showwarning("Aviso", "Por favor, digite um código para consultar.")
                return
            codigo = int(codigo_con)
            resultado = self.arvores['aluno'].buscar(codigo)

            self.consulta_resultado.configure(state="normal")
            self.consulta_resultado.delete("1.0", "end")

            if resultado:
                texto_resultado = str(resultado)
                imc_info = f"\n\nIMC: {resultado.calcular_imc():.2f} - Diagnóstico: {resultado.diagnostico_imc()}"
                texto_resultado += imc_info
                self.consulta_resultado.insert("1.0", texto_resultado)
            else:
                self.consulta_resultado.insert("1.0", "Aluno não encontrado com este código.")

            self.consulta_resultado.configure(state="disabled")
        except ValueError:
            messagebox.showerror("Erro de Entrada", "O código deve ser um número inteiro.")

    def excluir_aluno(self):
        try:
            codigo_exc = self.exclusao_codigo.get()
            if not codigo_exc:
                messagebox.showwarning("Aviso", "Digite um código para excluir.")
                return
            codigo = int(codigo_exc)
            if self.arvores['aluno'].buscar(codigo) is None:
                messagebox.showerror("Erro", "Aluno não encontrado com este código.")
                return
            for matricula in self.arvores['matricula'].percorrer():
                if matricula.cod_aluno.codAluno == codigo:
                    messagebox.showerror("Erro de Exclusão",
                                         f"O aluno não pode ser excluído, pois está na matrícula cód. {matricula.cod_Matricula}.")
                    return
            if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o aluno de código {codigo}?"):
                self.arvores['aluno'].remover(codigo)
                formato = lambda alu: f"{alu.codAluno},{alu.nome},{alu.data},{alu.peso},{alu.altura},{alu.cidade.codCidade}\n"
                self.arvores['aluno'].salvar("Dados/alunos.txt", formato)
                messagebox.showinfo("Sucesso", "Aluno excluído com sucesso.")
                self.exclusao_codigo.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Erro de Entrada", "O código deve ser um número.")

    def listar_alunos(self):
        self.leitura_exaustiva("aluno", "Alunos")

# ------- Área do Professor -------
    def incluir_professor(self):
        try:
            cod_professor = int(self.prof_cod.get())
            nome = self.prof_nome.get()
            endereco = self.prof_end.get()
            telefone = self.prof_tel.get()
            cod_cidade = int(self.prof_cidade_cod.get())

            if not all([nome, endereco, telefone]):
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
                return
            if self.arvores['professor'].buscar(cod_professor):
                messagebox.showerror("Erro", "Já existe um professor com este código.")
                return
            cidade = self.arvores['cidade'].buscar(cod_cidade)
            if not cidade:
                messagebox.showerror("Erro", "Cidade não encontrada. Cadastre a cidade primeiro.")
                return

            novo_professor = Professor(cod_professor, nome, endereco, telefone, cidade)
            self.arvores['professor'].inserir(cod_professor, novo_professor)
            formato = lambda \
                    prof: f"{prof.codProfessor},{prof.nome},{prof.endereco},{prof.telefone},{prof.cidade.codCidade}\n"
            self.arvores['professor'].salvar("Dados/professores.txt", formato)
            messagebox.showinfo("Sucesso", "Professor incluído com sucesso!")
            for entry in [self.prof_cod, self.prof_nome, self.prof_end, self.prof_tel, self.prof_cidade_cod]:
                entry.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Certifique-se que os códigos são números inteiros.")

    def consultar_professor(self):
        try:
            codigo_con = self.consulta_codigo.get()
            if not codigo_con:
                messagebox.showwarning("Aviso", "Por favor, digite um código para consultar.")
                return
            codigo = int(codigo_con)
            resultado = self.arvores['professor'].buscar(codigo)

            self.consulta_resultado.configure(state="normal")
            self.consulta_resultado.delete("1.0", "end")

            if resultado:
                self.consulta_resultado.insert("1.0", str(resultado))
            else:
                self.consulta_resultado.insert("1.0", "Professor não encontrado com este código.")

            self.consulta_resultado.configure(state="disabled")
        except ValueError:
            messagebox.showerror("Erro de Entrada", "O código deve ser um número inteiro.")

    def excluir_professor(self):
        try:
            codigo_exc = self.exclusao_codigo.get()
            if not codigo_exc:
                messagebox.showwarning("Aviso", "Digite um código para excluir.")
                return
            codigo = int(codigo_exc)

            if self.arvores['professor'].buscar(codigo) is None:
                messagebox.showerror("Erro", "Professor não encontrado com este código.")
                return
            for mod in self.arvores['modalidade'].percorrer():
                if mod.cod_professor.codProfessor == codigo:
                    messagebox.showerror("Erro de Exclusão",
                                         f"O professor não pode ser excluído, pois leciona a modalidade '{mod.desc_Modalidade}'.")
                    return
            if messagebox.askyesno("Confirmar Exclusão",
                                   f"Tem certeza que deseja excluir o professor de código {codigo}?"):
                self.arvores['professor'].remover(codigo)
                formato = lambda \
                        prof: f"{prof.codProfessor},{prof.nome},{prof.endereco},{prof.telefone},{prof.cidade.codCidade}\n"
                self.arvores['professor'].salvar("Dados/professores.txt", formato)
                messagebox.showinfo("Sucesso", "Professor excluído com sucesso.")
                self.exclusao_codigo.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Erro de Entrada", "O código deve ser um número.")

    def listar_professores(self):
        self.leitura_exaustiva("professor", "Professores")

# ------- Área da Modalidade -------
    def incluir_modalidade(self):
        try:
            cod_matricula = int(self.mat_cod.get())
            cod_aluno = int(self.mat_aluno_cod.get())
            cod_modalidade = int(self.mat_mod_cod.get())
            qtde_aulas = int(self.mat_aulas.get())

            if self.arvores['matricula'].buscar(cod_matricula):
                messagebox.showerror("Erro", "Já existe uma matrícula com este código.")
                return
            aluno = self.arvores['aluno'].buscar(cod_aluno)
            if not aluno:
                messagebox.showerror("Erro", "Aluno não encontrado.")
                return
            modalidade = self.arvores['modalidade'].buscar(cod_modalidade)
            if not modalidade:
                messagebox.showerror("Erro", "Modalidade não encontrada.")
                return
            if modalidade.totaAlunos >= modalidade.limiteAlunos:
                messagebox.showerror("Vagas Esgotadas",
                                     f"Não há mais vagas para a modalidade '{modalidade.desc_Modalidade}'.")
                return
            nova_matricula = Matricula(cod_matricula, aluno, modalidade, qtde_aulas)
            self.arvores['matricula'].inserir(cod_matricula, nova_matricula)

            modalidade.totaAlunos += 1
            formato_mod = lambda mod: f"{mod.cod_modalidade},{mod.desc_Modalidade},{mod.valorAula},{mod.limiteAlunos},{mod.totaAlunos},{mod.cod_professor.codProfessor}\n"
            self.arvores['modalidade'].salvar("Dados/modalidades.txt", formato_mod)

            formato_mat = lambda matri: f"{matri.cod_Matricula},{matri.qtdeAulas},{matri.cod_aluno.codAluno},{matri.cod_modalidade.cod_modalidade}\n"
            self.arvores['matricula'].salvar("Dados/matriculas.txt", formato_mat)

            valor_pago = nova_matricula.calcular_valor()
            messagebox.showinfo("Sucesso", f"Matrícula realizada com sucesso!\nValor a pagar: R${valor_pago:.2f}")

            for entry in [self.mat_cod, self.mat_aluno_cod, self.mat_mod_cod, self.mat_aulas]:
                entry.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Erro de Entrada. Todos os códigos e a quantidade de aulas devem ser números inteiros.")

    def consultar_modalidade(self):
        try:
            codigo_con = self.consulta_codigo.get()
            if not codigo_con:
                messagebox.showwarning("Aviso", "Por favor, digite um código para consultar.")
                return
            codigo = int(codigo_con)
            resultado = self.arvores['modalidade'].buscar(codigo)

            self.consulta_resultado.configure(state="normal")
            self.consulta_resultado.delete("1.0", "end")

            if resultado:
                self.consulta_resultado.insert("1.0", str(resultado))
            else:
                self.consulta_resultado.insert("1.0", "Modalidade não encontrada com este código.")
            self.consulta_resultado.configure(state="disabled")
        except ValueError:
            messagebox.showerror("Erro de Entrada", "O código deve ser um número inteiro.")

    def excluir_modalidade(self):
        try:
            codigo_str = self.exclusao_codigo.get()
            if not codigo_str:
                messagebox.showwarning("Aviso", "Digite um código para excluir.")
                return
            codigo = int(codigo_str)
            if self.arvores['modalidade'].buscar(codigo) is None:
                messagebox.showerror("Erro", "Modalidade não encontrada com este código.")
                return
            for matricula in self.arvores['matricula'].percorrer():
                if matricula.cod_modalidade.cod_modalidade == codigo:
                    messagebox.showerror("Erro de Exclusão",
                                         f"A modalidade não pode ser excluída, pois está na matrícula cód. {matricula.cod_Matricula}.")
                    return
            if messagebox.askyesno("Confirmar Exclusão",f"Tem certeza que deseja excluir a modalidade de código {codigo}?"):
                self.arvores['modalidade'].remover(codigo)
                formato = lambda \
                    mod: f"{mod.cod_modalidade},{mod.desc_Modalidade},{mod.valorAula},{mod.limiteAlunos},{mod.totaAlunos},{mod.cod_professor.codProfessor}\n"
                self.arvores['modalidade'].salvar("Dados/modalidades.txt", formato)
                messagebox.showinfo("Sucesso", "Modalidade excluída com sucesso.")
                self.exclusao_codigo.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Erro de Entrada", "O código deve ser um número.")

    def listar_modalidades(self):
        self.leitura_exaustiva("modalidade", "Modalidades")

# ------- Área da Matrícula -------
    def incluir_matricula(self):
        try:
            cod_matricula = int(self.mat_cod.get())
            cod_aluno = int(self.mat_aluno_cod.get())
            cod_modalidade = int(self.mat_mod_cod.get())
            qtde_aulas = int(self.mat_aulas.get())

            if self.arvores['matricula'].buscar(cod_matricula):
                messagebox.showerror("Erro", "Já existe uma matrícula com este código.")
                return
            aluno = self.arvores['aluno'].buscar(cod_aluno)
            if not aluno:
                messagebox.showerror("Erro", "Aluno não encontrado.")
                return
            modalidade = self.arvores['modalidade'].buscar(cod_modalidade)
            if not modalidade:
                messagebox.showerror("Erro", "Modalidade não encontrada.")
                return

            if modalidade.totaAlunos >= modalidade.limiteAlunos:
                messagebox.showerror("Vagas Esgotadas",f"Não há mais vagas para a modalidade '{modalidade.desc_Modalidade}'.")
                return

            nova_matricula = Matricula(cod_matricula, aluno, modalidade, qtde_aulas)
            self.arvores['matricula'].inserir(cod_matricula, nova_matricula)

            modalidade.totaAlunos += 1
            formato_mod = lambda mod: f"{mod.cod_modalidade},{mod.desc_Modalidade},{mod.valorAula},{mod.limiteAlunos},{mod.totaAlunos},{mod.cod_professor.codProfessor}\n"
            self.arvores['modalidade'].salvar("Dados/modalidades.txt", formato_mod)

            # Salva a nova matrícula
            formato_mat = lambda matri: f"{matri.cod_Matricula},{matri.qtdeAulas},{matri.cod_aluno.codAluno},{matri.cod_modalidade.cod_modalidade}\n"
            self.arvores['matricula'].salvar("Dados/matriculas.txt", formato_mat)
            valor_pago = nova_matricula.calcular_valor()
            messagebox.showinfo("Sucesso", f"Matrícula realizada com sucesso!\nValor a pagar: R${valor_pago:.2f}")

            for entry in [self.mat_cod, self.mat_aluno_cod, self.mat_mod_cod, self.mat_aulas]:
                entry.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Erro de Entrada. Todos os códigos e a quantidade de aulas devem ser números inteiros.")

    def consultar_matricula(self):
        try:
            codigo_con = self.consulta_codigo.get()
            if not codigo_con:
                messagebox.showwarning("Aviso", "Por favor, digite um código para consultar.")
                return
            codigo = int(codigo_con)
            resultado = self.arvores['matricula'].buscar(codigo)

            self.consulta_resultado.configure(state="normal")
            self.consulta_resultado.delete("1.0", "end")

            if resultado:
                self.consulta_resultado.insert("1.0", str(resultado))
            else:
                self.consulta_resultado.insert("1.0", "Matrícula não encontrada com este código.")

            self.consulta_resultado.configure(state="disabled")
        except ValueError:
            messagebox.showerror("Erro de Entrada", "O código deve ser um número inteiro.")

    def excluir_matricula(self):
        try:
            codigo_str = self.exclusao_codigo.get()
            if not codigo_str:
                messagebox.showwarning("Aviso", "Digite um código para excluir.")
                return
            codigo = int(codigo_str)

            matricula_para_excluir = self.arvores['matricula'].buscar(codigo)
            if matricula_para_excluir is None:
                messagebox.showerror("Erro", "Matrícula não encontrada com este código.")
                return

            if messagebox.askyesno("Confirmar Exclusão",
                                   f"Tem certeza que deseja excluir a matrícula de código {codigo}?"):
                modalidade = matricula_para_excluir.cod_modalidade
                if modalidade and modalidade.totaAlunos > 0:
                    modalidade.totaAlunos -= 1
                    formato_mod = lambda mod: f"{mod.cod_modalidade},{mod.desc_Modalidade},{mod.valorAula},{mod.limiteAlunos},{mod.totaAlunos},{mod.cod_professor.codProfessor}\n"
                    self.arvores['modalidade'].salvar("Dados/modalidades.txt", formato_mod)

                self.arvores['matricula'].remover(codigo)
                formato_matri = lambda matri: f"{matri.cod_Matricula},{matri.qtdeAulas},{matri.cod_aluno.codAluno},{matri.cod_modalidade.cod_modalidade}\n"
                self.arvores['matricula'].salvar("Dados/matriculas.txt", formato_matri)

                messagebox.showinfo("Sucesso", "Matrícula excluída com sucesso.")
                self.exclusao_codigo.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Erro de Entrada", "O código deve ser um número.")

    def listar_matriculas(self):
        self.leitura_exaustiva("matricula", "Matrículas")

# ------- Área de Relatorios -------
    def relatorio_faturamento(self):
        try:
            cod_rel = self.relatorio_cod.get()
            if not cod_rel:
                messagebox.showwarning("Aviso", "Por favor, digite o código da modalidade.")
                return

            cod_modalidade = int(cod_rel)
            modalidade = self.arvores['modalidade'].buscar(cod_modalidade)

            if modalidade is None:
                messagebox.showerror("Erro", "Modalidade não encontrada com este código.")
                return

            todas_as_matriculas = self.arvores['matricula'].percorrer()
            faturamento_total = 0.0
            alunos_na_modalidade = 0
            alunos_nomes = []

            for matricula in todas_as_matriculas:
                if matricula.cod_modalidade.cod_modalidade == cod_modalidade:
                    valor_pago_pelo_aluno = matricula.calcular_valor()
                    faturamento_total += valor_pago_pelo_aluno
                    alunos_na_modalidade += 1
                    alunos_nomes.append(f"- {matricula.cod_aluno.nome}")

            texto_relatorio = (
                f"--- Relatório de Faturamento por Modalidade ---\n\n"
                f"Descrição da Modalidade: {modalidade.desc_Modalidade}\n"
                f"Nome do Professor: {modalidade.cod_professor.nome}\n"
                f"Cidade do Professor: {modalidade.cod_professor.cidade.descricao} ({modalidade.cod_professor.cidade.estado})\n"
                f"---------------------------------------------\n"
                f"Total de Alunos Matriculados: {alunos_na_modalidade}\n"
                f"Valor Total Faturado: R${faturamento_total:.2f}\n"
                f"---------------------------------------------\n"
                f"Alunos na Modalidade:\n"
                f"{'\n'.join(alunos_nomes) if alunos_nomes else 'Nenhum aluno matriculado.'}"
            )

            self.relatorio.configure(state="normal")
            self.relatorio.delete("1.0", "end")
            self.relatorio.insert("1.0", texto_relatorio)
            self.relatorio.configure(state="disabled")

        except ValueError:
            messagebox.showerror("Erro de Entrada", "O código da modalidade deve ser um número inteiro.")

    def relatorio_geral(self):
        matriculas = self.arvores['matricula'].percorrer()
        self.relatorio.configure(state="normal")
        self.relatorio.delete("1.0", "end")

        if not matriculas:
            self.relatorio.insert("1.0", "Nenhuma matrícula encontrada para gerar o relatório.")
            self.relatorio.configure(state="disabled")
            return

        texto = "--- Relatório Geral de Matrículas ---\n\n"
        valor_total_geral = 0.0

        for m in matriculas:
            valor_aluno = m.calcular_valor()
            valor_total_geral += valor_aluno

            texto += f"Cód. Matrícula: {m.cod_Matricula}\n"
            texto += f"Aluno: {m.cod_aluno.nome} (Cidade: {m.cod_aluno.cidade.descricao})\n"
            texto += f"Modalidade: {m.cod_modalidade.desc_Modalidade}\n"
            texto += f"Professor: {m.cod_modalidade.cod_professor.nome}\n"
            texto += f"Valor a Pagar: R${valor_aluno:.2f}\n"
            texto += "-" * 40 + "\n"

        texto += f"\n--- TOTAIS ---\n"
        texto += f"Quantidade Total de Matrículas: {len(matriculas)}\n"
        texto += f"Valor Total Geral a ser Pago: R${valor_total_geral:.2f}"

        self.relatorio.insert("1.0", texto)
        self.relatorio.configure(state="disabled")

if __name__ == "__main__":
    os.makedirs("Dados", exist_ok=True)

    arvores = {
        "cidade": ArvoreBinaria(), "aluno": ArvoreBinaria(), "professor": ArvoreBinaria(),
        "modalidade": ArvoreBinaria(), "matricula": ArvoreBinaria()
    }

    carregar_dados("Dados/cidades.txt", arvores['cidade'], construtor_cidade)
    carregar_dados("Dados/professores.txt", arvores['professor'], construtor_professor, arvore_cidade=arvores['cidade'])
    carregar_dados("Dados/alunos.txt", arvores['aluno'], construtor_aluno, arvore_cidade=arvores['cidade'])
    carregar_dados("Dados/modalidades.txt", arvores['modalidade'], construtor_modalidade,
                   arvore_professor=arvores['professor'])
    carregar_dados("Dados/matriculas.txt", arvores['matricula'], construtor_matricula, arvore_aluno=arvores['aluno'],
                   arvore_modalidade=arvores['modalidade'])

    app = App(arvores)
    app.mainloop()