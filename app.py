"""Teaching assistant chatbot demo built with Streamlit.

Run locally:
    pip install streamlit
    streamlit run app.py
"""

from __future__ import annotations

from datetime import datetime
from typing import List

import streamlit as st

# Reference materials to cite in responses.
REFERENCE_MATERIALS = [
    "Serway",
    "Halliday",
    "Mechanics",
]


def _init_state() -> None:
    """Ensure session_state has the keys we expect."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history: List[dict] = []
    if "ideas" not in st.session_state:
        st.session_state.ideas: List[dict] = []
    if "feedback" not in st.session_state:
        st.session_state.feedback: List[dict] = []


def _fake_answer(question: str, ref: str | None) -> str:
    """Lightweight placeholder that fabricates a response using selected ref."""
    ref_text = ref if ref else "선택된 교재 없음"
    return (
        f"질문 요약: {question}\n\n"
        f"참고한 교재: {ref_text}\n"
        "→ 실제 모델 연동 시 여기에 근거 기반 답변을 생성하세요."
    )


def _render_chat(selected_ref: str | None) -> None:
    """Chat UI: input, history, and responses."""
    st.subheader("수준 맞춤형 튜터에게 질문하기")

    # Show history first
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("궁금한 내용을 입력하세요")
    if prompt:
        # User message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Bot response (placeholder)
        answer = _fake_answer(prompt, selected_ref)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)


def _render_idea_panel(selected_ref: str | None) -> None:
    """Panel for creative/critical ideas."""
    st.subheader("창의·비판 아이디어 제출")
    idea = st.text_area("수업 개선 아이디어를 적어주세요", placeholder="예) 토론형 과제 변형 제안 ...")
    if st.button("아이디어 제출", use_container_width=True):
        if not idea.strip():
            st.warning("내용을 입력해 주세요.")
        else:
            st.session_state.ideas.append(
                {
                    "text": idea.strip(),
                    "ref": selected_ref if selected_ref else "참고 교재 없음",
                    "ts": datetime.utcnow().isoformat(timespec="seconds"),
                }
            )
            st.success("아이디어가 저장되었습니다.")

    if st.session_state.ideas:
        st.markdown("#### 제출된 아이디어")
        for item in reversed(st.session_state.ideas):
            ref = item.get("ref", "참고 교재 없음")
            st.markdown(
                f"- ({item['ts']} UTC) {item['text']}  \n"
                f"  참고: {ref}"
            )


def _render_feedback_panel() -> None:
    """Panel for sending feedback to developers."""
    # 커스텀 divider
    st.markdown("""
    <div style="
        height: 40px;
        background-color: #22c55e;
        border-radius: 8px;
        margin: 1.5rem 0 1.8rem 0;
    "></div>
    """, unsafe_allow_html=True)
    st.subheader("개발자에게 의견 보내기")
    feedback = st.text_area("의견을 입력해주세요", placeholder="예) 버그 리포트, 기능 제안, 개선 사항 ...")
    if st.button("의견 보내기", use_container_width=True):
        if not feedback.strip():
            st.warning("내용을 입력해 주세요.")
        else:
            st.session_state.feedback.append(
                {
                    "text": feedback.strip(),
                    "ts": datetime.utcnow().isoformat(timespec="seconds"),
                }
            )
            st.success("의견이 전송되었습니다.")

    if st.session_state.feedback:
        st.markdown("#### 보낸 의견")
        for item in reversed(st.session_state.feedback):
            st.markdown(
                f"- ({item['ts']} UTC) {item['text']}"
            )


def main() -> None:
    st.set_page_config(page_title="Custom-Level Tutor", layout="wide")
    _init_state()

    # CSS 스타일: 배경색 그룹화 및 Streamlit 헤더 숨기기
    st.markdown("""
        <style>
        /* Streamlit 기본 헤더 숨기기 */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        .chat-container {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            border: 5px solid #ef4444;
        }
        .idea-container {
            background: linear-gradient(180deg, #f3f4f6 0%, #e5e7eb 100%);
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            border: 5px solid #22c55e;
        }
        /* 오른쪽 패널 내부의 divider(hr) 스타일 */
        [data-testid="column"] hr {
            border: none;
            height: 8px;
            margin: 1.2rem 0 1.5rem 0;
            background-color: #22c55e;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 메인 영역과 오른쪽 사이드바를 위한 컬럼 레이아웃
    col_main, col_sidebar = st.columns([3, 1], gap="large")

    # 메인 영역: 제목, 교재 선택, 챗봇 (왼쪽+중앙에 크게)
    with col_main:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        st.title("Custom-Level Tutor")
        st.caption("수준 맞춤형 튜터에게 질문해보세요.")
        st.divider()

        st.header("교재/레퍼런스 선택")
        selected_ref = st.selectbox(
            "수준 맞춤형 튜터가 답변에 참고할 교재를 골라주세요.",
            options=[None] + REFERENCE_MATERIALS,
            format_func=lambda x: x if x else "교재를 선택하세요",
        )
        st.info("실제 모델 연동 시 선택된 교재로 검색/인용하도록 연결하세요.")
        st.divider()
        
        # 챗봇을 메인 영역에 배치
        _render_chat(selected_ref)
        st.markdown('</div>', unsafe_allow_html=True)

    # 오른쪽 사이드바: 아이디어 제출 + 개발자에게 의견 보내기
    with col_sidebar:
        st.markdown('<div class="idea-container">', unsafe_allow_html=True)
        _render_idea_panel(selected_ref)
        _render_feedback_panel()
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
