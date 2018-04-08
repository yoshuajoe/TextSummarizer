import sys
import time
import telepot
import traceback
from pprint import pprint
from telepot.loop import MessageLoop
from bs4 import BeautifulSoup
from SummaryTool import SummaryTool as smt


ALLOWED_ID = [418516845]

def crawling(url):
    from urllib.request import urlopen
    import re
    try:
        
        response = urlopen(url)
        
        r = response.read()
                
        soup = BeautifulSoup(r, "lxml")

        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]
        [s.extract() for s in soup.findAll('div', attrs={'id':'section_terkait'})]

        div_content = soup.findAll('div', attrs={'class' : 'mdk-body-paragpraph'})

        content = ""
        if div_content: 
            content_raw = div_content[0].findAll("p")

            for cont in content_raw:
                content += "\n\n"+cont.extract().getText().replace("Rekomendasi Pilihan","")
            
            print(content)
            return content
        else:

            return "Halaman tidak ditemukan"
    except Exception as e:
        print(e)
        pass


def sum_up(url):

    content = crawling(url)
    print(content)
    title = url.split("/")[3].replace("-"," ").replace(".html","")
    # Create a SummaryTool object
    st = smt()

    # Build the sentences dictionary
    sentences_dic = st.get_senteces_ranks(content)

    # Build the summary with the sentences dictionary
    summary = st.get_summary(title, content, sentences_dic)

    # Print the summary
    res = summary

    # Print the ratio between the summary length and the original length
    res += "\n"
    res += "\nOriginal Length %s" % (len(title) + len(content))
    res += "\nSummary Length %s" % len(summary)
    res += "\nSummary Ratio: %s" % (100 - (100 * (len(summary) / (len(title) + len(content)))))
    return res

def check_is_allowed(chat_id):
        if chat_id in ALLOWED_ID:
                return True
        else:
                return False

def handle(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, msg['text'],chat_type, chat_id)
        if content_type == 'text':
                resp = msg["text"]
                if "ringkas" in msg["text"]:
                    resp = sum_up(msg["text"].replace("ringkas","").strip())
                
                bot.sendMessage(chat_id, resp)

bot = telepot.Bot('585073874:AAHWOr9AONxSQ1gV13lIe2b26utV5SdTgLw')
MessageLoop(bot, handle).run_as_thread()
response = bot.getUpdates()
pprint(response)
print ('Listening ...')

while True:

    time.sleep(10)

