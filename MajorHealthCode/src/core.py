from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler, RegexHandler

from conf.settings import TELEGRAM_TOKEN

import random
# Esse código é apenas para o MVP. Sendo assim, diversos aspectos do projeto final não estão implementadas, como o acesso a uma base de dados SQL(Um dos componentes da variável semanas viria do DB, por exemplo). Além disso, para que o bot funcione é necessário rodá-lo localmente e colocar o seu token, já que ele o processo de deploy não foi feito.
CPF = ""
SET_CPF = range(1)
pontos_classificacao = 0
semanas = 0
def start(bot, update):
    text='Olá, eu sou o Major Health! O astronauta-robô que ajuda a cuidar de você! Caso você já tenha se cadastrado, digite seu CPF! Caso não, preencha esse formulário: https://forms.gle/4qJbVnGVAvwx6CXx5' + update.message.text
    update.message.reply_text(text)
    return SET_CPF

def ajuda(bot, update):
    bot.send_message(
        chat_id = update.message.chat_id,
        text = '/ver_dieta : Ler a sua dieta.\n/ver_treino : Ler o seu treino.\n/ver_meta : Conferir a sua meta semanal.\n/enviar_resultados CLASSIFICAÇÃO : Para enviar resultados em relação a sua meta. CLASSIFICAÇÃO é um número de 1 a 3 definido por você para julgar o seu cumprimento da meta semanal: 1 é não-cumprimento, 2 é cumprimento parcial e 3 é cumprimento total.\n/conferir_classificacao : Para ver a sua classificação. Ela é calculada com base no seu desempenho médio. As classificações são, em ordem crescente: Major Espacial, Capitão Espacial e Aspirante Espacial. Ao atiginir o último nível, você ganha um "dia de luxo"(Um dia em que você pode comer o que quiser)\n/prevencao_covid Para obter informações para se prevnir do COVID-19.'
    )
def ver_dieta(bot, update):
    response_message = "Dieta definida pelo profissional da AEB."
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )
def ver_treino(bot, update):
    response_message = "Treino definido pelo profissional da AEB."
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )
def ver_meta(bot, update):
    response_message = "Meta definida pelo profissional da AEB."
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )
def enviar_resultados(bot, update, args):
    global pontos_classificacao
    global semanas
    pontos_classificacao += int(args[0])
    semanas += 1
    response_message = "Resultados enviados!"
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )
def conferir_classificacao(bot, update):
    global pontos_classificacao
    global semanas
    if semanas > 0:
        media_classificacao = pontos_classificacao/semanas
        if media_classificacao<2 and media_classificacao>=1:
            response_message = "Você é um major espacial!"
        elif media_classificacao<3 and media_classificacao>=2:
            response_message = "Você é um capitão espacial! Mantenha o bom trabalho!"
        elif media_classificacao==3:
            response_message = "Você é um aspirante espacial! Sendo assim, você ganha um dia de luxo! Isso mesmo, você pode comer o que quiser durante um dia! Parabéns pela dedicação!"
    else:
        response_message = "Parece que você ainda não enviou nenhum resultado :("
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )
def prevencao_covid(bot, update):
    bot.send_message(
        chat_id = update.message.chat_id,
        text = 'Lave as mãos frequentemente! \nUse o cotovelo para cobrir a tosse!\nEvite tocar no rosto!\nMatenha o distaciamento social!\nNão saia de casa, se possível!'
    )
def set_cpf(bot, update):
    global CPF
    CPF = update.message.text
    bot.send_message(
        chat_id = update.message.chat_id,
        text = 'CPF encontrando! Agora você tem os seguintes comandos: \n/ver_dieta : Ler a sua dieta.\n/ver_treino : Ler o seu treino.\n/ver_meta : Conferir a sua meta semanal.\n/enviar_resultados CLASSIFICAÇÃO : Para enviar resultados em relação a sua meta.\n/conferir_classificacao : Para ver a sua classificação.\n/prevencao_covid Para obter informações para se prevnir do COVID-19.\nDigite /ajuda, para mais informações'
    )
def main():
    updater = Updater(token=TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            SET_CPF: [RegexHandler(r'^([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})', set_cpf)]
        },

        fallbacks=[CommandHandler('ajuda', ajuda),
                   CommandHandler('ver_dieta', ver_dieta),
                   CommandHandler('ver_treino', ver_treino),
                   CommandHandler('ver_meta', ver_meta),
                   CommandHandler('enviar_resultados', enviar_resultados, pass_args = True),
                   CommandHandler('conferir_classificacao', conferir_classificacao),
                   CommandHandler('prevencao_covid', prevencao_covid)]
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()