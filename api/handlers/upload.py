from typing import List
import aiofiles
from fastapi import APIRouter, Request, HTTPException, status, UploadFile, File, Form
from streaming_form_data import StreamingFormDataParser
from streaming_form_data.targets import FileTarget, ValueTarget
from streaming_form_data.validators import MaxSizeValidator
import streaming_form_data
from starlette.requests import ClientDisconnect
import os
from api.validators import MaxBodySizeValidator
from api.exceptions import MaxBodySizeException
from core.settings import MAX_REQUEST_BODY_SIZE, MAX_FILE_SIZE

router = APIRouter()


@router.post("/api/endpoint_video")
async def process_form_data(request: Request):
    body_validator = MaxBodySizeValidator(MAX_REQUEST_BODY_SIZE)
    filename = request.headers.get('Filename')
    if not filename:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail='Filename header is missing')
    try:
        filepath = os.path.join('./', os.path.basename(filename))
        file_ = FileTarget(filepath, validator=MaxSizeValidator(MAX_FILE_SIZE))
        data = ValueTarget()
        parser = StreamingFormDataParser(headers=request.headers)
        parser.register('file', file_)
        parser.register('data', data)
        async for chunk in request.stream():
            body_validator(chunk)
            parser.data_received(chunk)
    except ClientDisconnect:
        print("Client Disconnected")
    except MaxBodySizeException as e:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            detail=f'Maximum request body size limit ({MAX_REQUEST_BODY_SIZE} bytes) exceeded ({e.body_len} bytes read)')
    except streaming_form_data.validators.ValidationError:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            detail=f'Maximum file size limit ({MAX_FILE_SIZE} bytes) exceeded')
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='There was an error uploading the file')
    if not file_.multipart_filename:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='File is missing')

    return {"message": f"Successfuly uploaded {filename}"}


@router.post("/api/endpoint_avatar")
async def process_form_data(file: UploadFile = File(...), style: str = Form(), strength: float = Form()):
    print(file.filename)
    print(style)
    print(strength)
    # генерация изображения
    return "images/avatar.jpg"


@router.post("/api/endpoint_shapka")
async def process_form_data(files: List[UploadFile] = File(...), name: str = Form()):
    for file in files:
        try:
            async with aiofiles.open(file.filename, 'wb') as f:
                while contents := file.file.read(1024 * 1024):
                    await f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file(s)"}
        finally:
            file.file.close()

    return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}
