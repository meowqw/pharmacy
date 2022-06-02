import aiogram.utils.markdown as md
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, executor
import settings
from barcode import get_code
from db import DB


# bot init
bot = Bot(token=settings.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Goods(StatesGroup):
    code = State()
    data = State()

class Review(StatesGroup):
    data = State()
    good_id = State()
    review_text = State()
    rating = State()


# KEYBOARD
pharmacy = types.KeyboardButton('➕ Аптеки')
search = types.KeyboardButton('🔎 Товары')
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(search)
keyboard.add(pharmacy)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    """START HANDLING"""
    await bot.send_message(message.chat.id, 'Для навигации используйте кнопки снизу.', reply_markup=keyboard)

    # save user data to base
    try:
        data = {'id': message.chat.id, 'login': message.chat.username,
                'username': message.chat.first_name}
        DB().add_user(data)
    except Exception as e:
        await bot.send_message(message.chat.id, e)


@dp.message_handler()
async def message_text_controller(message: types.Message):
    """TEXT Controller"""

    # pharmacy btn
    if message.text == '➕ Аптеки':
        for pharmacy in DB().get_all_pharmacy():
            await bot.send_message(message.chat.id, f"""🅰 {pharmacy[1]}\nАдрес: {pharmacy[2]}\nТелефон: {pharmacy[3]}\nГрафик работы: {pharmacy[4]}""")

    # search btn
    if message.text == '🔎 Товары':

        title_search = types.InlineKeyboardButton(
            '🔼 Название ', callback_data='title_search')
        barcode_search = types.InlineKeyboardButton(
            '🔽 Ввод шрихкода вручную ', callback_data='barcode_search')

        keyboard = types.InlineKeyboardMarkup().add(title_search).add(barcode_search)

        await bot.send_message(message.chat.id, 'Выберите способ поиска ручного ввода или просто отправьте изображение штрихкода: ', reply_markup=keyboard)



# SEARCH HANDLING
@dp.callback_query_handler(lambda call: call.data == 'title_search')
async def callback_search_title(callback_query: types.CallbackQuery):
    """Title"""
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введите название полностью или его часть.')

    await Goods.data.set()

@dp.message_handler(content_types=['photo'])
async def barcode_img(message):
    img_id = message.photo[-1]['file_unique_id']
    await message.photo[-1].download(f"{settings.IMG_BAR}{img_id}.jpg")
    await bot.send_message(message.chat.id, 'Обработка запроса...')
    result = get_code(img_id)
    result = DB().get_good_by_id(result)
     # output info
    if result != None:
        try:
            data_result = result[0]
            barcode = data_result[0]
            title = data_result[1]
            manufacturer = data_result[2]
            img = settings.IMG_PATH + data_result[3]
            info = data_result[4]
            price = data_result[5]
            if data_result[6] == 1:
                leave_condition = 'Да'
            else:
                leave_condition = 'Нет'

            # good menu keuboard
            available_check = types.InlineKeyboardButton('❓ Наличие', callback_data=f'available_check_{barcode}')
            reviews_view = types.InlineKeyboardButton('📋 Отзывы', callback_data=f'reviews_view_{barcode}')
            reviews_write = types.InlineKeyboardButton('✏ Написать отзыв', callback_data=f'reviews_write_{barcode}')

            keyboard = types.InlineKeyboardMarkup().add(available_check).add(reviews_view).add(reviews_write)
            await bot.send_photo(message.chat.id, photo=open(img, 'rb'), caption=f"*Название:* {title} " +
                                                                                f"\n*Производитель:* {manufacturer}\n" + 
                                                                                f"*Описание:* {info}\n\n" + 
                                                                                f"*💷 Цена:* {price} руб\n" + 
                                                                                f"*Отпуск без рецепта:* {leave_condition}\n" + 
                                                                                f"*Штрихкод:* {barcode}", parse_mode="Markdown", reply_markup=keyboard)
        except Exception as e:
            await bot.send_message(message.chat.id, 'К сожалению я не смог ничего найти 😞')
    
    else:
        await bot.send_message(message.chat.id, 'К сожалению я не смог ничего найти 😞')


# SEARCH HANDLING
@dp.callback_query_handler(lambda call: call.data == 'barcode_search')
async def callback_search_barcode(callback_query: types.CallbackQuery):
    """Barcode"""

    
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введите штрихкод.')

    await Goods.data.set()


@dp.message_handler(state=Goods.data)
async def search_title(message: types.Message, state: FSMContext):
    """ Search title """

    async with state.proxy() as data:
        result = DB().get_good_by_title(message.text)
        if len(result) == 0:
            result = DB().get_good_by_id(message.text)
            
        # output info
        if len(result):
            try:
                data_result = result[0]
                barcode = data_result[0]
                title = data_result[1]
                manufacturer = data_result[2]
                img = settings.IMG_PATH + data_result[3]
                info = data_result[4]
                price = data_result[5]
                if data_result[6] == 1:
                    leave_condition = 'Да'
                else:
                    leave_condition = 'Нет'

                # good menu keuboard
                available_check = types.InlineKeyboardButton('❓ Наличие', callback_data=f'available_check_{barcode}')
                reviews_view = types.InlineKeyboardButton('📋 Отзывы', callback_data=f'reviews_view_{barcode}')
                reviews_write = types.InlineKeyboardButton('✏ Написать отзыв', callback_data=f'reviews_write_{barcode}')

                keyboard = types.InlineKeyboardMarkup().add(available_check).add(reviews_view).add(reviews_write)
                await bot.send_photo(message.chat.id, photo=open(img, 'rb'), caption=f"*Название:* {title} " +
                                                                                    f"\n*Производитель:* {manufacturer}\n" + 
                                                                                    f"*Описание:* {info}\n\n" + 
                                                                                    f"*💷 Цена:* {price} руб\n" + 
                                                                                    f"*Отпуск без рецепта:* {leave_condition}\n" + 
                                                                                    f"*Штрихкод:* {barcode}", parse_mode="Markdown", reply_markup=keyboard)
            except Exception as e:
                await bot.send_message(message.chat.id, 'Я нашел товар, но вам его не покажу 😞')
        
        else:
            await bot.send_message(message.chat.id, 'К сожалению я не смог ничего найти 😞')

        await state.finish()

# MENU Goods

# available check
@dp.callback_query_handler(lambda call: 'available_check' in call.data)
async def callback_available_check(callback_query: types.CallbackQuery):

    id_ = callback_query.data.split('_')[-1]
    pharmacy = DB().get_pharmacy_available_by_id(id_)
    if len(pharmacy) > 0:
        await bot.send_message(callback_query.from_user.id, 'Данный товар в наличии в: ')
        for i in pharmacy:
            await bot.send_message(callback_query.from_user.id, f'✅ {i[1]}\nАдрес: {i[2]}\nТелефон: {i[3]}\nГрафик работы: {i[4]}')
    else:
        await bot.send_message(callback_query.from_user.id, 'Данного товара в наличии нет 😞')
    

# reviews write
@dp.callback_query_handler(lambda call: 'reviews_write' in call.data)
async def callback_reviews_write(callback_query: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        id_ = callback_query.data.split('_')[-1]
        await state.update_data(good_id=str(id_))

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '📝 Введите текст отзыва.')
    # await state.finish()
    await Review.review_text.set()

@dp.message_handler(state=Review.review_text)
async def reviews_write(message: types.Message, state: FSMContext):
    """ Review write text """
    async with state.proxy() as data:
        await state.update_data(review_text=str(message.text))
        await bot.send_message(message.chat.id, '⭕ Введите вашу оценку товару (0-10).')
        await Review.rating.set()
        # await Review.next()

@dp.message_handler(state=Review.rating)
async def reviews_write_rating(message: types.Message, state: FSMContext):
    """ Review write rating """
    async with state.proxy() as data:
        # print(Review.good_id)
        # print(Review.review_text)
        # print(message.text)
        try:
            data_ = {'id_user': message.chat.id, 'id_good': str(data['good_id']), 'text': str(data['review_text']), 'rating': int(message.text)}
            DB().add_review(data_)
            await bot.send_message(message.chat.id, 'Ваш отзыв успешно добавлен 🗒')
        except Exception as e:
            print(e)
            await bot.send_message(message.chat.id, 'Произошла ошибка, проверьте вводимые вами данные 😞')

        await state.finish() 

       

        
# reviews view
@dp.callback_query_handler(lambda call: 'reviews_view' in call.data)
async def callback_reviews_view(callback_query: types.CallbackQuery):

    id_ = callback_query.data.split('_')[-1]
    data = DB().get_reviews_by_id(id_)
    if len(data) > 0:
        average_score = sum([i[-1] for i in data]) / len(data)
        await bot.send_message(callback_query.from_user.id, f'🏆 Средний рейтинг {average_score} / 10')

        for n, i in enumerate(data):
            await bot.send_message(callback_query.from_user.id, f'🗒 Отзыв № {n+1}\n*Текст:* {i[2]}\n*Оценка*: {i[-1]}', parse_mode="Markdown")

    else:
        await bot.send_message(callback_query.from_user.id, "На данный товар еще нет отзывов 😞")

def start():
    executor.start_polling(dp, skip_updates=True)
