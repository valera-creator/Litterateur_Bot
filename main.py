from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

BOT_TOKEN = '7134752919:AAGCqQM82B3rswT_BgYjxb84hgs3HjkHqFA'
markup = [['да', 'нет']]
reply_markup_yes_no = ReplyKeyboardMarkup(markup, one_time_keyboard=True)

markup2 = [['suphler']]
reply_markup_suphler = ReplyKeyboardMarkup(markup2, one_time_keyboard=True)

text_data = [i.strip() for i in open('text.txt', encoding='utf8')]


async def start(update, context):
    context.user_data['current_string'] = 0
    context.user_data['start'] = True
    context.user_data['check_suphler'] = False
    context.user_data['end_game'] = False
    await update.message.reply_text('Запускаю')
    await update.message.reply_text(
        f"{text_data[context.user_data['current_string']]}")
    context.user_data['current_string'] += 1


async def check_text(update, context):
    text = update.message.text
    if 'start' not in context.user_data:  # пользователь запустит бота в начале без /start
        context.user_data['current_string'] = 0
        context.user_data['start'] = True
        context.user_data['check_suphler'] = False
        context.user_data['end_game'] = False
        await update.message.reply_text('Запускаю')
        await update.message.reply_text(
            f"{text_data[context.user_data['current_string']]}")
        context.user_data['current_string'] += 1
        return

    if context.user_data['end_game']:
        if text.lower() == 'да':
            context.user_data['current_string'] = 1
            context.user_data['end_game'] = False
            await update.message.reply_text(text_data[0], reply_markup=ReplyKeyboardRemove())
            return

        elif text.lower() == 'нет':
            await stop(update, context)
            return

        else:
            await update.message.reply_text('Я не понимаю. Сыграем ещё раз?', reply_markup=reply_markup_yes_no)
            return

    if context.user_data['check_suphler']:
        if text.lower() == 'suphler':
            context.user_data['check_suphler'] = False
            await update.message.reply_text(text_data[context.user_data['current_string']],
                                            reply_markup=ReplyKeyboardRemove())
            if context.user_data['current_string'] >= len(text_data) - 1:
                await update.message.reply_text('Ураааа! да мы с тобой поэты! Хочешь ещё раз??',
                                                reply_markup=reply_markup_yes_no)
                context.user_data['end_game'] = True  # , чтобы отслеживать да или нет в конце стиха
                return

            context.user_data['current_string'] += 1
            return
        check_text_e = text.replace('Ё', 'Е').replace('ё', 'е')
        if check_text_e == text_data[context.user_data['current_string']]:
            if context.user_data['current_string'] >= len(text_data) - 1:
                await update.message.reply_text('Ураааа! да мы с тобой поэты! Хочешь ещё раз??',
                                                reply_markup=reply_markup_yes_no)
                context.user_data['end_game'] = True  # , чтобы отслеживать да или нет в конце стиха
                return

            await update.message.reply_text(text_data[context.user_data['current_string'] + 1],
                                            reply_markup=ReplyKeyboardRemove())
            context.user_data['current_string'] += 2
            context.user_data['check_suphler'] = False

            if context.user_data['current_string'] >= len(text_data):
                await update.message.reply_text('Ураааа! да мы с тобой поэты! Хочешь ещё раз??',
                                                reply_markup=reply_markup_yes_no)
                context.user_data['end_game'] = True  # , чтобы отслеживать да или нет в конце стиха
            return

        else:
            await update.message.reply_text(
                f"Неправильно, нажми на suphler, чтобы увидеть текст",
                reply_markup=reply_markup_suphler)
            return
    check_text_e = text.replace('Ё', 'Е').replace('ё', 'е')
    if check_text_e == text_data[context.user_data['current_string']]:
        if context.user_data['current_string'] >= len(text_data) - 1:
            await update.message.reply_text('Ураааа! да мы с тобой поэты! Хочешь ещё раз??',
                                            reply_markup=reply_markup_yes_no)
            context.user_data['end_game'] = True  # , чтобы отслеживать да или нет в конце стиха
            return

        await update.message.reply_text(text_data[context.user_data['current_string'] + 1])
        context.user_data['current_string'] += 2

        if context.user_data['current_string'] >= len(text_data):
            await update.message.reply_text('Ураааа! да мы с тобой поэты! Хочешь ещё раз??',
                                            reply_markup=reply_markup_yes_no)
            context.user_data['end_game'] = True  # , чтобы отслеживать да или нет в конце стиха
        return
    else:
        await update.message.reply_text(
            f"Неправильно, нажми на suphler, чтобы увидеть текст",
            reply_markup=reply_markup_suphler)
        context.user_data['check_suphler'] = True


async def stop(update, context):
    await update.message.reply_text(f"Пока, пока)", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()  # очищаем словарь с пользовательскими данными
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler(["start"], start))
    application.add_handler(CommandHandler(["stop"], stop))
    text_handler = MessageHandler(filters.TEXT, check_text)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
