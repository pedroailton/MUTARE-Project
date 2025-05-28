from colorama import init, Fore 
#para instalação: pip install colorama bcrypt
#init permite a troca de cores no terminal e o Fore habilita 
#Fore: permite definir cores como Fore.YELLOW, Fore.RED, etc.

import sys
#usado em input_senha_asteriscos() para Unix.

import os
# Detecta o SO -Sistema Operacional (os.name) e executa comandos (os.system).

import time
#Controle de tempo e delays.
#Faz pausas com time.sleep() e mede tempo.
#Usado em: mensagens de erro, sucesso e carregamento.

import bcrypt
"""
Usa salt para diferenciar duas senhas iguais criptografadas no banco de dados
No código:
bcrypt.hashpw() para gerar senha criptografada.
bcrypt.checkpw() para validar senha no login.
📍 Usado em: tela_cadastro(), tela_login(), atualizar_senha(), excluir_conta().
"""

from datetime import datetime, timedelta, date
"""
No código:
datetime.strptime() para converter texto em data.
datetime.now() para registrar criação de hábitos.
date.today() para comparação com progresso atual.
timedelta pode ser usado para calcular diferenças de dias.
Usado em: funções de hábitos (inserir_habito, progresso), mascote, etc.
"""

import re #biblioteca para Regular Expression
"""
Função:
Expressões regulares (regex) para verificar padrões de texto.
No código:
re.match(r'^[A-Za-z0-9 ]+$', nome) valida se o nome do hábito tem apenas letras, números e espaços.
Usado em: inserir_habito().
"""

import sqlite3 
"""
Função:
Interface com o banco de dados SQLite.
Permite criar tabelas, inserir e consultar dados.
No código:
sqlite3.connect('Mutare.db'): conecta ao banco.
cursor.execute(): executa comandos SQL.
conn.commit(): salva mudanças.
cursor.fetchone(), cursor.fetchall() para ler dados.
Usado em: quase todas as funções que envolvem dados do usuário e hábitos.
"""


init(autoreset=True) #reseta a cor automaticamente após cada print()

# Conexão com o SQLite
conn = sqlite3.connect('Mutare.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_at DATE NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL, 
        frequency TEXT,
        motivation TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS habit_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        date DATE NOT NULL,
        start_date DATE,
        end_date DATE,
        status TEXT NOT NULL,
        FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
    )
''')

conn.commit()

# Verifica domínio do e-mail
def email_valido(email):
    '''Define os domínios de E-mail válidos para o cadastro no Mutare.
    '''
    return email.endswith('@gmail.com') or email.endswith('@ufrpe.br')

# Validação da senha
def validar_senha(senha):
    '''Valida uma senha de acordo com critérios de comprimento e presença de número.
    A senha deve ter entre 4 e 8 caracteres, conter pelo menos um número e uma letra maiúscula.
    Args:
        senha (str): A senha a ser validada.
    Returns:
        str: Uma mensagem indicando se a senha é válida ou qual critério não foi atendido.'''
    
    comprimento_minimo = 4
    comprimento_maximo = 8

    if len(senha) < comprimento_minimo:
        return f"A senha deve ter pelo menos {comprimento_minimo} caracteres."
    elif len(senha) > comprimento_maximo:
        return f"A senha não pode ter mais que {comprimento_maximo} caracteres."
    elif not any(char.isdigit() for char in senha):
        return "A senha deve conter pelo menos um número."
    elif not any(char.isupper() for char in senha):
        return "A senha deve conter pelo menos uma letra maiúscula."
    else:
        return "válida"

#Função senha de asteriscos 
if os.name == 'nt':
    import msvcrt
else:
    import tty
    import termios
def input_senha_asteriscos(prompt='Senha: '):
    '''Lê a senha do usuário ocultando os caracteres com asteriscos (*).
    Funciona em sistemas Windows e Unix.
    Args:
        prompt (str): Texto exibido antes da digitação. Padrão é 'Senha: '.
    Returns:
        str: A senha digitada pelo usuário.'''
    
    print(prompt, end='', flush=True)
    senha = ''
    
    if os.name == 'nt':
        while True:
            char = msvcrt.getch()
            if char in(b'\r', b'\n'):
                print()
                break
            elif char == b'\x08':
                if len(senha)>0:
                    senha = senha[:-1]
                    print('\b \b', end='', flush=True)
            elif char == b'\x03':
                raise KeyboardInterrupt
            else:
                try:
                    char_dec = char.decode('utf-8')
                    senha += char_dec
                    print(Fore.YELLOW + '*', end='', flush=True)
                except UnicodeDecodeError:
                    pass
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                char = sys.stdin.read(1)
                if char in ('\r', '\n'):
                    print()
                    break
                elif char == '\x7f':
                    if len(senha)>0:
                        senha = senha[:-1]
                        print('\b \b', end='', flush=True)
                elif char == '\x03':
                    raise KeyboardInterrupt
                else:
                    senha += char
                    print(Fore.YELLOW + '*', end='', flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return senha

#Limpar tela
def limpar_tela():
    '''Limpa o terminal, independente do sistema operacional.
    Usa 'cls' no Windows e 'clear' no Linux/MacOS.'''
    os.system('cls' if os.name == 'nt' else 'clear')

#Tela de Menu de login ou cadastro
def menu_log_cad():
    '''Exibe um menu do sistema Mutare com opções de login e cadastro.
    Direciona o usuário para a tela de login ou cadastro conforme a escolha.
    Em caso de entrada inválida, exibe uma mensagem de erro e recarrega o menu.'''

    while True: #ciclo sem fim
        limpar_tela() #limpa tela a cada ciclo
        print(Fore.WHITE + '\n=== Bem-vindo ao Mutare! ===')
        print(Fore.WHITE + 'Escolha uma opção')
        print(Fore.CYAN + '[1] Login')
        print(Fore.CYAN + '[2] Cadastro')

        escolha = input(Fore.YELLOW + 'Digite o número da opção: ').strip()

        if escolha == '1':
            tela_login()
            break  # Sai do loop após ação
        elif escolha == '2':
            tela_cadastro()
            break  # Sai do loop após ação
        else:
            print(Fore.RED + 'Insira uma opção válida.')
            time.sleep(2)

#Tela de cadastro
def tela_cadastro():
    '''Solicita e valida e-mail e senha, cadastra novo usuário no banco e redireciona para login.'''
    while True:
        limpar_tela()
        print(Fore.WHITE + '\n' + '='*40)
        print(' '*16 + 'CADASTRO')
        print('='*40)

        print(Fore.CYAN + "Digite 'voltar' a qualquer momento para retornar ao menu.\n")

        # Validação do e-mail
        Email = input(Fore.YELLOW + 'Seu E-mail: ').strip()
        if Email.lower() == 'voltar':
            menu_log_cad()
            return

        if ' ' in Email or not email_valido(Email.lower()):
            print(Fore.RED + 'E-mail inválido. Use apenas domínios @gmail.com ou @ufrpe.br e não utilize espaços.')
            time.sleep(4)
            continue

        # Validação da senha
        while True:
            nova_senha = input_senha_asteriscos(Fore.YELLOW + 'Nova senha: ').strip()
            if nova_senha.lower() == 'voltar':
                menu_log_cad()
                return

            resultado = validar_senha(nova_senha)
            if resultado != "válida":
                print(Fore.RED + resultado)
                time.sleep(2)
                continue

            confirmar_senha = input_senha_asteriscos(Fore.YELLOW + 'Confirme a senha: ').strip()
            if confirmar_senha.lower() == 'voltar':
                menu_log_cad()
                return

            if nova_senha != confirmar_senha:
                print(Fore.RED + 'As senhas não coincidem. Tente novamente.')
                time.sleep(2)
                continue

            break

        try:
            hash_senha = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute('INSERT INTO usuarios (Email, senha) VALUES (?, ?)', (Email, hash_senha))
            conn.commit()
            print(Fore.GREEN + f'\n{Email} cadastrado com sucesso!')
            time.sleep(2)
            tela_login()
            return
        except sqlite3.IntegrityError:
            print(Fore.RED + 'Usuário já cadastrado. Tente novamente com outro e-mail.')
            time.sleep(4)

#Tela de login
def tela_login():
    '''Solicita e-mail e senha, verifica credenciais no banco de dados e exibe mensagem de sucesso ou erro.'''

    tentativas = 0
    max_tentativas = 3

    while tentativas < max_tentativas:
        limpar_tela()
        print(Fore.WHITE + '='*40)
        print(' '*17 + 'LOGIN')
        print('='*40)

        print(Fore.CYAN + "Digite 'voltar' a qualquer momento para retornar ao menu.\n")

        Email = input(Fore.YELLOW + 'Seu E-mail: ').strip()
        if Email.lower() == 'voltar':
            menu_log_cad()
            return

        senha = input_senha_asteriscos(Fore.YELLOW + 'Senha: ').strip()
        if senha.lower() == 'voltar':
            menu_log_cad()
            return

        cursor.execute('SELECT senha FROM usuarios WHERE Email = ?', (Email,))
        resultado = cursor.fetchone()

        print(Fore.BLUE + '\nVerificando...\n')
        time.sleep(1)

        if resultado:
            senha_hash = resultado[0]
            if isinstance(senha_hash, str):
                senha_hash = senha_hash.encode('utf-8')

            if bcrypt.checkpw(senha.encode('utf-8'), senha_hash):
                print(Fore.GREEN + f'Bem vindo(a), {Email}!')
                time.sleep(2)
                menu_principal(Email)
                return  # Encerra a função após sucesso
            else:
                print(Fore.RED + 'E-mail ou senha incorretos.')
        else:
            print(Fore.RED + 'E-mail ou senha incorretos.')

        tentativas += 1
        print(Fore.YELLOW + f'Tentativa {tentativas} de {max_tentativas}.')
        time.sleep(2)

    print(Fore.RED + 'Número máximo de tentativas excedido. Retornando ao menu principal...')
    time.sleep(2)
    menu_log_cad()

#Menu principal
def menu_principal(Email):
    '''
    Exibe o menu principal do programa Mutare e gerencia a navegação entre as opções.
    '''
    while True:
        limpar_tela()
        print(Fore.WHITE + '=' * 40)
        print('      === BEM-VINDO AO MUTARE! ===')
        print('=' * 40)
        print(Fore.CYAN + '[1] Menu Hábitos')
        print(Fore.CYAN + '[2] Mascote')
        print(Fore.CYAN + '[3] Configurações')
        print(Fore.CYAN + '[4] Fechar Programa')
        escolha = input(Fore.YELLOW + 'Digite sua escolha: ').strip()

        if escolha == '1':
            menu_habitos()
        elif escolha == '2':
            mascote()
        elif escolha == '3':
            configuracoes(Email)
        elif escolha == '4':
            print(Fore.GREEN + "Encerrando programa...")
            time.sleep(1)
            break
        else:
            print(Fore.RED + 'Dígito inválido. Digite novamente.')
            time.sleep(2)
            limpar_tela()

#Menu de controle de hábitos
def menu_habitos():
    '''Exibe o menu de controle de hábitos.'''
    while True:
        limpar_tela()
        print(Fore.WHITE + '=' * 20)
        print('      HÁBITOS')
        print('=' * 20)
        print(Fore.CYAN + '[1] Inserir hábito')
        print(Fore.CYAN + '[2] Progresso')
        print(Fore.CYAN + '[3] Editar hábito')
        print(Fore.CYAN + '[4] Deletar hábito')
        print(Fore.CYAN + '[5] Voltar')
        escolha = input(Fore.YELLOW + 'Digite sua escolha: ').strip()

        if escolha == '1':
            inserir_habito()
        elif escolha == '2':
            progresso()
        elif escolha == '3':
            editar_habito(cursor, conn)
        elif escolha == '4':
            deletar_habito(cursor, conn)
        elif escolha == '5':
            return
        else:
            print(Fore.RED + 'Digito inválido. Digite novamente.')
            time.sleep(2)
            limpar_tela()

#Configurações(RUD)
def buscar_conta(Email):
    '''Busca a conta atual no banco de dados.'''
    cursor.execute('SELECT Email, senha FROM usuarios WHERE Email = ?', (Email,))
    return cursor.fetchone()

def configuracoes(Email):
    '''Exibe o menu de configurações.'''
    while True:
        limpar_tela()
        print(Fore.WHITE + '=' * 30) 
        print('        CONFIGURAÇÕES') 
        print('=' * 30)
        print(Fore.CYAN + '[1] Visualizar conta')
        print(Fore.CYAN + '[2] Sair da conta')
        print(Fore.CYAN + '[3] Voltar')
        escolha = input('Digite sua escolha: ').strip()

        if escolha == '1':
            visualizar_conta(Email)
        elif escolha == '2':
            print(Fore.BLUE + 'Saindo da conta...') 
            time.sleep(2)
            menu_log_cad()
        elif escolha == '3':
            return
        else:
            print('Digito inválido. Digite novamente.')   

def visualizar_conta(Email):
    '''Exibe dados da conta e as opções de atualização/exclusão.'''
    limpar_tela()
    conta = buscar_conta(Email)
    if not conta:
        print(Fore.RED + 'Conta não encontrada.')
        return
    
    print('-'*20)
    print(f"INFORMAÇÕES DA CONTA\nEmail: {conta[0]}\nSenha: {'*' * 8}")
    print('-'*20)

    while True:
        print('\n[1] Atualizar senha')
        print(Fore.RED + '[2] Excluir conta')
        print('[3] Voltar')
        escolha = input('Digite sua escolha: ').strip()

        if escolha == '1':
            atualizar_senha(Email)
        elif escolha == '2':
            excluir_conta(Email)
        elif escolha == '3':
            return
        else:
            print('Digito inválido. Digite novamente.')

def atualizar_senha(Email):
    '''Possibilita a atualização da senha do usuário.'''
    limpar_tela()
    conta = buscar_conta(Email)
    if not conta:
        print(Fore.RED + 'Conta não encontrada.')
        return

    senha_atual = input_senha_asteriscos('Confirme sua senha atual: ').strip().encode('utf-8') 

    senha_hash = conta[1].encode('utf-8') if isinstance(conta[1], str) else conta[1]

    if not bcrypt.checkpw(senha_atual, senha_hash):
        print(Fore.RED + 'Senha incorreta.')
        time.sleep(2)
        limpar_tela()
        visualizar_conta(Email)

    while True:
        nova_senha = input_senha_asteriscos('Digite sua nova senha (4-8 caracteres, ao menos uma letra e um número): ').strip()
        
        if validar_senha(nova_senha):
            nova_senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())
            
            cursor.execute('UPDATE usuarios SET senha = ? WHERE email = ?', (nova_senha_hash, Email))
            conn.commit()
            print(Fore.GREEN + 'Senha atualizada com sucesso!')
            break
        else:
            print(Fore.RED + 'Senha inválida. Tente novamente.')

def excluir_conta(Email):
    '''Possibilita a exclusão da conta atual.'''
    limpar_tela()
    conta = buscar_conta(Email)
    if not conta:
        print(Fore.RED + 'Conta não encontrada.')
        return

    confirmacao = input('Tem certeza que quer excluir sua conta? (1 - Sim / 2 - Não): ')
    if confirmacao != '1':
        print(Fore.YELLOW + 'Exclusão cancelada.')
        return

    senha = input_senha_asteriscos('Confirme sua senha: ').strip().encode('utf-8')
    
    senha_hash = conta[1] if isinstance(conta[1], bytes) else conta[1].encode('utf-8')
    
    if not bcrypt.checkpw(senha, senha_hash):
        print(Fore.RED + 'enha incorreta. Processo de exclusão interrompido.')
        time.sleep(1)
        limpar_tela()
        return

    confirmacao_final = input('Ao excluir sua conta, perderá acesso a todo o sistema. Deseja mesmo excluir? (1 - Sim / 2 - Não): ')
    if confirmacao_final != '1':
        print(Fore.YELLOW + 'Exclusão cancelada.')
        time.sleep(1)
        limpar_tela()
        return

    try:
        cursor.execute('DELETE FROM usuarios WHERE email = ?', (Email,))
        conn.commit()
        print(Fore.GREEN + 'Conta excluída com sucesso.')
        time.sleep(1)
        menu_log_cad()
    except Exception as e:
        print(Fore.RED + f'Erro ao excluir conta: {e}')
        conn.rollback()

#Hábitos
def inserir_habito():
    limpar_tela()
    nome = input('Nome do novo hábito (máx. 50 caracteres, sem caracteres especiais): ').strip()
    
    if not nome or len(nome) > 50 or not re.match(r'^[A-Za-z0-9 ]+$', nome):
        print('Nome inválido. Deve conter até 50 caracteres, apenas letras, números e espaços.')
        time.sleep(2)
        return

    frequencia = input('Frequência desejada (Ex.: Diária, Semanal ou Mensal.): ').strip().capitalize()
    if not frequencia:
        print('A frequência é obrigatória.\n')
        time.sleep(2)
        return

    motivacao = None
    resposta = input('Deseja adicionar uma motivação? (s/n): ').strip().lower()
    if resposta == 's':
        motivacao = input('Motivação (máx. 200 caracteres): ').strip()
        if len(motivacao) > 200:
            print('A motivação deve ter no máximo 200 caracteres.\n')
            time.sleep(2)
            return

    while True:
        try:
            start_date = input('Data de início (AAAA-MM-DD): ').strip()
            datetime.strptime(start_date, '%Y-%m-%d')
            break
        except ValueError:
            print('Formato inválido. Tente novamente.')

    while True:
        try:
            end_date = input('Data de término (YYYY-MM-DD): ').strip()
            datetime.strptime(end_date, '%Y-%m-%d')
            if end_date < start_date:
                print('A data de término não pode ser anterior à de início.')
                continue
            break
        except ValueError:
            print('Formato inválido. Tente novamente.')

    cursor.execute(
        'INSERT INTO habits (name, created_at, frequency, motivation, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)',
        (nome, datetime.now().date(), frequencia, motivacao, start_date, end_date)
    )
    conn.commit()
    print(f"Hábito '{nome}' adicionado com sucesso com período de {start_date} até {end_date}!\n")
    time.sleep(2)
   
#edição de hábitos
def listar_habitos(cursor):
    cursor.execute("SELECT id, name, frequency, motivation FROM habits")
    habitos = cursor.fetchall()

    if not habitos:
        print("Nenhum hábito cadastrado.")
        return []

    print("\nHÁBITOS CADASTRADOS:")
    for h in habitos:
        print(f"ID: {h[0]} | Nome: {h[1]} | Frequência: {h[2]} | Motivação: {h[3]}")

    return habitos

def editar_habito(cursor, conn):
    habitos = listar_habitos(cursor)
    if not habitos:
        return  # não há hábitos cadastrados

    habit_id = input("\nDigite o ID do hábito que deseja editar: ")

    try:
        habit_id = int(habit_id)
    except ValueError:
        print("ID inválido. Deve ser um número.")
        return

    cursor.execute("SELECT name, frequency, motivation FROM habits WHERE id = ?", (habit_id,))
    habit = cursor.fetchone()

    if habit is None:
        print("Nenhum hábito encontrado com esse ID.")
        return
    
    print("\nDeixe em branco e pressione ENTER para manter o valor atual.\n")

    novo_nome = input(f"Nome atual: {habit[0]}\nNovo nome: ").strip()
    nova_freq = input(f"Frequência atual: {habit[1]}\nNova frequência: ").strip()
    nova_motiv = input(f"Motivação atual: {habit[2]}\nNova motivação: ").strip()

    # Mantém valores atuais se o usuário não digitar nada
    novo_nome = novo_nome if novo_nome else habit[0]
    nova_freq = nova_freq if nova_freq else habit[1]
    nova_motiv = nova_motiv if nova_motiv else habit[2]

    cursor.execute('''
        UPDATE habits SET name = ?, frequency = ?, motivation = ?
        WHERE id = ?
    ''', (novo_nome, nova_freq, nova_motiv, habit_id)
    )
    conn.commit()
    print(f"Hábito ID {habit_id} atualizado com sucesso!")
    time.sleep(2)

def deletar_habito(cursor, conn):
    limpar_tela()
    print("\n=== Deletar Hábito ===")

    # Listar os hábitos
    cursor.execute("SELECT id, name FROM habits")
    habitos = cursor.fetchall()

    if not habitos:
        print("Nenhum hábito cadastrado.")
        return

    print("\nHábitos cadastrados:")
    for habito in habitos:
        print(f"{habito[0]} - {habito[1]}")

    try:
        habito_id = int(input("\nDigite o ID do hábito que deseja deletar: "))
    except ValueError:
        print("ID inválido.")
        return

    # Verificar se o hábito existe
    cursor.execute("SELECT * FROM habits WHERE id = ?", (habito_id,))
    habito = cursor.fetchone()

    if habito is None:
        print("Hábito não encontrado.")
        return

    # Confirmar exclusão
    confirm = input(f"Tem certeza que deseja deletar o hábito '{habito[1]}'? (s/n): ").lower()
    if confirm != 's':
        print("Operação cancelada.")
        return

    # Deletar hábito
    cursor.execute("DELETE FROM habits WHERE id = ?", (habito_id,))
    conn.commit()

    print("Hábito deletado com sucesso.")
    time.sleep(1)

def progresso():
    limpar_tela()
    print("\n=== Progresso ===\n")

    cursor.execute("SELECT id, name, start_date, end_date, frequency FROM habits")
    habits = cursor.fetchall()

    if not habits:
        print("Nenhum hábito cadastrado.")
        time.sleep(2)
        return

    for habit in habits:
        habit_id, name, start_date, end_date, frequency = habit

        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        today = date.today()

        # Calcula total previsto conforme frequência
        if frequency == 'Diária':
            total_previstos = (end - start).days + 1
        elif frequency == 'Semanal':
            total_previstos = ((end - start).days // 7) + 1
        elif frequency == 'Mensal':
            total_previstos = ((end.year - start.year) * 12 + end.month - start.month) + 1
        else:
            print(f"Frequência desconhecida: {frequency}. Pulando.")
            continue

        # Progresso real
        cursor.execute("SELECT COUNT(*) FROM habit_progress WHERE habit_id = ?", (habit_id,))
        feitos = cursor.fetchone()[0]

        # Percentual
        porcentagem = (feitos / total_previstos) * 100 if total_previstos > 0 else 0

        # Barra de progresso proporcional
        barra_len = total_previstos if total_previstos <= 10 else 10
        preenchido = '🟩' * int((porcentagem / 100) * barra_len)
        vazio = '⬜' * (barra_len - len(preenchido))
        barra = f"{preenchido}{vazio}"

        print(f"\nHábito: {name} ({frequency})")
        print(f"Período: {start} até {end}")
        print(f"Progresso: {barra} {porcentagem:.2f}% ({feitos}/{total_previstos} registros previstos)\n")

        adicionar = input("Deseja adicionar progresso para este hábito? (s/n): ").strip().lower()

        if adicionar == 's':
            status = input("Status (Feito/Não feito): ").strip().capitalize()
            data = input("Data (AAAA-MM-DD), ou deixe vazio para hoje: ").strip()
            if not data:
                data = today.isoformat()

            try:
                data_obj = datetime.strptime(data, '%Y-%m-%d').date()
            except ValueError:
                print("Data inválida. Progresso não registrado.")
                continue

            if data_obj < start or data_obj > end:
                print(f"A data deve estar entre {start} e {end}. Progresso não registrado.")
                continue

            # Verifica duplicata conforme frequência
            if frequency == 'Diário':
                condicao = data
            elif frequency == 'Semanal':
                ano, semana, _ = data_obj.isocalendar()
                condicao = f"{ano}-W{semana}"
            elif frequency == 'Mensal':
                condicao = f"{data_obj.year}-{data_obj.month}"

            # Busca registros existentes conforme condicao
            cursor.execute("SELECT date FROM habit_progress WHERE habit_id = ?", (habit_id,))
            datas_existentes = [d[0] for d in cursor.fetchall()]

            existe = False
            for d in datas_existentes:
                d_obj = datetime.strptime(d, '%Y-%m-%d').date()
                if frequency == 'Diária' and d == data:
                    existe = True
                    break
                elif frequency == 'Semanal' and f"{d_obj.isocalendar()[0]}-W{d_obj.isocalendar()[1]}" == condicao:
                    existe = True
                    break
                elif frequency == 'Mensal' and f"{d_obj.year}-{d_obj.month}" == condicao:
                    existe = True
                    break

            if existe:
                print("Progresso já registrado para essa frequência. Não é possível marcar novamente.")
                time.sleep(1)
            else:
                cursor.execute('''
                    INSERT INTO habit_progress (habit_id, date, status)
                    VALUES (?, ?, ?)
                ''', (habit_id, data, status))
                conn.commit()
                print("Progresso adicionado com sucesso!")

    print("\n=== Fim da visualização ===\n")
    time.sleep(1)

def mascote():
    limpar_tela()
    print("\n=== Seu mascote ===\n")

    #Algoritmo para determinar o desempenho 
    cursor.execute("SELECT status FROM habit_progress")
    status_list = cursor.fetchall()

    feitos = sum(1 for status in status_list if status[0] == 'Feito')
    total = len(status_list)

    if total == 0:
        desempenho_percentual = None  # nenhum progresso ainda
    else:
        desempenho_percentual = (feitos / total) * 100

    #Inicializa as variáveis
    desempenho_otimo = 0
    desempenho_bom = 0
    desempenho_fraco = 0
    desempenho_ruim = 0

    #Definindo o desempenho conforme o percentual
    if desempenho_percentual is None:
        pass  #não define nenhuma variável
    elif desempenho_percentual >= 80:
        desempenho_otimo = 1
    elif desempenho_percentual >= 60:
        desempenho_bom = 1
    elif desempenho_percentual >= 40:
        desempenho_fraco = 1
    else:
        desempenho_ruim = 1

    #Reações 
    if desempenho_otimo == 1:
        print(r"""
        \(^_^)/ 
        """)
        print("Você é incrível!!!")
    elif desempenho_bom == 1:
        print(r"""
        (^_^)
        """)
        print("É isso aí, tá arrasando!!")
    elif desempenho_fraco == 1:
        print(r"""
        (._.)
        """)
        print("Bora melhorar!")
    elif desempenho_ruim == 1:
        print(r"""
        (T_T)
        """)
        print("Lembre de tudo que fez até aqui e o porquê de tudo, não é hora de desistir")
    else:
        print(r"""
        (o_o)
        """)
        print("Estou esperando você começar a marcar o progresso.")

    input("\nPressione Enter para voltar ao menu.")
   
#Execução    
if __name__ == '__main__':
    try:
        menu_log_cad()
    finally:
        cursor.close()
        conn.close()