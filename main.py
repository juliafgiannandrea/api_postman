from fastapi import FastAPI
from sqlalchemy import create_engine, text
import pandas as pd

#infos para a conexão com o banco de dados
host = 'localhost'
port = '3306'
user = 'root'
senha = '1234' 
database_name = 'db_escola' 
 

DATABASE_URL = f'mysql+pymysql://{user}:{senha}@{host}:{port}/{database_name}'
engine = create_engine(DATABASE_URL)

#Criação de API:
app = FastAPI() #instancia uma pasta

#método GET 
@app.get("/")
def home():
    return {"message": "minha primeira api"}

#checar o funcionamento da API 
#1. pelo browser: no terminal > uvicorn main:app --reload
#2. postman:fornecer o "/   /" no postman 
#3. terminal: curl -X get URL 


#GET - tb_alunos:
#via sql 
@app.get("/alunos/")
def pegar_alunos():
    with engine.begin() as conn:
        result = conn.execute(text("Select * from tb_alunos"))
        alunos = [row._asdict() for row in result]
    return alunos

#via pandas 
@app.get("/alunos_pandas/")
def pegar_alunos():
    sql = text("Select * from tb_alunos")
    df = pd.read_sql(sql, con = engine)
    df = df.fillna(0)
    return df.to_dict(orient="records")


#metodo POST: inserir endereço
@app.post("/inserir_endereco/")
def inserir_enderecos(endereco:dict):
    with engine.begin() as conn:
         sql = text("""
INSERT INTO tb_enderecos (cep,endereco,cidade,estado)
VALUES (:cep, :endereco,:cidade, :estado) 
""")
         result = conn.execute(sql,endereco)
    return{"message": "endereço cadastrado com sucesso"}


#as infos do endereco que vc quer inserir 
# params_endereco = {
#         'cep': 32322223,
#         'endereco':"TESTE 25_04",
#         'cidade':"Palmas",
#         'estado':"TO",

#     }
# inserir_enderecos(params_endereco)


#update: método PUT 
@app.put("/atualizar_nota/")
def atualizar_nota(notas:dict):
    with engine.begin() as conn:
         sql = text(
                     """
UPDATE tb_notas  
SET nota = :nota
WHERE aluno_id = :aluno_id AND disciplina_id = :disciplina_id
"""
         )
         result = conn.execute(sql,notas)
    return{"message": "nota atualizada com sucesso"}

#as infos para atualizar a nota 
# params_nota = {
#     'aluno_id': 53,
#     'disciplina_id': 2,
#     'nota': 3
# }
#atualizar_nota(params_nota)


#atualizar aluno: NO POSTMAN O RECEBIMENTO DE PARÂMETROS NÃO FUNCIONA
@app.put("/atualizar_aluno/")


def atualizar_aluno(id_aluno, nome_aluno = None, email = None, cep = None, carro_id = None):
    with engine.begin() as conn:
        campos_atualizacao = []
        params = {"id": id_aluno}
        if nome_aluno: #verifica se cada campo (parâmetros da função) foi passado 
            campos_atualizacao.append("nome_aluno = :nome_aluno")
            params["nome_aluno"] = nome_aluno  #adiciona ao dicionário params a chave "nome_aluno" e o valor nome_aluno (que é o que o usuário inseriu)
        if email:
            campos_atualizacao.append("email = :email")
            params["email"] = email
        if cep:
            campos_atualizacao.append("cep = :cep")
            params["cep"] = cep
        if carro_id:
            campos_atualizacao.append("carro_id = :carro_id")
            params["carro_id"] = carro_id 
        sql = text(f"UPDATE tb_alunos  SET {','.join(campos_atualizacao)} WHERE id = :id")
        result = conn.execute(sql,params)
    return{"message": "aluno atualizado com sucesso"}

#as infos do aluno a serem atualizadas 
# atualizar_aluno(11, nome_aluno = None, email = 'alex@alex', cep = 1111222, carro_id = 1)


#método DELETE: 
@app.delete("/deletar_aluno/")
def deletar_aluno(id:int):
    with engine.begin() as conn:
         sql = text("""

DELETE from tb_alunos
WHERE id = :id;          
""")
         result = conn.execute(sql,{"id":id})
    return{"message": "aluno deletado com sucesso"}

#as infos do aluno a ser deletado são passadas na URL >>> /?id=2
# deletar_aluno(55)






