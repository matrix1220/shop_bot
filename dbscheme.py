
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Integer, String, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey

from sqlalchemy.ext.mutable import Mutable, MutableList, MutableDict

from sqlalchemy.types import TypeDecorator, VARCHAR, JSON
import json

class JSONEncoded(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None: value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None: value = json.loads(value)
        return value

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	menu_stack = Column(MutableList.as_mutable(JSONEncoded), nullable=False)
	shared_data = Column(JSON)
	keyboard = Column(MutableDict.as_mutable(JSONEncoded))
	language = Column(Integer)
	last_time = Column(Integer)
	blocked = Column(Boolean, default=False)

	name = Column(String)
	register_complete = Column(Boolean, default=False)

	def __init__(self, menu_stack=[], keyboard={}, **kwargs):
		super().__init__(menu_stack=menu_stack, keyboard=keyboard, **kwargs)

class Message(Base): # InlineMenu
	__tablename__ = 'messages'

	chat_id = Column(Integer, primary_key=True)
	message_id = Column(Integer, primary_key=True)
	content = Column(MutableDict.as_mutable(JSONEncoded))
	menu_stack = Column(MutableList.as_mutable(JSONEncoded), nullable=False)
	shared_data = Column(JSON)
	#menu_arguments = Column(MutableObject.as_mutable(JSONEncoded))
	keyboard = Column(MutableDict.as_mutable(JSONEncoded))
	sent_at = Column(Integer)

	def __init__(self, menu_stack=[], keyboard={}, **kwargs):
		super().__init__(menu_stack=menu_stack, keyboard=keyboard, **kwargs)


class Product(Base):
	__tablename__ = 'products'

	id = 		Column(Integer, primary_key=True)
	name = 		Column(String)

class OrderItem(Base):
	__tablename__ = 'order_items'

	user_id = 	Column(Integer, primary_key=True)
	order_id = 	Column(Integer, primary_key=True)
	product_id = Column(Integer, primary_key=True)

class Order(Base):
	__tablename__ = 'orders'

	user_id = 	Column(Integer, primary_key=True)
	id = 		Column(Integer, primary_key=True)




from config import engine
Base.metadata.create_all(engine)