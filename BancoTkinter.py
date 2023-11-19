from tkinter import *
from tkinter import ttk
import psycopg2
#alteracoes

root = Tk()

class Funcs():
    # Limpeza de telas:
    def limpa_tela_criar_conta(self):
        self.nome_entry.delete(0, END)
        self.cpf_entry.delete(0, END)
        self.rg_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.endereco_entry.delete(0, END)
    def limpa_tela_autenticacao(self):
        self.cpf_entry.delete(0, END)
        self.senha_entry.delete(0, END)
    def limpa_tela_senha_dep_inicial(self):
        self.inserir_senha_entry.delete(0, END)
        self.repetir_senha_entry.delete(0, END)

    def limpa_entry_deposito(self):
        self.deposito_entry.delete(0, END)

    def limpa_tela_areaPix(self):
        self.chavePix_alvo_entry.delete(0, END)
        self.valor_transferido_entry.delete(0, END)






    # Ir/Voltar para páginas
    def abrir_janela_criarConta(self):
        self.frame_adicionarCliente()
        self.widgets_adicionarCliente()

        self.frame_1.destroy()

    def abrir_janela_adicionarCliente(self):
        self.frames_continuar_criarConta()
        self.widgets_continuar_criarConta()

        self.frame_criarConta.destroy()


    def abrir_autenticacao(self):
        self.frames_autenticacao()
        self.widgets_autenticacao()

    def abrir_tela_inicial_conta(self):
        self.frame_conta()
        self.widgets_conta()

        self.frame_1.destroy()

    def abrir_areaPix(self):
        self.frame_areaPix()
        self.widgets_areaPix()

        self.frames_conta.destroy()



    def tela_inicial_conta_para_autenticacao(self):
        self.frames_conta.destroy()
        self.abrir_autenticacao()

    def areaPix_para_tela_inicial_conta(self):
        self.frame_areaPix1.destroy()
        self.frame_conta()
        self.widgets_conta()







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
                saldo float not null default 0,
                chave_pix varchar(20)
                )
                ''')
        self.conn.commit();
        print('banco de dados criado')








    # Inserção dos dados de Clientes no BD
    def adicionarContas(self):
        self.senha_1 = self.inserir_senha_entry.get()
        self.senha_2 = self.repetir_senha_entry.get()
        print(self.senha_1)
        print(self.senha_2)

        if self.senha_1 == self.senha_2:
            self.senha_criacao = self.senha_1
        else:
            self.senhas_diferentes()


        self.conecta_bd()
        self.cursor.execute(f"""SELECT cod_cliente FROM clientes WHERE cpf = '{self.cpf}'""")
        cod_cliente = self.cursor.fetchall()[0][0]
        print(cod_cliente)
        self.cursor.execute(f"""INSERT INTO contas (cod_cliente, senha, saldo) VALUES({cod_cliente}, '{self.senha_criacao}', {self.saldo})""")
        self.conn.commit()
        self.desconecta_bd()

        self.frame_continuar_criarConta.destroy()
        self.abrir_autenticacao()











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

        self.abrir_janela_adicionarCliente()
        # self.frame_continuar_criarConta()
        # self.widgets_continuar_criarConta()








    # Autenticação do cliente na tela de entrada para acessar a conta
    def autenticar_cliente(self):
        self.cpf = self.cpf_entry.get()
        self.senha = self.senha_entry.get()

        self.conecta_bd()

        self.cursor.execute("""SELECT cpf FROM clientes""")
        lista_de_cpf_usuarios = self.cursor.fetchall()
        self.conn.commit()
        print(lista_de_cpf_usuarios)


        self.cursor.execute(f"""SELECT cod_cliente FROM clientes WHERE cpf='{self.cpf}'""")
        self.conn.commit()
        try:
            lista_cod_cliente = self.cursor.fetchall()[0]
            cod_cliente = lista_cod_cliente[0]
            print('Len lista cod_cliente', len(lista_cod_cliente))

            if len(lista_cod_cliente) == 1:
                print('Codigo cliente: ', cod_cliente)

                # self.conn.commit()

                for i in range(len(lista_de_cpf_usuarios)):
                    if self.cpf in lista_de_cpf_usuarios[i]:
                        self.cursor.execute(f"""SELECT senha FROM contas WHERE cod_cliente='{cod_cliente}'""")
                        self.conn.commit()
                        senha_obtida = self.cursor.fetchall()
                        print(senha_obtida)
                        if len(senha_obtida) < 1:



                            self.sem_senha_lb = Label(self.frame_1, text='Usuário não possui senha!', bg='red')
                            self.sem_senha_lb.place(relx=0.4, rely=0.57, relwidth=0.3, relheight=0.08)

                            print('Senha: ',senha_obtida)

                        else:
                            senha_obtida = senha_obtida[0][0]
                            print(senha_obtida)
                            if self.senha == senha_obtida:

                                print('senha digitada é igual no bd')
                                self.limpa_tela_autenticacao()
                                #abrir frame tela inicial

                                self.cursor.execute(f"""SELECT * FROM clientes cl, contas c WHERE cl.cod_cliente=c.cod_cliente and cpf='{self.cpf}' and senha='{self.senha}'""")
                                self.conn.commit()
                                lista_dados_gerais_cliente_conta = self.cursor.fetchall()[0]
                                print(lista_dados_gerais_cliente_conta)
                                self.cliente_conta_cod_cliente, self.cliente_conta_nome_cliente, self.cliente_conta_cpf, self.cliente_conta_rg, self.cliente_conta_telefone, self.cliente_conta_endereco, self.cliente_conta_cod_conta, self.cliente_conta_cod_cliente, self.cliente_conta_senha, self.cliente_conta_saldo, self.cliente_conta_chave_pix = lista_dados_gerais_cliente_conta

                                print(f"Nome: {self.cliente_conta_nome_cliente}\nSaldo: {self.cliente_conta_saldo}")
                                self.desconecta_bd()

                                self.abrir_tela_inicial_conta()
                            else:

                                self.senha_errada_lb = Label(self.frame_1, text='Senha incorreta!', bg='red')
                                self.senha_errada_lb.place(relx=0.4, rely=0.57, relwidth=0.2, relheight=0.08)
        except:
            print('Cliente não encontrado.')
            self.limpa_tela_autenticacao()

            self.usuario_errado_lb = Label(self.frame_1, text='Usuário não encontrado!', bg='red')
            self.usuario_errado_lb.place(relx=0.35, rely=0.57, relwidth=0.3, relheight=0.08)

        # else:
        #     print('Cliente não encontrado.')
        #     self.limpa_tela_autenticacao()
        #
        #     self.usuario_errado_lb = Label(self.frame_1, text='Usuário não encontrado!', bg='red')
        #     self.usuario_errado_lb.place(relx=0.4, rely=0.57, relwidth=0.3, relheight=0.08)














    # Para caso o cliente deseje fazer um depósito inicial ao criar a conta
    def confirmacao_deposito_inicial(self):
        self.deposito_inicial_lb = Label(self.frame_continuar_criarConta, text='R$')
        self.deposito_inicial_lb.place(relx=0.375, rely=0.65, relwidth=0.05, relheight=0.1)

        self.deposito_inicial_entry = Entry(self.frame_continuar_criarConta)
        self.deposito_inicial_entry.place(relx=0.425, rely=0.65, relwidth=0.2, relheight=0.1)

        self.confirmacao_deposito_inicial_bt = Button(self.frame_continuar_criarConta, text='Confirmar depósito', command=self.atualizar_saldo_inicial)
        self.confirmacao_deposito_inicial_bt.place(relx=0.35, rely=0.78, relwidth=0.3, relheight=0.1)
        print(self.saldo)










    # Para atualizar o saldo inicial do cliente para o inserido
    def atualizar_saldo_inicial(self):
        self.saldo = self.deposito_inicial_entry.get()
        print(self.saldo)






    # Caso senhas não sejam iguais
    def senhas_diferentes(self):


        self.senha_diferente_1_lb = Label(self.frame_continuar_criarConta, text='Senhas são diferentes.', bg='red')
        self.senha_diferente_1_lb.place(relx=0.71, rely=0.1, relwidth=0.28, relheight=0.1)

        self.senha_diferente_2_lb = Label(self.frame_continuar_criarConta, text="Senhas são diferentes.", bg='red')
        self.senha_diferente_2_lb.place(relx=0.71, rely=0.25, relwidth=0.28, relheight=0.1)

        self.limpa_tela_senha_dep_inicial()

    #Botoes para depositar no frame conta
    def depositar_dinheiro(self):
        self.deposito_label = Label(self.frames_conta, text='R$')
        self.deposito_label.place(relx=0.35, rely=0.25, relwidth=0.05, relheight=0.1)

        self.deposito_entry = Entry(self.frames_conta)
        self.deposito_entry.place(relx=0.4, rely=0.25, relwidth=0.2, relheight=0.1)

        self.ok_deposito = Button(self.frames_conta, text="OK", command=self.depositar_dinheiro2)
        self.ok_deposito.place(relx=0.65, rely=0.25, relwidth=0.1, relheight=0.1)
    def depositar_dinheiro2(self):

        deposito = int(self.deposito_entry.get())
        print(deposito)

        self.conecta_bd()
        self.cursor.execute(f"""UPDATE contas SET saldo = saldo+{deposito} WHERE cod_cliente={self.cliente_conta_cod_cliente}""")
        self.conn.commit()
        self.desconecta_bd()
        self.cliente_conta_saldo += deposito

        self.saldo_lb.destroy()

        self.saldo_lb = Label(self.frames_conta, text=f"Saldo atual: R${self.cliente_conta_saldo:.2f}")
        self.saldo_lb.place(relx=0.375, rely=0.12, relwidth=0.25, relheight=0.1)

        self.limpa_entry_deposito()







    # Comando para abrir campo de digitar chave pix
    def campos_inserir_chavePix(self):
        self.insira_chavePix_lb = Label(self.frame_areaPix1, text='Insira a chave pix que deseja adicionar:')
        self.insira_chavePix_lb.place(relx=0.02, rely=0.29, relwidth=0.4, relheight=0.1)

        self.insira_chavePix_entry = Entry(self.frame_areaPix1)
        self.insira_chavePix_entry.place(relx=0.43, rely=0.29, relwidth=0.4, relheight=0.1)

        self.chavePix_bt = Button(self.frame_areaPix1, text='Confirmar', command=self.inserir_chavePix_criada)
        self.chavePix_bt.place(relx=0.85, rely=0.29, relwidth=0.14, relheight=0.1)

    def inserir_chavePix_criada(self):
        self.cliente_conta_chave_pix = self.insira_chavePix_entry.get()

        self.conecta_bd()
        self.cursor.execute(
            f"""UPDATE contas SET chave_pix = '{self.cliente_conta_chave_pix}' WHERE cod_cliente={self.cliente_conta_cod_cliente}"""
        )
        self.conn.commit()
        self.desconecta_bd()

        self.frame_areaPix1.destroy()
        self.abrir_areaPix()



    # Transferencia via Pix
    def transferir_viaPix(self):
        self.chavePix_alvo_lb = Label(self.frame_areaPix1, text='Insira a chave Pix:')
        self.chavePix_alvo_lb.place(relx=0.2, rely=0.4, relwidth=0.2, relheight=0.09)

        self.chavePix_alvo_entry = Entry(self.frame_areaPix1)
        self.chavePix_alvo_entry.place(relx=0.45, rely=0.4, relwidth=0.3, relheight=0.09)

        self.valor_transferido_lb = Label(self.frame_areaPix1, text='Insira o valor a ser transferido:')
        self.valor_transferido_lb.place(relx=0.2, rely=0.55, relwidth=0.32, relheight=0.09)

        self.valor_transferido_entry = Entry(self.frame_areaPix1)
        self.valor_transferido_entry.place(relx=0.55, rely=0.55, relwidth=0.2, relheight=0.09)


        self.realizar_transferenciaPix = Button(self.frame_areaPix1, text='Confirmar transferência', command=self.transferir_viaPix2)
        self.realizar_transferenciaPix.place(relx=0.35, rely=0.7, relwidth=0.3, relheight=0.09)


    def transferir_viaPix2(self):
        self.chavePix_alvo = self.chavePix_alvo_entry.get()
        self.valor_transferido = int(self.valor_transferido_entry.get())

        self.conecta_bd()

        self.cursor.execute("""SELECT chave_pix FROM contas""")
        self.conn.commit()
        lista_de_chaves_pix = self.cursor.fetchall()
        lista_de_chaves_pix_2 = []
        print(lista_de_chaves_pix)

        self.desconecta_bd()

        for i in lista_de_chaves_pix:
            lista_de_chaves_pix_2.append(i[0])

        if self.chavePix_alvo in lista_de_chaves_pix_2:
            print('Está aqui!')
            if self.valor_transferido <= self.cliente_conta_saldo:
                self.conecta_bd()

                self.cursor.execute(f"""UPDATE contas SET saldo = saldo + {self.valor_transferido} WHERE chave_pix='{self.chavePix_alvo}'""")
                self.conn.commit()

                self.cursor.execute(f"""UPDATE contas SET saldo = saldo - {self.valor_transferido} WHERE cod_cliente='{self.cliente_conta_cod_cliente}'""")
                self.conn.commit()
                self.desconecta_bd()

                self.transferencia_realizada_com_sucesso_lb = Label(self.frame_areaPix1, text='Transferência realizada com sucesso!', bg='green')
                self.transferencia_realizada_com_sucesso_lb.place(relx=0.3, rely=0.9, relwidth=0.4, relheight=0.08)

                self.cliente_conta_saldo -= self.valor_transferido
                self.saldo_lb = Label(self.frames_conta, text=f"Saldo atual: R${self.cliente_conta_saldo:.2f}")
                self.saldo_lb.place(relx=0.375, rely=0.12, relwidth=0.25, relheight=0.1)
            else:
                self.dinheiro_insuficiente_lb = Label(self.frame_areaPix1, text='Saldo insuficiente!', bg='red')
                self.dinheiro_insuficiente_lb.place(relx=0.35, rely=0.9, relwidth=0.3, relheight=0.08)

        else:
            self.dinheiro_insuficiente_lb = Label(self.frame_areaPix1, text='Chave Pix não encontrada!', bg='red')
            self.dinheiro_insuficiente_lb.place(relx=0.35, rely=0.9, relwidth=0.4, relheight=0.08)

        self.limpa_tela_areaPix()





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
        self.lb_cpf = Label(self.frame_1, text='CPF:', bg='#1e3743', fg='white')
        self.lb_cpf.place(relx=0.2, rely=0.2, relwidth=0.2, relheight=0.1)

        self.cpf_entry = Entry(self.frame_1)
        self.cpf_entry.place(relx=0.45, rely=0.2, relwidth=0.3, relheight=0.1)

        ### Criação da label e input senha
        self.lb_senha = Label(self.frame_1, text='Senha:', bg='#1e3743', fg='white')
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
    def frames_continuar_criarConta(self):
        self.frame_continuar_criarConta = Frame(self.root, bd=4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=2)
        self.frame_continuar_criarConta.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)
    def widgets_continuar_criarConta(self):
        self.root.title('Criar Conta')
        self.saldo = 0
        print(f'Saldo: {self.saldo}')

        self.inserir_senha_label = Label(self.frame_continuar_criarConta, text='Insira uma senha:')
        self.inserir_senha_label.place(relx=0.2, rely=0.1, relwidth=0.25, relheight=0.1)
        self.inserir_senha_entry = Entry(self.frame_continuar_criarConta)
        self.inserir_senha_entry.place(relx=0.5, rely=0.1, relwidth=0.2, relheight=0.1)


        self.repetir_senha_label = Label(self.frame_continuar_criarConta, text='Repita a senha:')
        self.repetir_senha_label.place(relx=0.2, rely=0.25, relwidth=0.2, relheight=0.1)
        self.repetir_senha_entry = Entry(self.frame_continuar_criarConta)
        self.repetir_senha_entry.place(relx=0.5, rely=0.25, relwidth=0.2, relheight=0.1)


        self.deposito_inicial_label = Label(self.frame_continuar_criarConta, text='Deseja realizar um depósito inicial?')
        self.deposito_inicial_label.place(relx=0.3, rely=0.4, relwidth=0.45, relheight=0.1)
        self.deposito_inicial_confirmacao_sim_bt = Button(self.frame_continuar_criarConta, text='Sim', command=self.confirmacao_deposito_inicial)
        self.deposito_inicial_confirmacao_sim_bt.place(relx=0.45, rely=0.52, relwidth=0.1, relheight=0.1)



        self.criar_conta_bt = Button(self.frame_continuar_criarConta, text='Deseja criar sua conta no banco agora?', command=self.adicionarContas)
        self.criar_conta_bt.place(relx=0.25, rely=0.9, relwidth=0.5, relheight=0.1)




    # Frame e Widgets Tela Inicial Conta
    def frame_conta(self):
        self.frames_conta = Frame(self.root, bd=4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=2)
        self.frames_conta.place(relx= 0.06, rely=0.06, relwidth=0.86, relheight=0.86)

    def widgets_conta(self):
        self.root.title('Tela inicial')

        self.bem_vindo_lb = Label(self.frames_conta, text=f'Bem vindo {self.cliente_conta_nome_cliente}')
        self.bem_vindo_lb.place(relx=0.25, rely=0.01, relwidth=0.5, relheight=0.08)

        self.saldo_lb = Label(self.frames_conta, text=f"Saldo atual: R${self.cliente_conta_saldo:.2f}")
        self.saldo_lb.place(relx=0.375, rely=0.12, relwidth= 0.25, relheight=0.1)

        self.depositar_bt = Button(self.frames_conta, text='Depositar', command=self.depositar_dinheiro)
        self.depositar_bt.place(relx=0.1, rely=0.25, relwidth=0.2, relheight=0.1)

        self.area_pix_bt = Button(self.frames_conta, text='Área Pix', command=self.abrir_areaPix)
        self.area_pix_bt.place(relx=0.43, rely=0.4, relwidth=0.15, relheight=0.1)

        self.solicitar_emprestimo_bt = Button(self.frames_conta, text='Solicitar empréstimo')
        self.solicitar_emprestimo_bt.place(relx=0.35, rely=0.55, relwidth=0.3, relheight=0.1)

        self.depositar_poupanca_bt = Button(self.frames_conta, text='Depositar poupança')
        self.depositar_poupanca_bt.place(relx=0.35, rely=0.7, relwidth=0.3, relheight=0.1)

        self.voltar_autenticacao_bt = Button(self.frames_conta, text='Voltar', command=self.tela_inicial_conta_para_autenticacao)
        self.voltar_autenticacao_bt.place(relx=0.01, rely=0.9, relwidth=0.15, relheight=0.1)




    # Frame e Widgets Area Pix
    def frame_areaPix(self):
        self.frame_areaPix1 = Frame(self.root, bd=4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=2)
        self.frame_areaPix1.place(relx= 0.04, rely=0.04, relwidth=0.92, relheight=0.92)
    def widgets_areaPix(self):
        self.root.title('Área Pix')

        self.voltar_autenticacao_bt = Button(self.frame_areaPix1, text='Voltar', command=self.areaPix_para_tela_inicial_conta)
        self.voltar_autenticacao_bt.place(relx=0.01, rely=0.9, relwidth=0.15, relheight=0.1)
        print(self.cliente_conta_chave_pix)

        if self.cliente_conta_chave_pix != None:
            self.chave_pix_ativa_lb = Label(self.frame_areaPix1, text=f'Chave pix ativa: {self.cliente_conta_chave_pix}')
            self.chave_pix_ativa_lb.place(relx=0.2, rely=0.05, relwidth=0.6, relheight=0.1)

            self.transferencia_viaPix_lb = Label(self.frame_areaPix1, text='Dejesa fazer uma transferencia via pix?')
            self.transferencia_viaPix_lb.place(relx=0.2, rely=0.2, relwidth=0.4, relheight=0.09)

            self.transferencia_viaPix_bt = Button(self.frame_areaPix1, text='Sim', command=self.transferir_viaPix)
            self.transferencia_viaPix_bt.place(relx=0.7, rely=0.2, relwidth=0.1, relheight=0.09)


        else:
            self.sem_chave_pix_ativa_lb = Label(self.frame_areaPix1, text=f'Você não possui chave pix ativa. Deseja adicionar uma para poder receber transferências via pix?')
            self.sem_chave_pix_ativa_lb.place(relx=0, rely=0.05, relwidth=1, relheight=0.1)

            self.confirmacao_criacao_chavePix_bt = Button(self.frame_areaPix1, text='Sim', command=self.campos_inserir_chavePix)
            self.confirmacao_criacao_chavePix_bt.place(relx=0.4, rely=0.2, relwidth=0.2, relheight=0.07)




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
