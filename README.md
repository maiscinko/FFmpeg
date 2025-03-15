# Video Frame Extractor API

Serviço simples para extrair frames de vídeos, projetado para integração com n8n ou outras ferramentas de automação.

## Funcionalidades

- Extrai frames de vídeos enviados diretamente ou via URL
- Retorna frames como strings base64
- Configurável para diferentes taxas de extração de frames (fps)
- Design simples e fácil de implantar

## Como usar

### Endpoint principal

`POST /extract-frames`

### Parâmetros

O endpoint aceita dois métodos para fornecer o vídeo:

1. **Upload direto de arquivo**:
   - Use `multipart/form-data` com um campo chamado `video`

2. **URL remota**:
   - Use `application/x-www-form-urlencoded` com um campo chamado `url`

### Parâmetros opcionais

- `fps`: Taxa de extração de frames (padrão: 1 frame por segundo)

### Resposta

```json
{
  "success": true,
  "frames": [
    "base64_encoded_image_1",
    "base64_encoded_image_2",
    "..."
  ],
  "count": 10
}
```

### Exemplo de uso com cURL

```bash
# Usando URL
curl -X POST \
  -F "url=https://exemplo.com/video.mp4" \
  -F "fps=0.5" \
  https://seu-app.onrender.com/extract-frames

# Usando upload de arquivo
curl -X POST \
  -F "video=@/caminho/para/video.mp4" \
  https://seu-app.onrender.com/extract-frames
```

### Exemplo de integração com n8n

1. Use o nó HTTP Request para fazer download do vídeo do Instagram
2. Use outro nó HTTP Request para enviar o vídeo para este serviço
3. Processe os frames resultantes conforme necessário

## Implantação

### No Render.com

1. Crie uma nova conta ou faça login em [render.com](https://render.com)
2. Clique em "New" e selecione "Web Service"
3. Conecte ao repositório GitHub ou forneça URL do repositório
4. O Render detectará automaticamente o Dockerfile
5. Configure um nome para o serviço
6. Escolha o plano (o plano gratuito funcionará para testes)
7. Clique em "Create Web Service"

## Desenvolvimento Local

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/video-frame-extractor.git
cd video-frame-extractor

# Instalar dependências
pip install -r requirements.txt

# Executar o servidor de desenvolvimento
python app.py
```

Requisitos: Python 3.9+ e FFmpeg instalados no sistema.
