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

# Crie a janela principal
root = tk.Tk()
root.title("Visualizador de Tabela MySQL com Colunas Dinâmicas")

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
tree = ttk.Treeview(root)
tree.pack()

root.mainloop()
