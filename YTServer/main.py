from fastapi import FastAPI
from text_analysis import get_analysis
import json

app = FastAPI()


@app.get("/analysis")
async def root(url):
    data = get_analysis(url)
    print(data)
    json_output = json.dumps(data, indent=4, ensure_ascii=False).encode('utf8')
    return json_output

