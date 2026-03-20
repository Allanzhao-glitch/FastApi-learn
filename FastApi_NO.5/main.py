from typing import List
from starlette.requests import Request
from fastapi import FastAPI, Form, File, UploadFile
from starlette.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/files/")
async def files(request: Request,files_list: List[bytes] = File(...),files_name: List[UploadFile] = File(...)):
    print("files_name:",files_name)
    return templates.TemplateResponse("index.html", 
            {
                "request":      request,
                "file_sizes":   [len(file) for file in files_list], 
                "filenames":    [file.filename for file in files_name],    
             })

    
@app.post("/create_file/")
async def create_file(
                        request: Request,
                        file: bytes         = File(...), 
                        fileb: UploadFile   = File(...), 
                        notes: str          = Form(...),
                      ):
    print("request:",request)
    print("file:",file)
    print("fileb:",fileb)
    print("notes:",notes)
    return templates.TemplateResponse("index.html", 
            {
                "request":               request,
                "file_size":             len(file),
                "notes":                 notes,
                "fileb_content_type":    fileb.content_type,
             })


@app.get("/")
async def main(request: Request):
    print("=== 请求信息 ===")
    print(f"URL: {request.url}")
    print(f"路径: {request.url.path}")
    print(f"方法: {request.method}")
    print(f"Headers: {dict(request.headers)}")
    print(f"Query参数: {dict(request.query_params)}")
    print(f"Path参数: {request.path_params}")
    print(f"Client IP: {request.client.host if request.client else 'Unknown'}")
    print(f"Cookies: {request.cookies}")
    return templates.TemplateResponse('post.html', {'request': request})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)