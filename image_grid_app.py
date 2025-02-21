import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ExifTags
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import math
from datetime import datetime
import threading
import customtkinter as ctk

class ModernProgressBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.percentage = 0
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(padx=10, pady=(10, 5), fill="x", expand=True)
        self.progress_bar.set(0)
        
        # Progress labels frame
        self.labels_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.labels_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Percentage label
        self.percentage_label = ctk.CTkLabel(self.labels_frame, text="0%")
        self.percentage_label.pack(side="left")
        
        # Image counter label
        self.counter_label = ctk.CTkLabel(self.labels_frame, text="(0/0)")
        self.counter_label.pack(side="right")
        
    def update_progress(self, percentage, current_image, total_images):
        self.percentage = percentage
        self.progress_bar.set(percentage / 100)
        self.percentage_label.configure(text=f"{percentage:.1f}%")
        self.counter_label.configure(text=f"({current_image}/{total_images})")
        self.update()
        
    def show(self):
        self.pack(fill="x", padx=10, pady=10)
        
    def hide(self):
        self.pack_forget()

class ImageGridApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Modern Image Grid Generator")
        self.geometry("1000x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables
        self.images = []
        self.output_path = ""
        self.processing = False
        self.columns = ctk.IntVar(value=2)
        self.rows = ctk.IntVar(value=2)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create main container
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left sidebar - Controls
        sidebar = ctk.CTkFrame(self.main_container)
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        
        # App title
        title = ctk.CTkLabel(
            sidebar, 
            text="Image Grid Generator",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20, padx=10)
        
        # Grid controls
        grid_frame = ctk.CTkFrame(sidebar)
        grid_frame.pack(fill="x", padx=10, pady=10)
        
        # Columns control frame with label
        columns_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
        columns_frame.pack(fill="x", padx=10, pady=(10, 0))
        self.columns_label = ctk.CTkLabel(columns_frame, text=f"Columns: {self.columns.get()}")
        self.columns_label.pack(side="left")
        
        columns_slider = ctk.CTkSlider(
            grid_frame,
            from_=1,
            to=5,
            number_of_steps=4,
            variable=self.columns,
            command=self.on_columns_change
        )
        columns_slider.pack(padx=10, pady=(0, 10), fill="x")
        
        # Rows control frame with label
        rows_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
        rows_frame.pack(fill="x", padx=10, pady=(10, 0))
        self.rows_label = ctk.CTkLabel(rows_frame, text=f"Rows: {self.rows.get()}")
        self.rows_label.pack(side="left")
        
        rows_slider = ctk.CTkSlider(
            grid_frame,
            from_=1,
            to=5,
            number_of_steps=4,
            variable=self.rows,
            command=self.on_rows_change
        )
        rows_slider.pack(padx=10, pady=(0, 10), fill="x")
        
        # Buttons
        ctk.CTkButton(
            sidebar,
            text="Select Images",
            command=self.select_images
        ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            sidebar,
            text="Select Output Path",
            command=self.select_output_path
        ).pack(fill="x", padx=10, pady=5)
        
        self.generate_btn = ctk.CTkButton(
            sidebar,
            text="Generate PDF",
            command=self.generate_pdf
        )
        self.generate_btn.pack(fill="x", padx=10, pady=5)
        
        # Progress bar
        self.progress_frame = ModernProgressBar(sidebar)
        self.progress_frame.hide()  # Hide initially
        
        # Status text
        self.status_label = ctk.CTkLabel(sidebar, text="Ready")
        self.status_label.pack(pady=10)
        
        # Right panel - Preview area
        preview_frame = ctk.CTkFrame(self.main_container)
        preview_frame.pack(side="left", fill="both", expand=True)
        
        # Preview scroll area
        self.preview_scroll = ctk.CTkScrollableFrame(
            preview_frame,
            label_text="Image Preview"
        )
        self.preview_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
    def on_columns_change(self, value):
        """Handle column slider change"""
        self.columns_label.configure(text=f"Columns: {int(value)}")
        self.update_preview()
        
    def on_rows_change(self, value):
        """Handle row slider change"""
        self.rows_label.configure(text=f"Rows: {int(value)}")
        self.update_preview()
        
    def select_images(self):
        """Handle image selection"""
        file_types = [
            ('Image files', ('*.jpg', '*.jpeg', '*.png', '*.bmp')),
            ('All files', '*.*')
        ]
        
        filenames = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=file_types
        )
        
        if filenames:
            # Sort by modification date
            sorted_files = sorted(
                filenames,
                key=lambda x: os.path.getmtime(x)
            )
            
            # Store image data
            self.images = []
            for path in sorted_files:
                try:
                    with Image.open(path) as img:
                        # Get original rotation
                        rotation = self.get_image_rotation(img)
                        self.images.append({
                            'path': path,
                            'rotation': rotation,
                            'name': os.path.basename(path)
                        })
                except Exception as e:
                    messagebox.showerror(
                        "Error",
                        f"Failed to process {path}: {str(e)}"
                    )
            
            self.update_preview()
            self.status_label.configure(
                text=f"Selected {len(self.images)} images"
            )
            
    def get_image_rotation(self, img):
        """Get image rotation from EXIF data"""
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = dict(img._getexif().items())
            
            if exif[orientation] == 3:
                return 180
            elif exif[orientation] == 6:
                return 270
            elif exif[orientation] == 8:
                return 90
        except (AttributeError, KeyError, IndexError):
            pass
        return 0
        
    def select_output_path(self):
        """Handle output path selection"""
        filename = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if filename:
            self.output_path = filename
            self.status_label.configure(
                text=f"Output: {os.path.basename(self.output_path)}"
            )
            
    def update_preview(self, _=None):
        """Update the preview grid"""
        # Clear previous preview
        for widget in self.preview_scroll.winfo_children():
            widget.destroy()
            
        if not self.images:
            return
            
        # Get grid dimensions
        num_columns = self.columns.get()
        num_rows = self.rows.get()
        preview_size = 150  # thumbnail size
        
        # Calculate how many rows we need
        total_rows = (len(self.images) + num_columns - 1) // num_columns
        
        # Create all row containers first
        row_containers = []
        for _ in range(total_rows):
            row_container = ctk.CTkFrame(self.preview_scroll, fg_color="transparent")
            row_container.pack(fill="x", expand=True, pady=5)
            row_containers.append(row_container)
        
        # Create grid frames
        for i, img_data in enumerate(self.images):
            try:
                row_num = i // num_columns
                
                # Create frame for image and label with fixed width
                frame = ctk.CTkFrame(row_containers[row_num])
                frame.pack(side="left", padx=10, expand=True)
                
                # Set a minimum width for the frame
                frame.configure(width=200)  # Minimum width
                
                # Load and resize image
                with Image.open(img_data['path']) as img:
                    # Create thumbnail
                    img.thumbnail((preview_size, preview_size))
                    # Apply rotation if needed
                    if img_data['rotation']:
                        img = img.rotate(
                            img_data['rotation'],
                            expand=True
                        )
                    
                    photo = ImageTk.PhotoImage(img)
                    
                    # Create container for the image
                    img_container = ctk.CTkFrame(frame, fg_color="transparent")
                    img_container.pack(padx=5, pady=5, fill="both", expand=True)
                    
                    # Create and pack image label with fixed dimensions
                    img_label = ctk.CTkLabel(
                        img_container, 
                        image=photo, 
                        text="",
                    )
                    img_label.pack(padx=5, pady=5)
                    
                    # Force minimum width on the image container
                    img_container.configure(width=180, height=180)
                    
                    # Add filename label with proper wrapping
                    name_label = ctk.CTkLabel(
                        frame,
                        text=img_data['name'],
                        wraplength=180  # Match container width
                    )
                    name_label.pack(padx=5, pady=(0, 5))
                    
                    # Add remove button
                    remove_btn = ctk.CTkButton(
                        frame,
                        text="Remove",
                        command=lambda idx=i: self.remove_image(idx),
                        width=80,
                        height=25
                    )
                    remove_btn.pack(pady=(0, 5))
                    
                    # Store references to avoid garbage collection
                    if not hasattr(self, '_photo_references'):
                        self._photo_references = []
                    self._photo_references.append(photo)
                    
            except Exception as e:
                print(f"Error creating preview for {img_data['path']}: {e}")
                
    def remove_image(self, index):
        """Remove an image from the list"""
        if 0 <= index < len(self.images):
            del self.images[index]
            # Clear photo references
            if hasattr(self, '_photo_references'):
                self._photo_references = []
            self.update_preview()
            self.status_label.configure(
                text=f"Selected {len(self.images)} images"
            )
            
    def generate_pdf(self):
        """Generate PDF with image grid"""
        if not self.images:
            messagebox.showerror("Error", "Please select images first")
            return
            
        if not self.output_path:
            messagebox.showerror("Error", "Please select output path first")
            return
            
        # Show progress bar and disable generate button
        self.progress_frame.show()
        self.generate_btn.configure(state="disabled")
        
        # Run PDF generation in separate thread
        thread = threading.Thread(target=self._generate_pdf_thread)
        thread.start()
        
    def _generate_pdf_thread(self):
        """PDF generation worker thread"""
        try:
            # Create PDF
            c = canvas.Canvas(self.output_path, pagesize=A4)
            width, height = A4
            
            # Calculate grid layout
            num_columns = self.columns.get()
            num_rows = self.rows.get()
            margin = 50  # points
            usable_width = width - 2 * margin
            usable_height = height - 2 * margin
            
            # Calculate image size
            image_width = usable_width / num_columns
            image_height = usable_height / num_rows
            
            # Images per page
            images_per_page = num_columns * num_rows
            total_pages = math.ceil(len(self.images) / images_per_page)
            
            for i, img_data in enumerate(self.images):
                # Update progress
                progress = (i / len(self.images)) * 100
                self.after(10, self.progress_frame.update_progress, progress, i + 1, len(self.images))
                
                # New page if needed
                if i % images_per_page == 0 and i > 0:
                    c.showPage()
                
                # Calculate position in grid
                page_index = i % images_per_page
                row = page_index // num_columns
                col = page_index % num_columns
                
                x = margin + col * image_width
                y = height - margin - (row + 1) * image_height
                
                # Open and process image
                with Image.open(img_data['path']) as img:
                    # Get dimensions
                    img_width, img_height = img.size
                    rotation = img_data['rotation']
                    
                    # Swap dimensions if rotated
                    if rotation in [90, 270]:
                        img_width, img_height = img_height, img_width
                    
                    # Calculate scaling
                    aspect = img_width / float(img_height)
                    
                    if aspect > image_width / image_height:
                        scaled_width = image_width
                        scaled_height = scaled_width / aspect
                    else:
                        scaled_height = image_height
                        scaled_width = scaled_height * aspect
                    
                    # Center image
                    x_centered = x + (image_width - scaled_width) / 2
                    y_centered = y + (image_height - scaled_height) / 2
                    
                    # Draw with rotation
                    c.saveState()
                    c.translate(
                        x_centered + scaled_width/2,
                        y_centered + scaled_height/2
                    )
                    c.rotate(rotation)
                    c.drawImage(
                        img_data['path'],
                        -scaled_width/2,
                        -scaled_height/2,
                        width=scaled_width,
                        height=scaled_height,
                        preserveAspectRatio=True
                    )
                    c.restoreState()
            
            c.save()
            
            # Update progress to 100%
            self.after(10, self.progress_frame.update_progress, 100, len(self.images), len(self.images))
            
            # Show success message
            messagebox.showinfo(
                "Success",
                f"PDF generated successfully!\n{total_pages} page(s) created."
            )
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to generate PDF: {str(e)}"
            )
            
        finally:
            # Reset UI
            self.after(10, self.progress_frame.hide)
            self.after(10, lambda: self.generate_btn.configure(state="normal"))
            self.after(10, lambda: self.status_label.configure(text="Ready"))

def main():
    app = ImageGridApp()
    app.mainloop()

if __name__ == "__main__":
    main()