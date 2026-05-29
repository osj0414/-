import streamlit as st

# 웹앱 제목 설정
st.title("⚾ 나만의 미니 야구 데이터 계산기")
st.write("타자의 기록을 입력하면 예상 안타 수와 주요 스탯을 계산해줍니다!")

# 구분선
st.divider()

# 사이드바 또는 메인 화면에 입력창 만들기
st.header("👤 타자 정보 입력")

# 사용자 입력 받기 (기본값 설정으로 오류 방지)
player_name = st.text_input("타자 이름", value="홍길동")
at_bats = st.number_input("타석 수 (AB)", min_value=1, max_value=1000, value=100)
batting_average = st.slider("타율 (AVG)", min_value=0.000, max_value=1.000, value=0.300, step=0.001)

# 간단한 야구 스탯 계산 공식
# 안타 수 = 타석 수 * 타율 (반올림)
hits = round(at_bats * batting_average)

# 장타율과 출루율은 입력된 타율을 기반으로 한 가상의 심플 계산 (오류 방지용)
slugging = min(batting_average * 1.5, 1.000) 
on_base = min(batting_average + 0.070, 1.000)

st.divider()

# 결과 출력
st.header(f"📊 {player_name} 선수의 예상 성적 리포트")

# 메트릭(카드 형태)으로 깔끔하게 보여주기
col1, col2, col3 = st.columns(3)
col1.metric(label="예상 안타 수", value=f"{hits} 개")
col2.metric(label="출루율 (상정)", value=f"{on_base:.3f}")
col3.metric(label="장타율 (상정)", value=f"{slugging:.3f}")

# 응원 메시지
if batting_average >= 0.300:
    st.success(f"🔥 {player_name} 선수는 3할이 넘는 최고의 타자입니다!")
elif batting_average >= 0.250:
    st.info(f"👍 {player_name} 선수는 준수한 활약을 펼치고 있습니다.")
else:
    st.warning(f"💪 {player_name} 선수, 다음 경기에서 반등을 기대합니다!")
