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

		inlist = False
		typelist = ""
		#md rendering
		if (".md" in file_n):
			with open(file_path) as f:
				for x in f:

					if(not re.search("^\d+\.+\s+(.*)$", x) and not re.findall("^-\s+(.*)$", x)):
						if(inlist):
							inlist = False
							html += f"</{typelist}>"
							typelist = ""

					exist = re.findall("(?<!!)\[.+?\]\(.+?\)", x)
					if(exist):
						url = x[x.index("(") + 1: x.index(")")]
						message = x[x.index("[") + 1: x.index("]")]
						x = re.sub("(?<!!)\[.+?\]\(.+?\)", f"<a href={url}>{message}</a>", x)

					exist = re.findall("^(!){1}\[.{1,}\]\(.{1,}\)$", x)	
					if(exist):
						url = x[x.index("(") + 1: x.index(")")]
						message = x[x.index("[") + 1: x.index("]")]
						x = re.sub("^(!){1}\[.{1,}\]\(.{1,}\)$",f"<br><img src=\"file://{url}\" alt=\"{message}\" width=\"500px\" height=\"500px\">" ,x)

					exist = re.findall("^(-){3,}$", x)
					if(exist):
						x = re.sub("^(-){3,}$", "<div width=\"100%\" style=\"background-color:white;\"></div>", x)

					exist = re.findall("(`){1}.{0,}(`){1}", x)
					if(exist):
						message = x[x.index("`") + 1: len(x) - 2]
						x = re.sub("(`){1}.{0,}(`){1}", f"<code>{message}</code>", x)

					exist = re.findall("\*\*(.*?)\*\*", x)
					if(exist):
						message = re.findall("[^*]", x)
						word = ""
						for w in message:
							word += w
						x = re.sub("\*\*(.*?)\*\*", f"<b>{word}</b>", x)	

					exist = re.findall("(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)", x)
					if(exist):
						message = re.findall("[^*]", x)
						word = ""
						for w in message:
							word += w
						x = re.sub("(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)", f"<em>{word}</em>", x)	

					exist = re.findall("[>] .{0,}", x)
					if(exist):
						message = x[2: len(x) - 1]
						x = re.sub("[>] .{0,}", f"<div style=\"border-left: 3px solid gray;\"><p>{message}</p></div>", x)
					
					exist = re.findall("^\d+\.+\s+(.*)$", x)
					if(exist):
						if(not inlist):
							typelist = "ol"
							html += "<ol>"
							inlist = True
						elif(inlist and typelist != "ol"):
							html += "</ul><br><ol>"

						message = x[2: len(x)]
						x = re.sub("\d+\.+\s+(.*)$", f"<li>{message}</li>", x)

					exist = re.findall("^-\s+(.*)$", x)
					if(exist):
						if(not inlist):
							typelist = "ul"
							html += "<ul>"
							inlist = True
						elif(inlist and typelist != "ul"):
							html += "</ol><br><ul>"

						message = x[2: len(x)]
						x = re.sub("-\s+(.*)$", f"<li>{message}</li>", x)	

					exist = re.findall("\n$", x)
					if(exist):
						x = re.sub("\n$", "<br>", x)

					html += x		
		'''
			dynamic images (if height > width... etc. [max size 500 x 500])
			add support for https:// res:// and data: images
			add nested blockquotes
			add the ability to add the things (**, ``, etc.) in the text
			fix the gaps under the lists
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


			
			