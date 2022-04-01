from flask import Flask, render_template, request
import datetime
import json

app = Flask(__name__)

DB_FILE = "./data/db.json"  # Путь к файлу с сообщениями
db = open(DB_FILE, "rb")  # Открываем файл для чтения
data = json.load(db)  # Загрузить все данные в формате JSON из файла
messages = data["messages"]  # Из полученных данных берем поле messages


#  Функция для сохранения всех сообщений (в списке message) в файл
def save_messages_to_file():
    db = open(DB_FILE, "w")  # Открываем файл для записи
    data = {   # Создаем структуру для записи в файл
        "messages": messages
    }
    json.dump(data, db)  # Записываем структуру в файл



def add_message(text, sender):  # Объявим функцию, которая добавит сообщение в список
    now = datetime.datetime.now()  # текущее время и дата
    new_message = {
        "text": text,
        "sender": sender,
        "time": now.strftime("%H:%M")  # Текущий час:минуты
    }

    messages.append(new_message)  # Добавляем новое сообщение в список
    save_messages_to_file()


def print_message(message):  # Объявляем функцию, которая будет печатать одно сообщение
    print(f"[{message['sender']}]: {message['text']} / {message['time']} ")


# Главная страница
@app.route("/")
def index_page():
    return "Здравствуйте, вас приветствует СкиллЧат2022"


# Показать все сообщения в формате JSON
@app.route("/get_messages")
def get_messages():
    return {"messages": messages}


# Показать форму чата
@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/send_message")
def send_message():
    #  Получить имя и текст от пользователя
    name = request.args["name"]  # Получаем имя
    if len(name) < 3 or len(name) > 100: return "ERROR"
    text = request.args["text"]  # Получаем текст
    if len(text) < 1 or len(text) > 3000: return "ERROR"
    #  Вызвать функцию add_message
    add_message(text, name)
    return "OK"

@app.route("/clear_data")
def clear_data():
    messages.clear()
    return "messages are clear"

app.run()  # Запускаем веб-приложение


# # Форма чата в формате html и скрипт JS
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Skillbox Chat</title>

#     <!-- Подключение библиотеки jQuery-->
#     <script
#         src="https://code.jquery.com/jquery-3.6.0.min.js"
#         integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4="
#         crossorigin="anonymous">
#     </script>

#     <!-- Код взаимодействия с сервером -->
#     <script language="JavaScript">
#         // Загрузка и отображение сообщений
#         function loadMessages() {
#            $.get(
#             "/get_messages",
#             (data) => {
#                 $("#chat_window").empty();
#                 var messages = data["messages"];
#                 for (var i in messages) {
#                     var message = messages[i];
#                     var name = message["sender"];
#                     var text = message["text"];
#                     var time = message["time"];
#                     console.log(name, text, time);
#                     var html = "<div> [<b> " + name + " </b>]: " + text + " <i>" + time + "</i> </div>";
#                     var div = $(html); // div = визуальный элемент с сообщением

#                     $("#chat_window").append(div);
#                 }
#             }
#            );
#         }

#         // Отправка сообщения
#         function sendMessage() {
#             var name = $("#name").val(); // Кладем текст из поля "name" в переменную
#             var text = $("#text").val();
#             $.get("/send_message", { "name" : name, "text" : text});

#             $("#text").val("");
#         }

#         // При загрузке страницы
#         $(() => {
#            // При нажатии клавиш в поле текст
#            $("#text").on("keypress", (event) => {
#                 // При нажатии Enter, вызвать функцию sendMessage
#                 if (event.keyCode == 13) {
#                     sendMessage();
#                 }
#            });

#            // Каждую секунду вызывать loadMessages
#            setInterval(loadMessages, 1000);
#         });

#     </script>
# </head>
# <body>
# <!-- Интерфейс: имя, окно чата, текст сообщения -->
# <b>Ваше Имя:</b>
# <input id="name" type="text" placeholder="Ваше имя"/>

# <div id="chat_window"></div> <!-- окно чата -->

# <br/>
# <input id="text" type="text" placeholder="Текст сообщения">

# </body>
# </html>
