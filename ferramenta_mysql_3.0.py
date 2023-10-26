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

        # Consulta SQL para obter as informações da tabela
        cursor.execute(f"DESCRIBE {table_name}")
        columns_info = cursor.fetchall()

        # Limpe a exibição anterior
        for i in tree.get_children():
            tree.delete(i)

        # Obtenha os nomes das colunas a partir das informações da tabela
        columns = [col[0] for col in columns_info]

        # Configure as colunas dinamicamente
        tree["columns"] = columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)  # Defina a largura apropriada para as colunas

        # Consulta SQL para exibir os dados da tabela
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        resultados = cursor.fetchall()

        # Atualize a exibição na interface gráfica
        for linha in resultados:
            tree.insert('', 'end', values=linha)

        # Feche o cursor e a conexão
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Erro: {err}")

def atualizar_registro():
    # Obtenha as informações do banco de dados, tabela, coluna, valor antigo e novo valor
    db_name = db_name_entry.get()
    table_name = table_name_entry.get()
    column_name = col_name_entry.get()
    old_value = old_value_entry.get()
    new_value = new_value_entry.get()

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

        # Consulta SQL para atualizar o registro
        query = f"UPDATE {table_name} SET {column_name} = %s WHERE {column_name} = %s"
        cursor.execute(query, (new_value, old_value))

        # Commit para salvar as alterações
        conn.commit()

        # Feche o cursor e a conexão
        cursor.close()
        conn.close()

        # Recarregue a tabela após a atualização
        exibir_tabela()
    except mysql.connector.Error as err:
        print(f"Erro: {err}")

# Crie a janela principal
root = tk.Tk()
root.title("Visualizador e Atualização de Tabela MySQL com Colunas Dinâmicas")

# Crie os campos para inserir o nome do banco de dados, o nome da tabela, coluna, valor antigo e novo valor
db_name_label = ttk.Label(root, text="Nome do Banco de Dados:")
db_name_label.pack()
db_name_entry = ttk.Entry(root)
db_name_entry.pack()

table_name_label = ttk.Label(root, text="Nome da Tabela:")
table_name_label.pack()
table_name_entry = ttk.Entry(root)
table_name_entry.pack()

col_name_label = ttk.Label(root, text="Nome da Coluna:")
col_name_label.pack()
col_name_entry = ttk.Entry(root)
col_name_entry.pack()

old_value_label = ttk.Label(root, text="Valor Antigo:")
old_value_label.pack()
old_value_entry = ttk.Entry(root)
old_value_entry.pack()

new_value_label = ttk.Label(root, text="Novo Valor:")
new_value_label.pack()
new_value_entry = ttk.Entry(root)
new_value_entry.pack()

# Botão para exibir a tabela
exibir_button = ttk.Button(root, text="Exibir Tabela", command=exibir_tabela)
exibir_button.pack()

# Botão para atualizar registro
atualizar_button = ttk.Button(root, text="Atualizar Registro", command=atualizar_registro)
atualizar_button.pack()

# Crie uma árvore para exibir os dados da tabela
tree = ttk.Treeview(root)
tree.pack()

root.mainloop()
