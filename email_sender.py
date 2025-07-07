import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import zipfile

# Page setup
st.set_page_config(page_title="Certificate Generator", layout="centered")
st.title("🎓 Certificate Generator")

# Upload certificate template
uploaded_file = st.file_uploader("📤 Upload your certificate template (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    try:
        cert_template = Image.open(uploaded_file).convert("RGBA")
        st.image(cert_template, caption="🖼️ Certificate Template Preview", use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error reading uploaded image: {e}")
        st.stop()
else:
    st.warning("⚠️ Please upload a certificate template to continue.")
    st.stop()

# Name input
names_input = st.text_area("✍️ Enter names (comma-separated)", placeholder="e.g. Jay Shaj, Surani Sujal")

# Y-position input
y_position = st.number_input("📍 Enter Y-position for name placement", min_value=0, value=630)

# Font size input
font_size = st.number_input("🔤 Font Size", min_value=10, max_value=150, value=90)

# Font color
font_color = st.color_picker("🎨 Choose font color", "#FFA500")  # Default: orange

# Generate button
if names_input:
    names = [name.strip() for name in names_input.split(",") if name.strip()]

    if st.button("🚀 Generate Certificates"):
        try:
            font_file = "OpenSans-Regular.ttf"  # Must be in the same folder as this .py file

            output_images = []

            for name in names:
                cert_img = cert_template.copy()
                draw = ImageDraw.Draw(cert_img)

                try:
                    font = ImageFont.truetype(font_file, font_size)
                except Exception as e:
                    st.warning(f"⚠️ Font file not found or invalid. Using default font. Error: {e}")
                    font = ImageFont.load_default()

                # Center the name horizontally
                text = name
                bbox = font.getbbox(text)
                text_width = bbox[2] - bbox[0]
                image_width = cert_img.width
                x_position = (image_width - text_width) // 2

                # Draw name on certificate
                draw.text((x_position, y_position), text, font=font, fill=font_color)

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
            st.error(f"❌ Error generating certificates: {e}")
