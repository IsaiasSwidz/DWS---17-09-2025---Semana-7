import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Caminho base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

# Cria instância da aplicação Flask
app = Flask(__name__)

# Configurações do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'receitas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Cria a pasta instance se não existir
instance_path = os.path.join(basedir, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

# Inicializa o banco
db = SQLAlchemy(app)

# Importa os modelos
from models import Chef, PerfilChef, Receita, Ingrediente, ReceitaIngrediente

# --- Rotas ---
@app.route('/')
def index():
    receitas = Receita.query.all()
    return render_template('index.html', receitas=receitas)

@app.route('/receita/nova', methods=['GET', 'POST'])
def criar_receita():
    if request.method == 'POST':
        titulo = request.form['titulo']
        instrucoes = request.form['instrucoes']
        chef_id = request.form['chef_id']

        nova_receita = Receita(titulo=titulo, instrucoes=instrucoes, chef_id=chef_id)
        db.session.add(nova_receita)

        ingredientes_str = request.form['ingredientes']
        pares_ingredientes = [par.strip() for par in ingredientes_str.split(',') if par.strip()]

        for par in pares_ingredientes:
            if ':' in par:
                nome, qtd = par.split(':', 1)
                nome_ingrediente = nome.strip().lower()
                quantidade = qtd.strip()

                ingrediente = Ingrediente.query.filter_by(nome=nome_ingrediente).first()
                if not ingrediente:
                    ingrediente = Ingrediente(nome=nome_ingrediente)
                    db.session.add(ingrediente)

                associacao = ReceitaIngrediente(receita=nova_receita, ingrediente=ingrediente, quantidade=quantidade)
                db.session.add(associacao)

        db.session.commit()
        return redirect(url_for('index'))

    chefs = Chef.query.all()
    return render_template('criar_receita.html', chefs=chefs)

@app.route('/chef/<int:chef_id>')
def detalhes_chef(chef_id):
    chef = Chef.query.get_or_404(chef_id)
    return render_template('detalhes_chef.html', chef=chef)

# --- Comando para inicializar banco ---
@app.cli.command('init-db')
def init_db_command():
    """Cria as tabelas e popula com dados de exemplo."""
    db.drop_all()
    db.create_all()

    chef1 = Chef(nome='Ana Maria')
    perfil1 = PerfilChef(especialidade='Culinária Brasileira', anos_experiencia=25, chef=chef1)
    chef2 = Chef(nome='Érick Jacquin')
    perfil2 = PerfilChef(especialidade='Culinária Francesa', anos_experiencia=30, chef=chef2)

    ingredientes = {
        'tomate': Ingrediente(nome='tomate'),
        'cebola': Ingrediente(nome='cebola'),
        'farinha': Ingrediente(nome='farinha'),
        'ovo': Ingrediente(nome='ovo'),
        'manteiga': Ingrediente(nome='manteiga')
    }

    db.session.add_all([chef1, chef2] + list(ingredientes.values()))

    receita1 = Receita(titulo='Molho de Tomate Clássico', instrucoes='...', chef=chef1)
    receita2 = Receita(titulo='Bolo Simples', instrucoes='...', chef=chef1)
    receita3 = Receita(titulo='Petit Gâteau', instrucoes='...', chef=chef2)
    db.session.add_all([receita1, receita2, receita3])

    db.session.add_all([
        ReceitaIngrediente(receita=receita1, ingrediente=ingredientes['tomate'], quantidade='5 unidades'),
        ReceitaIngrediente(receita=receita1, ingrediente=ingredientes['cebola'], quantidade='1 unidade'),
        ReceitaIngrediente(receita=receita2, ingrediente=ingredientes['farinha'], quantidade='2 xícaras'),
        ReceitaIngrediente(receita=receita2, ingrediente=ingredientes['ovo'], quantidade='3 unidades'),
        ReceitaIngrediente(receita=receita3, ingrediente=ingredientes['manteiga'], quantidade='150g')
    ])

    db.session.commit()
    print('Banco de dados inicializado com sucesso!')

if __name__ == '__main__':
    app.run(debug=True)