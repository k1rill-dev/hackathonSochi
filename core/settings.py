from envparse import Env

env = Env()

env.read_envfile()

MAX_FILE_SIZE = 1024 * 1024 * 1024 * 20
MAX_REQUEST_BODY_SIZE = MAX_FILE_SIZE + 1024
PROMPTS = {
    'anime': 'anime artwork human. anime style, key visual, vibrant, studio anime, highly detailed',
    'fantasy': "ethereal fantasy concept art of human . magnificent, celestial, ethereal, painterly, epic, majestic, magical, fantasy art, cover art, dreamy",
    "neon": "neonpunk style human . cyberpunk, vaporwave, neon, vibes, vibrant, stunningly beautiful, crisp, detailed, sleek, ultramodern, magenta highlights, dark purple shadows, high contrast, cinematic, ultra detailed, intricate, professional",
    "pixel": "pixel-art human . low-res, blocky, pixel art style, 8-bit graphics",
    "gta": "GTA-style artwork human  . satirical, exaggerated, pop art style, vibrant colors, iconic characters, action-packed",
    "biomech": "biomechanical style human . blend of organic and mechanical elements, futuristic, cybernetic, detailed, intricate"
}

IAM_TOKEN = env.str('IAM_TOKEN')
FOLDER_ID = env.str('FOLDER_ID')
