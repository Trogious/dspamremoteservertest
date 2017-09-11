#!/usr/local/bin/python3.6

import json
import socket
import ssl
import random, string, requests

host = '0.0.0.0'
port = 3000
backlog = 5
size = 4096

SIGNATURE_LEN = 23
MSGID_PRE_AT_LEN = 50

def get_random_string(size):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(size))

def get_from(user):
    return '"' + user['name']['first'] + ' ' + user['name']['last'] + '"' + ' <' + user['email'] + '>'

def get_msg_id(user):
    domain = 'example2.com'
    atIdx = user['email'].find('@')
    if atIdx >= 0:
        domain = user['email'][atIdx+1:]
    return get_random_string(MSGID_PRE_AT_LEN) + '@' + domain

def get_status(user):
    return 'Delivered'

def get_subject(user):
    return 'This is a test email ' + get_random_string(4)

def get_spam_status(user):
    return random.choice('ISMF')

def get_random_emails():
    emails = []
    resp = requests.get('https://randomuser.me/api/?results=20')
    if 200 == resp.status_code:
        data = resp.json()
        for user in data['results']:
            emails.append({'from': get_from(user), 'signature': get_random_string(SIGNATURE_LEN), 'timestamp': '1457000174', 'msgid': get_msg_id(user), 'status': get_status(user), 'subject': get_subject(user), 'spamstatus': get_spam_status(user)})
    return emails

def decode(str):
    decoded = str
    encodings = ['utf8','iso8859-2','cp1250','cp437','cp500','cp1252']
    for e in encodings:
        try:
            decoded = str.decode(e)
            break
        except UnicodeDecodeError:
            print('UnicodeDecodeError: ' + e)
            print(str)
            pass
    return decoded


def getJsonResponse(result, requestId):
    jsonObj = {}
    jsonObj['jsonrpc'] = '2.0'
    jsonObj['id'] = requestId
    jsonObj['result'] = result
    return jsonObj

def getJsonResponseEntries(entries, requestId):
    return getJsonResponse({ 'entries': entries }, requestId)

def getJsonResponseRetrain(okEntries, errEntries, requestId):
    jsonObj = {}
    jsonObj['ok'] = [entry['signature'] for entry in okEntries]
    jsonObj['fail'] = []
    return getJsonResponse(jsonObj, requestId)

def process(line):
    data = line.split('\t')
    jsonObj = {}
    jsonObj['timestamp'] = data[0]
    jsonObj['spamstatus'] = data[1]
    jsonObj['from'] = data[2]
    jsonObj['signature'] = data[3]
    jsonObj['subject'] = data[4]
    jsonObj['status'] = data[5]
    jsonObj['msgid'] = data[6]
    return jsonObj

def getEntries():
    entries = []
    try:
        with open('a@example.com.log','rb') as f:
                line = f.readline()
                str = ''
                i = 0
                while line is not None and len(line) > 0 and i < 500:
                        if len(line) > 1:
                                entry = process(decode(line))
                                entries.append(entry)
                        line = f.readline()
                        i = i + 1
    except:
        pass
    return entries

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host,port))
    s.listen(backlog)
    historyEntries = getEntries()[::-1]
    historyEntries = get_random_emails()
    while True:
        client, address = s.accept()
        print('accepted: ' + str(address))
        try:
            sslClient = ssl.wrap_socket(client, server_side=True, certfile="server.pem", keyfile="server.key", ssl_version=ssl.PROTOCOL_TLSv1_2,cert_reqs=ssl.CERT_REQUIRED,ca_certs='ca.pem')
    #        sslClient = ssl.wrap_socket(client, server_side=True, certfile="server.pem", keyfile="server.key", ssl_version=ssl.PROTOCOL_TLSv1_2,cert_reqs=ssl.CERT_OPTIONAL,ca_certs='ca.pem')
        except ssl.SSLError as e:
            print('no client cert: ' + e.strerror)
            client.close()
            continue
        client = None
        data = sslClient.recv(size)
        while data and len(data) > 0:
            print(data)
            data = data.decode('utf8')
            print(data)
            req = json.loads(data)
            keys = req.keys()
            if 'jsonrpc' in keys and req['jsonrpc'] == '2.0' and 'method' in keys and 'id' in keys:
                method = req['method']
                if 'retrain' == method:
                    if 'params' in keys and 'entries' in req['params']:
                        entries = req['params']['entries']
                        if len(entries) > 0:
                            response = json.dumps(getJsonResponseRetrain(entries,[],req['id']))
                            encodedResponse = response.encode('utf8')
                            respLen = len(encodedResponse)
                            fullContent = 'Content-Length: ' + str(respLen) + "\r\n\r\n" + response
                            sslClient.sendall(fullContent.encode('utf8'))
                            print(fullContent)
                elif 'get_entries' == method:
                    response = json.dumps(getJsonResponseEntries(historyEntries, req['id']))
                    encodedResponse = response.encode('utf8')
                    respLen = len(encodedResponse)
                    fullContent = 'Content-Length: ' + str(respLen) + "\r\n\r\n" + response
                    sslClient.sendall(fullContent.encode('utf8'))
                    print(fullContent)
            print('recv')
            data = sslClient.recv(size)
        sslClient.close()
        print('client closed')
