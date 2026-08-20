from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.utils import platform

import json
import urllib.request
import urllib.error

SUPABASE_URL = "https://cgzenucjljpwslwuttjz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNnemVudWNqbGpwd3Nsd3V0dGp6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODcxNjQ0NjEsImV4cCI6MjEwMjc0MDQ2MX0.cck74uVjeRnZE_u5upT2K4-5T4yHyfIAtfL0fYCOVyM"

class OSCANApp(App):
    def build(self):
        self.scanned_barcode = "123456789"

        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        self.image = Image(size_hint=(1, 0.4))
        layout.add_widget(self.image)

        self.label = Label(
            text="OSCAN - Ready to Scan",
            font_size='18sp',
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.label)

        self.input_name = TextInput(
            hint_text="Enter Product Name...",
            multiline=False,
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.input_name)

        btn_capture = Button(
            text="Take Photo / Scan",
            font_size='18sp',
            size_hint=(1, 0.15),
            on_press=self.open_camera
        )
        layout.add_widget(btn_capture)

        btn_save = Button(
            text="Save to Supabase",
            font_size='18sp',
            size_hint=(1, 0.15),
            on_press=self.save_to_supabase
        )
        layout.add_widget(btn_save)

        return layout

    def open_camera(self, instance):
        if platform == 'android':
            try:
                from plyer import camera
                camera.take_picture(filename='product.jpg', on_complete=self.process_image)
            except Exception:
                self.label.text = "Camera Error"
        else:
            self.scanned_barcode = "9780201379624"
            self.label.text = f"Demo Barcode: {self.scanned_barcode}"

    def process_image(self, filepath):
        self.image.source = filepath
        self.image.reload()
        self.label.text = "Photo Taken Successfully"

    def save_to_supabase(self, instance):
        product_name = self.input_name.text.strip()
        
        if not product_name:
            self.label.text = "Please enter product name!"
            return

        try:
            url = f"{SUPABASE_URL}/rest/v1/products"
            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal"
            }
            payload = json.dumps({
                "barcode": self.scanned_barcode,
                "name": product_name
            }).encode('utf-8')

            req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
            with urllib.request.urlopen(req) as response:
                if response.status in [200, 201]:
                    self.label.text = "Saved Successfully to Supabase!"
                    self.input_name.text = ""
                else:
                    self.label.text = "Database Save Failed"
        except urllib.error.HTTPError as e:
            self.label.text = f"Server Error: {e.code}"
        except Exception:
            self.label.text = "Connection Error"

if __name__ == '__main__':
    OSCANApp().run()
