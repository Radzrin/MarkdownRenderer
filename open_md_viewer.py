import sublime
import sublime_plugin
import os
import re


class open_md_viewer(sublime_plugin.TextCommand):

	def is_visible(self):
		file_path = self.view.file_name()
		file_n = os.path.splitext(file_path.lower())	

		if not file_path:	
			return False

		if (".md" in file_n or ".html" in file_n or ".htm" in file_n):
			return True

	def run(self, edit):
		#self.view.insert(edit, 0, "Hello, World!")
		current_window= self.view.window()
		file_path = self.view.file_name()
		file_n = os.path.splitext(file_path.lower())
		view = self.view


		for view in current_window.views_in_group(1):
			view.close()
		#resets the view
		current_window.set_layout({
			"cols": [0.0, 1.0],
			"rows": [0.0, 1.0],
			"cells": []
		})

		#sets split view
		current_window.set_layout({
			"cols": [0.0, 0.5, 1.0],
			"rows": [0.0, 1.0],
			"cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
		})

		
		new_tab_view = current_window.new_file()
		#image = "file://C:/Users/user/Downloads/tgdfgtd.png"
		html = "<br>"
		
		#html rendering
		if (".html" in file_n or ".htm" in file_n):
			with open(file_path) as f:
				for x in f:
					if "img" in x:
						html += "<br>"		
					html += x

		#md rendering
		if (".md" in file_n):
			with open(file_path) as f:
				for x in f:
					exist = re.findall("^\[.{1,}\]\(.{1,}\)$", x)
					if(exist):
						url = x[x.index("(") + 1: x.index(")")]
						message = x[x.index("[") + 1: x.index("]")]
						html += f"<a href={url}>{message}</a>"
						continue

					exist = re.findall("^(!){1}\[.{1,}\]\(.{1,}\)$", x)	
					if(exist):
						url = x[x.index("(") + 1: x.index(")")]
						message = x[x.index("[") + 1: x.index("]")]
						html += f"<br><img src=\"file://{url}\" alt=\"{message}\" width=\"500px\" height=\"500px\">"	
						continue

					exist = re.findall("^(-){3,}$", x)
					if(exist):
						html += "<div width=\"100%\" style=\"background-color:white;\"></div>"	
						continue

					exist = re.findall("^(`){1}.{0,}(`){1}", x)
					if(exist):
						message = x[x.index("`") + 1: len(x) - 2]
						html += f"<code>{message}</code>"	

		'''
			dynamic images (if height > width... etc. [max size 500 x 500])
			add support for https:// res:// and data: images
		
		'''
			
		f.close()	
		new_tab_view.erase_phantoms ("test")
		new_tab_view.add_phantom ("test", new_tab_view.sel()[0], html, sublime.LAYOUT_BLOCK)	
		new_tab_view.set_name("Markdown viewer")
		
		#new_tab_view.run_command("insert",{"characters": "Hello! このテキストは新しいタブを開いた直後に自動生成されました。\n"})
		#new_tab_view.run_command("insert",{"characters": "Hello! このテキストは新しいタブを開いた直後に自動生成されました。\n"})
		#current_window.open_file("http://127.0.0.1:8080")
		# open new window in splitview (2nd hardest)x
		# read the file
		# render the md
		# optional (render the html)


			
			