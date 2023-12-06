from flask import Flask, render_template
import pymysql

user = 'root'
passwd = 'password'
host =  'localhost'
port = 3306
database = 'Movies'

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('web.html', corpo=[], cabecalho=[])

@app.route("/ator_filme/<parametro1>")
def ator_filme(parametro1):
    conn = pymysql.connect(host=host,
                       port=port,
                       user=user, 
                       passwd=passwd,  
                       db=database,
                       charset='utf8')
    cursor = conn.cursor()

    cursor.execute(f"SELECT Pessoa.nome FROM Pessoa JOIN Atuacao ON Atuacao.id_ator = Pessoa.id JOIN Filmes ON Filmes.id = Atuacao.id_filme WHERE Filmes.title='{parametro1}'")
    rows = cursor.fetchall()

    conn.commit()
    conn.close()
    return render_template('web.html', corpo=rows, cabecalho=['Nome'])

@app.route("/filme_ator/<parametro1>")
def filme_ator(parametro1):
    conn = pymysql.connect(host=host,
                       port=port,
                       user=user, 
                       passwd=passwd,  
                       db=database,
                       charset='utf8')
    cursor = conn.cursor()

    cursor.execute(f"SELECT Filmes.title FROM Pessoa JOIN Atuacao ON Atuacao.id_ator = Pessoa.id JOIN Filmes ON Filmes.id = Atuacao.id_filme WHERE Pessoa.nome='{parametro1.replace('_', ' ')}'")
    rows = cursor.fetchall()

    conn.commit()
    conn.close()
    return render_template('web.html', corpo=rows, cabecalho=['Titulo'])

@app.route("/media_ava")
def media_ava():
    conn = pymysql.connect(host=host,
                       port=port,
                       user=user, 
                       passwd=passwd,  
                       db=database,
                       charset='utf8')
    cursor = conn.cursor()

    cursor.execute(f"SELECT Filmes.id, Filmes.title, AVG(Avaliacao.rating) AS MediaAvaliacao FROM Filmes LEFT JOIN Avaliacao ON Filmes.id = Avaliacao.id_filme GROUP BY Filmes.id LIMIT 20;")
    rows = cursor.fetchall()

    conn.commit()
    conn.close()
    return render_template('web.html', corpo=rows, cabecalho=['ID', 'Título', 'Média'])

@app.route("/orc_ator")
def orc_ator():
    conn = pymysql.connect(host=host,
                       port=port,
                       user=user, 
                       passwd=passwd,  
                       db=database,
                       charset='utf8')
    cursor = conn.cursor()

    cursor.execute(f"SELECT Pessoa.id, Pessoa.nome, AVG(Filmes.budget) AS MediaOrcamento FROM Pessoa JOIN Atuacao ON Pessoa.id= Atuacao.id_ator JOIN Filmes ON Atuacao.id_filme = Filmes.id GROUP BY Pessoa.id LIMIT 20;")
    rows = cursor.fetchall()

    conn.commit()
    conn.close()
    return render_template('web.html', corpo=rows, cabecalho=['Id', 'Nome', 'Média'])

@app.route("/pop_acima")
def pop_acima():
    conn = pymysql.connect(host=host,
                       port=port,
                       user=user, 
                       passwd=passwd,  
                       db=database,
                       charset='utf8')
    cursor = conn.cursor()

    cursor.execute(f"SELECT id, orig_title, popularity FROM Filmes WHERE popularity > (SELECT AVG(popularity) FROM Filmes) LIMIT 20;")
    rows = cursor.fetchall()

    conn.commit()
    conn.close()
    return render_template('web.html', corpo=rows, cabecalho=['Id', 'Título', 'Popularidade'])

@app.route("/melhores_dir")
def melhores_dir():
    conn = pymysql.connect(host=host,
                       port=port,
                       user=user, 
                       passwd=passwd,  
                       db=database,
                       charset='utf8')
    cursor = conn.cursor()

    cursor.execute(f"SELECT orig_title,nome as nome_diretor FROM Filmes JOIN Producao ON Filmes.id=id_filme JOIN Pessoa ON id_produtor=Pessoa.id WHERE Pessoa.id in (select id from top_3_directors);")
    rows = cursor.fetchall()

    conn.commit()
    conn.close()
    return render_template('web.html', corpo=rows, cabecalho=['Título', 'Nome do diretor',])

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)