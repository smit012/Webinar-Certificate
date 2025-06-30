import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
import io
import zipfile

# Page setup
st.set_page_config(page_title="Certificate Generator", layout="centered")
st.title("🎓 Certificate Generator")

# Google Drive direct link (hardcoded)
GOOGLE_DRIVE_DIRECT_LINK = "https://drive.google.com/uc?export=download&id=1Jrth3dtK4XsuLOmD7W7X75IHVN5XqMHd"

# Load and preview certificate template
try:
    response = requests.get(GOOGLE_DRIVE_DIRECT_LINK)
    if response.status_code == 200:
        preview_image_bytes = io.BytesIO(response.content)
        st.image(preview_image_bytes, caption="🖼️ Certificate Template Preview", use_container_width=True)
    else:
        st.warning("⚠️ Could not load certificate preview from Google Drive.")
        st.stop()
except Exception as e:
    st.error(f"❌ Error loading template preview: {e}")
    st.stop()

# Name input
names_input = st.text_area("Enter names (comma-separated)", placeholder="e.g. Jay Shaj, Surani Sujal")

# Y-position input
y_position = st.number_input("Enter Y-position for name placement", min_value=0, value=640)

# Generate button
if names_input:
    names = [name.strip() for name in names_input.split(",") if name.strip()]

    if st.button("🚀 Generate Certificates"):
        try:
            font_path = "C:/Windows/Fonts/arial.ttf"  # Use non-bold font
            font_size = 90

            # Load certificate template for editing
            cert_template = Image.open(preview_image_bytes).convert("RGBA")
            output_images = []

            for name in names:
                cert_img = cert_template.copy()
                draw = ImageDraw.Draw(cert_img)
                try:
                     font = ImageFont.truetype("OpenSans-Regular.ttf", font_size)
                except:
                     font = ImageFont.load_default()

                # Center the name horizontally
                text = f'"{name}"'
                bbox = font.getbbox(text)
                text_width = bbox[2] - bbox[0]
                image_width = cert_img.width
                x_position = (image_width - text_width) // 2

                # Draw name on certificate
                draw.text((x_position, y_position), text, font=font, fill="orange")

                # Save to buffer
                img_bytes = io.BytesIO()
                cert_img.save(img_bytes, format="PNG")
                output_images.append((f"{name.replace(' ', '_')}_certificate.png", img_bytes.getvalue()))

            st.success("✅ Certificates generated!")

            # Individual download buttons
        

            for i, (filename, data) in enumerate(output_images):
                 st.download_button(
                     label=f"📥 Download {filename}",
                     data=data,
                     file_name=filename,
                     mime="image/png",
                     key=f"{filename}_{i}"
                )

            # ZIP download
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for filename, data in output_images:
                    zip_file.writestr(filename, data)
            zip_buffer.seek(0)

            st.download_button(
                "📦 Download All as ZIP",
                data=zip_buffer,
                file_name="certificates.zip",
                mime="application/zip"
            )

        except Exception as e:
            st.error(f"❌ Error: {e}")
