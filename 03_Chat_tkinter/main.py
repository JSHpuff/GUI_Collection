import tkinter as tk
import requests

# Create the main window
root = tk.Tk()
root.title("Tavern AI Chat")

# Text display area
text_display = tk.Text(root, height=20, width=50)
text_display.pack()

# Input field
entry = tk.Entry(root, width=40)
entry.pack()

# Function to send input to AI and receive response
def send_message():
    user_input = entry.get()
    entry.delete(0, tk.END)

    # Example API request (Modify with actual Tavern AI API endpoint)
    api_url = "http://localhost:5000/api/chat"  # Change this to the correct API URL
    payload = {"message": user_input}
    response = requests.post(api_url, json=payload)

    # Display the response in the GUI
    ai_response = response.json().get("reply", "No response")
    text_display.insert(tk.END, f"You: {user_input}\nAI: {ai_response}\n\n")

# Send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

# Run the GUI loop
root.mainloop()