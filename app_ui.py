import streamlit as st
from main import app

st.set_page_config(
    page_title="💬 Мотивационный чат-бот",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Мотивационный чат-бот")
st.caption("Этот бот анализирует ваше настроение и поддерживает вас: помогает, если вы стараетесь, мотивирует, если ленитесь, и направляет, если вы начинающий.")

if "username" not in st.session_state:
    st.session_state.username = "user"

username= st.text_input(
    "Ввведите ваше имя:",
    value = st.session_state.username,
    key="username_input"
)
st.session_state.username = username

thread_id  =f"chat_{username}"
config = {
    "configurable":
    {
        "thread_id" : thread_id
    }
}

if "history" not in st.session_state:
    st.session_state.history = []

col1, col2 = st.columns([4, 1])
with col2:
    if st.button("🔄 Очистить"):
        st.session_state.history = []
        st.rerun()

for msg in st.session_state.history:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])

user_input =st.chat_input("Введите сообщение:")

if user_input:
    st.session_state.history.append({"role" : "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    messages_for_graph = []
    for msg in st.session_state.history:
        messages_for_graph.append({
            "role" : msg["role"],
            "content" : msg["content"]
        })
    state = {"messages": messages_for_graph, "message_type" : None}

    with st.chat_message("assistant"):
        with st.spinner("🤖 Обрабатываю сообщение..."):
            try:
                result = app.invoke(state, config)
            
                if result.get("messages") and len(result["messages"]) > 0:
                    last_message = result["messages"][-1]

                    if isinstance(last_message, dict):
                        reply = last_message.get("content", "Извините, не смог обработать ответ.")

                    else:
                        reply = last_message.content if hasattr(last_message, 'content') else str(last_message)

                    st.write(reply)

                    st.session_state.history.append({"role" : "assistant", "content" : reply})

                else:
                    st.error("Бот не вернул ответ.")
        
            except Exception as e:
                st.error(f"Ошибка при обработке сообщения: {e}")
                st.exception(e)  

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <p>💡 Разработано с использованием LangGraph + Google Gemini</p>
    <p style='font-size: 0.8em;'>Бот определяет ваше состояние и отвечает в стиле коуча.</p>
    </div>
    """,
    unsafe_allow_html=True
)