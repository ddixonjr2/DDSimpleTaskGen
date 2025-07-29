import asyncio
import streamlit as st
from messaging_common import *
from taskgenselection import TaskListGeneratorSelector, Engine

async def main():            
    st.set_page_config(page_title=UI_MAIN_HEADER_TEXT)
    st.title(UI_MAIN_HEADER_TEXT)
    tasklistgen_selector = TaskListGeneratorSelector()
    request = st.text_area(UI_TASK_OBJECTIVE_PROMPT, placeholder=REQUEST_PLACEHOLDER)
    engine = Engine(st.selectbox(
        UI_API_SELECTOR_TITLE,
        options=[str(Engine.OPENAIAGT.value), str(Engine.LANGCHAIN.value), str(Engine.CREWAI.value)],
        index=0
        )
    )

    ph_execute = st.empty()
    ph_success = st.empty()
    ph_response = st.empty()

    if ph_execute.button(UI_GENERATE_BUTTON_TEXT):
        ph_success.empty()
        ph_response.empty()
        with st.spinner(UI_INPROGRESS_TEXT):
            generator = tasklistgen_selector.cur_task_list_generator(engine)
            response = await generator.gen_task_list(request=request, instructions=DEFAULT_INSTRUCTIONS)
            ph_success.success(UI_COMPLETION_HEADER_TEXT)
            ph_response.markdown(f'\n{response}\n')

if __name__ == '__main__':
    asyncio.run(main())
