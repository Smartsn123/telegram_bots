def update_on_telegram(channel, bot_name, message, file_name=None, user=''):
    """
    function to push message/ images/ documents to a telegram channel
    :param channel:  channel_id for the channel to push updates
    :param bot_name: bot_id of the bot which is added to the channel
    :param message: string message to be pushed to the channel
    :param file_name: path of image/ document file to be uploaded and sent
    :param user: '@user_name' of user to tag
    :return:  None
    """

    bot_config = {
        "proxy_uid": "",
        "proxy_pswd": "",
        "proxy_host": "",
        "proxy_port": "",
        # Leave above empty if you are not behind proxy
        "BOT_TOKENS": {"my_bot": "---"},  # add bot name with bot token
        "CHAT_IDS": {"my_channel1": {"my_bot1": "chat_id1"}, 
                     "my_channel2": {"my_bot2": "chat_id2"}
                     }

    }
    try:
        import os, json, urllib, urllib2, requests
        proxy_user = bot_config.get("proxy_uid")
        proxy_pswd = bot_config.get("proxy_pswd")
        proxy_host = bot_config.get("proxy_host")
        proxy_port = bot_config.get("proxy_port")
        bot_token = bot_config.get("BOT_TOKENS", {}).get(bot_name)
        chat_id = bot_config.get("CHAT_IDS", {}).get(channel, {}).get(bot_name)

        if not bot_token:
            print("JOB_LOG, bot token not added ")
            return

        if not chat_id:
            print("JOB_LOG, could not determine chat id please check config ")
            return

        if not (bot_config and bot_token):
            print("JOB_LOG, error in bot config file couldnt send message ")
            return
        else:
            print(bot_config, proxy_user, proxy_pswd, proxy_host, proxy_port, bot_token)
        
        if  proxy_user and proxy_pswd and proxy_host and proxy_port :
            http_proxy = "http://{}:{}@{}:{}".format(proxy_user, proxy_pswd, proxy_host, proxy_port)
            https_proxy = "https://{}:{}@{}:{}".format(proxy_user, proxy_pswd, proxy_host, proxy_port)
            ftp_proxy = "ftp://{}:{}@{}:{}".format(proxy_user, proxy_pswd, proxy_host, proxy_port)
            proxyDict = {
                "http": http_proxy,
                "https": https_proxy,
                "ftp": ftp_proxy
            }
            proxy = urllib2.ProxyHandler(proxyDict)
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
        else:
            proxyDict = {}
            
        headers = {"Content-Type": "application/json"}
        url = "https://api.telegram.org/bot{}/sendMessage".format(bot_token)
        body = {"chat_id": "{}".format(chat_id),
                "text": "@{} <b> {} </b>".format(user, message),
                "parse_mode": "html",
                "disable_notification": True
                }

        if file_name:
            file_type = 'photo' if file_name.split('.')[-1].lower() in ['.png', '.jpg', '.jpeg'] else 'document'
            files = {file_type: open(file_name, 'rb')}
            url = "https://api.telegram.org/bot{}/sendDocument".format(bot_token)
            response = requests.post(url, data={'chat_id': chat_id}, files=files)
            print (response.text)
        else:
            data = urllib.urlencode(body)
            req = urllib2.Request(url=url, data=data)
            content = urllib2.urlopen(req).read()
            print (content)
    except Exception as ex:
        print ("JOB_LOG, BOT EXCEPTION: {}".format(ex))
