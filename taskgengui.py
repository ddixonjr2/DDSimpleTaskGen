
import asyncio
import os
import tkinter as tk
import messaging_common as msgc

from taskgenselection import TaskListGeneratorSelector, Engine
from datetime import datetime
from customtkinter import (
    CTk, CTkButton, CTkLabel, CTkFrame, CTkEntry, CTkTextbox, CTkFont, CTkOptionMenu,
    set_appearance_mode, set_default_color_theme
)

# Helper Functions
def write_new_result(text: str):
    result_textbox.delete(0.0, tk.END)
    result_textbox.insert(0.0, text)

def set_is_busy(is_busy: bool):
    request_entry.configure(state='disabled' if is_busy else 'normal')
    clear_button.configure(state='disabled' if is_busy else 'normal')
    generate_button.configure(state='disabled' if is_busy else 'normal')
    save_button.configure(state='disabled' if is_busy else 'normal')

def current_task_list_text():
    return result_textbox.get(0.0, tk.END)

def task_list_populated() -> bool:
    task_list = current_task_list_text()
    is_preset = task_list in [msgc.RESPONSE_PLACEHOLDER, msgc.RESPONSE_INVALID_OBJECTIVE]
    return not is_preset and len(task_list) > 0

# Async Task Generation Functions
async def gen_task_list(request: str):
    global engine, tasklistgen_selector

    if request:
        set_is_busy(True)
        generator = tasklistgen_selector.cur_task_list_generator(engine)
        response = await generator.gen_task_list(
            request=request, 
            instructions=msgc.DEFAULT_INSTRUCTIONS
            )
        set_is_busy(False)
        return response
    else:
        return msgc.RESPONSE_INVALID_OBJECTIVE

async def generate_task_list():
    request = request_entry.get()
    if request:
        response = await gen_task_list(request)
        root.after(0, write_new_result, response)
    else:
        root.after(0, write_new_result, msgc.RESPONSE_INVALID_OBJECTIVE)

# Button Action Functions
def clear_button_pressed():
    request_entry.delete(0, tk.END)
    result_textbox.delete(0.0, tk.END)
    result_textbox.insert(0.0, msgc.RESPONSE_PLACEHOLDER)

def generate_button_pressed():
    asyncio.run(generate_task_list())

def save_button_pressed():
    if task_list_populated():
        fallback_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.getenv('HOME', fallback_dir)
        tasklist_dir = os.path.join(base_dir, msgc.DEFAULT_TASKLIST_DIR)
        os.makedirs(tasklist_dir, exist_ok=True)

        datestring = datetime.now().strftime('%m-%d-%Y_%H%M%S')
        full_path = os.path.join(tasklist_dir, f'{msgc.TASKLIST_OUTFILENAME_PREFIX}{datestring}.txt')
        with open(full_path, 'w') as outfile:
            outfile.write(current_task_list_text())

def exit_button_pressed():
    root.destroy()
    
    
# Menu Action Functions
def engine_menu_selection_made(selection: str):
    global engine
    engine = Engine(selection) or None
    

# Setup the UI window frame, controls, and then render
if __name__ == '__main__':
    set_appearance_mode('dark')
    set_default_color_theme('blue') 

    root = CTk()
    root.title(msgc.UI_MAIN_HEADER_TEXT)
    root.geometry('700x700')

    frame = CTkFrame(root)
    frame.pack(pady=20, padx=20, fill='both', expand=True)

    header_font = CTkFont(family='Helvetica', size=24, weight='bold')
    request_label = CTkLabel(frame, text=msgc.UI_TASK_OBJECTIVE_PROMPT, font=header_font)
    request_label.pack(pady=10)

    request_entry = CTkEntry(frame, placeholder_text=msgc.REQUEST_PLACEHOLDER)
    request_entry.pack(pady=10, padx=20, fill='x')
    
    entry_button_frame = CTkFrame(frame)
    entry_button_frame.pack(pady=10, padx=20, fill='x')
    
    generate_button = CTkButton(entry_button_frame, text=msgc.UI_GENERATE_BUTTON_TEXT, command=generate_button_pressed)
    generate_button.pack(side='right', pady=10, padx=60)

    clear_button = CTkButton(entry_button_frame, text=msgc.UI_CLEAR_ENTRY_BUTTON_TEXT, command=clear_button_pressed)
    clear_button.pack(side='left', pady=10, padx=60)
    
    tasklistgen_selector = TaskListGeneratorSelector()
    engine = Engine.OPENAIAGT
    engines = [str(Engine.OPENAIAGT.value), str(Engine.LANGCHAIN.value), str(Engine.CREWAI.value)]
    engine_menu = CTkOptionMenu(root, values=engines, command=engine_menu_selection_made)
    engine_menu.pack(pady=10, padx=20, fill='x')

    result_textbox = CTkTextbox(frame)
    result_textbox.pack(pady=10, padx=20, fill='both', expand=True)
    result_textbox.insert(0.0, msgc.RESPONSE_PLACEHOLDER)
    
    bottom_button_frame = CTkFrame(frame)
    bottom_button_frame.pack(pady=10, padx=20, fill='x', expand=True)

    save_button = CTkButton(bottom_button_frame, text=msgc.UI_SAVE_BUTTON_TEXT, command=save_button_pressed)
    save_button.pack(side='left', pady=10, padx=60)
    
    exit_button = CTkButton(bottom_button_frame, text=msgc.UI_EXIT_BUTTON_TEXT, command=exit_button_pressed)
    exit_button.pack(side='right', pady=10, padx=60)
    root.mainloop()
    