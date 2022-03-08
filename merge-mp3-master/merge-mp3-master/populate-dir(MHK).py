import os
import pathlib
import shutil
import subprocess
import tkinter
from tkinter import messagebox, font
HAS_0 = False

# Desired functionality:
# put in folder, and it should create folders based on num of episodes and populate those
# with the corresponding audio based on anki2/media.collection.
FONT = ('Arial', 11, 'normal')
SRC = r'C:\Users\thegr\AppData\Roaming\Anki2\passive\collection.media'
DST = pathlib.Path().cwd()
CWD = DST

root = tkinter.Tk()
root.geometry('500x550+500+100')
root.title('Passive Immersion Manager')
root.config(bg="#22223B", pady=20, padx=20)
my_canvas = tkinter.Canvas(bg='#22223B', borderwidth=0, highlightthickness=0)
my_canvas.grid(column=0, row=0, columnspan=3)

# create folders in specified directory


def create_folder(SRCC, FILENAME_PREFIX, NUM_EPISODES, OUTPUT_FOLDERS_NAME):
    print('create folder function')
    file_ls = fetch_file(SRCC, FILENAME_PREFIX, NUM_EPISODES)

    if pathlib.Path(SRCC).exists() and DST.exists():
        if FILENAME_PREFIX == '':
            return SyntaxError
        else:

            for fol_num in range(1, NUM_EPISODES + 1):
                if OUTPUT_FOLDERS_NAME == '':
                    OUTPUT_FOLDERS_NAME = FILENAME_PREFIX
                if fol_num < 10:
                    folder_done = CWD / f'{OUTPUT_FOLDERS_NAME}_EP_0{fol_num}'

                else:
                    folder_done = CWD / f'{OUTPUT_FOLDERS_NAME}_EP_{fol_num}'

                folder_done.mkdir(exist_ok=False)

                # debugging in console

                if folder_done.exists():
                    print('_' * 40)
                    print(f'Successfully created folder {OUTPUT_FOLDERS_NAME}_EP_0{fol_num}\nin {CWD}.')
                else:
                    return NotImplementedError

                populate_folder(folder_done, file_ls, SRC, int(fol_num - 1))
    else:
        return FileNotFoundError


# fetches files and creates nested list for easier parsing
def fetch_file(source_folder, FILENAME_PREFIX, NUM_EPISODES):

    EP_NUM_STRT_INDX = len(FILENAME_PREFIX)
    if HAS_0:
        EP_NUM_END_INDX = EP_NUM_STRT_INDX + 2
    else:
        EP_NUM_END_INDX = EP_NUM_STRT_INDX + 1

    print('fetch file function')
    global file_ep_number
    init_file_list = os.listdir(source_folder)
    for file in init_file_list:
        if file.lower().endswith('.jpg'):
            path = f"{source_folder}\{file}"
            os.unlink(path)
    mod_file_list = []
    iterated = []

    for num in range(1, NUM_EPISODES + 1):
        if num < 10:
            if HAS_0:
                ep_num_check = f'0{num}'
            else:
                ep_num_check = f'{num}'

        else:
            ep_num_check = str(num)
        mod_nested = []
        for file in range(len(init_file_list)):
            file_ep_number = init_file_list[file][EP_NUM_STRT_INDX: EP_NUM_END_INDX]
            if init_file_list[file].lower().endswith('.mp3'):
                if file_ep_number not in iterated:
                    if file_ep_number == ep_num_check:
                        mod_nested.append(init_file_list[file])

                    else:
                        break


        mod_file_list.append(mod_nested)
        iterated.append(ep_num_check)

    return mod_file_list


# populate relative folders with files from the media collection folder in anki

def populate_folder(dest_folder, modded_file_list, source, fol_ep_num):

    print('pop function')
    success = 0
    total = 0
    for file in modded_file_list[fol_ep_num]:
        total += 1
        full_path_before = f'{source}\{file}'
        full_path_after = f'{dest_folder}\{file}'
        shutil.move(full_path_before, dest_folder)
        if pathlib.Path(full_path_after).exists():
            success += 1
    print(f'completed {success}/{total} file transfers to: {dest_folder}')


def open_media_collection():
    subprocess.Popen(f'explorer {os.path.realpath(SRC)}')


def execute():
    file_name = file_name_entry.get()
    ep = episodes_entry.get()
    if ep == '':
        ep = 0
    else:
        ep = int(ep)
    out_name = output_entry.get()
    if file_name == '' or ep == '':
        messagebox.showerror('Error', 'One or more fields are blank.\nPlease fill those fields.')
        return
    font1 = font.Font(name='TkCaptionFont', exists=True)
    font1.config(family='courier new', size=20)

    continuee = messagebox.askokcancel('Confirmation Window',
                                       f'Please confirm:\n\nFile Prefix: {file_name}\n Episodes: {ep}\n Output Folder Name: {out_name}', )
    if continuee:
        info = [file_name, ep, out_name]

        FILENAME_PREFIX = info[0]
        OUTPUT_FOLDERS_NAME = info[2]
        NUM_EPISODES = info[1]

        create_folder(SRC, FILENAME_PREFIX, NUM_EPISODES, OUTPUT_FOLDERS_NAME)
        root.destroy()

    else:
        return


image = tkinter.PhotoImage(
    file='C:\\Users\\thegr\\Desktop\\MIA\\tools\\merge-mp3-master\\merge-mp3-master\\file_pic.png')
my_canvas.create_image(210, 120, image=image)

file_name_label = tkinter.Label(text='Filename Prefix: ', font=FONT, foreground='white', background='#22223B')
file_name_label.grid(column=0, row=1, pady=10)

file_name_entry = tkinter.Entry(font=FONT, width=29)
file_name_entry.grid(column=1, row=1, pady=10, padx=15, )

open_Anki_folder = tkinter.Button(text='Anki Folder', command=open_media_collection)
open_Anki_folder.grid(column=2, row=1, pady=10)

episodes_label = tkinter.Label(text='Episodes: ', font=FONT, foreground='white', background='#22223B')

episodes_label.grid(column=0, row=2, pady=10)

episodes_entry = tkinter.Entry(font=FONT, width=10)

episodes_entry.grid(column=1, row=2, pady=10, sticky='ew')

output_label = tkinter.Label(text='Output Name: ', font=FONT, foreground='white', background='#22223B')
output_label.grid(column=0, row=4, pady=10)

output_entry = tkinter.Entry(font=FONT, width=19)
output_entry.grid(column=1, row=4, pady=10, sticky='ew')

Execute_button = tkinter.Button(text='Execute', command=execute)
Execute_button.grid(column=1, row=5, pady=20,rowspan=2)


root.mainloop()
