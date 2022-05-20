from aiogram import Bot, Dispatcher, executor, types
import asyncio
from db import Database
from config import TOKEN, admins

bot = Bot(TOKEN) # токен бота
dp = Dispatcher(bot)

db = Database()

admins = [334537799,] # telegram id админов котором будет отправлять сообщение бот

async def spam():
    while True:
        tasks = db.get_orders() # получение истекших сроков поставки
        
        for order in tasks:
            for admin in admins:
                await bot.send_message(admin, f'Срок поставки заказа №{order[1]} истек!')
            
            db.del_order(int(order[1]))   
        
        
if __name__ == "__main__":
    asyncio.run(spam())