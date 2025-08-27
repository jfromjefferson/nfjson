from pathlib import Path

import xmltodict
from fastapi import FastAPI, Request, Response, HTTPException
from weasyprint import HTML
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.post('/convert/json')
async def to_json(request: Request) -> dict:
    try:
        body = await request.body()
        body_str: str = body.decode('utf-8')
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))

    if not body_str:
        raise HTTPException(status_code=400, detail='Empty body')

    json_data: dict = xmltodict.parse(body)

    return json_data


@app.post('/convert/pdf')
async def to_pdf(request: Request) -> Response:
    try:
        body = await request.body()
        body_str: str = body.decode('utf-8')
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))

    if not body_str:
        raise HTTPException(status_code=400, detail='Empty body')

    json_data: dict = xmltodict.parse(body)
    context = {
        **json_data['nfeProc']
    }

    rendered_html = templates.get_template("invoice.html").render(context)
    pdf = HTML(string=rendered_html).write_pdf()
    headers = {
        'Content-Disposition': 'attachment; filename="output.pdf"'
    }

    return Response(content=pdf, media_type='application/pdf', headers=headers)
