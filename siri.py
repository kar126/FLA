import tkinter as tk

# Function to eliminate epsilon productions in the CFG
def eliminate_epsilon_productions(cfg_text):
    productions = {}
    non_terminals = set()

    # Split input text into lines and process each line
    lines = cfg_text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line:
            parts = line.split('->')
            lhs = parts[0].strip()
            rhs = parts[1].strip()

            non_terminals.add(lhs)
            symbols = rhs.split('|')
            productions[lhs] = symbols

    # Find nullable non-terminals
    nullable = set()
    changed = True

    while changed:
        changed = False
        for non_terminal, symbols in productions.items():
            for symbol in symbols:
                if all(s in nullable or s == 'ε' or not s.isupper() for s in symbol):
                    if non_terminal not in nullable:
                        nullable.add(non_terminal)
                        changed = True

    # Generate new productions to eliminate ε-productions
    updated_productions = {key: [value for value in values if value != 'ε'] for key, values in productions.items()}

    for key, values in productions.items():
        for symbol in values:
            if all(s in nullable or s == 'ε' for s in symbol):
                for subset in range(1, 2 ** len(symbol)):
                    new_prod = ''.join(symbol[i] for i in range(len(symbol)) if not ((subset >> i) & 1))
                    if new_prod and new_prod not in updated_productions[key]:
                        updated_productions[key].append(new_prod)

    return updated_productions

# Function to handle the GUI process button
def process_cfg():
    input_text = input_textbox.get("1.0", "end-1c")  # Get text from input textbox
    updated_cfg = eliminate_epsilon_productions(input_text)
    
    output_textbox.delete("1.0", "end")  # Clear previous content in output textbox
    for key, values in updated_cfg.items():
        output_textbox.insert("end", f"{key} -> {'|'.join(values)}\n")  # Display the result in output textbox

# Create the main application window
app = tk.Tk()
app.title("CFG Epsilon Eliminator")

# Input Textbox
input_label = tk.Label(app, text="Enter CFG:")
input_label.pack()

input_textbox = tk.Text(app, height=10, width=40)
input_textbox.pack()

# Output Textbox
output_label = tk.Label(app, text="CFG without ε-productions:")
output_label.pack()

output_textbox = tk.Text(app, height=10, width=40)
output_textbox.pack()

# Process Button
process_button = tk.Button(app, text="Process CFG", command=process_cfg)
process_button.pack()

# Start the GUI application
app.mainloop()
