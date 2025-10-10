import tkinter as tk
from tkinter import scrolledtext, messagebox
import tkinter.filedialog as fd
import ttkbootstrap as tb
from ttkbootstrap import ttk
import sys
import io
import threading
import argparse
from neuroflow.core import get_parser, run_command
from neuroflow.citations import citations


class RedirectText(io.StringIO):
    """Redirect sys.stdout and sys.stderr to a Tkinter Text widget."""

    def __init__(self, text_ctrl):
        super().__init__()
        self.text_ctrl = text_ctrl

    def write(self, s):
        self.text_ctrl.configure(state="normal")
        self.text_ctrl.insert(tk.END, s)
        self.text_ctrl.see(tk.END)
        self.text_ctrl.configure(state="disabled")

    def flush(self):
        pass


class NeuroflowGUI(tb.Window):
    def __init__(self):
        super().__init__(themename="superhero")

        self.title("Neuroflow GUI")
        self.geometry("900x300")
        self.resizable(True, True)

        # Load parser & commands
        self.parser = get_parser()
        self.subparsers_actions = self._get_subparsers(self.parser)

        # Variables
        self.selected_command = None
        self.arg_vars = {}  # Map arg name -> tk variable

        # Setup UI panels
        self._setup_ui()

        # Populate left panel with commands
        self._populate_commands()

    def _get_subparsers(self, parser):
        # Extract subparsers action object from parser._actions list
        for action in parser._actions:
            if isinstance(action, argparse._SubParsersAction):
                return action.choices
        return {}

    def _setup_ui(self):
        # Layout: 3 frames side-by-side
        self.left_frame = ttk.Frame(self, width=150, relief=tk.SUNKEN, borderwidth=1)
        self.middle_frame = ttk.Frame(self, width=500, relief=tk.SUNKEN, borderwidth=1)
        self.right_frame = ttk.Frame(self, width=250, relief=tk.SUNKEN, borderwidth=1)

        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.middle_frame.pack(
            side=tk.LEFT, fill=tk.BOTH, expand=True, padx=12, pady=12
        )
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)

        # Left: Listbox for commands
        ttk.Label(self.left_frame, text="Commands").pack(pady=5)
        self.cmd_tree = ttk.Treeview(self.left_frame, show="tree")
        self.cmd_tree.pack(fill=tk.BOTH, expand=True, padx=5)
        self.cmd_tree.bind("<<TreeviewSelect>>", self.on_command_select)

        # Middle: Scrollable frame for argument inputs
        self.middle_canvas = tk.Canvas(self.middle_frame)
        self.middle_scrollbar = ttk.Scrollbar(
            self.middle_frame, orient="vertical", command=self.middle_canvas.yview
        )
        self.args_frame = ttk.Frame(self.middle_canvas)

        self.args_frame.bind(
            "<Configure>",
            lambda e: self.middle_canvas.configure(
                scrollregion=self.middle_canvas.bbox("all")
            ),
        )

        self.middle_canvas.create_window((0, 0), window=self.args_frame, anchor="nw")
        self.middle_canvas.configure(yscrollcommand=self.middle_scrollbar.set)

        self.middle_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.middle_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Right: Run button + output text
        self.run_button = ttk.Button(
            self.right_frame, text="Run", command=self.run_selected_command
        )
        self.run_button.pack(pady=10, padx=10, anchor="n")

        ttk.Label(self.right_frame, text="Output").pack()
        self.output_text = scrolledtext.ScrolledText(
            self.right_frame, state="disabled", height=30, width=40
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _populate_commands(self):
        commands = [cmd for cmd in self.subparsers_actions.keys() if cmd != "gui"]

        grouped = {}
        for cmd in commands:
            subparser = self.subparsers_actions[cmd]
            cat = getattr(subparser, "category", "Other")
            grouped.setdefault(cat, []).append(cmd)

        # Clear and rebuild the tree
        for category, cmds in sorted(grouped.items()):
            parent = self.cmd_tree.insert("", "end", text=category, open=True)
            for cmd in sorted(cmds):
                self.cmd_tree.insert(parent, "end", text=cmd, values=(cmd,))

    def on_command_select(self, event):
        selected = self.cmd_tree.selection()
        if not selected:
            return

        item = selected[0]
        cmd = self.cmd_tree.item(item, "text")

        # Ignore category headers (which have children)
        if len(self.cmd_tree.get_children(item)) > 0:
            return

        self.selected_command = cmd
        self._build_args_form(cmd)

    def _show_help_window(self, title, help_text):
        win = tk.Toplevel()
        win.title(title)
        win.geometry("600x400")
        txt = scrolledtext.ScrolledText(win, wrap=tk.WORD)
        txt.pack(fill=tk.BOTH, expand=True)
        txt.insert(tk.END, help_text)
        txt.configure(state="disabled")

    def _build_args_form(self, cmd):
        # Clear previous widgets
        for widget in self.args_frame.winfo_children():
            widget.destroy()
        self.arg_vars.clear()

        parser = self.subparsers_actions[cmd]

        self.args_frame.grid_columnconfigure(0, weight=1)
        self.args_frame.grid_columnconfigure(1, weight=1)

        citation_text = citations.get(cmd, "")

        help_btn = ttk.Button(
            self.args_frame,
            text=f"Show help for '{cmd}'",
            command=lambda: self._show_help_window(
                f"Help: {cmd}",
                f"{parser.format_help()}\n\nReferences:\n{citation_text}",
            ),
            bootstyle="info-outline",
        )
        help_btn.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Build argument fields starting at row=1 (or just skip inputs if you want)
        row = 1
        for action in parser._actions:
            if action.help == argparse.SUPPRESS or action.dest in ("command", "help"):
                continue

            label_text = f"{action.dest}"
            if action.required:
                label_text += " *"
            ttk.Label(self.args_frame, text=label_text).grid(
                row=row, column=0, sticky=tk.W, pady=2, padx=5
            )

            var = None
            frame = ttk.Frame(self.args_frame)
            frame.grid(row=row, column=1, sticky=tk.EW, pady=2, padx=5)
            self.args_frame.columnconfigure(1, weight=1)

            def browse_file(var=var):
                path = fd.askopenfilename()
                if path:
                    var.set(path)

            def browse_dir(var=var):
                path = fd.askdirectory()
                if path:
                    var.set(path)

            def browse_file_list(var):
                files = fd.askopenfilenames(title="Select files")
                if files:
                    # Store as a tuple/list
                    var.set(", ".join(files))  # for display in Entry
                    var.file_list = list(files)  # store actual list separately

            def browse_file_save(var):
                path = fd.asksaveasfilename(
                    title="Select output file",
                    defaultextension=".csv",
                    filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
                )
                var.set(path)

            def create_browswer_dialog(frame, var, browse_function):
                entry_widget = ttk.Entry(frame, textvariable=var)
                entry_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
                browse_btn = ttk.Button(
                    frame, text="Browse", command=lambda v=var: browse_function(v)
                )
                browse_btn.pack(side=tk.RIGHT)

            if action.choices:
                var = tk.StringVar(value=action.choices[0])
                entry_widget = ttk.Combobox(
                    frame, textvariable=var, values=action.choices, state="readonly"
                )
                entry_widget.pack(fill=tk.X, expand=True)
            elif action.type == int:
                var = tk.IntVar()
                entry_widget = ttk.Entry(frame, textvariable=var)
                entry_widget.pack(fill=tk.X, expand=True)
            elif action.type == float:
                var = tk.DoubleVar()
                entry_widget = ttk.Entry(frame, textvariable=var)
                entry_widget.pack(fill=tk.X, expand=True)
            else:
                var = tk.StringVar()

                # Detect if arg looks like a path or file
                name_lower = action.dest.lower()

                match name_lower.split("_")[0]:
                    case "savefile":
                        create_browswer_dialog(frame, var, browse_file_save)
                    case "savedir":
                        create_browswer_dialog(frame, var, browse_dir)
                    case "file":
                        create_browswer_dialog(frame, var, browse_file)
                    case "list":
                        create_browswer_dialog(frame, var, browse_file_list)
                    case _:
                        entry_widget = ttk.Entry(frame, textvariable=var)
                        entry_widget.pack(fill=tk.X, expand=True)

            self.arg_vars[action.dest] = (var, action)
            row += 1

    def run_selected_command(self):
        cmd = self.selected_command
        if not cmd:
            messagebox.showwarning(
                "No command selected", "Please select a command to run."
            )
            return

        # Build args namespace
        args_dict = {"command": cmd}
        for argname, (var, action) in self.arg_vars.items():
            val = var.get()
            if val == "" and action.required:
                messagebox.showerror(
                    "Missing argument", f"Argument '{argname}' is required."
                )
                return
            # Convert type if needed (comboboxes etc.)
            if action.type and val != "":
                try:
                    val = action.type(val)
                except Exception as e:
                    messagebox.showerror(
                        "Invalid argument",
                        f"Could not convert argument '{argname}': {e}",
                    )
                    return
            args_dict[argname] = val

        args = argparse.Namespace(**args_dict)

        # Clear output
        self.output_text.configure(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.configure(state="disabled")

        # Run command in separate thread to avoid freezing UI
        threading.Thread(target=self._run_in_thread, args=(args,), daemon=True).start()

    def _run_in_thread(self, args):
        # Redirect stdout/stderr
        sys.stdout = RedirectText(self.output_text)
        sys.stderr = RedirectText(self.output_text)
        try:
            run_command(args)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Reset stdout/stderr after done
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__


if __name__ == "__main__":
    app = NeuroflowGUI()
    app.mainloop()
