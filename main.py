import FreeSimpleGUI as sg

# Theme
sg.theme('SandyBeach')

# Define compact window contents (single-cycle model)
timer_row = [sg.Text('00:00', key='-TIME-', font=('Consolas', 40, 'bold'), justification='center')]
top_button_row = [
    sg.Push(),
    sg.Button('Study', key='-STUDY-', button_color=('white', 'green')),
    sg.Button('Break', key='-REST-', button_color=('white', 'green')),
    sg.Push(),
]
bottom_button_row = [
    sg.Push(),
    sg.Button('Pause', key='-PAUSE-', button_color=('white', 'red')),
    sg.Button('Reset', key='-RESET-', button_color=('white', 'red')),
    sg.Push(),
]

layout = [
    timer_row,
    top_button_row,
    bottom_button_row
]

# Create the window
window = sg.Window('Sloth Study Timer', layout, icon='sloth_logo.ico', margins=(100, 50), finalize=True)

# Internal state
mode = 'study'  # 'study' (count up) or 'break' (count down)
running = False
seconds = 0     # single counter; study increments, break decrements

def format_time(seconds: int) -> str:
    m, s = divmod(max(0, int(seconds)), 60)
    return f"{m:02d}:{s:02d}"

def render_time():
    window['-TIME-'].update(format_time(seconds))

def start_study():
    global mode, running
    # Switch to study and resume counting up from current seconds
    mode = 'study'
    running = True
    render_time()

def start_break():
    global mode, running
    # Switch to break and count down from current seconds
    mode = 'break'
    running = True
    render_time()

def pause():
    global running
    running = False

def reset_all():
    global running, seconds, mode
    running = False
    seconds = 0
    mode = 'study'
    render_time()

def tick():
    global seconds, running
    if not running:
        return
    if mode == 'study':
        seconds += 1
    else:
        seconds -= 1
        if seconds <= 0:
            seconds = 0
            running = False
    render_time()

# Event Loop
while True:
    event, values = window.read(timeout=1000 if running else None)
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    if event == '-STUDY-':
        start_study()
    elif event == '-REST-':
        start_break()
    elif event == '-PAUSE-':
        pause()
    elif event == '-RESET-':
        reset_all()
    if running and (event is None or event == sg.TIMEOUT_EVENT):
        tick()