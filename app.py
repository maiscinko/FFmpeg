from flask import Flask, request, jsonify
import subprocess
import os
import tempfile
import base64
import uuid

app = Flask(__name__)

@app.route('/extract-frames', methods=['POST'])
def extract_frames():
    if 'video' not in request.files and 'url' not in request.form:
        return jsonify({"error": "No video or URL provided"}), 400
    
    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, f"{uuid.uuid4()}.mp4")
    
    # Recebe vídeo por upload ou URL
    if 'video' in request.files:
        video_file = request.files['video']
        video_file.save(video_path)
    else:
        url = request.form['url']
        # Baixa o vídeo da URL
        try:
            subprocess.call(['wget', '-O', video_path, url])
        except Exception as e:
            return jsonify({"error": f"Failed to download: {str(e)}"}), 400
    
    # Extrai frames a cada 1 segundo
    output_pattern = os.path.join(temp_dir, 'frame_%03d.jpg')
    try:
        subprocess.call(['ffmpeg', '-i', video_path, '-vf', 'fps=1', output_pattern])
    except Exception as e:
        return jsonify({"error": f"FFmpeg error: {str(e)}"}), 500
    
    # Coleta frames como base64
    frames = []
    for file in sorted(os.listdir(temp_dir)):
        if file.startswith('frame_'):
            with open(os.path.join(temp_dir, file), 'rb') as img:
                img_data = base64.b64encode(img.read()).decode('utf-8')
                frames.append(img_data)
    
    # Limpa arquivos temporários
    subprocess.call(['rm', '-rf', temp_dir])
    
    return jsonify({"frames": frames})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
