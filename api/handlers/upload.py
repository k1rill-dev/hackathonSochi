from typing import List

import torch
from PIL import Image
import aiofiles
from diffusers import StableDiffusionImg2ImgPipeline
from fastapi import APIRouter, Request, HTTPException, status, UploadFile, File, Form
from streaming_form_data import StreamingFormDataParser
from streaming_form_data.targets import FileTarget, ValueTarget
from streaming_form_data.validators import MaxSizeValidator
import streaming_form_data
from starlette.requests import ClientDisconnect
import os
from api.utils.preprocess_video import VideoPreprocessing
from api.utils.generate_image import ImageGenerator
from api.validators import MaxBodySizeValidator
from api.exceptions import MaxBodySizeException
from core.settings import MAX_REQUEST_BODY_SIZE, MAX_FILE_SIZE, PROMPTS

router = APIRouter()


def init_pipeline():
    with torch.no_grad():
        a = StableDiffusionImg2ImgPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16
        )
        a = a.to("cuda")
        torch.cuda.empty_cache()
        return a


# def init_avatar_pipeline():
#     with torch.no_grad():
#         a = StableDiffusionImg2ImgPipeline.from_pretrained(
#             "dreamlike-art/dreamlike-photoreal-2.0", torch_dtype=torch.float16
#         )
#         a = a.to("cuda")
#         torch.cuda.empty_cache()
#         return a


pipe = init_pipeline()
# pipe_ava = init_avatar_pipeline()


@router.post("/api/endpoint_video")
async def process_form_data(request: Request):
    body_validator = MaxBodySizeValidator(MAX_REQUEST_BODY_SIZE)
    filename = request.headers.get('Filename')
    if not filename:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail='Filename header is missing')
    try:
        filepath = os.path.join(f'./temp/videos/', os.path.basename(filename))
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

    VideoPreprocessing.trim_video(f'./temp/videos/{filename}', './temp/clips', filename)
    prompt = "cooking, food, happines, photorealism, volumetric lighting, Ultra HD, octane render,amazingly detailed, masterpiece, full shot"
    negative_prior_prompt = "lowres, text, error, cropped, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, username, watermark, signature"
    init_image = Image.open(f'./temp/clips/thumbnail_{filename}_{0}.jpg')
    img = ImageGenerator.generate(prompt=prompt, negative_prompt=negative_prior_prompt, initial_image=init_image,
                                  pipe=pipe)
    img.save(f'./temp/{filename[:-4]}.png')
    url = request.url_for('static', path=f'{filename[:-4]}.png')
    return [url.path[1:]]


# @router.post("/api/endpoint_avatar")
# async def process_form_data(request: Request, file: UploadFile = File(...), style: str = Form(),
#                             strength: float = Form()):
#     async with aiofiles.open('./temp/avatars/' + file.filename, 'wb') as f:
#         while contents := file.file.read(1024 * 1024):
#             await f.write(contents)
#
#     prompt = PROMPTS.get(style)
#     negative_prior_prompt = "lowres, text, error, cropped, jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, mutation, deformed, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, username, watermark, signature"
#     init_image = Image.open('./temp/avatars/' + file.filename)
#     img = ImageGenerator.generate(prompt=prompt, negative_prompt=negative_prior_prompt, initial_image=init_image,
#                                   pipe=pipe_ava, strength=0.4)
#     img.save(f'./temp/avatars/{file.filename}')
#     del img
#     url = request.url_for('static', path=f'avatars/{file.filename}')
#     return url.path[1:]


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
