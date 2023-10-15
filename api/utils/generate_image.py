from typing import Union
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline
import torch
import gc


class ImageGenerator:
    @staticmethod
    def generate(prompt: str, negative_prompt: str, initial_image: Image.Image, strength: float = 0.8,
                 pipe: StableDiffusionImg2ImgPipeline = None) \
            -> Union[None, Image.Image]:
        with torch.no_grad():
            image = pipe(prompt=prompt, negative_prompt=negative_prompt, image=initial_image, strength=strength).images[0]
            torch.cuda.empty_cache()
            return image



# with torch.no_grad():
#     repo_id = "dreamlike-art/dreamlike-photoreal-2.0"
#     pipe1_5 = StableDiffusionImg2ImgPipeline.from_pretrained(repo_id, use_safetensors=True, torch_dtype=torch.float16)
#     pipe1_5 = pipe1_5.to("cuda")

gc.collect()
torch.cuda.empty_cache()
