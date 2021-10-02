import paho.mqtt.client as mqtt
import time, json, re, argparse, smtplib, requests, configparser

### update Oct 01 2021 !!!!
# working with ncid 1.11
# run on manager1 in the background with supervisord
# sudo chmod 777 /var/log/cidcall.log

config = configparser.ConfigParser()
config.read("secrets.ini")
token = config["prd-auth"]["token"]
user_key = config["prd-auth"]["user_key"]

regex = r"((\*DATE\*)(\d{8}))((\*TIME\*)(\d{4}))(\*LINE\*POTS\*)((NMBR\*)(\d{10,11}))(\*MESG\*NONE\*)((NAME\*)(.+)(\*))"
log_file = "/var/log/cidcall.log" # prod callers id log file
# log_file = "cidcall.log" # for testing local file.


def extract_tel_data():
    with open(log_file, "r") as file:
        for i in file:
            matches = re.finditer(regex, i, re.MULTILINE)
            for match in matches:
                payload = (
                    match.group(3),
                    match.group(6),
                    match.group(10),
                    match.group(14),
                )
                print(payload)
                # print(type(payload))
                send_mqtt_message(" ".join(map(str, payload)))
                time.sleep(1)


def follow_data(thefile):
    print("Reading log  ...")
    thefile.seek(0, 2)  # file. seek(offset[, whence]) absolute file positioning
    while True:
        read_line = thefile.readline()
        if not read_line:  # if not True
            time.sleep(1)  # wait
            #            print("time sleep {}.".format(time.asctime()))
            continue
        yield read_line


def send_mqtt_message(message):
    broker = "192.168.2.5"
    port = 1883
    timeout = 60
    topic = "callerid/incoming"
    client = mqtt.Client()
    client.connect(broker, port, timeout)
    client.publish(topic, message)
    client.disconnect()


def send_email_message(body_text):
    host = "192.168.2.3"
    subject = "Caller ... {}".format(body_text[3])
    to_addr = (
        "alerts@home.lan"  # send to nas smtp which will send to yzeralerts@gmail.com
    )
    from_addr = "callerid@home.lan"
    kv_body_text = "Date: {}, Time: {}, Phone: {}, Caller: {}".format(
        body_text[0], body_text[1], body_text[2], body_text[3]
    )

    message_body = "\r\n".join(("To: {}", "From: {}", "Subject: {}", "", "{}")).format(
        from_addr, to_addr, subject, kv_body_text
    )
    server = smtplib.SMTP(host)
    server.sendmail(from_addr, [to_addr], message_body)
    server.quit()


def send_to_pushovernet(message, token, user_key):
    url = "https://api.pushover.net/1/messages.json"

    token = token
    user_key = user_key
    message = message

    r = requests.post(
        url=url,
        data={
            "token": token,
            "user": user_key,
            "message": message,
        },
    )
    print(r.text)


def send_to_google_mini():
    pass


def send_to_sql():
    pass


if __name__ == "__main__":
    print("Starting Main ..")
    logfile = open(log_file, "r")  # read the contents of logfile.
    loglines = follow_data(logfile)  # call the function and assing to loglines.
    for line in loglines:
        matches = re.finditer(regex, line, re.MULTILINE)
        for match in matches:
            payload = match.group(3), match.group(6), match.group(10), match.group(14)
            print(payload)
            send_mqtt_message(" ".join(map(str, payload)))
            send_email_message(payload)
            send_to_pushovernet(" ".join(map(str, payload)), token, user_key)
