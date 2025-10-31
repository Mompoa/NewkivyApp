

Kivy app to list and dump .so files from a chosen directory.

Intended for legal analysis of files you own or have permission to inspect.

from kivy.app import App from kivy.lang import Builder from kivy.uix.boxlayout import BoxLayout from kivy.properties import ListProperty, StringProperty from kivy.clock import mainthread import os import shutil import hashlib from datetime import datetime

try to use plyer.filechooser on Android/desktop

try: from plyer import filechooser except Exception: filechooser = None

KV = ''' <Box>: orientation: 'vertical' padding: 12 spacing: 8

BoxLayout:
    size_hint_y: None
    height: '40dp'
    spacing: 8
    TextInput:
        id: path_input
        text: root.current_path
        hint_text: 'Enter folder path or use Browse'
    Button:
        text: 'Browse'
        size_hint_x: None
        width: '90dp'
        on_release: root.browse()
    Button:
        text: 'Scan .so'
        size_hint_x: None
        width: '90dp'
        on_release: root.scan_so_files()

Label:
    size_hint_y: None
    height: '24dp'
    text: root.status_text

ScrollView:
    GridLayout:
        id: list_grid
        cols:1
        size_hint_y: None
        height: self.minimum_height
        row_default_height: '48dp'
        row_force_default: True

BoxLayout:
    size_hint_y: None
    height: '40dp'
    spacing: 8
    Button:
        text: 'Dump Selected'
        on_release: root.dump_selected()
    Button:
        text: 'Copy All'
        on_release: root.copy_all()

Label:
    size_hint_y: None
    height: '120dp'
    text: root.selected_info
    text_size: self.width, None
    valign: 'top'
    halign: 'left'

'''

from kivy.uix.gridlayout import GridLayout from kivy.uix.label import Label from kivy.uix.checkbox import CheckBox from kivy.uix.textinput import TextInput from kivy.uix.button import Button

class FileRow(BoxLayout): path = StringProperty('') name = StringProperty('') checked = False def init(self, path, name, **kwargs): super().init(**kwargs) self.path = path self.name = name self.orientation = 'horizontal' self.size_hint_y = None self.height = '48dp' self.checkbox = CheckBox(size_hint_x=None, width='48dp') self.add_widget(self.checkbox) self.add_widget(Label(text=name, halign='left', valign='middle')) btn = Button(text='Info', size_hint_x=None, width='90dp') btn.bind(on_release=self.show_info) self.add_widget(btn)

def show_info(self, *a):
    app = App.get_running_app()
    app.root.show_file_info(self.path)

class Box(BoxLayout): so_files = ListProperty([]) current_path = StringProperty(os.path.expanduser('~')) status_text = StringProperty('Ready') selected_info = StringProperty('Select a file and press Info to see metadata')

def browse(self):
    if filechooser:
        filechooser.choose_dir(on_selection=self._on_dir)
    else:
        self.status_text = 'filechooser not available on this platform. Enter path manually.'

def _on_dir(self, selection):
    if selection:
        self.current_path = selection[0]
        self.status_text = f'Selected: {self.current_path}'

def scan_so_files(self):
    path = self.ids.path_input.text.strip()
    if not path:
        path = self.current_path
    if not os.path.isdir(path):
        self.status_text = 'Folder path invalid.'
        return
    self.status_text = 'Scanning...'
    self.ids.list_grid.clear_widgets()
    found = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.so'):
                full = os.path.join(root, f)
                found.append(full)
                row = FileRow(full, os.path.relpath(full, path))
                self.ids.list_grid.add_widget(row)
    self.so_files = found
    self.status_text = f'Found {len(found)} .so files.'

def get_checked_paths(self):
    paths = []
    for child in self.ids.list_grid.children:
        if isinstance(child, FileRow) and child.checkbox.active:
            paths.append(child.path)
    return paths

def dump_selected(self):
    sel = self.get_checked_paths()
    if not sel:
        self.status_text = 'No files selected.'
        return
    out = os.path.join(os.path.expanduser('~'), 'so_dumps')
    os.makedirs(out, exist_ok=True)
    for p in sel:
        try:
            shutil.copy2(p, out)
        except Exception as e:
            print('copy error', e)
    self.status_text = f'Dumped {len(sel)} files to {out}'

def copy_all(self):
    if not self.so_files:
        self.status_text = 'No files to copy. Scan first.'
        return
    out = os.path.join(os.path.expanduser('~'), 'so_dumps')
    os.makedirs(out, exist_ok=True)
    count = 0
    for p in self.so_files:
        try:
            shutil.copy2(p, out)
            count += 1
        except Exception as e:
            print('copy error', e)
    self.status_text = f'Copied {count} files to {out}'

def show_file_info(self, filepath):
    try:
        stat = os.stat(filepath)
        size = stat.st_size
        mtime = datetime.fromtimestamp(stat.st_mtime).isoformat()
        sha256 = self.compute_sha256(filepath)
        elf_info = self.parse_elf_header(filepath)
        info = f"Path: {filepath}\nSize: {size} bytes\nModified: {mtime}\nSHA256: {sha256}\nELF: {elf_info}"
        self.selected_info = info
    except Exception as e:
        self.selected_info = f'Error reading file: {e}'

def compute_sha256(self, filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def parse_elf_header(self, filepath):
    try:
        with open(filepath, 'rb') as f:
            magic = f.read(16)
        if len(magic) < 16:
            return 'Not ELF or too small'
        if magic[0:4] != b"\x7fELF":
            return 'Not an ELF file'
        cls = magic[4]
        data = magic[5]
        ei_version = magic[6]
        abi = magic[7]
        cls_str = '32-bit' if cls == 1 else '64-bit' if cls == 2 else f'unknown({cls})'
        data_str = 'little-endian' if data == 1 else 'big-endian' if data == 2 else f'unknown({data})'
        return f'{cls_str}, {data_str}, version={ei_version}, abi={abi}'
    except Exception as e:
        return f'Error parsing ELF: {e}'

class SoDumperApp(App): def build(self): Builder.load_string(KV) root = Box() return root

if name == 'main': SoDumperApp().run()
