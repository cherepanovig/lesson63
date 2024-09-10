# Домашнее задание по теме "Написание примитивной ORM"
# Цель: написать простейшие CRUD функции для взаимодействия с базой данных.

# Установлен Aiogram последней версии для Python 3.12!!!

from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import FSInputFile
import asyncio
from crud_functions import get_all_products, add_user, is_included

# Инициализация бота и диспетчера
TOKEN = "7247438168:AAEOBuL3PvZz8tMAi1lvsg-5DyilPzPY3zU"
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
button_3 = KeyboardButton(text='Купить')

kb = ReplyKeyboardMarkup(keyboard=[[button_1, button_2], [button_3]], resize_keyboard=True)

# Создание инлайн-клавиатуры с 4 кнопками
but_inl_1 = InlineKeyboardButton(text='Продукт1', callback_data='product_buying')
but_inl_2 = InlineKeyboardButton(text='Продукт2', callback_data='product_buying')
but_inl_3 = InlineKeyboardButton(text='Продукт3', callback_data='product_buying')
but_inl_4 = InlineKeyboardButton(text='Продукт4', callback_data='product_buying')

catalog_kb = InlineKeyboardMarkup(inline_keyboard=[
    [but_inl_1],
    [but_inl_2],
    [but_inl_3],
    [but_inl_4]])

# Создание клавиатуры для выбора пола
def gender_keyboard():
    buttons_sex = [KeyboardButton(text="Мужчина"), KeyboardButton(text="Женщина")]
    return ReplyKeyboardMarkup(keyboard=[buttons_sex], resize_keyboard=True, one_time_keyboard=True) # Когда
    # one_time_keyboard=True, клавиатура автоматически скрывается после первого нажатия на любую кнопку

# Создание инлайн-клавиатуры с кнопкой 'регистрация'
but_inl_5 = InlineKeyboardButton(text='Регистрация', callback_data='registr')
registr_kb = InlineKeyboardMarkup(inline_keyboard=[[but_inl_5]])

# Определение состояний регистрации
class RegistrationState(StatesGroup): # создаем класс, который наследуется от группы состояний
    username = State() # экземпляр класса State для определения состояния логина
    email = State()  # экземпляр класса State для определения состояния email
    age = State()  # экземпляр класса State для определения состояния возраста
    #balance = State()  # экземпляр класса State для определения состояния баланса


# Хендлер для нажатия кнопки 'Регистрация'
@router.callback_query(F.data == 'registr')
async def sing_up(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите имя пользователя (только латинский алфавит):")
    await state.set_state(RegistrationState.username)


# Хендлер для установки имени пользователя
@router.message(RegistrationState.username)
async def set_username(message: Message, state: FSMContext):
    username = message.text.strip()
    if is_included(username):
        await message.answer("Пользователь существует, введите другое имя.")
        return
    await state.update_data(username=username)
    await message.answer("Введите свой email:")
    await state.set_state(RegistrationState.email)


# Хендлер для установки email
@router.message(RegistrationState.email)
async def set_email(message: Message, state: FSMContext):
    email = message.text.strip()
    await state.update_data(email=email)
    await message.answer("Введите свой возраст:")
    await state.set_state(RegistrationState.age)


# Хендлер для установки возраста и добавления пользователя
@router.message(RegistrationState.age)
async def set_age(message: Message, state: FSMContext):
    age = message.text.strip()
    if not age.isdigit() or int(age) <= 0:
        await message.answer("Возраст должен быть положительным числом. Пожалуйста, введите корректное значение.")
        return
    await state.update_data(age=int(age))

    # Получаем данные и добавляем пользователя
    data = await state.get_data()
    username = data['username']
    email = data['email']
    age = data['age']

    add_user(username, email, age)  # Добавляем пользователя в базу данных
    await message.answer("Вы успешно зарегистрированы!")
    await state.clear()  # Сброс состояний


# Запуск функции get_all_products из модуля crud_functions
get_all_products()

@router.message(F.text == 'Купить') # Фильтр F.text == 'Купить' проверяет, соответствует ли текст
# входящего сообщения строке 'Купить'
async def get_buying_list(message: types.Message):
    products = get_all_products()
    for product in products:
        id, title, description, price = product
        await message.answer(f"Название: {title} | Описание: {description} | Цена: {price}")
    # for i in range(1, 5):
    #     await message.answer(f"Название: Product{i} | Описание: описание {i} | Цена: {i * 100}")
        file_path = f'files/vit{id}.png'
        try:
            # Открываем файл вручную и передаем его в FSInputFile
            with open(file_path, 'rb') as file:
                photo = FSInputFile(file_path)
                await message.answer_photo(photo)
        except FileNotFoundError:
            await message.answer("Файл не найден.")
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
            print(e)
    await message.answer("Выберите продукт для покупки:", reply_markup=catalog_kb)

# Callback хэндлер, который реагирует на текст "product_buying"
@router.callback_query(F.data == 'product_buying')
async def send_confirm_message(call: CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")


# Определение состояний пользователя
class UserState(StatesGroup):  # создаем класс, который наследуется от группы состояний
    gender = State()  # Добавим еще пол человека
    age = State()  # экземпляр класса State для определения состояния возраста
    growth = State()  # ...состояния роста
    weight = State()  # ...состояния веса


# Проверка, является ли вводимое значение положительным целым числом
# value.isdigit() — проверяем, что строка состоит только из цифр.
# int(value) > 0 — проверяем, что число положительное.
def is_valid_number(value):
    return value.isdigit() and int(value) > 0


# Ответ на нажатие кнопки 'Рассчитать'
@router.message(F.text.lower() == 'рассчитать')
async def set_gender(message: types.Message, state: FSMContext):
    await message.answer("Выберите ваш пол:", reply_markup=gender_keyboard())  # Выбираем пол человека
    await state.set_state(UserState.gender)  # устанавливаем состояние gender, где бот ожидает выбора пола

# Хендлер для обработки выбора пола
@router.message(UserState.gender)
async def set_age(message: types.Message, state: FSMContext):
    gender = message.text.lower() # приводим к нижнему регистру текст кнопок выбора пола
    if gender not in ["мужчина", "женщина"]:
        await message.answer("Пожалуйста, выберите пол, используя кнопки ниже.")
        return
    await state.update_data(gender=gender) # обновляем данные состояния, сохраняя пол пользователя
    await message.answer("Введите свой возраст:", reply_markup=types.ReplyKeyboardRemove()) # бот отправляет
    # сообщение с просьбой ввести возраст и ReplyKeyboardRemove: Убирает клавиатуру после выбора пола
    await state.set_state(UserState.age) # устанавливаем состояние age, где бот ожидает ввода возраста


# Хендлер для обработки возраста
@router.message(UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    if is_valid_number(message.text):
        await state.update_data(age=int(message.text))  # обновляет данные состояния, сохраняя возраст пользователя
        await message.answer("Введите свой рост (в см):")
        await state.set_state(UserState.growth)  # устанавливаем состояние growth, где бот ожидает ввода роста
    else:
        await message.answer("Возраст должен быть положительным числом. Пожалуйста, введите корректное значение.")


# Хендлер для обработки роста
@router.message(UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    if is_valid_number(message.text):
        await state.update_data(growth=int(message.text))  # обновляет данные состояния, сохраняя рост пользователя
        await message.answer("Введите свой вес (в кг):")
        await state.set_state(UserState.weight)  # устанавливаем состояние weight, где бот ожидает ввода вес
    else:
        await message.answer("Рост должен быть положительным числом. Пожалуйста, введите корректное значение.")


# Хендлер для обработки веса и вычисления нормы калорий
@router.message(UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    if is_valid_number(message.text):
        await state.update_data(weight=int(message.text))  # обновляет данные состояния, сохраняя вес пользователя
        data = await state.get_data()  # извлекаем все данные введенные пользователем (пол, возраст, рост, вес)

        gender = data['gender']
        age = data['age']
        growth = data['growth']
        weight = data['weight']

        # Формула Миффлина - Сан Жеора для мужчин и женщин
        if gender == "мужчина":
            calories = 10 * weight + 6.25 * growth - 5 * age + 5
        else:
            calories = 10 * weight + 6.25 * growth - 5 * age - 161

        await message.answer(f"Ваша норма калорий: {calories:.2f} ккал в день.")

        await state.clear()  # Завершение машины состояний
    else:
        await message.answer("Вес должен быть положительным числом. Пожалуйста, введите корректное значение.")

# Ответ на нажатие кнопки 'Информация'
@router.message(F.text == 'Информация')
async def inform(message: types.Message):
    formula_text = ("Формула Миффлина-Сан Жеора:\n"
                    "Для мужчин: 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) + 5\n"
                    "Для женщин: 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161")
    await message.answer(formula_text)


# Команда start
@dp.message(Command("start"))
async def start_form(message: Message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью. Чтобы зарегистрироваться в системе "
                         "нажми 'Регистрация'", reply_markup=registr_kb)
    await message.answer("Если хочешь узнать свою суточную норму калорий, то нажми 'Рассчитать'. "
                         "Если хочешь купить витамины, то нажми 'Купить' "
                         "Если хочешь узнать формулы рассчета калорий то нажми 'Информация", reply_markup=kb)


# Хендлер для перенаправления всех остальных сообщений на start
@router.message(~F.text.lower('Рассчитать') and ~F.state(UserState.age) and ~F.state(UserState.growth)
                and ~F.state(UserState.weight))
async def redirect_to_start(message: types.Message):
    await start_form(message)  # Перенаправляем сообщение на хендлер команды /start


# Основная функция запуска бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())