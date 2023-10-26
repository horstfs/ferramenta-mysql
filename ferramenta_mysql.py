import mysql.connector
import tkinter as tk
from tkinter import ttk

def exibir_tabela():
    # Obtenha as informações do banco de dados e da tabela a partir da interface gráfica
    db_name = db_name_entry.get()
    table_name = table_name_entry.get()

    # Configurações de conexão
    config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": db_name
    }

    try:
        # Conecte-se ao banco de dados
        conn = mysql.connector.connect(**config)

        # Crie um cursor
        cursor = conn.cursor()

        # Consulta SQL
        query = f"SELECT * FROM {table_name}"

        # Execute a consulta
        cursor.execute(query)

        # Recupere todos os resultados
        resultados = cursor.fetchall()

        # Limpe a exibição anterior
        for i in tree.get_children():
            tree.delete(i)

        # Atualize a exibição na interface gráfica
        for linha in resultados:
            tree.insert('', 'end', values=linha)

        # Feche o cursor e a conexão
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Erro: {err}")

def inserir_dados():
    # Obtenha os valores a serem inseridos a partir da interface gráfica
    col1_value = col1_entry.get()
    col2_value = col2_entry.get()
    col3_value = col3_entry.get()

    try:
        # Configurações de conexão
        config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": db_name_entry.get()
        }

        # Conecte-se ao banco de dados
        conn = mysql.connector.connect(**config)

        # Crie um cursor
        cursor = conn.cursor()

        # Consulta SQL de inserção
        query = f"INSERT INTO {table_name_entry.get()} (coluna1, coluna2, coluna3) VALUES (%s, %s, %s)"

        # Execute a consulta com os valores fornecidos
        cursor.execute(query, (col1_value, col2_value, col3_value))

        # Commit para salvar as alterações
        conn.commit()

        # Feche o cursor e a conexão
        cursor.close()
        conn.close()

        # Recarregue a tabela após a inserção
        exibir_tabela()
    except mysql.connector.Error as err:
        print(f"Erro: {err}")

# Crie a janela principal
root = tk.Tk()
root.title("Visualizador e Inserção de Dados em Tabela MySQL")

# Crie os campos para inserir o nome do banco de dados e o nome da tabela
db_name_label = ttk.Label(root, text="Nome do Banco de Dados:")
db_name_label.pack()
db_name_entry = ttk.Entry(root)
db_name_entry.pack()

table_name_label = ttk.Label(root, text="Nome da Tabela:")
table_name_label.pack()
table_name_entry = ttk.Entry(root)
table_name_entry.pack()

# Botão para exibir a tabela
exibir_button = ttk.Button(root, text="Exibir Tabela", command=exibir_tabela)
exibir_button.pack()

# Crie uma árvore para exibir os dados da tabela
columns = ("Coluna 1", "Coluna 2", "Coluna 3")  # Substitua pelas colunas reais da sua tabela
tree = ttk.Treeview(root, columns=columns, show="headings")

# Configure as colunas
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)  # Defina a largura apropriada para as colunas

tree.pack()

# Crie campos para inserir dados
col1_label = ttk.Label(root, text="Coluna 1:")
col1_label.pack()
col1_entry = ttk.Entry(root)
col1_entry.pack()

col2_label = ttk.Label(root, text="Coluna 2:")
col2_label.pack()
col2_entry = ttk.Entry(root)
col2_entry.pack()

col3_label = ttk.Label(root, text="Coluna 3:")
col3_label.pack()
col3_entry = ttk.Entry(root)
col3_entry.pack()

# Botão para inserir dados
inserir_button = ttk.Button(root, text="Inserir Dados", command=inserir_dados)
inserir_button.pack()

root.mainloop()
