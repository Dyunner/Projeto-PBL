from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import logging
import sqlite3
import unicodedata
import random

app = Flask(__name__)
app.secret_key = "segredo"
logging.basicConfig(level=logging.DEBUG)


def conectar():
    return sqlite3.connect("banco.db")


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        nome TEXT PRIMARY KEY,
        preco REAL
    )
    """)

    conn.commit()
    conn.close()


# 👉 ESSA É A PARTE QUE RESOLVE NO RENDER
with app.app_context():
    criar_tabela()


# =========================
# FUNÇÕES AUX
# =========================

def normalizar(texto):
    if not texto:
        return ""

    texto = texto.strip().lower()

    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto)
        if not unicodedata.combining(c)
    )


def extrair_codigo_busca(texto):
    texto_norm = normalizar(texto).replace(" ", "")

    if texto_norm.startswith("combo"):
        numero = ""

        for caractere in texto_norm[5:]:
            if caractere.isdigit():
                numero += caractere
            else:
                break

        if numero:
            return numero

    return texto_norm


def eh_combo(texto):
    return normalizar(texto).replace(" ", "").startswith("combo")


def buscar_produto_por_nome(nome_busca):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT nome, preco FROM produtos")
    linhas = cursor.fetchall()
    conn.close()

    termo_busca_norm = normalizar(nome_busca)
    codigo_busca = extrair_codigo_busca(nome_busca)
    busca_combo = eh_combo(nome_busca)

    for nome_db, preco in linhas:
        nome_db_norm = normalizar(nome_db)
        codigo_db = extrair_codigo_busca(nome_db)
        item_combo = eh_combo(nome_db)

        if nome_db_norm == termo_busca_norm:
            return nome_db, preco

        if busca_combo and item_combo and codigo_db == codigo_busca:
            return nome_db, preco

    return None, None

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        nome TEXT PRIMARY KEY,
        preco REAL
    )
    """)

    conn.commit()
    conn.close()

respostas_bot = {
#Opção matriz
    "inicio": {
        "gatilhos": ["inicio"],
        "respostas": [
            "Olá! Posso ajudar com uma sugestão, selecione a ocasião desejada..."
        ],
        "opcoes": ["Sugestões"]
    },
#Opção matriz

#Opção secundária
"Sugestões": {
        "gatilhos": ["Sugestões"],
        "respostas": ["O que você busca?..."],
        "opcoes": ["Produtos Casuais", "Produtos para Festas", "Produtos para ocasiões frias", "Produtos para ocasiões quentes"]
},    
#Opção secundária

#Opção terciária
    "Produtos Casuais": {
        "gatilhos": ["Produtos Casuais"],                     
        "respostas": ["Quais tipos de produtos causais você busca?..."],
        "opcoes": ["Bebidas", "Comidas", "Combos"]
},
#Opção terciária

#Casuais
    "bebidas": {
        "gatilhos": ["Bebidas"],
        "respostas": ["Essas são nossas bebidas casuais..."],
        "opcoes": ["Café Tradicional", "Refrigerantes (500 mL)", "Café com Leite", "Sucos Naturais", "inicio"]
},

    "valores": {
        "gatilhos": ["Café Tradicional"],
        "respostas": ["O valor do item selecionado é: R$6,00"],
        "opcoes": ["inicio"]
},
    "valores2": {
        "gatilhos": ["Refrigerantes (500 mL)"],
        "respostas": ["O valor do item selecionado é: R$10,00"],
        "opcoes": ["inicio"]
},
    "valores3": {
        "gatilhos": ["Café com Leite"],
        "respostas": ["O valor do item selecionado é: R$7,00"],
        "opcoes": ["inicio"]
},
    "valoresIII": {
        "gatilhos": ["Sucos Naturais"],
        "respostas": ["O valor do item selecionado é: R$10,00"],
        "opcoes": ["inicio"]
},

    "comidas": {
        "gatilhos": ["Comidas"],
        "respostas": ["Essas são nossas bebidas casuais..."],
        "opcoes": ["Pão de Queijo", "Pão na Chapa", "Sanduíches Naturais", "Cookies", "Macarons", "inicio"]
},

    "valores4": {
        "gatilhos": ["Pão de Queijo"],
        "respostas": ["O valor do item selecionado é: R$4,00"],
        "opcoes": ["inicio"]
},
    "valores5": {
        "gatilhos": ["Pão na Chapa"],
        "respostas": ["O valor do item selecionado é: R$6,00"],
        "opcoes": ["inicio"]
},
    "valores6": {
        "gatilhos": ["Sanduíches Naturais"],
        "respostas": ["O valor do item selecionado é: R$5,00"],
        "opcoes": ["inicio"]
},
    "valores7": {
            "gatilhos": ["Cookies"],
            "respostas": ["O valor do item selecionado é: R$18,00"],
            "opcoes": ["inicio"]
},
    "valores8": {
            "gatilhos": ["Macarons"],
            "respostas": ["O valor do item selecionado é: R$8,50"],
            "opcoes": ["inicio"]
},
  

    "combo": {
        "gatilhos": ["Combos"],
        "respostas": ["Esses são nossos combos casuais..."],
        "opcoes": ["COMBO1:(MANHÃ CLASSICA)", "COMBO5:(LEVE DA TARDE)", "COMBO8:(CAFÉ COMPLETO TRADICIONAL)", "COMBO33:(CAFÉ DA MANHÃ ESPECIAL)", "COMBO32:(CAFÉ SIMPLES & CONFORTO)", "inicio"]
},

"valores9": {
            "gatilhos": ["COMBO1:(MANHÃ CLASSICA)"],
            "respostas": ["O valor do item selecionado é: R$22,30"],
            "opcoes": ["inicio"]
},
"valores10": {
            "gatilhos": ["COMBO5:(LEVE DA TARDE)"],
            "respostas": ["O valor do item selecionado é: R$25,50"],
            "opcoes": ["inicio"]
},
"valores11": {
            "gatilhos": ["COMBO8:(CAFÉ COMPLETO TRADICIONAL)"],
            "respostas": ["O valor do item selecionado é: R$29,75"],
            "opcoes": ["inicio"]
},
"valores12": {
            "gatilhos": ["COMBO33:(CAFÉ DA MANHÃ ESPECIAL)"],
            "respostas": ["O valor do item selecionado é: R$23,80"],
            "opcoes": ["inicio"]
},
"valores13": {
            "gatilhos": ["COMBO32:(CAFÉ SIMPLES & CONFORTO)"],
            "respostas": ["O valor do item selecionado é: R$26,00"],
            "opcoes": ["inicio"]
},

#Casuais


#Opção quaternária
"Produtos festas": {
        "gatilhos": ["Produtos para Festas"],                     
        "respostas": ["Quais tipos de produtos festeiros você busca?..."],
        "opcoes": ["Bebidas festa", "Comidas para festa", "Combos para festa"]
},
#Opção quaternária

#festa

"bebidas festeiras": {
        "gatilhos": ["Bebidas festa"],
        "respostas": ["Essas são nossas bebidas para festa..."],
        "opcoes": ["Refrigerantes (500 mL)", "Sucos Naturais", "Café Expresso", "inicio"]
},

"valores14": {
            "gatilhos": ["Refrigerantes (500 mL)"],
            "respostas": ["O valor do item selecionado é: R$10,00"],
            "opcoes": ["inicio"]
},
"valores15": {
            "gatilhos": ["Sucos Naturais"],
            "respostas": ["O valor do item selecionado é: R$10,00"],
            "opcoes": ["inicio"]
},
"valores16": {
            "gatilhos": ["Café Expresso"],
            "respostas": ["O valor do item selecionado é: R$8,00"],
            "opcoes": ["inicio"]
},



"comidas festeiras": {
        "gatilhos": ["Comidas para festa"],
        "respostas": ["Essas são nossas bebidas para festa..."],
        "opcoes": ["Croissants", "Empadas", "Quiches", "Sanduíches Tostados", "Coxinhas", "Pastéis", "Fatias de Bolo Caseiro", "Bombas de Chocolate", "Macarons", "Tortas de Frutas", "Pão de Queijo", "inicio"]
},

"valores17": {
            "gatilhos": ["Croissants"],
            "respostas": ["O valor do item selecionado é: R$12,00"],
            "opcoes": ["inicio"]
},
"valores18": {
            "gatilhos": ["Empadas"],
            "respostas": ["O valor do item selecionado é: R$10,00"],
            "opcoes": ["inicio"]
},
"valores19": {
            "gatilhos": ["Quiches"],
            "respostas": ["O valor do item selecionado é: R$20,00"],
            "opcoes": ["inicio"]
},
"valores20": {
            "gatilhos": ["Sanduíches Tostados"],
            "respostas": ["O valor do item selecionado é: R$5,00"],
            "opcoes": ["inicio"]
},
"valores21": {
            "gatilhos": ["Coxinhas"],
            "respostas": ["O valor do item selecionado é: R$16,00"],
            "opcoes": ["inicio"]
},
"valores22": {
            "gatilhos": ["Pastéis"],
            "respostas": ["O valor do item selecionado é: R$17,50"],
            "opcoes": ["inicio"]
},
"valores23": {
            "gatilhos": ["Fatias de Bolo Caseiro"],
            "respostas": ["O valor do item selecionado é: R$11,00"],
            "opcoes": ["inicio"]
},
"valores24": {
            "gatilhos": ["Bombas de Chocolate"],
            "respostas": ["O valor do item selecionado é: R$10,00"],
            "opcoes": ["inicio"]
},
"valores25": {
            "gatilhos": ["Macarons"],
            "respostas": ["O valor do item selecionado é: R$8,50"],
            "opcoes": ["inicio"]
},
"valores26": {
            "gatilhos": ["Tortas de Frutas"],
            "respostas": ["O valor do item selecionado é: R$20,00"],
            "opcoes": ["inicio"]
},
"valores27": {
            "gatilhos": ["Pão de Queijo"],
            "respostas": ["O valor do item selecionado é: R$4,00"],
            "opcoes": ["inicio"]
},


"combos festeiros": {
        "gatilhos": ["Combos para festa"],
        "respostas": ["Esses são nossos combos para festa..."],
        "opcoes": ["COMBO3:(SALGADO & REFRESCO)", "COMBO6:(CAFÉ BISTRÔ PREMIUM)", "COMBO11:(COMPLETO DA CASA)", "COMBO13:(FESTA SALGADA DOCE)", "COMBO14:(CROISSANT CHOCOLATE LOVER)", "COMBO28:(SALGADO COMPLETO)", "inicio"]
},

"valores28": {
            "gatilhos": ["COMBO3:(SALGADO & REFRESCO)"],
            "respostas": ["O valor do item selecionado é: R$36,10"],
            "opcoes": ["inicio"]
},
"valores29": {
            "gatilhos": ["COMBO6:(CAFÉ BISTRÔ PREMIUM)"],
            "respostas": ["O valor do item selecionado é: R$74,60"],
            "opcoes": ["inicio"]
},
"valores30": {
            "gatilhos": ["COMBO11:(COMPLETO DA CASA)"],
            "respostas": ["O valor do item selecionado é: R$50,00"],
            "opcoes": ["inicio"]
},
"valores31": {
            "gatilhos": ["COMBO13:(FESTA SALGADA DOCE)"],
            "respostas": ["O valor do item selecionado é: R$52,40"],
            "opcoes": ["inicio"]
},
"valores32": {
            "gatilhos": ["COMBO14:(CROISSANT CHOCOLATE LOVER)"],
            "respostas": ["O valor do item selecionado é: R$22,35"],
            "opcoes": ["inicio"]
},
"valores33": {
            "gatilhos": ["COMBO28:(SALGADO COMPLETO)"],
            "respostas": ["O valor do item selecionado é: R$33,00"],
            "opcoes": ["inicio"]
},

#festa


#Opção quinária
"Produtos clima frio": {
        "gatilhos": ["Produtos para ocasiões frias"],                     
        "respostas": ["Quais tipos de produtos para clima frio você busca?..."],
        "opcoes": ["Bebidas para clima frio", "Comidas para clima frio", "Combos para clima frio"]
},
#Opção quinária

#Opções clima frio

"bebidas clima frio": {
        "gatilhos": ["Bebidas para clima frio"],
        "respostas": ["Essas são nossas bebidas para clima frio..."],
        "opcoes": ["Café Tradicional", "Café Extraforte", "Café Expresso", "Macchiato",
                    "Café com Leite", "Chás e Infusões", "Mocha", "Chocolate Quente", "inicio"]
},

"valores34": {
            "gatilhos": ["Café Tradicional"],
            "respostas": ["O valor do item selecionado é: R$6,00"],
            "opcoes": ["inicio"]
},
"valores35": {
            "gatilhos": ["Café Extraforte"],
            "respostas": ["O valor do item selecionado é: R$5,00"],
            "opcoes": ["inicio"]
},
"valores36": {
            "gatilhos": ["Café Expresso"],
            "respostas": ["O valor do item selecionado é: R$8,00"],
            "opcoes": ["inicio"]
},
"valores37": {
            "gatilhos": ["Macchiato"],
            "respostas": ["O valor do item selecionado é: R$13,00"],
            "opcoes": ["inicio"]
},
"valores38": {
            "gatilhos": ["Café com Leite"],
            "respostas": ["O valor do item selecionado é: R$7,00"],
            "opcoes": ["inicio"]
},
"valores39": {
            "gatilhos": ["Chás e Infusões"],
            "respostas": ["O valor do item selecionado é: R$5,00"],
            "opcoes": ["inicio"]
},
"valores40": {
            "gatilhos": ["Mocha"],
            "respostas": ["O valor do item selecionado é: R$8,00"],
            "opcoes": ["inicio"]
},
"valores41": {
            "gatilhos": ["Chocolate Quente"],
            "respostas": ["O valor do item selecionado é: R$7,00"],
            "opcoes": ["inicio"]
},



"comidas clima frio": {
        "gatilhos": ["Comidas para clima frio"],
        "respostas": ["Essas são nossas bebidas para clima frio..."],
        "opcoes": ["Pão na Chapa", "Quiches", "Empadas", "Sanduíches Tostados", "Sanduíches Quentes",
                    "Croque Monsieur / Croque Madame", "Brownies", "Cookies", "inicio"]
},

"valores42": {
            "gatilhos": ["Pão na Chapa"],
            "respostas": ["O valor do item selecionado é: R$6,00"],
            "opcoes": ["inicio"]
},
"valores43": {
            "gatilhos": ["Quiches"],
            "respostas": ["O valor do item selecionado é: R$20,00"],
            "opcoes": ["inicio"]
},
"valores44": {
            "gatilhos": ["Empadas"],
            "respostas": ["O valor do item selecionado é: R$10,00"],
            "opcoes": ["inicio"]
},
"valores45": {
            "gatilhos": ["Sanduíches Tostados"],
            "respostas": ["O valor do item selecionado é: R$5,00"],
            "opcoes": ["inicio"]
},
"valores46": {
            "gatilhos": ["Sanduíches Quentes"],
            "respostas": ["O valor do item selecionado é: R$5,00"],
            "opcoes": ["inicio"]
},
"valores47": {
            "gatilhos": ["Croque Monsieur / Croque Madame"],
            "respostas": ["O valor do item selecionado é: R$45,00"],
            "opcoes": ["inicio"]
},
"valores48": {
            "gatilhos": ["Brownies"],
            "respostas": ["O valor do item selecionado é: R$16,00"],
            "opcoes": ["inicio"]
},
"valores49": {
            "gatilhos": ["Cookies"],
            "respostas": ["O valor do item selecionado é: R$18,00"],
            "opcoes": ["inicio"]
},






"combos clima frio": {
        "gatilhos": ["Combos para clima frio"],
        "respostas": ["Esses são nossos combos para clima frio..."],
        "opcoes": ["COMBO1:(MANHÃ CLASSICA)", "COMBO2:(CHOCOLATE SUPREMO)", "COMBO4:(PARIS DOCE GOURMET)", "COMBO6:(CAFÉ BISTRÔ PREMIUM)", "COMBO7:(ESCOLHA PERFEITA)", "COMBO14:(CROISSANT CHOCOLATE LOVER)", "COMBO16:(CLÁSSICO QUENTE & DOCE)", "COMBO22:(LANCHE RÁPIDO PREMIUM)", "inicio"]
},

"valores50": {
            "gatilhos": ["COMBO1:(MANHÃ CLASSICA)"],
            "respostas": ["O valor do item selecionado é: R$22,30"],
            "opcoes": ["inicio"]
},
"valores51": {
            "gatilhos": ["COMBO2:(CHOCOLATE SUPREMO)"],
            "respostas": ["O valor do item selecionado é: R$19,70"],
            "opcoes": ["inicio"]
},
"valores52": {
            "gatilhos": ["COMBO4:(PARIS DOCE GOURMET)"],
            "respostas": ["O valor do item selecionado é: R$41,90"],
            "opcoes": ["inicio"]
},
"valores53": {
            "gatilhos": ["COMBO6:(CAFÉ BISTRÔ PREMIUM)"],
            "respostas": ["O valor do item selecionado é: R$74,60"],
            "opcoes": ["inicio"]
},
"valores54": {
            "gatilhos": ["COMBO7:(ESCOLHA PERFEITA)"],
            "respostas": ["O valor do item selecionado é: R$24,00"],
            "opcoes": ["inicio"]
},
"valores55": {
            "gatilhos": ["COMBO14:(CROISSANT CHOCOLATE LOVER)"],
            "respostas": ["O valor do item selecionado é: R$22,35"],
            "opcoes": ["inicio"]
},
"valores56": {
            "gatilhos": ["COMBO16:(CLÁSSICO QUENTE & DOCE)"],
            "respostas": ["O valor do item selecionado é: R$25,20"],
            "opcoes": ["inicio"]
},
"valores57": {
            "gatilhos": ["COMBO22:(LANCHE RÁPIDO PREMIUM)"],
            "respostas": ["O valor do item selecionado é: R$30,20"],
            "opcoes": ["inicio"]
},

#Opções clima frio

#Opção senária
"Produtos clima quente": {
        "gatilhos": ["Produtos para ocasiões quentes"],                     
        "respostas": ["Quais tipos de produtos para clima quente você busca?..."],
        "opcoes": ["Bebidas para clima quente", "Comidas para clima quente", "Combos para clima quente"]
},
#Opção senária

#Opções clima quente

"bebidas clima quente": {
        "gatilhos": ["Bebidas para clima quente"],
        "respostas": ["Essas são nossas bebidas para clima quente..."],
        "opcoes": ["Café Tradicional", "Sucos Naturais", "Refrigerantes (500 mL)", "Iced Latte", "Latte", "Affogato", "inicio"]
},

"valores58": {
        "gatilhos": ["Café Tradicional"],
        "respostas": ["O valor do item selecionado é: R$6,00"],
        "opcoes": ["inicio"]
},
"valores59": {
        "gatilhos": ["Sucos Naturais"],
        "respostas": ["O valor do item selecionado é: R$10,00"],
        "opcoes": ["inicio"]
},
"valores60": {
        "gatilhos": ["Refrigerantes (500 mL)"],
        "respostas": ["O valor do item selecionado é: R$10,00"],
        "opcoes": ["inicio"]
},
"valores61": {
        "gatilhos": ["Iced Latte"],
        "respostas": ["O valor do item selecionado é: R$8,50"],
        "opcoes": ["inicio"]
},
"valores62": {
        "gatilhos": ["Latte"],
        "respostas": ["O valor do item selecionado é: R$13,00"],
        "opcoes": ["inicio"]
},
"valores63": {
        "gatilhos": ["Affogato"],
        "respostas": ["O valor do item selecionado é: R$26,00"],
        "opcoes": ["inicio"]
},

"comidas clima quente": {
        "gatilhos": ["Comidas para clima quente"],
        "respostas": ["Essas são nossas bebidas para clima quente..."],
        "opcoes": ["Croissants", "Quiches", "Empadas", "Croque Monsieur / Croque Madame", "Sanduíches Naturais", "Pão de Queijo", "Fatias de Bolo Caseiro", "Tortas de Frutas", "Cookies", "Brownies", "Pudins", "Bombas de Chocolate", "inicio"]
},


"valores64": {
        "gatilhos": ["Croissants"],
        "respostas": ["O valor do item selecionado é: R$12,00"],
        "opcoes": ["inicio"]
},
"valores65": {
        "gatilhos": ["Quiches"],
        "respostas": ["O valor do item selecionado é: R$20,00"],
        "opcoes": ["inicio"]
},
"valores66": {
        "gatilhos": ["Empadas"],
        "respostas": ["O valor do item selecionado é: R$10,00"],
        "opcoes": ["inicio"]
},
"valores67": {
        "gatilhos": ["Croque Monsieur / Croque Madame"],
        "respostas": ["O valor do item selecionado é: R$45,00"],
        "opcoes": ["inicio"]
},
"valores68": {
        "gatilhos": ["Sanduíches Naturais"],
        "respostas": ["O valor do item selecionado é: R$5,00"],
        "opcoes": ["inicio"]
},
"valores69": {
        "gatilhos": ["Pão de Queijo"],
        "respostas": ["O valor do item selecionado é: R$4,00"],
        "opcoes": ["inicio"]
},
"valores70": {
        "gatilhos": ["Fatias de Bolo Caseiro"],
        "respostas": ["O valor do item selecionado é: R$11,00"],
        "opcoes": ["inicio"]
},
"valores71": {
        "gatilhos": ["Tortas de Frutas"],
        "respostas": ["O valor do item selecionado é: R$20,00"],
        "opcoes": ["inicio"]
},
"valores72": {
        "gatilhos": ["Cookies"],
        "respostas": ["O valor do item selecionado é: R$18,00"],
        "opcoes": ["inicio"]
},
"valores73": {
        "gatilhos": ["Brownies"],
        "respostas": ["O valor do item selecionado é: R$16,00"],
        "opcoes": ["inicio"]
},
"valores74": {
        "gatilhos": ["Pudins"],
        "respostas": ["O valor do item selecionado é: R$16,00"],
        "opcoes": ["inicio"]
},
"valores75": {
        "gatilhos": ["Bombas de Chocolate"],
        "respostas": ["O valor do item selecionado é: R$10,00"],
        "opcoes": ["inicio"]
},

"combos clima quente": {
        "gatilhos": ["Combos para clima quente"],
        "respostas": ["Esses são nossos combos para clima quente..."],
        "opcoes": ["COMBO10:(DOCE GELADO SIMPLES)", "COMBO18:(NATURAL FRESH)", "COMBO26:(GELADO NATURAL)", "inicio"]
},

"valores76": {
        "gatilhos": ["COMBO10:(DOCE GELADO SIMPLES)"],
        "respostas": ["O valor do item selecionado é: R$18,90"],
        "opcoes": ["inicio"]
},
"valores77": {
        "gatilhos": ["COMBO18:(NATURAL FRESH)"],
        "respostas": ["O valor do item selecionado é: R$50,00"],
        "opcoes": ["inicio"]
},
"valores78": {
        "gatilhos": ["COMBO26:(GELADO NATURAL)"],
        "respostas": ["O valor do item selecionado é: R$31,00"],
        "opcoes": ["inicio"]
},


#Opções clima quente

#valores
#Opções prontas

    "x": {
        "gatilhos": ["x"],
        "respostas": ["Opção X selecionada"],
        "opcoes": ["inicio"]
},

}

def responder_chatbot(mensagem):
    mensagem = normalizar(mensagem)

    for categoria in respostas_bot.values():
        for gatilho in categoria["gatilhos"]:
            if normalizar(gatilho) == mensagem:
                return {
                    "texto": random.choice(categoria["respostas"]),
                    "opcoes": categoria.get("opcoes", [])
                }

    return {
        "texto": "Ótima escolha!! Confira mais informações no Cardápio...",
        "opcoes": ["inicio"]
    }



@app.route("/chat", methods=["POST"])
def chat():
    dados = request.get_json()
    msg = dados.get("mensagem", "")
    return jsonify(responder_chatbot(msg))


@app.route("/", methods=["GET", "POST"])
def home():
    
    if request.method == "POST":
        return index()
    return redirect(url_for("karinto"))

@app.route("/index", methods=["GET", "POST"])
def index():

    resultado = ""
    nome = ""
    debug_received_raw = None
    debug_received_norm = None
    debug_result = None

    if request.method == "POST":
        nome = request.form.get("produto", "")

        
        with open('search_debug.log', 'a', encoding='utf-8') as f:
            f.write(f"RECEBIDO_RAW: {repr(nome)}\n")
            f.write(f"RECEBIDO_NORM: {repr(normalizar(nome))}\n")

        nome_encontrado, preco_encontrado = buscar_produto_por_nome(nome)

        debug_received_raw = nome
        debug_received_norm = normalizar(nome)
        debug_result = f"{nome_encontrado} | {preco_encontrado}"

        if preco_encontrado is not None:
            resultado = f"R$ {preco_encontrado:.2f}".replace(".", ",")
            nome = nome_encontrado
        else:
            resultado = "Insira um item válido!"

    return render_template("index.html", resultado=resultado, nome=nome,
                           debug_received_raw=debug_received_raw,
                           debug_received_norm=debug_received_norm,
                           debug_result=debug_result)

@app.route("/pagamento", methods=["GET", "POST"])
def pagamento():
    erro = None
    valor = None

    if request.method == "POST":
        valor = request.form.get("valor")

        cartao = request.form.get("cartao", "")
        validade = request.form.get("validade", "")
        cvv = request.form.get("cvv", "")

        if cartao or validade or cvv:
            if not cartao.isdigit() or len(cartao) != 16:
                erro = "Número do cartão inválido"
            elif not validade.isdigit() or len(validade) != 4:
                erro = "Validade inválida"
            elif not cvv.isdigit() or len(cvv) != 3:
                erro = "CVV inválido"
            else:
                return redirect(url_for("carrinho"))

    return render_template("pagamento.html", erro=erro, valor=valor)

@app.route("/carrinho")
def carrinho():
    carrinho = session.get("carrinho", [])

    nomes = [item["nome"] for item in carrinho]
    precos = [f'{item["preco"]:.2f}'.replace(".", ",") for item in carrinho]
    total = sum(item["preco"] for item in carrinho)

    return render_template("carrinho.html",
                           nomes=",".join(nomes),
                           precos=";".join(precos),
                           total=f'{total:.2f}'.replace(".", ","))

@app.route("/adicionar", methods=["POST"])
def adicionar():
    nome = request.form.get("produto", "")

    nome_encontrado, preco_encontrado = buscar_produto_por_nome(nome)

    if preco_encontrado is None:
        return redirect(url_for("index"))

    preco = float(preco_encontrado)

    if "carrinho" not in session:
        session["carrinho"] = []

    carrinho = session["carrinho"]
    carrinho.append({"nome": nome, "preco": preco})

    session["carrinho"] = carrinho

    return redirect(url_for("carrinho"))

@app.route("/karinto")
def karinto():
    return render_template("KarintoCoffe.html")

@app.route("/nos")
def nos():
    return render_template("nos.html")

@app.route("/cardapio")
def cardapio():
    return render_template("cardapio.html")

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/horarios")
def horarios():
    return render_template("horarios.html")

@app.route("/localizacao")
def localizacao():
    return render_template("localizacao.html")

@app.route("/atividade")
def atividade():
    return render_template("atividade05.html")

@app.route("/limpar_carrinho", methods=["POST"])
def limpar_carrinho():
    session.pop("carrinho", None)
    return redirect(url_for("carrinho"))

@app.route("/mapa")
def mapa():
    return render_template("map.html")

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


@app.route('/__debug_db')
def __debug_db():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, preco FROM produtos LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    criar_tabela()
    app.run(debug=True)
