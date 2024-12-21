import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os

# --------------------- BACKEND ---------------------
# Save posts in a text file
def save_post_to_file(username, caption, image_path):
    with open("user_posts.txt", "a") as file:
        file.write(f"Username: {username}\nCaption: {caption}\nImage Path: {image_path}\n{'-'*30}\n")

# --------------------- FRONTEND ---------------------
class SocialMediaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Media Platform")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f8ff")  # Light blue background

        self.current_user = None
        self.image_path = None

        self.show_login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Login", font=("Arial", 24), bg="#f0f8ff", fg="#4682b4").pack(pady=20)

        tk.Label(self.root, text="Username", bg="#f0f8ff", fg="#4682b4").pack(pady=5)
        self.login_username_entry = tk.Entry(self.root, width=30)
        self.login_username_entry.pack(pady=5)

        tk.Label(self.root, text="Password", bg="#f0f8ff", fg="#4682b4").pack(pady=5)
        self.login_password_entry = tk.Entry(self.root, show="*", width=30)
        self.login_password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", bg="#4682b4", fg="white", command=self.handle_login).pack(pady=10)
        tk.Button(self.root, text="Register", bg="#4682b4", fg="white", command=self.show_registration_screen).pack()

    def show_registration_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Register", font=("Arial", 24), bg="#f0f8ff", fg="#4682b4").pack(pady=20)

        tk.Label(self.root, text="Username", bg="#f0f8ff", fg="#4682b4").pack(pady=5)
        self.register_username_entry = tk.Entry(self.root, width=30)
        self.register_username_entry.pack(pady=5)

        tk.Label(self.root, text="Password", bg="#f0f8ff", fg="#4682b4").pack(pady=5)
        self.register_password_entry = tk.Entry(self.root, show="*", width=30)
        self.register_password_entry.pack(pady=5)

        tk.Button(self.root, text="Register", bg="#4682b4", fg="white", command=self.handle_registration).pack(pady=10)
        tk.Button(self.root, text="Back to Login", bg="#4682b4", fg="white", command=self.show_login_screen).pack()

    def handle_registration(self):
        username = self.register_username_entry.get().strip()
        password = self.register_password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        with open("users.txt", "a") as file:
            file.write(f"{username},{password}\n")

        messagebox.showinfo("Success", "Registration successful! Please log in.")
        self.show_login_screen()

    def handle_login(self):
        username = self.login_username_entry.get().strip()
        password = self.login_password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        with open("users.txt", "r") as file:
            users = file.readlines()

        for user in users:
            saved_username, saved_password = user.strip().split(",")
            if username == saved_username and password == saved_password:
                self.current_user = username
                self.show_main_interface()
                return

        messagebox.showerror("Error", "Invalid username or password!")

    def show_main_interface(self):
        self.clear_window()

        tk.Label(self.root, text=f"Welcome, {self.current_user}", font=("Arial", 18), bg="#f0f8ff", fg="#4682b4").pack(pady=10)

        self.caption_entry = tk.Entry(self.root, width=50)
        self.caption_entry.pack(pady=10)
        self.caption_entry.insert(0, "Write your caption here...")
        self.caption_entry.bind("<FocusIn>", self.clear_placeholder)

        tk.Button(self.root, text="Upload Image", bg="#4682b4", fg="white", command=self.upload_image).pack(pady=5)

        tk.Button(self.root, text="Post", bg="#4682b4", fg="white", command=self.handle_post).pack(pady=10)

        self.feed_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.feed_frame.pack(fill="both", expand=True, pady=10)

        tk.Button(self.root, text="Exit", bg="#ff4500", fg="white", command=self.root.quit).pack(pady=10)

    def clear_placeholder(self, event):
        if self.caption_entry.get() == "Write your caption here...":
            self.caption_entry.delete(0, tk.END)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_path = file_path
            messagebox.showinfo("Success", "Image uploaded successfully!")

    def handle_post(self):
        caption = self.caption_entry.get().strip()

        if not caption and not self.image_path:
            messagebox.showerror("Error", "Caption or image is required to post!")
            return

        self.display_post(self.current_user, caption, self.image_path)
        save_post_to_file(self.current_user, caption, self.image_path)
        self.caption_entry.delete(0, tk.END)
        self.caption_entry.insert(0, "Write your caption here...")
        self.image_path = None

    def display_post(self, username, caption, image_path):
        post_frame = tk.Frame(self.feed_frame, bg="#ffffff", bd=2, relief="groove")
        post_frame.pack(fill="x", pady=5, padx=10)

        tk.Label(post_frame, text=username, font=("Arial", 12, "bold"), bg="#ffffff", fg="#4682b4").pack(anchor="w", padx=5, pady=2)

        if caption:
            tk.Label(post_frame, text=caption, font=("Arial", 10), bg="#ffffff", wraplength=400, justify="left").pack(anchor="w", padx=5)

        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img.thumbnail((400, 300))
                img = ImageTk.PhotoImage(img)

                tk.Label(post_frame, image=img, bg="#ffffff").pack(anchor="w", padx=5, pady=5)
                post_frame.image = img  # Keep a reference to prevent garbage collection
            except Exception as e:
                tk.Label(post_frame, text="[Error loading image]", bg="#ffffff", fg="red").pack(anchor="w", padx=5)

# --------------------- RUN APPLICATION ---------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SocialMediaApp(root)
    root.mainloop()
