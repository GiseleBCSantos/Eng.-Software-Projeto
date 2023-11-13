from tkinter import *
from tkinter import ttk
import psycopg2

root = Tk()
#
# conexao = psycopg2.connect(database = 'Banco',
#                             host = 'localhost',
#                             user = 'postgres',
#                             password = 'postgres',
#                             port = '5432')
# print(conexao.info)
# print(conexao.status)

class Funcs():
    # Limpeza de telas:
    def limpa_tela_criar_conta(self):
        self.nome_entry.delete(0, END)
        self.cpf_entry.delete(0, END)
        self.rg_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.endereco_entry.delete(0, END)
    def limpa_tela_autenticacao(self):
        self.user_entry.delete(0, END)
        self.senha_entry.delete(0, END)
    def limpa_tela_senha_dep_inicial(self):
        self.inserir_senha_entry.delete(0, END)
        self.repetir_senha_entry.delete(0, END)





    # Ir/Voltar para páginas
    def abrir_janela_criarConta(self):
        self.frame_adicionarCliente()
        self.widgets_adicionarCliente()
    def abrir_autenticacao(self):
        self.frames_autenticacao()
        self.widgets_autenticacao()






    # Conexões BD
    def conecta_bd(self):
        self.conn = psycopg2.connect(database='Banco',
                                   host='localhost',
                                   user='postgres',
                                   password='postgres',
                                   port='5432')
        self.cursor = self.conn.cursor()
        print('Conectando ao banco de dados')
    def desconecta_bd(self):
        self.conn.close()






    # Criação da tabela clientes e contas no BD
    def criarClientes(self):

        self.conecta_bd()
        # Criar tabela
        self.cursor.execute('''
        create table if not exists clientes (
        cod_cliente serial primary key,
        nome_cliente varchar(40) not null,
        cpf varchar(18) not null unique,
        rg int not null,
        telefone varchar(20) not null,
        endereco varchar(50) not null
        )
        ''')
        self.conn.commit(); print('banco de dados criado')
        self.desconecta_bd()
    def criarContas(self):
        self.conecta_bd()

        self.cursor.execute('''
                create table if not exists contas (
                cod_conta serial primary key,
                cod_cliente int not null references clientes(cod_cliente),
                senha varchar(20) not null,
                saldo float not null default 0
                )
                ''')
        self.conn.commit();
        print('banco de dados criado')








    # Inserção dos dados de Clientes no BD
    def adicionarContas(self):
        self.senha_1 = self.inserir_senha_entry.get()
        self.senha_2 = self.repetir_senha_entry.get()

        if self.senha_1 == self.senha_2:
            self.senha_criacao = self.senha_1
        else:
            self.senhas_diferentes()


        self.conecta_bd()
        self.cursor.execute(f"""SELECT cod_cliente FROM clientes WHERE cpf = '{self.cpf}'""")
        cod_cliente = self.cursor.fetchall()[0][0]
        print(cod_cliente)
        self.cursor.execute(f"""INSERT INTO contas (cod_cliente, senha, saldo) VALUES({cod_cliente}, {self.senha_criacao}, {self.saldo})""")
        self.conn.commit()
        self.desconecta_bd()











    # Inserção dos dados de Conta Corrente no BD
    def add_cliente(self):

        self.nome = self.nome_entry.get()
        self.cpf = self.cpf_entry.get()
        self.rg = self.rg_entry.get()
        self.telefone = self.telefone_entry.get()
        self.endereco = self.endereco_entry.get()
        self.conecta_bd()

        if self.conn is not None:
            print("Conexão estabelecida com sucesso")
        else:
            print("Falha na conexão com o banco de dados")

        self.cursor.execute(
            """INSERT INTO clientes (nome_cliente, cpf, rg, telefone, endereco) VALUES (%s, %s, %s, %s, %s)""",
            (self.nome, self.cpf, self.rg, self.telefone, self.endereco)
        )
        self.conn.commit()
        self.limpa_tela_criar_conta()
        self.desconecta_bd()
        # self.select_lista()
        print('conta criada com sucesso')
        self.frame_continuar_criarConta()
        self.widgets_continuar_criarConta()








    # Autenticação do cliente na tela de entrada para acessar a conta
    def autenticar_cliente(self):
        self.user = self.user_entry.get()
        self.senha = self.senha_entry.get()
        self.conecta_bd()

        self.cursor.execute("""SELECT nome_cliente FROM clientes""")

        lista_de_nomes_usuario = self.cursor.fetchall()
        print(lista_de_nomes_usuario)
        self.conn.commit()
        for i in range(len(lista_de_nomes_usuario)):
            if self.user in lista_de_nomes_usuario[i]:
                self.cursor.execute(f"""SELECT cpf FROM clientes WHERE nome_cliente='{self.user}'""")
                self.conn.commit()
                senha_obtida = self.cursor.fetchall()
                print(senha_obtida)
                for i in range(len(senha_obtida)):
                    if self.senha in senha_obtida[i]:
                        print('senha digitada é igual no bd')
                        self.limpa_tela_autenticacao()
                        self.desconecta_bd()
                        ###
                        ### COLOCAR AQUI UM NOVO FRAME PRA QUANDO O USUARIO FOR AUTENTICADO









    # Para caso o cliente deseje fazer um depósito inicial ao criar a conta
    def confirmacao_deposito_inicial(self):
        self.deposito_inicial_lb = Label(self.frame_continuar_criarConta, text='R$')
        self.deposito_inicial_lb.place(relx=0.2, rely=0.65, relwidth=0.1, relheight=0.1)

        self.deposito_inicial_entry = Entry(self.frame_continuar_criarConta)
        self.deposito_inicial_entry.place(relx=0.35, rely=0.65, relwidth=0.3, relheight=0.1)

        self.confirmacao_deposito_inicial_bt = Button(self.frame_continuar_criarConta, text='Confirmar depósito', command=self.atualizar_saldo_inicial)
        self.confirmacao_deposito_inicial_bt.place(relx=0.35, rely=0.78, relwidth=0.3, relheight=0.1)
        print(self.saldo)










    # Para atualizar o saldo inicial do cliente para o inserido
    def atualizar_saldo_inicial(self):
        self.saldo = self.deposito_inicial_entry.get()
        print(self.saldo)






    # Caso senhas não sejam iguais
    def senhas_diferentes(self):
        self.senha_diferente_1_lb = Label(self.frame_continuar_criarConta, text="Senhas são diferentes.")
        self.senha_diferente_1_lb.place(relx=0.75, rely=0.1, relwidth=0.2, relheight=0.1)

        self.senha_diferente_2_lb = Label(self.frame_continuar_criarConta, text="Senhas são diferentes.")
        self.senha_diferente_2_lb.place(relx=0.75, rely=0.25, relwidth=0.2, relheight=0.1)

    # Criar tabela futuramente
    # def select_lista(self):
    #     self.listaCli.delete(*self.listaCli.get_children())
    #     self.conecta_bd()
    #     self.cursor.execute(""" SELECT nome_cliente, cpf, rg, telefone, endereco, saldo FROM clientes; """)
    #     lista = self.cursor.fetchall()
    #
    #     for i in lista:
    #         self.listaCli.insert("", END, values=i)
    #     self.desconecta_bd()

class Application(Funcs):
    def __init__(self):
        self.root = root
        self.tela()

        # Abrir tela de autenticação no inicio da aplicação
        self.frames_autenticacao()
        self.widgets_autenticacao()




        # Criação das tabelas no inicio da aplicação
        self.criarClientes()
        self.criarContas()

        root.mainloop()

    def tela(self):
        self.root.title('Tela inicial')
        self.root.configure(background='#1e3743')
        self.root.geometry('600x400')
        self.root.resizable(True, True)
        self.root.maxsize(width=988, height=788)
        self.root.minsize(width=400, height=300)





    # Criação do frame e dos widgets da autenticação
    def frames_autenticacao(self):
        self.root.title("Autenticação")
        self.frame_1 = Frame(self.root, bd=4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=2)
        self.frame_1.place(relx= 0.1, rely=0.1, relwidth=0.8, relheight=0.8)
    def widgets_autenticacao(self):
        ### Criação do botão limpar
        self.bt_autenticar = Button(self.frame_1, text='Autenticar', bg='#1e3743', fg='white', command=self.autenticar_cliente)
        self.bt_autenticar.place(relx=0.4, rely=0.7, relwidth=0.2, relheight=0.1)

        ### Criação do botão criar conta
        self.bt_criar = Button(self.frame_1, text='Criar conta', bg='#1e3743', fg='white', command=self.abrir_janela_criarConta)
        self.bt_criar.place(relx=0.2, rely=0.85, relwidth=0.2, relheight=0.1)

        ### Criação do botão alterar senha
        self.bt_mudarSenha = Button(self.frame_1, text='Esqueci minha senha', bg='#1e3743', fg='white')
        self.bt_mudarSenha.place(relx=0.6, rely=0.85, relwidth=0.35, relheight=0.1)

        ### Criação da label e input user
        self.lb_user = Label(self.frame_1, text='Nome:', bg='#1e3743', fg='white')
        self.lb_user.place(relx=0.2, rely=0.2, relwidth=0.2, relheight=0.1)

        self.user_entry = Entry(self.frame_1)
        self.user_entry.place(relx=0.45, rely=0.2, relwidth=0.3, relheight=0.1)

        ### Criação da label e input senha
        self.lb_senha = Label(self.frame_1, text='CPF:', bg='#1e3743', fg='white')
        self.lb_senha.place(relx=0.2, rely=0.4, relwidth=0.2, relheight=0.1)

        self.senha_entry = Entry(self.frame_1)
        self.senha_entry.place(relx=0.45, rely=0.4, relwidth=0.3, relheight=0.1)












    # Frame e Widgets Adicionar Cliente
    def frame_adicionarCliente(self):
        self.root.title('Criar Usuário')
        self.frame_criarConta = Frame(self.root, bd=3, bg='#dfe3ee', highlightbackground='#759fe6',
                                      highlightthickness=2)
        self.frame_criarConta.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
    def widgets_adicionarCliente(self):
        self.codigo = 1
        self.codigo += 1

        self.lb_nome = Label(self.frame_criarConta, text='Nome:')
        self.lb_nome.place(relx=0.2, rely=0.05, relwidth=0.2, relheight=0.1)
        self.nome_entry = Entry(self.frame_criarConta)
        self.nome_entry.place(relx=0.5, rely=0.05, relwidth=0.3, relheight=0.1)

        self.lb_cpf = Label(self.frame_criarConta, text='CPF:')
        self.lb_cpf.place(relx=0.2, rely=0.2, relwidth=0.2, relheight=0.1)
        self.cpf_entry = Entry(self.frame_criarConta)
        self.cpf_entry.place(relx=0.5, rely=0.2, relwidth=0.3, relheight=0.1)

        self.lb_rg = Label(self.frame_criarConta, text='RG:')
        self.lb_rg.place(relx=0.2, rely=0.35, relwidth=0.2, relheight=0.1)
        self.rg_entry = Entry(self.frame_criarConta)
        self.rg_entry.place(relx=0.5, rely=0.35, relwidth=0.3, relheight=0.1)

        self.lb_telefone = Label(self.frame_criarConta, text='Telefone:')
        self.lb_telefone.place(relx=0.2, rely=0.5, relwidth=0.2, relheight=0.1)
        self.telefone_entry = Entry(self.frame_criarConta)
        self.telefone_entry.place(relx=0.5, rely=0.5, relwidth=0.3, relheight=0.1)

        self.lb_endereco = Label(self.frame_criarConta, text='Endereço:')
        self.lb_endereco.place(relx=0.2, rely=0.65, relwidth=0.2, relheight=0.1)
        self.endereco_entry = Entry(self.frame_criarConta)
        self.endereco_entry.place(relx=0.5, rely=0.65, relwidth=0.45, relheight=0.1)

        self.bt_criarConta = Button(self.frame_criarConta, text='Avançar', command=self.add_cliente)
        self.bt_criarConta.place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.1)

        self.bt_voltar = Button(self.frame_criarConta, text='Voltar', command=self.abrir_autenticacao)
        self.bt_voltar.place(relx=0.01, rely=0.9, relwidth=0.2, relheight=0.1)








    # Frame e Widgets Criar Conta
    def frame_continuar_criarConta(self):
        self.frame1_continuar_criarConta = Frame(self.root, bd=4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=2)
        self.frame1_continuar_criarConta.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)
    def widgets_continuar_criarConta(self):
        self.root.title('Criar Conta')
        self.saldo = 0
        print(self.saldo)
        #botao voltar nao funciona
        self.bt_voltar_criarConta = Button(self.frame1_continuar_criarConta, text='Voltar', command=self.abrir_janela_criarConta)
        self.bt_voltar_criarConta.place(relx=0.01, rely=0.9, relwidth=0.2, relheight=0.1)

        self.inserir_senha_label = Label(self.frame1_continuar_criarConta, text='Insira uma senha:')
        self.inserir_senha_label.place(relx=0.2, rely=0.1, relwidth=0.25, relheight=0.1)
        self.inserir_senha_entry = Entry(self.frame1_continuar_criarConta)
        self.inserir_senha_entry.place(relx=0.5, rely=0.1, relwidth=0.2, relheight=0.1)


        self.repetir_senha_label = Label(self.frame1_continuar_criarConta, text='Repita a senha:')
        self.repetir_senha_label.place(relx=0.2, rely=0.25, relwidth=0.2, relheight=0.1)
        self.repetir_senha_entry = Entry(self.frame1_continuar_criarConta)
        self.repetir_senha_entry.place(relx=0.5, rely=0.25, relwidth=0.2, relheight=0.1)

        self.deposito_inicial_label = Label(self.frame1_continuar_criarConta, text='Deseja realizar um depósito inicial?')
        self.deposito_inicial_label.place(relx=0.4, rely=0.4, relwidth=0.45, relheight=0.1)
        self.deposito_inicial_confirmacao_sim_bt = Button(self.frame1_continuar_criarConta, text='Sim', command=self.confirmacao_deposito_inicial)
        self.deposito_inicial_confirmacao_sim_bt.place(relx=0.3, rely=0.52, relwidth=0.1, relheight=0.1)
        self.deposito_inicial_confirmacao_nao_bt = Button(self.frame1_continuar_criarConta, text='Não')
        self.deposito_inicial_confirmacao_nao_bt.place(relx=0.55, rely=0.52, relwidth=0.1, relheight=0.1)


        self.criar_conta_bt = Button(self.frame1_continuar_criarConta, text='Deseja criar sua conta no banco agora?', command=self.adicionarContas)
        self.criar_conta_bt.place(relx=0.35, rely=0.9, relwidth=0.5, relheight=0.1)

        # if self.inserir_senha_entry.get() != None:
        #     self.senha = self.inserir_senha_entry.get()
        #     print(self.senha)
        #     self.bt_criarContaBancaria = Button(self.frame1_continuar_criarConta, text='Criar Conta no Banco', command=self.voltar_autenticacao)
        #     self.bt_criarContaBancaria.place(relx=0.35, rely=0.89, relwidth=0.3, relheight=0.1)




    # def lista_frame2(self):
    #     self.listaCli = ttk.Treeview(self.frame_2, height=3, columns=('col1', 'col2', 'col3', 'col4'))
    #     self.listaCli.heading('#0', text='')
    #     self.listaCli.heading('#1', text='Nome')
    #     self.listaCli.heading('#2', text='CPF')
    #     self.listaCli.heading('#3', text='RG')
    #     self.listaCli.heading('#4', text='Telefone')
    #     self.listaCli.heading('#5', text='Endereco')
    #
    #     self.listaCli.column('#0', width=1)
    #     self.listaCli.column('#1', width=50)
    #     self.listaCli.column('#2', width=200)
    #     self.listaCli.column('#3', width=125)
    #     self.listaCli.column('#4', width=125)
    #     self.listaCli.column('#5', width=125)
    #
    #     self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)
    #
    #     self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
    #     self.listaCli.configure(yscroll= self.scroolLista.set)
    #     self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)












Application()
