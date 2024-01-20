import PySimpleGUI as sg
import time
from function import TextEditor

sg.theme("Black")
text_editor = TextEditor()

layout = [
    [sg.Text("", key='clock')],
    [sg.Text("Upload a file to edit")],
    [sg.InputText(), sg.FileBrowse("Upload", size=(10, 1), file_types=(("Text files", "*.txt"), ("All files", "*.*")), key="Upload")],
    [sg.Button("read", size=(5, 1))],
    [sg.Listbox(values=[], key="book", enable_events=True, size=(45, 10))],
    [sg.Button("Edit"), sg.Button("Save", size=(10, 1), mouseover_colors="LightBlue2", tooltip="Save", key="Save")],
    [sg.Button("Exit")]
]

window = sg.Window("Text Editor", layout, font=("Helvetica", 20))

while True:
    event, values = window.read()
    window["clock"].update(value=time.strftime("%b %d, %Y %H:%M:%S"))

    if event in (sg.WIN_CLOSED, "Exit"):
        break

    if event == "Upload":
        filepath = values["Upload"]
        text_editor.open_file(filepath)
        window["book"].update(values=text_editor.content.split('\n'))

    elif event == "Edit":
        edited_content = sg.popup_get_text("Edit Content", default_text=text_editor.content, size=(80, 20))
        if edited_content is not None:
            text_editor.content = edited_content
        window["book"].update(values=text_editor.content.split('\n'))

    elif event == "Save":
        file_type = sg.popup_get_text("Enter 'txt' or 'pdf' to save:", default_text="txt")
        if file_type.lower() not in ["txt", "pdf"]:
            sg.popup_error("Invalid file type. Please enter 'txt' or 'pdf'.")
        else:
            text_editor.save_file(file_type.lower())

window.close()
