
from config import bot

#from photon.client import inline_button
#from photon.utils import format

from photon import OutlineMenu, InlineMenu
from photon.objects import Message
from photon import key, act, explicit_act, back

#from photon.methods import sendMessage

from dbscheme import Product, Order
from sqlalchemy import func


class RegisterMenu(OutlineMenu):
	keyboard = [
		[ ("Orqaga", back()) ],
	]
	async def _act(self):
		self.register()
		return await getattr(self, f"act_{len(self.args)}")()

	async def act_0(self):
		return Message('Ismiggizni kiriting:')

	async def act_1(self):
		name, = self.args
		user = self.context.user
		user.name = name
		user.register_complete = True

		await self.exec(Message('Muvaffaqiyatli yakunlandi'))
		return await self.context.back()

	async def handle_text(self, text):
		return await self.context.explicit_act(RegisterMenu, *self.args, text)

class ProductsMenu(InlineMenu):
	keyboard = [
		[ ("Oldingi", key("prev")), ("Keyingi", key("next")) ],
		[ ("Sotib olish", key("buy")) ],
	]

	def _init(self, product = None, product_id=None):
		if product:
			product_id = product.id

		if not product_id:
			product = self.context.db.query(Product).first()
			product_id = product.id

		self.product_id = product_id
		self.product = product

		super()._init(product_id=product_id)

	async def _act(self):
		self.register()
		return Message(f"Mahsulot: {self.product.name}")


	async def handle_key_prev(self):
		product = self.context.db.query(Product).filter(Product.id<self.product_id).order_by(Product.id.desc()).first()
		if not product: return "Mahsulot topilmadi"
		return await self.context.explicit_act(ProductsMenu, product)
	async def handle_key_next(self):
		product = self.context.db.query(Product).filter(Product.id>self.product_id).first()
		if not product: return "Mahsulot topilmadi"
		return await self.context.explicit_act(ProductsMenu, product)
	async def handle_key_buy(self):
		return "ishlab chiqilmagan"



@bot.set_main_menu
class MainMenu(OutlineMenu):
	keyboard = [
		[ ("Mahsulotlar", act(ProductsMenu) ) ],
		#[ ("Calculate", act(CalculateMenu)) ],
	]
	async def _act(self, arg=None):
		self.register()
		if not self.context.user.register_complete:
			self.keyboard = [[ ("Ro'yxatdan o'tish", act(RegisterMenu) ) ]]
		return Message('Bosh Menyu')