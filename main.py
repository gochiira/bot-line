from flask import Flask, request
from line_magic.line_magic import LineMessagingClient, LineMessagingTracer
from line_magic.line_magic import TextMessage, FlexMessage
from gochiira_client import GochiiraClient
from copy import deepcopy
import json
import os


# 各種クライアントの作成
with open("auth.json", "r", encoding="utf8") as f:
    authFile = json.loads(f.read())
    cl = LineMessagingClient(channelAccessToken=authFile["line"]["token"])
    tracer = LineMessagingTracer(cl, prefix=["!", "?", "#", "."])
    icl = GochiiraClient(
        authFile["illust"]["token"],
        authFile["illust"]["endpoint"]
    )

# フレックスメッセージの読み出し
flex = {}
for file in os.listdir("flex"):
    with open(os.path.join("flex", file), "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    flex[file[:-5]] = data


# イベント別受信処理
class Operations(object):
    @tracer.Before("Operation")
    def set_Token(self, cl, op):
        if "replyToken" in op:
            cl.setReplyToken(op["replyToken"])

    @tracer.Operation("message")
    def got_message(self, cl, msg):
        self.trace(msg, "Content")

    @tracer.Operation("follow")
    def got_follow(self, cl, msg):
        msgs = [TextMessage("Thanks for add me!")]
        cl.replyMessage(msgs)

    @tracer.Operation("unfollow")
    def got_unfollow(self, cl, msg):
        print("UNFOLLOW")

    @tracer.Operation("join")
    def got_join(self, cl, msg):
        msgs = [TextMessage("Thanks for invite me!")]
        cl.replyMessage(msgs)


# コンテンツ別受信処理
class Contents(object):
    @tracer.Content("text")
    def got_text(self, cl, msg):
        self.trace(msg, "Command")

    @tracer.Content("image")
    def got_image(self, cl, msg):
        with open("test.jpg", "wb") as f:
            f.write(cl.getContent(msg["message"]["id"]))
        msgs = [TextMessage("Kawaii!")]
        cl.replyMessage(msgs)


# コマンド別受信処理
class Commands(object):
    @tracer.Command(alt=["ハロー", "hello"])
    def hi(self, cl, msg):
        '''Check the bot Alive'''
        msgs = [TextMessage("Hi too!")]
        cl.replyMessage(msgs)

    @tracer.Command(noPrefix=True)
    def help(self, cl, msg):
        '''Display this help message'''
        msgs = [TextMessage(self.genHelp())]
        cl.replyMessage(msgs)

    @tracer.Command(prefix=False)
    def 検索方法(self, cl, msg):
        msgs = [FlexMessage(flex["search_methods"])]
        cl.replyMessage(msgs)

    @tracer.Command(prefix=False)
    def タグから探す(self, cl, msg):
        tags = icl.getTagList()
        contents = []
        for d in tags["data"]["contents"][:10]:
            result = deepcopy(flex["search_tag"])
            result["action"]["text"] = f"タグ検索 {d['id']}"
            result["body"]["contents"][1]["text"] = f"該当数: {d['count']}"
            result["body"]["contents"][2]["text"] = f"いいね数: {d['lcount']}"
            result["footer"]["contents"][0]["contents"][0]["text"] = d["name"]
            contents.append(result)
        msgs = [FlexMessage({"type": "carousel", "contents": contents})]
        cl.replyMessage(msgs)

    @tracer.Command(prefix=False)
    def キャラクターから探す(self, cl, msg):
        tags = icl.getCharacterList()
        contents = []
        for d in tags["data"]["contents"][:10]:
            result = deepcopy(flex["search_tag"])
            result["action"]["text"] = f"キャラクター検索 {d['id']}"
            result["body"]["contents"][1]["text"] = f"該当数: {d['count']}"
            result["body"]["contents"][2]["text"] = f"いいね数: {d['lcount']}"
            result["footer"]["contents"][0]["contents"][0]["text"] = d["name"]
            contents.append(result)
        msgs = [FlexMessage({"type": "carousel", "contents": contents})]
        cl.replyMessage(msgs)

    @tracer.Command(prefix=False)
    def ランキングから探す(self, cl, msg):
        ranking = icl.getRankings()
        contents = []
        for d in ranking["data"]["imgs"][:9]:
            result = deepcopy(flex["search_result"])
            result["action"]["uri"] = d["originUrl"]
            result["body"]["contents"][0]["url"] = f"https://cdn.gochiusa.team/illusts/thumb/{d['illustID']}.jpg"
            result["body"]["contents"][1]["contents"][0]["text"] = d["artist"]["name"]
            result["body"]["contents"][2]["contents"][0]["text"] = d["date"].split(" ")[0]
            result["body"]["contents"][3]["contents"][0]["text"] = d["originService"]
            result["footer"]["contents"][0]["contents"][0]["text"] = d["title"]
            contents.append(result)
        msgs = [FlexMessage({"type": "carousel", "contents": contents})]
        cl.replyMessage(msgs)


def app_callback():
    if request.method == "POST":
        data = request.get_json()
        for d in data["events"]:
            tracer.trace(d, "Operation")
    return "OK"

def createApp():
    app = Flask(__name__)
    app.add_url_rule('/callback', 'callback', app_callback, methods=["GET", "POST"])
    tracer.addClass(Operations())
    tracer.addClass(Contents())
    tracer.addClass(Commands())
    tracer.startup()
    return app


if __name__ == "__main__":
    app = createApp()
    app.run(host="localhost", port=8080)
