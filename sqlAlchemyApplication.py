from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column, create_engine, inspect, select, func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
    # atributos
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=True)

    user = relationship("User", back_populates="address")

    def __repr__(self):
        return f"Address(id={self.id}, email={self.email_address}"

print(User.__tablename__)
# conexão com o banco de dados
engine = create_engine("sqlite://")

# criando as classes como tabelaas no banco de dados
Base.metadata.create_all(engine)

# depreciado - será removido em futuros release
# print(engine.table_names())

inspector_engine = inspect(engine)
print(inspector_engine.has_table("user_account"))
print(inspector_engine.get_table_names())
print(inspector_engine.default_schema_name)

with Session(engine) as session:
    juliana = User(
        name = 'Juliana',
        fullname = 'Juliana Mascarenhas',
        address=[Address(email_address='julianam@gmail.com')]
    )
    sandy = User(
        name='sandy',
        fullname='Sandy Cardoso',
        address=[Address(email_address='sandyjunior@gmail.com'),
                 Address(email_address='vasco@gmail.com')]
    )
    patrick = User(name='patrick', fullname='Patrick Cardoso')

    # enviando para o BD (persistência de dados)
    session.add_all([juliana, sandy, patrick])

    session.commit()

stmt = select(User).where(User.name.in_(["juliana", 'sandy']))
print("Recuperando usuários a partir de condução de filtragem")
for user in session.scalars(stmt):
    print(user)

stmt_address = select(Address).where(Address.user_id.in_([2]))
print("Recuperando os endereços de email de Sandy")
for address in session.scalars(stmt_address):
    print(address)

order_stmt = select(User).order_by(User.fullname.desc())
print("\nRecuperando info de maneira ordenada")
for result in session.scalars(order_stmt):
    print(result)

stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
print("\n")
for result in session.scalars(stmt_join):
    print(result)


connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir da connection")
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(User)
print('\nTotal de instâncias em User')
for result in session.scalars(stmt_count):
    print(result)