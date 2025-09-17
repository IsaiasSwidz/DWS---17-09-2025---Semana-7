from app import db

class ReceitaIngrediente(db.Model):
    __tablename__ = 'receita_ingredientes'
    receita_id = db.Column(db.Integer, db.ForeignKey('receita.id'), primary_key=True)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'), primary_key=True)
    quantidade = db.Column(db.String(50), nullable=False)

    ingrediente = db.relationship("Ingrediente", back_populates="receitas_associadas")
    receita = db.relationship("Receita", back_populates="ingredientes_associados")

class Chef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    perfil = db.relationship('PerfilChef', back_populates='chef', uselist=False, cascade="all, delete-orphan")
    receitas = db.relationship('Receita', back_populates='chef')

class PerfilChef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    especialidade = db.Column(db.String(100))
    anos_experiencia = db.Column(db.Integer)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef.id'), nullable=False, unique=True)

    chef = db.relationship('Chef', back_populates='perfil')

class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    instrucoes = db.Column(db.Text, nullable=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef.id'), nullable=False)

    chef = db.relationship('Chef', back_populates='receitas')
    ingredientes_associados = db.relationship('ReceitaIngrediente', back_populates='receita', cascade="all, delete-orphan")

class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

    receitas_associadas = db.relationship('ReceitaIngrediente', back_populates='ingrediente', cascade="all, delete-orphan")