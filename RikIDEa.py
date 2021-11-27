import builtins as builtins
import symtable
import math
import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
from tkinter.scrolledtext import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import messagebox as MessageBox
import decimal
import os
import tkinter.font as tkfont
import subprocess
import idlelib.colorizer as ic
import idlelib.percolator as ip
from pathlib import Path
from sys import exit
import io
import tokenize
import keyword
import re

# Global variables
ide_title = 'RikIDEa'
file_path = ''
file_name = ''
arg_text = ''
search_text_widget = ''
searchwin = ''
font_size = 10
font_name = 'Courier New'
rowsbackground = 'dimgrey'
background = 'black'
foreground = 'white'
search_list = list()
s = ""
ontop = False
text_list = []
word_now = ''
maybe_list = []
dec = 0
curr = 0
new_integ = 0
index = 0
autofill = False
oksearch	= ''
var_label = ''

# General geometry
ide = Tk()
ide.title(ide_title)
fullscreen = False
w = ide.winfo_reqwidth()
h = ide.winfo_reqheight()
ws = ide.winfo_screenwidth()
hs = ide.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
ide.geometry('%dx%d' % (x + 200, y +200))

# Menu functions
def set_file_path(path, name):
	global file_path
	global file_name
	file_path = path
	file_name = name
	
def setflag(event):
	global ontop
	ontop = False
	
def new_file(*k):
	global file_path
	file_path = ''
	file_name = ''
	editor.delete('1.0', END)
	set_file_path('', '')
	ide.title(ide_title)
	draw_lines(True)
	text_list_update(True)

def open_file(*k):
	try:
		global file_name
		path = askopenfilename(filetypes = [('Python Files', '*.py')])
		name = path.split('/')[-1]
		ide.title(ide_title + ' - ' + name)
		with open(path, 'r') as file:
			code = file.read()
			editor.delete('1.0', END)
			editor.insert('1.0', code)
			set_file_path(path, name)
		draw_lines(True)
		text_list_update(True)
	except:
		pass
	
def save_as(*k):
	try:
		path = asksaveasfilename(defaultextension=".py", filetypes = [('Python Files', '*.py')])
		name = path.split('/')[-1]
		ide.title(ide_title + ' - ' + name)
		with open(path, 'w') as file:
			code = editor.get('1.0', END)
			file.write(code)
			set_file_path(path, name)
	except:
		pass

def save(*k):
	global file_path
	try:
		if file_path == '':
			path = asksaveasfilename(defaultextension=".py", filetypes=[('Python Files', '*.py')])
			name = path.split('/')[-1]
			ide.title(ide_title + ' - ' + name)
			set_file_path(path, name)
		else:
			path = file_path
		with open(path, 'w') as file:
			code = editor.get('1.0', END)
			file.write(code)
	except:
		pass

def cmd_run_shell(*k):
	base_cmd(f'python ')

def cmd_run(*k):
	global file_path
	if file_path == '':
		save_prompt = Toplevel()
		text = Label(save_prompt, text='Please save your code')
		text.pack()
		return
	save()
	base_cmd(f'python {file_path} ')
	
def base_cmd(command):
	cmd = f'start cmd.exe @cmd /k {command}'
	global file_path
	general_path = file_path.rsplit('/', 1)
	general_path = general_path[0] + '/'
	os.chdir(general_path)
	os.system(cmd)   

def is_tab_reversible():
	try:
		start_line = math.trunc(float(editor.index("sel.first")))
		last_line = math.trunc(float(editor.index("sel.last")))
		for x in range(start_line, last_line + 1):
				if editor.get(f"{x}.0").isalpha():
					return False
		return True
	except:
		pass 
		
def check_tab_alone(text):
	count = 0
	tabs = []
	d = "\n"
	lines =  [e+d for e in text.split(d) if e]
	for st in lines:
		i = 0
		tab_count = 0
		for c in st:
			if c == "\t":
				tab_count += 1
				i += 1
		tabs.append(tab_count)
	count = min(tabs)
	
	new_text = ''
	for st in lines:
		new_text = new_text + st[count:]
	return new_text
	
def run_alone(*event):	
	alone_file = open("alone.py","w+")
	path = Path("alone.py").absolute()
	start_line = math.trunc(float(editor.index("sel.first")))
	last_line = math.trunc(float(editor.index("sel.last")))
	
	count = 0
	while(count < start_line - 1):
		alone_file.writelines('\n')
		count += 1
	
	alone_text = editor.get(editor.index("sel.first"), editor.index("sel.last"))
	alone_text = check_tab_alone(alone_text)
	alone_file.writelines(alone_text)
	alone_file.close()	
	
	path = str(path)
	general_path = path.rsplit('\\', 1)
	general_path = general_path[0] + '\\'
	cmd = f'start cmd.exe @cmd /k python {path}'
	os.chdir(general_path)
	os.system(cmd)
	
def cmd_run_args():
	global file_path
	global arg_text
	if file_path == '':
		save_prompt = Toplevel()
		text = Label(save_prompt, text='Please save your code')
		text.pack()
		return
	save()
	a_text = arg_text.get("1.0",END)
	base_cmd(f'python {file_path} ' + a_text)
	
def run_args():
	global arg_text
	if file_path == '':
		save_prompt = Toplevel()
		text = Label(save_prompt, text='Please save your code')
		text.pack()
		return
	argswin = Toplevel(ide)
	argswin.configure(bg=rowsbackground)
	argswin.title("Run with arguments")
	argswin.geometry("300x85")
	argswin.resizable(False, False)
	argswin.focus()
	arg_label = Label(argswin, text="Arguments:", fg='white', bg='black')
	arg_label.pack(side="top")
	arg_text = Text(argswin, height=1)
	arg_text.pack()
	runargs = tk.Button(argswin, text="Run", fg='white', height=2, width=5, command=cmd_run_args, bg='black')
	runargs.pack()

def search_text(*event):
	global search_text_widget
	global searchwin
	global oksearch
	global var_label
	var_label = StringVar()
	
	searchwin = Toplevel(ide)
	searchwin.transient(ide)
	searchwin.configure(bg=rowsbackground) 
	searchwin.title("Finder")
	searchwin.geometry("300x65")
	searchwin.resizable(False, False)
	search_text_widget = Entry(searchwin, width=65)
	search_text_widget.focus()
	search_text_widget.pack()
	oksearch = tk.Button(searchwin, text="Search", fg='white', height=2, width=5, command=find_now, bg='black')
	oksearch.pack()
	search_label = Label(searchwin, textvariable=var_label , fg='white', bg=rowsbackground).place(x = 250, y = 30)
	
	if editor.tag_ranges("sel"):
		start = float(editor.index("sel.first"))
		last = float(editor.index("sel.last"))
		to_search = editor.get(start, last)
		search_text_widget.insert('0', to_search)

def reset_list():
	global search_text_widget
	global search_list
	global s
	if s != search_text_widget.get():
		search_list.clear()
		editor.tag_remove(SEL, 1.0,"end-1c")

def find_now():
	reset_list()
	
	global searchwin
	global search_text_widget
	global search_list
	global s
	global var_label
	
	all_text = editor.get('1.0', END).lower()	
	editor.focus_set()
	s = search_text_widget.get()
	card = all_text.count(s.lower())
	
	if s:
		if search_list == []:
			idx = "1.0"
		else:
			idx = search_list[-1]
		idx = editor.search(s, idx, nocase=1, stopindex=END)
		lastidx = '%s+%dc' % (idx, len(s))
		try:
			editor.tag_remove(SEL, 1.0,lastidx)
		except:
			pass
		try:
			editor.tag_add(SEL, idx, lastidx)
			counter_list = []
			counter_list = str(idx).split('.')	 
			editor.mark_set("insert", "%d.%d" % (float(int(counter_list[0])), float(int(counter_list[1]))))
			editor.see(float(int(counter_list[0])))
			search_list.append(lastidx)
			var_label.set(str(len(search_list)) + "/" + str(card))
		except:
			search_list.clear()
			editor.tag_remove(SEL, 1.0,"end-1c")

			
def set_fullscreen(*event):
   global fullscreen
   fullscreen = not fullscreen
   ide.attributes("-fullscreen", fullscreen)

def end_fullscreen(event):
	ide.attributes("-fullscreen", False)
	
def zoom_in(*event):
	global font_name
	global font_size
	font_size += 2
	editor.configure(font=(font_name, font_size))
	rows.configure(font=(font_name, font_size))
	
	font = tkfont.Font(font=editor['font'])
	tab_size = font.measure('    ', displayof = editor)
	editor.config(tabs=tab_size)

def zoom_out(*event):
	global font_name
	global font_size
	if font_size > 2:
		font_size -= 2
		editor.configure(font=(font_name, font_size))
		rows.configure(font=(font_name, font_size))
		
		font = tkfont.Font(font=editor['font'])
		tab_size = font.measure('    ', displayof = editor)
		editor.config(tabs=tab_size)
		
def text_copy():
	editor.event_generate('<Control-c>')

def text_cut():
	editor.event_generate('<Control-x>')
	
def text_paste():
	editor.event_generate('<Control-v>')
	
def select_all():
	editor.event_generate('<Control-a>')	

def gen_indent():
	editor.event_generate('<Tab>')
	
def gen_revindent():
	editor.event_generate('<Control-,>')
		
def indent_fix(*event):
	try:
		x = float(editor.index("sel.first"))
		y = float(editor.index("sel.last"))
		m = editor.get(x, y)
		m = m.replace("    ", "\t")		
		editor.delete(x, y)
		editor.insert(x, m)
	except:
		pass
		
def split(delimiters, string, maxsplit=0):
    import re
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)		
		
def text_list_update(*event):
	global text_list
	text_list = editor.get('1.0', END)
	text_list = text_list.replace("\n", " ").replace("\t", " ").replace("'", " ").replace("\\", " ").replace("'", " ").replace(")", " ").replace(":", " ")
	
	text_list = list(set(text_list.split(' ')))
	to_remove = []
	for st in text_list:
		nogood = False
		if len(st) < 2 or "\\" in st or st.isnumeric():
			nogood = True
		elif "(" in st:
			new_st = st.split("(")[0]
			text_list.append(new_st)
		if not st.isalpha():
			for c in st:
				if (not c.isalpha()) and c != '_' and c != '-':
					nogood = True
		if nogood:
			to_remove.append(st)
	for rem in to_remove:
		text_list.remove(rem)
	text_list = list(set(text_list))
	
def on_hscrollbar(*args):
	editor.xview(*args)
	
def ontext_horizscroll(*args):
	horscrollbar.set(*args)
	on_hscrollbar('moveto', args[0])

def on_scrollbar(*args):
	'''Scrolls both text widgets when the scrollbar is moved'''
	rows.yview(*args)
	editor.yview(*args)
	
def on_textscroll(*args):
	'''Moves the scrollbar and scrolls text widgets when the mousewheel
	is moved on a text widget'''
	scrollbar.set(*args)
	on_scrollbar('moveto', args[0])
	
def set_word_boundaries(ed):
	# this first statement triggers tcl to autoload the library
	# that defines the variables we want to override.  
	ed.tk.call('tcl_wordBreakAfter', '', 0) 

	# this defines what tcl considers to be a "word". For more
	# information see http://www.tcl.tk/man/tcl8.5/TclCmd/library.htm#M19
	ed.tk.call('set', 'tcl_wordchars', '[a-zA-Z0-9_]')
	ed.tk.call('set', 'tcl_nonwordchars', '[^a-zA-Z0-9_]')

horscrollbar = Scrollbar(ide, orient = 'horizontal')
horscrollbar.pack(side=BOTTOM, fill=X)
		
scrollbar = Scrollbar(ide)
scrollbar.pack(side=RIGHT, fill=Y)

rows = Text(ide)
rows.insert('1.0', '1')
rows.configure(width=5, bg=rowsbackground, fg='white', state=DISABLED)
rows.pack(side=LEFT, fill=BOTH)

editor = Text(ide, wrap="none", undo=True, maxundo=-1, autoseparators=True)
editor.configure(width=80, bg=background, fg=foreground, insertbackground='white', selectbackground='darkviolet')
editor.pack(side=LEFT, fill=BOTH, expand=True)
editor.focus()

scrollbar['command'] = on_scrollbar
horscrollbar['command'] = on_hscrollbar
rows['yscrollcommand'] = on_textscroll
editor['yscrollcommand'] = on_textscroll
editor['xscrollcommand'] = ontext_horizscroll

set_word_boundaries(editor)

# Syntax Highlighting
cdg = ic.ColorDelegator()

cdg.tagdefs['COMMENT'] = {'foreground': 'orangered', 'background': background}
cdg.tagdefs['KEYWORD'] = {'foreground': 'lime', 'background': background}
cdg.tagdefs['BUILTIN'] = {'foreground': 'cyan', 'background': background}
cdg.tagdefs['STRING'] = {'foreground': 'yellow', 'background': background}
cdg.tagdefs['DEFINITION'] = {'foreground': 'orange', 'background': background}
	
ip.Percolator(editor).insertfilter(cdg)
		
def new_word_fun(event):
	global text_list
	curr = editor.index(tk.INSERT)
	d = decimal.Decimal(curr)
	exp_num = abs(d.as_tuple().exponent)
	new_integ, dec = divmod(float(curr), 1)
	#x
	new_integ = decimal.Decimal(new_integ)
	dec_num = d - new_integ
	for i in range(exp_num):
		#y
		dec_num = dec_num * 10
	new_word = ""
	found = False
	dec_num -= 1
	while(dec_num >= 0 and not found):
		c = editor.get("%d.%d" % (new_integ, dec_num))
		if c.isalpha() or c == '_' or c == '-':
			dec_num -= 1
			new_word = new_word + c
		else:
			found = True
	new_word = new_word[::-1]
	text_list.append(new_word)
	text_list = list(set(text_list))
	
def ok_word(event):
	editor.tag_remove(SEL, '1.0', END)
	editor.unbind('<Tab>')
	editor.bind('<Tab>', tab)
	
def auto_fill(event):
	global curr
	global text_list
	global index
	global maybe_list
	global word_now
	global dec
	global new_integ
	if len(event.keysym) == 1:		
		maybe_list = []
		curr = editor.index(tk.INSERT)
		d = decimal.Decimal(curr)
		exp_num = abs(d.as_tuple().exponent)
		new_integ, dec = divmod(float(curr), 1)
		#x
		new_integ = decimal.Decimal(new_integ)
		dec_num = d - new_integ
		for i in range(exp_num):
			#y
			dec_num = dec_num * 10
		dec_num = int(dec_num)
		dec = dec_num
		new_word = ""
		found = False
		dec_num = dec_num -1
		count = 0
		first = ''
		while(dec_num >= 0 and not found):
			c = editor.get("%d.%d" % (new_integ, dec_num))
			if count == 0:
				first = c
			count += 1
			if c.isalpha() or c == '_' or c == '-':
				dec_num -= 1
				new_word = new_word + c
			else:
				found = True
		new_word = new_word[::-1]
		if not word_now:
			word_now = new_word
		if first.isalpha():
			for l in text_list:
				try:
					m = l.index(new_word)
					if m == 0:
						#maybe_list.append(l)
						maybe_list.append(l.replace(new_word, ''))
				except:
					pass
	
		if maybe_list:
			editor.unbind('<Tab>')
			editor.bind('<Tab>', ok_word)
			index = 0
			editor.insert(curr, maybe_list[index])
			editor.tag_add('sel', curr, '%d.%d' % (new_integ, dec + len(maybe_list[index])))

def control_auto_fill(event):
	global curr
	global text_list
	global index
	global maybe_list
	global word_now
	global dec
	global new_integ
	global selected

	if maybe_list:	
		if event.keysym == "Shift_R":
			editor.tag_remove(SEL, '1.0', END)
		try:	
			if event.keysym == "Alt_R":
				selected = True
				if index < len(maybe_list) - 1:
					index += 1
				else:
					index = 0
				first = editor.index("sel.first")
				editor.delete("sel.first", "sel.last")
				editor.insert(curr, maybe_list[index])
				editor.tag_add('sel', first, '%d.%d' % (new_integ, dec + len(maybe_list[index])))
		except:
			pass
			
def set_auto_fill(*event):
	global autofill
	if autofill:
		editor.unbind('<space>')
		editor.unbind('<Key>')	
		editor.unbind('<KeyRelease>')
	if not autofill:
		text_list_update(True)
		editor.bind('<space>', text_list_update)
		editor.bind('<Key>', control_auto_fill)	
		editor.bind('<KeyRelease>', auto_fill)
	autofill = not autofill

# Menu settings  
menu_bar = Menu(ide)
file_menu = Menu(menu_bar, bg='navy', fg='white')

file_menu.add_command(label = 'New', command = new_file, accelerator = "Ctrl+N")
file_menu.add_command(label = 'Open', command = open_file, accelerator = "Ctrl+O")
file_menu.add_command(label = 'Save', command = save, accelerator = "Ctrl+S")
file_menu.add_command(label = 'Save as', command = save_as, accelerator = "Ctrl+Alt+S")
file_menu.add_command(label = 'Exit', command = exit, accelerator = "Ctrl+Q")
menu_bar.add_cascade(label = 'File', menu = file_menu)

edit_menu = Menu(menu_bar, bg='navy', fg='white')
edit_menu.add_command(label = 'Copy', command = text_copy, accelerator = "Ctrl-C")
edit_menu.add_command(label = 'Cut', command = text_cut, accelerator = "Ctrl-X")
edit_menu.add_command(label = 'Paste', command = text_paste, accelerator = "Ctrl-V")
edit_menu.add_command(label = 'Select All', command = select_all, accelerator = "Ctrl-A")
edit_menu.add_command(label = 'Indent', command = gen_indent, accelerator = "Tab")
edit_menu.add_command(label = 'Reverse Indent', command = gen_revindent, accelerator = "Ctrl-,")
edit_menu.add_command(label = 'Search text', command = search_text, accelerator = "Ctrl-F")
edit_menu.add_command(label = 'Auto-fill on/off', command = set_auto_fill, accelerator = "Ctrol-Alt-B")
edit_menu.add_command(label = 'Indentation fixer', command = indent_fix, accelerator = "Ctrl-L")
menu_bar.add_cascade(label = 'Edit', menu = edit_menu)

window_menu = Menu(menu_bar, bg='navy', fg='white')
window_menu.add_command(label = 'Fullscreen on/off', command = set_fullscreen, accelerator = "F11")
window_menu.add_command(label = 'Zoom in', command = zoom_in, accelerator = "Ctrl'+'")
window_menu.add_command(label = 'Zoom out', command = zoom_out, accelerator = "Ctrl'-'")
menu_bar.add_cascade(label = 'Window', menu = window_menu)

run_bar = Menu(menu_bar, bg='navy', fg='white')
run_bar.add_command(label = 'Run', command = cmd_run, accelerator = "Ctrl+R")
run_bar.add_command(label = 'Shell', command = cmd_run_shell, accelerator = "Ctrl+Alt+R")
run_bar.add_command(label = 'Run alone', command = run_alone, accelerator = "Ctrl+P")
run_bar.add_command(label = 'Run with arguments', command = run_args)
menu_bar.add_cascade(label = 'Run', menu = run_bar)
ide.config(menu = menu_bar)	
	
# Non-menu functions
def tab(*args):	
	try:
		start_line = math.trunc(float(editor.index("sel.first")))
		last_line = math.trunc(float(editor.index("sel.last")))
		for x in range(start_line, last_line + 1):
			editor.insert(f"{x}.0", "\t")
			
		return 'break'   
	except:
		pass

def add_comments(*args):
	try:
		start_line = math.trunc(float(editor.index("sel.first")))
		last_line = math.trunc(float(editor.index("sel.last")))
		
		for x in range(start_line, last_line+1):
			if editor.get(f"{x}.0") == '#':
				editor.delete(f"{x}.0")
			else:	
				editor.insert(f"{x}.0", "#")

		return 'break'

	except:
		pass

def is_tab_reversible():
	try:
		start_line = math.trunc(float(editor.index("sel.first")))
		last_line = math.trunc(float(editor.index("sel.last")))
		for x in range(start_line, last_line + 1):
				if editor.get(f"{x}.0").isalpha():
					return False
		return True
	except:
		pass 
		
def reverse_tab(*args):
	if is_tab_reversible():
		try:
			start_line = math.trunc(float(editor.index("sel.first")))
			last_line = math.trunc(float(editor.index("sel.last")))
			
			for x in range(start_line, last_line+1):
				if not editor.get(f"{x}.0").isalpha():
					editor.delete(f"{x}.0")
					
			return 'break'
		except:
			pass
	
def colon_auto_indent(event):
	current = math.trunc(float(editor.index("insert")))
	current = str(current) + '.0'
	current_text = editor.get(current, "insert")
	print(current_text)
	for k in keyword.kwlist:	
		if k in current_text:		
			line = editor.get("insert linestart", "insert")
			match = re.match(r'^(\s+)', line)
			whitespace = match.group(0) if match else ""
			editor.insert("insert", f":\n{whitespace}\t")
			draw_lines(event)
			return "break"
	
def auto_indent(event):
	text = event.widget
	line = text.get("insert linestart", "insert")
	match = re.match(r'^(\s+)', line)
	whitespace = match.group(0) if match else ""
	text.insert("insert", f"\n{whitespace}")
	draw_lines(event)
	return "break"
	
def cursor_back():
	curr = editor.index(tk.INSERT)
	d = decimal.Decimal(curr)
	exp_num = abs(d.as_tuple().exponent)
	new_integ, dec = divmod(float(curr), 1)
	new_integ = decimal.Decimal(new_integ)
	dec_num = d - new_integ
	for i in range(exp_num):
		dec_num = dec_num * 10
	editor.mark_set("insert", "%d.%d" % (new_integ, dec_num - 1))

def autocomplete_rpar(event):
	editor.insert(tk.INSERT, ')')
	cursor_back()
	
def autocomplete_quote(event):
	editor.insert(tk.INSERT, "'")
	cursor_back()

def autocomplete_dbquote(event):
	editor.insert(tk.INSERT, '"')
	cursor_back()
		
def draw_lines(event):
	num_rows = int(editor.index('end').split('.')[0])
	rows.configure(state=NORMAL)
	rows.delete("1.0","end")
	rows.insert('1.0', '1')
	row = 2
	while(row < num_rows):
		rows.configure(state=NORMAL)
		rows.insert(END,"\n" + str(row))
		row += 1
	rows.configure(state=DISABLED)
	
def zoom_wheel(event):
	if event.delta == 120:
		zoom_in(event)
	else:
		zoom_out(event)
		
def rClicker(e):
	''' right click context menu for all Tk Entry and Text widgets
	'''

	try:
		def rClick_Copy(e, apnd=0):
			e.widget.event_generate('<Control-c>')

		def rClick_Cut(e):
			e.widget.event_generate('<Control-x>')

		def rClick_Paste(e):
			e.widget.event_generate('<Control-v>')

		e.widget.focus()

		nclst=[
			(' Cut', lambda e=e: rClick_Cut(e)),
			(' Copy', lambda e=e: rClick_Copy(e)),
			(' Paste', lambda e=e: rClick_Paste(e)),
			]

		rmenu = Menu(None, tearoff=0, takefocus=0)

		for (txt, cmd) in nclst:
			rmenu.add_command(label=txt, command=cmd)

		rmenu.tk_popup(e.x_root+10, e.y_root+10,entry="0")

	except TclError:
		print (' - rClick menu, something wrong')
		pass

	return "break"
	
def rClickbinder(r):
	try:
		for b in [ 'Text', 'Entry', 'Listbox', 'Label']:
			r.bind_class(b, sequence='<Button-3>',
						 func=rClicker, add='')
	except TclError:
		print (' - rClickbinder, something wrong')
		pass

def check_rparen(event):
	curr = editor.index(tk.INSERT)
	d = decimal.Decimal(curr)
	exp_num = abs(d.as_tuple().exponent)
	new_integ, dec = divmod(float(curr), 1)
	new_integ = decimal.Decimal(new_integ)
	dec_num = d - new_integ
	for i in range(exp_num):
		dec_num = dec_num * 10
	if editor.get("%d.%d" % (new_integ, dec_num - 1)) == '(':
		editor.delete("%d.%d" % (new_integ, dec_num))
	
# Key Bindings
editor.bind('<Tab>', tab)
editor.bind('<Control-,>', reverse_tab)
editor.bind('<Control-q>', exit)
editor.bind('<Control-n>', new_file)	
editor.bind('<Control-o>', open_file)
editor.bind('<Control-s>', save)
editor.bind('<Control-Alt-s>', save_as)
editor.bind('<Control-r>', cmd_run)
editor.bind('<Control-p>', run_alone)
editor.bind('<Control-Alt-r>', cmd_run_shell)
editor.bind('<Control-/>', add_comments)
editor.bind(':', colon_auto_indent)
editor.bind('<Return>', auto_indent)
editor.bind('<KeyRelease-parenleft>', autocomplete_rpar)
editor.bind('<)>', check_rparen)
editor.bind('"', autocomplete_dbquote)
editor.bind("'", autocomplete_quote)
editor.bind('<Control-+>', zoom_in)
editor.bind('<Control-minus>', zoom_out)
editor.bind('<Control-MouseWheel>', zoom_wheel)
editor.bind('<Button-3>',rClicker, add='')
editor.bind('<Control-f>', search_text)
editor.bind('<Control-l>', indent_fix)
editor.bind('<Control-Alt-b>', set_auto_fill)
ide.bind('<F11>', set_fullscreen)
ide.bind('<Escape>', end_fullscreen)

zoom_in(True)

ide.mainloop()









