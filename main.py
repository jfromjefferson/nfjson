import xmltodict
from fastapi import FastAPI, Request, HTTPException
app = FastAPI()

@app.post('/convert/json')
async def to_json(request: Request) -> dict:
    body = await request.body()
    body_str: str = body.decode("utf-8")

    if not body_str:
        raise HTTPException(status_code=400, detail="Empty body")

    json_data: dict = xmltodict.parse(body)

    return json_data


@app.post('/convert/pdf')
async def to_pdf(request: Request) -> dict:
    body = await request.body()
    body_str: str = body.decode("utf-8")

    if not body_str:
        raise HTTPException(status_code=400, detail="Empty body")

    raise HTTPException(status_code=501, detail="Not implemented yet")
