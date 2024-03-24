
import logging
import streamlit as st
import google.generativeai as genai


st.set_page_config(page_title="LLM Chat Application", page_icon=":gem:")

with st.sidebar:

    api_key = "AIzaSyAkP7jdbvu9IsY47RacdGJt6PXalMiNsxs"

    genai.configure(api_key=api_key)


def get_response(messages):
    model = genai.GenerativeModel("gemini-pro")
    res = model.generate_content(messages)
    return res


if "messages" not in st.session_state:
    st.session_state["messages"] = []
messages = st.session_state["messages"]

# The vision model gemini-pro-vision is not optimized for multi-turn chat.
st.header("LLM Chat Application")
st.write("Welcome to the LLM Chat Application")


if messages:
    for item in messages:
        role, parts = item.values()
        if role == "user":
            st.chat_message("user").markdown(parts[0])
        elif role == "model":
            st.chat_message("assistant").markdown(parts[0])

chat_message = st.chat_input("Say something")

res = None
if chat_message:
    st.chat_message("user").markdown(chat_message)
    res_area = st.chat_message("assistant").markdown("...")


    messages.append(
        {"role": "user", "parts":  [chat_message]},
    )
    try:
        res = get_response(messages)
    except Exception as e:
        logging.error(e)
        st.error("Error occured. Please refresh your page and try again.")
    
    if res is not None:
        res_text = ""
        for chunk in res:
            if chunk.candidates:
                res_text += chunk.text
            if res_text == "":
                res_text = "unappropriate words"
                st.error("Your words violate the rules that have been set. Please try again!")
        res_area.markdown(res_text)

        messages.append({"role": "model", "parts": [res_text]})

