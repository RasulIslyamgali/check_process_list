import psutil
import smtplib # need to install
import datetime
import getpass

# Для корректной работы требуется: в мобильном приложении: Разрешить небезопасным программам управлять почтой
# gmail приложение > Настройки > Выбирайте нужный аккаунт > Аккаунт(Управление аккаунтом Google) > Безопасность > Ненадежные приложения, у которых есть доступ
# к аккаунту Нажимаем Разрешить

# Так же с этим аккаунтом должен совершаться вход в почту в текущей машине

USER = getpass.getuser()

proc_count = 0
proc_name = "HCSBKKZ_robot.exe" # example name

curr_time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

send_from = "email from"
send_to = "email to"
password = "your password for send_from email"


title = f'SOMETHING HAPPENED WITH {proc_name[:len(proc_name) - 4]}'
message_text = f"{title}\n\n" \
               f"{curr_time}\n\n" \
               f"USER: {USER}\n\n" \
               f"ROBOT: {proc_name[:len(proc_name) - 4]}"

BODY = "\r\n".join((
    "From: %s" % send_from,
    "To: %s" % send_to,
    "Subject: %s" % title,
    "",
    message_text
))


def send_message(send_from, send_to, BODY):
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    server.login(send_from, password)

    server.sendmail(send_from, send_to, BODY)

    server.quit()


while True:
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            processName = proc.name()
            if processName == proc_name:
                proc_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if proc_count < 4: # your proceses count
        print(f"WAS SEND MESSAGE TO: {send_to}")
        send_message(send_from=send_from, send_to=send_to, BODY=BODY)
        break

    proc_count = 0






