import os
import sys
import shutil
import tempfile

# 현재 파일 기준 경로
base_dir = os.path.dirname(os.path.abspath(__file__))

# GPT-SoVITS 디렉토리 경로
gpt_sovits_dir = os.path.join(base_dir, "GPT-SoVITS")

# 작업 디렉토리를 GPT-SoVITS로 변경
os.chdir(gpt_sovits_dir)

# sys.path에 GPT-SoVITS 경로 추가
sys.path.insert(0, gpt_sovits_dir)

# tts_zunda.py에서 synthesize 함수 불러오기
from tts_zunda import synthesize

# 모델 경로 설정
GPT_MODEL_PATH = os.path.join(gpt_sovits_dir, "GPT_weights_v2", "zudamon_style_1-e15.ckpt")
SOVITS_MODEL_PATH = os.path.join(gpt_sovits_dir, "SoVITS_weights_v2", "zudamon_style_1_e8_s96.pth")

# 참조 오디오 및 텍스트 경로
ref_audio_path = os.path.join(gpt_sovits_dir, "reference", "reference.wav")
ref_text_path = os.path.join(gpt_sovits_dir, "reference", "ref_text.txt")

audio_suffix = os.path.splitext(ref_audio_path)[1]

with tempfile.NamedTemporaryFile(delete=False, suffix=audio_suffix) as tmp_audio:
    shutil.copyfile(ref_audio_path, tmp_audio.name)
    ref_audio_tmp_path = tmp_audio.name

# 합성할 텍스트
target_text = "안녕하세요, 즌다몬입니다. 오늘은 음성 테스트를 진행하고 있습니다. 이 모델은 일본어와 한국어를 모두 처리할 수 있습니다. 감사합니다!"
target_language = "Korean"
ref_language = "Japanese"

# 임시로 타겟 텍스트 파일 생성
tmp_target_path = os.path.join(gpt_sovits_dir, "target_text_tmp.txt")
with open(tmp_target_path, "w", encoding="utf-8") as f:
    f.write(target_text)

# 출력 경로
output_dir = os.path.join(gpt_sovits_dir, "output")
os.makedirs(output_dir, exist_ok=True)

print(ref_language, target_language, target_text)

# 음성 합성 실행
synthesize(
    GPT_model_path=GPT_MODEL_PATH,
    SoVITS_model_path=SOVITS_MODEL_PATH,
    ref_audio_path=ref_audio_tmp_path,
    ref_text_path=ref_text_path,
    ref_language=ref_language,
    target_text=target_text,
    target_language=target_language,
    output_path=output_dir
)

print("✅ 음성 합성이 완료되었습니다.")
print("📁 출력 경로:", os.path.join(output_dir, "output.wav"))
