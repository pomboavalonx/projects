from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import time
import urllib.parse
import random
import logging

# Configuração de Logging para debugar a desgraça
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/data/data/com.termux/files/home/projects/pollinations-openai-api/api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("nebula_api")

app = FastAPI()

# Resolve o problema de CORS para que qualquer front-end consiga chamar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageGenerationRequest(BaseModel):
    prompt: str
    n: Optional[int] = 1
    size: Optional[str] = "1024x1024"

class ImageURL(BaseModel):
    url: str

class ImageGenerationResponse(BaseModel):
    created: int
    data: List[ImageURL]

@app.get("/v1/models")
@app.get("/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {"id": "pollinations", "object": "model", "created": 1700000000, "owned_by": "pollinations"}
        ]
    }

@app.post("/v1/images/generations")
@app.post("/images/generations")
async def generate_images(request: ImageGenerationRequest):
    logger.info(f"Request recebido: prompt='{request.prompt}', n={request.n}, size={request.size}")
    
    try:
        # URL encode o prompt para evitar quebra na URL do Pollinations
        encoded_prompt = urllib.parse.quote(request.prompt)
        
        # Lógica de dimensões básica
        width, height = "1024", "1024"
        if request.size and "x" in request.size:
            try:
                width, height = request.size.split("x")
            except ValueError:
                logger.warning(f"Tamanho inválido '{request.size}', usando 1024x1024")

        images = []
        for i in range(request.n):
            # Use random.randint para evitar sementes idênticas em requisições rápidas
            seed = random.randint(0, 2**31 - 1)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={seed}&nologo=true"
            images.append(ImageURL(url=url))
            logger.info(f"Gerada URL: {url}")

        return ImageGenerationResponse(
            created=int(time.time()),
            data=images
        )
    except Exception as e:
        logger.error(f"Erro ao gerar imagem: {str(e)}")
        return {"error": "Internal Server Error", "details": str(e)}, 500

if __name__ == "__main__":
    import uvicorn
    # Rodando na porta 8000 por padrão
    uvicorn.run(app, host="0.0.0.0", port=8000)
