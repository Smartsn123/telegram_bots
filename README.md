# telegram_bots
simple telegram bot function to push notifications from code to a telegram channel


#sample usage

```
from telegram_bots.bot import update_on_telegram

def check_yarn_status():
    """
    function to update yarn queue status on telegram when capacity exceeds 70 percent
    """
    val = !yarn queue -status datascience
    print val
    current_capacity = float(val.grep("Current Capacity").fields(-1)[0].strip("%"))
    if current_capacity >= 70.0:
        update_on_telegram(
            channel = "yarn_alerts" , 
            bot_name = "yarn_bot" , 
            message = "Queue Resource Alert: Queue is "+str(current_capacity)+"% used"
        )


```
