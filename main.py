from typing import List, Optional
from fastapi import FastAPI, Query, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

from nlp_process import nlp_process
import os
from send_chat import send_chatwork


app = FastAPI()

templates = Jinja2Templates(directory="templates")
@app.get('/')
async def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/kwds/v1')
async def scrape_nlp(kwd: Optional[List[str]] = Query(
    None, 
    title="ニュース記事を絞り込むのに用いたいキーワード",
    description="yahooやrakuten.infoseekでニュース検索・スクレイピングを行うときに使用するキーワードです。複数指定できます。キーワードが多いほど、処理に時間が掛かります。"
)):
    result = nlp_process(kwd)
    kwds = result['Keywords']
    urls = result['Urls']
    contents = result['Contents']
    count = 1
    send_chatwork(f'[info][title]Googleトレンドキーワードからニュース記事を抽出[/title][info][title]キーワード[/title]{kwds}[/info][/info]')
    for i in range(len(urls)):
        send_chatwork(f'[info][title]記事{count}[/title]{urls[i]} \n\n{contents[i]}[/info]')
        count += 1
    
    return result

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))