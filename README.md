# A markdown viewer addon for Sublime Text

This was made for Sublime Text 3 to render markdown directly inside the text editor.

!["this is what the markdown looks like in use"](img.png)

## Usage

by pressing the "open markdown in another window" option in the context menu on a markdown file or by pressing [alt+ctrl+m], a secondary window will open displaying the markdown rendered.

As of now all images have a fixed size of 500px x 500px however there are plans to allow custom sizes as well as more dynamic sizes.

More features are currently being worked on.

## Installation

As of now you can download the addon by simply cloning the directory.
and move "open_md_viewer.py" to Preferences -> Browse Packages -> User

then go to Preferences -> Key Bindings and add "{"keys": ["ctrl+alt+m"], "command": "open_md_viewer"}" to the options

and finally add "{ "command": "open_md_viewer", "caption": "Open markdown in another window" }" to (ctrl+shift+p) Open Ressource -> Default -> Context.sublime_menu

### Notes

HTML rendering is also supported
Only PNG, JPG and GIF (static) are supported by phantom.

[a list of supported html tags]("https://www.sublimetext.com/docs/minihtml.html")

