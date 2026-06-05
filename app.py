import streamlit as st  # <-- 이 부분이 tf에서 st로 수정되었습니다.
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 페이지 설정
st.set_page_config(page_title="자리배치 마스터 챗봇", page_icon="🪑")
st.title("🪑 자리배치 마스터 챗봇")
st.caption("학급, 사무실, 행사 등의 효율적이고 재미있는 자리배치 아이디어를 제안해 드립니다!")

# Streamlit Secrets에서 API 키 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 설정 후 다시 시도해주세요.")
    st.stop()

# Gemini 클라이언트 초기화
@st.cache_resource
def get_gemini_client(api_key):
    return genai.Client(api_key=api_key)

try:
    client = get_gemini_client(api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 초기화 중 오류가 발생했습니다: {e}")
    st.stop()

# 세션 상태(Session State)로 채팅 기록 유지
if "messages" not in st.session_state:
    st.session_state.messages = []
    # 챗봇의 기본 페르소나 및 역할 부여 (System Instruction)
    st.session_state.system_instruction = (
        "당신은 자리배치 전문가입니다. 학교 교실, 회사 사무실, 결혼식이나 파티 같은 행사 등 "
        "다양한 상황에 맞는 창의적이고 효율적인 자리배치 방법과 아이디어를 제공해야 합니다. "
        "사용자가 인원수, 공간 특성, 목적(예: 협업 중시, 집중도 향상, 서먹함 해소 등)을 말하면 "
        "그에 맞는 최적의 배치법(예: ㄷ자형, 모둠형, 무작위 등)과 장단점을 친절하게 설명해주세요."
    )

# 기존 채팅 기록 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("예: 고등학교 2학년 교실인데, 떠드는 걸 방지하면서도 조별 활동하기 좋은 배치 알려줘."):
    # 사용자 메시지 화면에 표시 및 저장
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 챗봇 답변 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # 이전 대화 맥락을 Gemini API 형식에 맞게 변환
        history = []
        for msg in st.session_state.messages[:-1]:  # 현재 입력 직전까지의 기록
            role = "user" if msg["role"] == "user" else "model"
            history.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))
        
        try:
            # gemini-2.5-flash-lite 모델 호출
            response = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=st.session_state.system_instruction,
                    temperature=0.7,
                )
            )
            
            # 답변 출력 및 저장
            full_response = response.text
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except APIError as e:
            # Gemini API 관련 오류 처리
            error_msg = f"Gemini API 오류가 발생했습니다: {e.message} (상태 코드: {e.code})"
            message_placeholder.error(error_msg)
        except Exception as e:
            # 기타 예상치 못한 오류 처리
            error_msg = f"알 수 없는 오류가 발생했습니다: {str(e)}"
            message_placeholder.error(error_msg)
