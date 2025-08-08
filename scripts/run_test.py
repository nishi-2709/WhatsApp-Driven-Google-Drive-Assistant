#!/usr/bin/env python3
"""
WhatsApp-Driven Google Drive Assistant - Test Launcher
This script provides options to run the test in different modes.
"""

import sys
import os
import json
import time
import threading
from datetime import datetime

# Try to import optional dependencies
try:
    import flask
    from flask import Flask, render_template_string, request, jsonify
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

class WhatsAppDriveAssistant:
    def __init__(self):
        self.audit_log = []
        self.simulation_mode = True
        
    def log_operation(self, operation, details):
        """Log an operation for audit purposes"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'details': details
        }
        self.audit_log.append(log_entry)
        return log_entry
        
    def parse_command(self, message_body):
        """Parse WhatsApp message and extract command"""
        message_body = message_body.strip().upper()
        parts = message_body.split()
        
        if not parts:
            return {'command': 'UNKNOWN', 'args': []}
            
        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        return {'command': command, 'args': args}
        
    def handle_help(self, args):
        """Handle HELP command"""
        help_text = """🤖 WhatsApp-Driven Google Drive Assistant

Available Commands:
• LIST /folder - List files in a folder
• DELETE /path/to/file - Delete a file (requires CONFIRM)
• MOVE /source /destination - Move a file
• SUMMARY /folder - Summarize documents in a folder
• HELP - Show this help message

Examples:
• LIST /ProjectX
• DELETE /ProjectX/report.pdf CONFIRM
• MOVE /ProjectX/report.pdf /Archive
• SUMMARY /ProjectX"""
        return help_text
        
    def handle_list(self, args):
        """Handle LIST command"""
        if not args:
            return "❌ Error: Please specify a folder path (e.g., LIST /ProjectX)"
            
        folder_path = args[0]
        self.log_operation('LIST', f"Listing files in {folder_path}")
        
        # Simulate file listing
        mock_files = [
            {"name": "report.pdf", "type": "PDF", "size": "2.3MB", "modified": "2024-01-15"},
            {"name": "presentation.pptx", "type": "PowerPoint", "size": "5.1MB", "modified": "2024-01-14"},
            {"name": "data.xlsx", "type": "Excel", "size": "1.2MB", "modified": "2024-01-13"},
            {"name": "notes.txt", "type": "Text", "size": "15KB", "modified": "2024-01-12"}
        ]
        
        response = f"📁 Files in {folder_path}:\n"
        for file in mock_files:
            response += f"• {file['name']} ({file['type']}, {file['size']}, {file['modified']})\n"
            
        return response.strip()
        
    def handle_delete(self, args):
        """Handle DELETE command"""
        if not args:
            return "❌ Error: Please specify a file path (e.g., DELETE /ProjectX/report.pdf)"
            
        file_path = args[0]
        
        # Check for confirmation
        if len(args) < 2 or args[1] != 'CONFIRM':
            return f"⚠️  To delete {file_path}, please add 'CONFIRM' to your command.\nExample: DELETE {file_path} CONFIRM"
            
        self.log_operation('DELETE', f"Deleting file {file_path}")
        return f"✅ Successfully deleted {file_path}"
        
    def handle_move(self, args):
        """Handle MOVE command"""
        if len(args) < 2:
            return "❌ Error: Please specify source and destination (e.g., MOVE /source/file.pdf /destination)"
            
        source = args[0]
        destination = args[1]
        
        self.log_operation('MOVE', f"Moving {source} to {destination}")
        return f"✅ Successfully moved {source} to {destination}"
        
    def handle_summary(self, args):
        """Handle SUMMARY command"""
        if not args:
            return "❌ Error: Please specify a folder path (e.g., SUMMARY /ProjectX)"
            
        folder_path = args[0]
        self.log_operation('SUMMARY', f"Summarizing documents in {folder_path}")
        
        # Simulate AI summarization
        mock_summaries = {
            "report.pdf": "Quarterly financial report showing 15% revenue growth and improved profit margins.",
            "presentation.pptx": "Sales presentation covering Q4 results and Q1 projections.",
            "data.xlsx": "Customer analytics data with key performance indicators.",
            "notes.txt": "Meeting notes from the quarterly planning session."
        }
        
        response = f"📊 Summary of documents in {folder_path}:\n"
        for filename, summary in mock_summaries.items():
            response += f"• {filename}: {summary}\n"
            
        return response.strip()
        
    def handle_unknown(self, args):
        """Handle unknown commands"""
        return "❌ Unknown command. Type 'HELP' for available commands."
        
    def process_message(self, message_body):
        """Process incoming WhatsApp message"""
        # Parse command
        parsed = self.parse_command(message_body)
        command = parsed['command']
        args = parsed['args']
        
        # Route to appropriate handler
        if command == 'HELP':
            response = self.handle_help(args)
        elif command == 'LIST':
            response = self.handle_list(args)
        elif command == 'DELETE':
            response = self.handle_delete(args)
        elif command == 'MOVE':
            response = self.handle_move(args)
        elif command == 'SUMMARY':
            response = self.handle_summary(args)
        else:
            response = self.handle_unknown(args)
            
        return response

def run_terminal_test():
    """Run the terminal-based test"""
    print("🚀 Starting terminal-based test...")
    print("=" * 50)
    
    assistant = WhatsAppDriveAssistant()
    
    # Run test scenarios
    test_cases = [
        "HELP",
        "LIST /ProjectX",
        "DELETE /ProjectX/report.pdf",
        "DELETE /ProjectX/report.pdf CONFIRM",
        "MOVE /ProjectX/report.pdf /Archive",
        "SUMMARY /ProjectX",
        "UNKNOWN_COMMAND"
    ]
    
    for test_case in test_cases:
        print(f"\n🔍 Testing: {test_case}")
        print("-" * 30)
        response = assistant.process_message(test_case)
        print(f"📤 Response:\n{response}")
        
    print(f"\n✅ Test scenarios completed!")
    print(f"📊 Total operations logged: {len(assistant.audit_log)}")
    
    # Interactive mode
    print("\n🎯 Interactive Mode (type 'quit' to exit):")
    while True:
        try:
            message = input("\n📱 Enter WhatsApp message: ").strip()
            if message.lower() in ['quit', 'exit', 'q']:
                break
                
            if message:
                response = assistant.process_message(message)
                print(f"\n📤 Response:\n{response}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def run_web_test():
    """Run the web-based test"""
    if not FLASK_AVAILABLE:
        print("❌ Flask is required for web mode. Please install it first:")
        print("   pip install flask")
        return
    
    print("🌐 Starting web-based test...")
    
    app = Flask(__name__)
    assistant = WhatsAppDriveAssistant()
    
    # HTML template for the web interface
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WhatsApp-Driven Google Drive Assistant - Test Interface</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #25d366;
                text-align: center;
                margin-bottom: 30px;
            }
            .chat-container {
                height: 400px;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 20px;
                overflow-y: auto;
                background-color: #fafafa;
                margin-bottom: 20px;
            }
            .message {
                margin-bottom: 15px;
                padding: 10px 15px;
                border-radius: 8px;
                max-width: 80%;
            }
            .user-message {
                background-color: #dcf8c6;
                margin-left: auto;
                text-align: right;
            }
            .bot-message {
                background-color: #e8e8e8;
            }
            .input-container {
                display: flex;
                gap: 10px;
            }
            input[type="text"] {
                flex: 1;
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 8px;
                font-size: 14px;
            }
            button {
                padding: 12px 24px;
                background-color: #25d366;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
            }
            button:hover {
                background-color: #128c7e;
            }
            .examples {
                margin-top: 20px;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 8px;
            }
            .examples h3 {
                margin-top: 0;
                color: #333;
            }
            .example-btn {
                display: inline-block;
                margin: 5px;
                padding: 8px 12px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                font-size: 12px;
            }
            .example-btn:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 WhatsApp-Driven Google Drive Assistant</h1>
            
            <div class="chat-container" id="chatContainer">
                <div class="message bot-message">
                    Welcome! I'm your WhatsApp-Driven Google Drive Assistant. Type a command to get started, or click one of the examples below.
                </div>
            </div>
            
            <div class="input-container">
                <input type="text" id="messageInput" placeholder="Type your command here (e.g., HELP, LIST /ProjectX)" onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">Send</button>
            </div>
            
            <div class="examples">
                <h3>Quick Examples:</h3>
                <a href="#" class="example-btn" onclick="sendExample('HELP')">HELP</a>
                <a href="#" class="example-btn" onclick="sendExample('LIST /ProjectX')">LIST /ProjectX</a>
                <a href="#" class="example-btn" onclick="sendExample('DELETE /ProjectX/report.pdf')">DELETE /ProjectX/report.pdf</a>
                <a href="#" class="example-btn" onclick="sendExample('DELETE /ProjectX/report.pdf CONFIRM')">DELETE /ProjectX/report.pdf CONFIRM</a>
                <a href="#" class="example-btn" onclick="sendExample('MOVE /ProjectX/report.pdf /Archive')">MOVE /ProjectX/report.pdf /Archive</a>
                <a href="#" class="example-btn" onclick="sendExample('SUMMARY /ProjectX')">SUMMARY /ProjectX</a>
            </div>
        </div>

        <script>
            function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (message) {
                    addMessage(message, 'user');
                    input.value = '';
                    
                    fetch('/process', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({message: message})
                    })
                    .then(response => response.json())
                    .then(data => {
                        addMessage(data.response, 'bot');
                    })
                    .catch(error => {
                        addMessage('❌ Error: ' + error.message, 'bot');
                    });
                }
            }
            
            function sendExample(example) {
                document.getElementById('messageInput').value = example;
                sendMessage();
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }
            
            function addMessage(text, sender) {
                const container = document.getElementById('chatContainer');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}-message`;
                messageDiv.textContent = text;
                container.appendChild(messageDiv);
                container.scrollTop = container.scrollHeight;
            }
        </script>
    </body>
    </html>
    """
    
    @app.route('/')
    def index():
        return render_template_string(HTML_TEMPLATE)
    
    @app.route('/process', methods=['POST'])
    def process_message():
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'response': '❌ Please enter a message'})
        
        response = assistant.process_message(message)
        return jsonify({'response': response})
    
    print("🌐 Web interface starting...")
    print("🌐 URL: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the web server")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n🛑 Stopping web server...")

def run_gui_test():
    """Run the GUI-based test"""
    if not TKINTER_AVAILABLE:
        print("❌ tkinter is required for GUI mode.")
        print("   It usually comes with Python installation.")
        return
    
    print("🖥️  Starting GUI-based test...")
    
    try:
        class WhatsAppAssistantGUI:
            def __init__(self, root):
                self.root = root
                self.root.title("WhatsApp-Driven Google Drive Assistant - Test Interface")
                self.root.geometry("800x600")
                self.root.configure(bg='#f0f0f0')
                
                # Center the window on screen
                self.root.update_idletasks()
                width = self.root.winfo_width()
                height = self.root.winfo_height()
                x = (self.root.winfo_screenwidth() // 2) - (width // 2)
                y = (self.root.winfo_screenheight() // 2) - (height // 2)
                self.root.geometry(f'{width}x{height}+{x}+{y}')
                
                # Bring window to front
                self.root.lift()
                self.root.attributes('-topmost', True)
                self.root.attributes('-topmost', False)
                
                self.assistant = WhatsAppDriveAssistant()
                self.create_widgets()
                
            def create_widgets(self):
                main_frame = ttk.Frame(self.root, padding="10")
                main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
                
                self.root.columnconfigure(0, weight=1)
                self.root.rowconfigure(0, weight=1)
                main_frame.columnconfigure(1, weight=1)
                main_frame.rowconfigure(1, weight=1)
                
                title_label = ttk.Label(main_frame, text="🤖 WhatsApp-Driven Google Drive Assistant", 
                                       font=('Arial', 16, 'bold'))
                title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
                
                chat_frame = ttk.LabelFrame(main_frame, text="Chat", padding="5")
                chat_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
                chat_frame.columnconfigure(0, weight=1)
                chat_frame.rowconfigure(0, weight=1)
                
                self.chat_display = scrolledtext.ScrolledText(chat_frame, height=15, width=80, 
                                                             font=('Consolas', 10))
                self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
                
                input_frame = ttk.Frame(main_frame)
                input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
                input_frame.columnconfigure(0, weight=1)
                
                self.input_field = ttk.Entry(input_frame, font=('Arial', 10))
                self.input_field.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
                self.input_field.bind('<Return>', self.send_message)
                
                send_button = ttk.Button(input_frame, text="Send", command=self.send_message)
                send_button.grid(row=0, column=1)
                
                examples_frame = ttk.LabelFrame(main_frame, text="Quick Examples", padding="5")
                examples_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
                examples_frame.columnconfigure(0, weight=1)
                
                examples = [
                    "HELP",
                    "LIST /ProjectX", 
                    "DELETE /ProjectX/report.pdf",
                    "DELETE /ProjectX/report.pdf CONFIRM",
                    "MOVE /ProjectX/report.pdf /Archive",
                    "SUMMARY /ProjectX"
                ]
                
                for i, example in enumerate(examples):
                    btn = ttk.Button(examples_frame, text=example, 
                                   command=lambda e=example: self.send_example(e))
                    btn.grid(row=i//3, column=i%3, padx=5, pady=2, sticky=(tk.W, tk.E))
                
                self.add_message("Welcome! I'm your WhatsApp-Driven Google Drive Assistant. Type a command to get started, or click one of the examples below.", "bot")
                
            def send_message(self, event=None):
                message = self.input_field.get().strip()
                if message:
                    self.input_field.delete(0, tk.END)
                    self.add_message(message, "user")
                    
                    try:
                        response = self.assistant.process_message(message)
                        self.add_message(response, "bot")
                    except Exception as e:
                        self.add_message(f"❌ Error: {str(e)}", "bot")
            
            def send_example(self, example):
                self.input_field.delete(0, tk.END)
                self.input_field.insert(0, example)
                self.send_message()
            
            def add_message(self, text, sender):
                timestamp = datetime.now().strftime("%H:%M:%S")
                if sender == "user":
                    prefix = f"[{timestamp}] You: "
                else:
                    prefix = f"[{timestamp}] Assistant: "
                
                self.chat_display.insert(tk.END, prefix + text + "\n\n")
                self.chat_display.see(tk.END)
        
        print("Creating GUI window...")
        root = tk.Tk()
        print("GUI window created, initializing application...")
        app = WhatsAppAssistantGUI(root)
        print("Application initialized, starting main loop...")
        print("✅ GUI window should now be visible on your screen!")
        root.mainloop()
        print("GUI closed.")
        
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        import traceback
        traceback.print_exc()

def print_banner():
    print("=" * 60)
    print("🤖 WhatsApp-Driven Google Drive Assistant - Test Launcher")
    print("=" * 60)
    print()

def main():
    print_banner()
    
    # Check dependencies
    missing_deps = []
    if not FLASK_AVAILABLE:
        missing_deps.append("Flask (pip install flask)")
    if not TKINTER_AVAILABLE:
        missing_deps.append("tkinter (usually comes with Python)")
    
    if missing_deps:
        print("⚠️  Missing dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print()
        print("💡 To install Flask: pip install flask")
        print()
    
    while True:
        print("Choose your test mode:")
        print("1. 🖥️  Terminal Mode (Command line interface)")
        print("2. 🌐 Web Mode (Browser interface)" + (" - Requires Flask" if not FLASK_AVAILABLE else ""))
        print("3. 🖥️  GUI Mode (Desktop application)" + (" - Requires tkinter" if not TKINTER_AVAILABLE else ""))
        print("4. ❌ Exit")
        print()
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            run_terminal_test()
            break
        elif choice == "2":
            if not FLASK_AVAILABLE:
                print("❌ Flask is required for web mode. Please install it first:")
                print("   pip install flask")
                print()
                continue
            run_web_test()
            break
        elif choice == "3":
            if not TKINTER_AVAILABLE:
                print("❌ tkinter is required for GUI mode.")
                print("   It usually comes with Python installation.")
                print()
                continue
            run_gui_test()
            break
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
            print()

if __name__ == "__main__":
    main()
