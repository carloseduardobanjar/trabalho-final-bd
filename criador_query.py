import csv
from datetime import date

# Este arquivo cria queries .SQL para alteração de campos 
# (conforme tamanhos máximos encontrados) e inserção nas seguintes tabelas:
# - Filmes
# - Coletanea
# - Pessoa 
# - Producao 
# - Atuacao 
# Os arquivos credits.csv e movies_metadata.csv precisam estar na mesma pasta que este arquivo.

#checa se uma pessoa já esta incluida na lista sendo construida
def checa_pessoa(candidato,lista_pessoas,id_pessoas):
    if candidato["id"] in id_pessoas:
        # for pessoa in lista_pessoas:
        #     if(pessoa["id"]==candidato["id"]):
        #         if(pessoa["name"]!=candidato["name"]):
        #             print("deu merda com o {}".format(candidato["name"]))
        #         else:
        return False
    return True

#adiciona uma pessoa e conta o numero máximo de caracteres do nome
def addpessoa(person,lista,id_pessoas,maxval):
    if('\'' in person["name"]):
        person.update({"name": person["name"].replace('\'',"''")})

    lista.append({"id":person["id"], 
                            "gender":person["gender"],
                            "name":person["name"]})
    id_pessoas.add(person["id"])
    if(len(person["name"])>maxval["name"]):
        maxval.update({"name":len(person["name"])})

#adiciona uma relacao de atuacao e checa caracteres maximos
def addatuacao(idf,pessoa,lista,maxlen,check):
    pessoa.update({"character":pessoa["character"].replace('\'',"''")})
    atuacao = {"id_filme":idf,
                        "id_ator":pessoa["id"], 
                        "personagem":'\'' + pessoa["character"]+'\''}
    #checar se ja existe
    if((atuacao["id_filme"],atuacao["id_filme"]) in check):
        return

    lista.append(atuacao)
    check.add((atuacao["id_filme"],atuacao["id_filme"]))
    if(len(pessoa["character"])>maxlen["character"]):
        maxlen.update({"character":len(pessoa["character"])})

#adiciona uma relacao de producao e checa caracteres maximos
def addprod(idf,pessoa,lista,maxlen,check):
    pessoa.update({"job":pessoa["job"].replace('\'',"''")})
    pessoa.update({"department":pessoa["department"].replace('\'',"''")})
    prod = {"id_filme":idf,
                "id_produtor":pessoa["id"],
                "job":'\''+pessoa["job"]+'\'',
                "department":'\''+pessoa["department"]+'\''}
    #checando duplicatas
    if((prod["id_filme"],prod["id_produtor"],prod["job"]) in check):
        return
    lista.append(prod)
    check.add((prod["id_filme"],prod["id_produtor"],prod["job"]))
    
    if(len(pessoa["job"])>maxlen["job"]):
        maxlen.update({"job":len(pessoa["job"])})
        
    if(len(pessoa["department"])>maxlen["department"]):
        maxlen.update({"department":len(pessoa["department"])}) 

#atualiza tamanho necessario dos atributos e constroi a query
def query_pessoa(pessoas,maxlen):
    arqv = open("pessoas.sql",'w')
    strg = '''USE movies; 
    ALTER TABLE Pessoa 
    MODIFY COLUMN nome VARCHAR({});
    INSERT INTO Pessoa VALUES '''.format(maxlen["name"])
    arqv.write(strg)
    for p in pessoas:
        strg = "({}, {}, {}),\n".format(p["id"],p["gender"],p["name"])
        if p==pessoas[-1]:
            strg = strg.replace("),\n",");")
        arqv.write(strg)
    
    arqv.close()
    print("\tquery pra pessoas escrita")

#atualiza tamanho necessario dos atributos e constroi a query
def query_atuacao(atuacao,maxlen):
    arqv = open("q_atuacao.sql",'w')
    strg = '''USE movies; 
    ALTER TABLE Atuacao 
    MODIFY COLUMN personagem VARCHAR({}),;
    INSERT INTO Atuacao VALUES '''.format(maxlen["character"])
    arqv.write(strg)

    for p in atuacao:
        strg = "({}, {}, {}),\n".format(p["id_filme"],p["id_ator"],p["personagem"])
        if p==atuacao[-1]:
            strg = strg.replace("),\n",");")
        arqv.write(strg)
    
    arqv.close()
    print("\tquery pra atuacoes escrita")
    
#atualiza tamanho necessario dos atributos e constroi a query
def query_producao(prod,maxlen):
    arqv = open("q_producao.sql",'w')
    strg = '''USE movies; 
    ALTER TABLE Producao 
    MODIFY COLUMN job VARCHAR({}),
    MODIFY COLUMN department VARCHAR({});
    INSERT INTO Producao VALUES '''.format(maxlen["job"],maxlen["department"])
    arqv.write(strg)

    for p in prod:
        strg = '''({}, {}, {},{}),\n'''.format(p["id_filme"],p["id_produtor"],p["job"],p["department"])
        if p==prod[-1]:
            strg = strg.replace("),\n",");")
        arqv.write(strg)
    
    arqv.close()
    print("\tquery pra Producao escrita")

#adiciona filme _à uma lista 
def addfilme(movies,record,maxlen,ids):
    if(record[5] in ids):
        return
    ids.add(record[5])
    movie = {
            "id":record[5],
            "homepage":record[4],
            "adult":record[0],
            "budget":record[2],
            "orig_language":record[7],
            "orig_title":record[8],
            "overview":record[9] }
    if record[1]!=None:
        movie.update({"id_coletanea":record[1]["id"]})
    else:
        movie.update({"id_coletanea":record[1]})

    movie.update({"title":record[20],
        "runtime":record[16],
        "popularity":record[10],
        "revenue":record[15],
        "release_date":record[14],
        "status":record[18],
    })
    
    #update max value
    for key,value in maxlen.items():
        if(movie[key]!= None and len(movie[key])>value):
            maxlen.update({key:len(movie[key])})
    #string formatation
    for key,value in movie.items():
        if type(movie[key])==type("stringkk"):
            if(len(movie[key])==0) :
                movie.update({key:None})
            else:
                movie.update({key:movie[key].replace('\'',"''")})
                movie.update({key:"'"+movie[key]+"'"})
            
        if(movie[key]==None):
            movie.update({key:'Null'})
    # if movie["revenue"]>2147483640:
    #     print(movie)
    movies.append(movie)

# lida com inconsistencias no tamanho das linhas/objetos no arquivo
def formata_linha(record):
    for i in range(len(record)):
        match i:
            case 20: pass
            case 14: pass
            case 9: pass
            case 8: pass
            case 7: pass
            case _:
                try:
                    record[i] = eval(record[i])
                except:
                    if(len(record[i])==0):
                        record[i] = None

#cria query dos filmes
def cria_query_filme(movies,maxlen):
    arqv = open("q_movies.sql",'w')
    strg = '''USE movies; 
    ALTER TABLE Filmes 
    MODIFY COLUMN homepage VARCHAR({}),
    MODIFY COLUMN orig_title VARCHAR({}),
    MODIFY COLUMN overview VARCHAR({}),
    MODIFY COLUMN title VARCHAR({}),
    MODIFY COLUMN status VARCHAR({});
    INSERT INTO Filmes VALUES '''.format(maxlen["homepage"],maxlen["orig_title"],
                                         maxlen["overview"],maxlen["title"],
                                         maxlen["status"])
    arqv.write(strg)
    print("temos {} filmes".format(len(movies)))
    for p in movies:
        strg = '''({}, {}, {},{},{},{},{},{},{},{},{},{},{},{}),\n'''.format(*p.values())
        if p==movies[-1]:
            strg = strg.replace("),\n",");")
        arqv.write(strg)
    
    arqv.close()
    print("\tquery pra Filmes escrita")

#cria query de coletanea
def cria_q_clt(clts,maxcolt):
    arqv = open("q_clt.sql",'w')
    strg = '''USE movies; 
    ALTER TABLE Coletanea 
    MODIFY COLUMN nome VARCHAR({});
    INSERT INTO Coletanea VALUES '''.format(maxcolt[0])
    arqv.write(strg)

    print("temos {} coletaneas".format(len(clts)))
    for p in clts:
        strg = '''({}, {}),\n'''.format(*p.values())
        if p==clts[-1]:
            strg = strg.replace("),\n",");")
        arqv.write(strg)
    print("\t query para coletaneas escrita")

# adiciona coletanea à lista
def add_clt(coletaneas,record,maxcolt,idclt):
    if(record[1]==None) or (record[1]["id"] in idclt):
        return
    
    clt = { "nome":'\''+record[1]["name"].replace('\'',"''")+'\'',
           "id":record[1]["id"]}
    idclt.add(clt["id"])

    if(len(clt["nome"])>maxcolt[0]):
        maxcolt[0]=len(clt["nome"])
    coletaneas.append(clt)


# funcoes principais
    
def criar_filmes():


    
    with open("movies_metadata.csv") as csvfile:
        data = csv.reader(csvfile)
        datalist = []
        for record in data:
            datalist.append(record)
    datalist.pop(0)

    movies = []
    maxlen = {
            "homepage":0,
            "orig_title":0,
            "overview":0,
            "title":0,
            "status":0,
        }
    MAXI = 3
    c = 0
    maxcolt = [0]
    idclt= set([])
    ids = set([])
    coletaneas = []
    for record in datalist:
        
        formata_linha(record)
        add_clt(coletaneas,record,maxcolt,idclt)
        addfilme(movies,record,maxlen,ids)
        
        
        c+=1
        if not(c%300):
            print(c,'\n')
        # if c>MAXI: break
       
    #criar queries
    print("{} filmes lidos!\n".format(c))
    cria_q_clt(coletaneas,maxcolt)
    cria_query_filme(movies,maxlen)

def criar_pessoas():
    # lê csv e constroi lista das entradas
    with open("credits.csv") as csvfile:
        data = csv.reader(csvfile)
        datalist = []
        for record in data:
            datalist.append(record)

    #retirando nome das colunas
    datalist.pop(0)

    tam = len(datalist)
    i=0
    id_pessoas = set([])
    lista_atuacoes = set([])
    lista_producao = set([])
    pessoas = []
    atuacao = []
    producao = []
    maxlen = {"name":0,
            "job":0,
            "department":0,
            "character":0 }
    for record in datalist:
        record[0] = eval(record[0])
        record[1] = eval(record[1])

        record[2] = int(record[2])
        
        #para cada pessoa in cast
        for person in record[0]:
            if(checa_pessoa(person,pessoas,id_pessoas)):
                addpessoa(person,pessoas,id_pessoas,maxlen)
                
            addatuacao(record[2],person,atuacao,maxlen,lista_atuacoes)
            
            

        #persons in crew
        for person in record[1]:
            if(checa_pessoa(person,pessoas,id_pessoas)):
                addpessoa(person,pessoas,id_pessoas,maxlen)
            addprod(record[2],person,producao,maxlen,lista_producao)
        #mostrar status 
        i+=1
        if not(i%300):
            print("{}/{}, np={}".format(i,tam, len(id_pessoas)))
            print(maxlen,'\n')


    print("{} filmes parseados!".format(i))
    print("existem {} pessoas!".format(len(pessoas)))
    #criar queries
    query_pessoa(pessoas,maxlen)
    query_atuacao(atuacao,maxlen)
    query_producao(producao,maxlen)

    

    
# Indices dos dados para referência: 
# adult	0
# belongs_to_collection 1
# budget 2
# genres	3
# homepage 4
# id 5
# original_language 7
# original_title 8
# overview	9
# popularity
# release_date 12
# revenue	13
# runtime	 14
# status 16
# title 18



criar_pessoas()
criar_filmes()
