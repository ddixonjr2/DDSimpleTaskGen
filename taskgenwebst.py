import asyncio
import streamlit as st
from messaging_common import *
from taskgen_openaiagt import TaskListGeneratorOAA

async def main():
    generator = TaskListGeneratorOAA()
    
    st.set_page_config(page_title=UI_MAIN_HEADER_TEXT)
    st.title(UI_MAIN_HEADER_TEXT)
    request = st.text_area(UI_TASK_OBJECTIVE_PROMPT, placeholder=REQUEST_PLACEHOLDER)

    ph_execute = st.empty()
    ph_success = st.empty()
    ph_response = st.empty()

    if ph_execute.button(UI_GENERATE_BUTTON_TEXT):
        ph_success.empty()
        ph_response.empty()
        with st.spinner('Generating your response...'):
            response = await generator.gen_task_list(request=request, instructions=DEFAULT_INSTRUCTIONS)
            ph_success.success('Yay!!! Here\'s your tasklist!')
            ph_response.markdown(f'\n{response}\n')

if __name__ == '__main__':
    asyncio.run(main())
