import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import difflib
import os
import datetime
import pdfOperator
import dbOperator
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, CallbackQueryHandler, MessageHandler
from datetime import time
import hashlib
import pytz
import fitz

TOKEN = os.environ.get("TOKEN")
#TOKEN = "your-url"
print(f"{TOKEN} initialized.")


available_commands = {
    '/abonelik': 'abonelik',
    '/start': 'start',
    '/menu': 'menu',
    '/idogren': 'idogren',
    '/abonelikiptal': 'abonelikiptal',
    '/duyuruyap': 'duyuruyap',
    '/aylikmenu': 'aylikmenu',
    '/adminekle': 'adminekle',
    '/adminsil': 'adminsil',
    '/komutlar': 'komutlar',
}
istanbul_tz = pytz.timezone('Europe/Istanbul')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

pdfOp = pdfOperator.PdfOp()
dbOp = dbOperator.DbOperator()

if not pdfOp.read_pdf():
    dbOp.save_log("PDF ERROR : \nThe menu cannot be downloaded automatically. Refresh manually!")




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = update.effective_sender
    dbOp.addSub(sender=sender)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bursa Teknik Üniversitesi yemekhane botuna hoşgeldiniz.\nKullanabileceğiniz komutlara ulaşmak için : /komutlar")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE,args):
    menu_list = pdfOp.menu_list
    if not menu_list:
        dbOp.save_log("MENU ERROR : There's a error with menu! Refresh manually!")
        await alertAdmins(context=context, text="Birisi menü hatası aldı!!")
        return
    try:
        day = args
        if not day:
            day = datetime.datetime.now().day
        day = int(day)
    except ValueError:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Lütfen geçerli bir gün girin. Örneğin /menu 23 size olduğunuz ayın 23.günündeki menüyü verir.")      
        return
    
    if day < 1 or day > 31: 
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Lütfen geçerli bir gün girin. Örneğin /menu 23 size olduğunuz ayın 23.günündeki menüyü verir.")
        return
    
    text = pdfOp.getText(day)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def idogren(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_sender.id
    username = update.effective_sender.username
    text = f"{username} isimli kullanıcının idsi : \n{user_id}"
    await context.bot.send_message(chat_id=user_id, text=text)
async def abonelik(update: Update, context: ContextTypes.DEFAULT_TYPE):

    sender_id = update.effective_sender.id
    answer = dbOp.addMenuSub(sender_id)
    
    if not answer:
        text = "Kullanıcı zaten kayıtlı. Kaydınızı silmek için /abonelikiptal"
    elif answer:
        text = "Kayıt başarılı! Her sabah saat 09.00'da menüyü alacaksınız."
        dbOp.save_log(f"New menu subscriber! User id : {sender_id}     -     Username : {update.effective_sender.username}")
    await context.bot.send_message(chat_id=sender_id, text=text)

async def abonelikiptal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_id = update.effective_sender.id
    if dbOp.leaveMenuSub(sender_id):
        text = "Kaydınız başarıyla silindi. Yeniden kayıt olmak isterseniz /abonelik"
        dbOp.save_log(f"Subscriber left! User id : {sender_id}     -     Username : {update.effective_sender.username}")
    else:
        text = "Kaydınız bulunamadı veya bir hata oluştu."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def sendMenu(context: ContextTypes.DEFAULT_TYPE):
    all_subs = dbOp.getMenuSubs()
    if all_subs:
        text = pdfOp.getText(datetime.datetime.now().day) 
        for sub_id in all_subs:
            await context.bot.send_message(chat_id=sub_id, text=text)
            dbOp.save_log(f"DAILY MENU SENT!! Menu sent to chat_id: {sub_id} at {datetime.datetime.now()}")
async def alertAdmins(context: ContextTypes.DEFAULT_TYPE, text):
    admins_id = dbOp.getAdmins()
    for admin in admins_id:
        await context.bot.send_message(chat_id=admin,text=text)


async def updateMenu(context: ContextTypes.DEFAULT_TYPE):
    pdfOp.get_pdf()
    st = pdfOp.read_pdf()
    if not st:
        dbOp.save_log("PDF ERROR : \nThe menu cannot be downloaded automatically. Refresh manually!")
        await alertAdmins(context=context,text="Menü yenilenirken bir hata oluştu!!!!")

async def duyuruyap(update: Update, context: ContextTypes.DEFAULT_TYPE,args):
    user_id = update.effective_sender.id
    staffcheck = dbOp.checkStaff(user_id)


    if staffcheck != 1:
        await update.message.reply_text("Duyuru yapmak için admin olmalısın.")
        return
    #context_list = context.args
    #args = ""
    #for arg in context_list:
    #    args+= f"{arg} "
    hash_object = hashlib.sha256(args.encode())
    hex_dig = hash_object.hexdigest()
    dbOp.dict_ekle(hex_dig,args)


    if not args:
        await update.message.reply_text("Duyuru boş olamaz.")
        return
    keyboard = [
        [
            InlineKeyboardButton("Evet", callback_data=f"{hex_dig}"),
            InlineKeyboardButton("Hayır", callback_data="False"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"{args}\nÜstteki metni kayıtlı bütün kullanıcılara duyurmak istediğinize emin misiniz?", reply_markup=reply_markup) 

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()
    choose = query.data
    if choose == "False":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Duyuru iptal edildi.")
    else:
        choose = dbOp.dict_cek(choose)
        all_subs = dbOp.getSubs()
        if all_subs:
            i=0
            for sub_id in all_subs:
                i+=1
                text = f"Duyuru: \n\n{choose}"
                await context.bot.send_message(chat_id=sub_id, text=text)
            dbOp.save_log(f"{update.effective_sender.username} just made an announcement!! Text : {text} at {datetime.datetime.now()}")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Duyuru toplam {i} kişiye yapıldı.")
async def aylikmenu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pdf_document = pdfOp.menu_folder
    await context.bot.send_message(chat_id=update.effective_chat.id,text="İşte bu ayın menüsü:")
    await context.bot.send_document(chat_id=update.effective_chat.id,document=pdf_document)
    doc = fitz.open(pdf_document)

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num) 
        pix = page.get_pixmap() 
        output = f'menuler/page_{page_num + 1}.png' 
        pix.save(output) 
        await context.bot.send_document(chat_id=update.effective_chat.id,document=output)
        

    doc.close()
async def adminekle(update: Update, context: ContextTypes.DEFAULT_TYPE,args):

    user_id = update.effective_sender.id
    adminname = update._effective_sender.username
    num = dbOp.checkStaff(user_id)
    if not args:
            text = "Admin yapılacak kişinin kullanici id'Sini giriniz.\n Örnek kullanım: /adminekle userID \nUser id şuradan öğrenilebilir : /idogren"
    else:
        arg_id = args
    if num==1 and args:
        if str(arg_id) == str(user_id):
            text= "Kendinle ilgili işlem yapamazsın."
        else:
            text, check= dbOp.addStaff(arg_id=arg_id)
            if check:
                await context.bot.send_message(chat_id=arg_id, text=f"{adminname} isimli kişi seni admin yaptı.")
    elif num==2:
        text = "Abone degilsin. Önce /abonelik komutunu kullan."
    elif num==0:
        text = "Yetkiniz bulunmamakta."
    await context.bot.send_message(chat_id=user_id, text=text)
        
   
async def adminsil(update: Update, context: ContextTypes.DEFAULT_TYPE,args):

    user_id = update.effective_sender.id
    adminname = update._effective_sender.username
    num = dbOp.checkStaff(user_id)
    if not args:
        text = "Admin yapılacak kişinin kullanici id'Sini giriniz.\n Örnek kullanım: /adminekle userID \nUser id şuradan öğrenilebilir : /idogren"
    else:
        arg_id = args
    
    if num==1 and args:
        if str(arg_id) == str(user_id):
            text= "Kendinle ilgili işlem yapamazsın."
        else:
            text, check= dbOp.deleteStaff(arg_id)
            if check:
                await context.bot.send_message(chat_id=arg_id, text=f"{adminname} isimli kişi senin adminliğini aldı.")
    elif num==2:
        text = "Abone degilsin. Önce /abonelik komutunu kullan."
    elif num==0:
        text = "Yetkiniz bulunmamakta."
    await context.bot.send_message(chat_id=user_id, text=text)
async def komutlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text='''/aylikmenu -> bulunduğumuz ayın menüsünü pdf ve resim olarak iletir.
    \n/abonelik -> abonelere her sabah saat 09.00'da günün menüsünü mesaj olarak iletilir.
    \n/abonelikiptal -> aboneliğini iptal edilebilir.
    \n/menu -> günün menüsünü bu komutla öğrenilebilir /menu 8 seklindeki kullanım bulunduğumuz ayın 8.günündeki menüyü iletir.
    \nHerhangi bir sorununuz için @efekanaksoy35 'e ulaşabilirsiniz.'''
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
async def pdfyukle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_id = update.effective_sender.id
    if dbOp.checkStaff(sender_id) != 1:
        return
    file = await context.bot.get_file(update.message.document)
    check = pdfOp.manuel_pdf(file)
    if not check:
        await context.bot.send_message(chat_id=sender_id, text="Pdf içeriği uygun değil.. Değişim gerçekleştirilmedi.")
    else:
        await context.bot.send_message(chat_id=sender_id, text="Pdf başarıyla değiştirildi.")


def check_command(user_input, available_commands):
    closest_matches = difflib.get_close_matches(user_input, available_commands.keys(), n=1, cutoff=0.6)
    if closest_matches:
        return closest_matches[0]
    return None

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text 
    user_id = update.effective_sender.id
    user_name = update.effective_sender.username
    dbOp.save_log(f"BASIC LOG: User id : {user_id}     -     Username : {user_name}     -     Content : {user_input}     -     Time : {datetime.datetime.now()}")


    if user_input.startswith("/"):
        command_parts = user_input.split()
        command = command_parts[0]
        args = command_parts[1:]     
        if command == "/menu" or command == "/adminekle" or command == "/adminsil" or command == "/duyuruyap":
            content = ""
            if args:
                if len(args) == 1:
                    content = args[0]
                else:
                    for arg in args:
                        content += f"{arg} "
            func_to_call = available_commands[command]
            await globals()[func_to_call](update, context, content)
            return

        correct_command = check_command(user_input, available_commands)
        if correct_command:
            if user_input != correct_command:
                await update.message.reply_text(f"{correct_command}' mı demek istediniz? \n\n/komutlar yazarak bütün komutlara erişebilirsiniz.")
            else:
                function_to_call = available_commands[correct_command]
                await globals()[function_to_call](update, context) 
        else:
            await update.message.reply_text("Geçersiz komut. /komutlar yazarak bütün komutlara erişebilirsiniz..")
    else:
        await update.message.reply_text("Merhaba.. Sadece komutla çalışmaktayım. /komutlar yazarak bütün komutlara erişebilirsin.")

if __name__ == '__main__':
    
    application = ApplicationBuilder().token(token=TOKEN).build()
    
    application.job_queue.run_daily(sendMenu,days=(1,2,3,4,5), time=time(9,0,tzinfo=istanbul_tz)) 
    application.job_queue.run_monthly(updateMenu,when=time(8,00,tzinfo=istanbul_tz),day=5)

    command_handler = MessageHandler(filters.COMMAND, message_handler)
    message_handlerr = MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)

    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.Document.ALL, pdfyukle))
    application.add_handler(message_handlerr)
    application.add_handler(command_handler)
    application.run_polling()
