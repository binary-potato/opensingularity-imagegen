import streamlit as st
import requests
import io
from PIL import Image
import base64

def main():
    st.title("🎨 AI Image Generator")
    st.write("Generate images using Stable Diffusion")

    # API Configuration
    API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    api_key = "sk-T9DKUt2oRsTtnmu67M1uetzYQsnWvxSkycOhJZXWeV0wnuh8"

    # UI Elements
    prompt = st.text_area("Enter your prompt:", "A magical forest with glowing mushrooms, digital art")
    
    # Style selection
    style = st.selectbox(
        "Choose an art style:",
        ["Digital Art", "Photographic", "Anime", "Cinematic", "Fantasy", "Abstract"]
    )
    
    # Advanced options in sidebar
    st.sidebar.header("Advanced Options")
    num_images = st.sidebar.slider("Number of images", 1, 4, 1)
    
    # Generation settings
    cfg_scale = st.sidebar.slider("CFG Scale (Creativity)", 1, 20, 7)
    steps = st.sidebar.slider("Steps", 10, 50, 30)

    if st.button("Generate Image"):
        if not prompt:
            st.error("Please enter a prompt!")
            return

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        body = {
            "text_prompts": [
                {
                    "text": f"{prompt}, {style.lower()} style",
                    "weight": 1
                }
            ],
            "cfg_scale": cfg_scale,
            "steps": steps,
            "samples": num_images,
        }

        with st.spinner("Generating your image(s)..."):
            try:
                response = requests.post(API_URL, headers=headers, json=body)
                
                if response.status_code != 200:
                    st.error(f"Error: {response.text}")
                    return

                # Create columns for multiple images
                cols = st.columns(num_images)
                
                # Display each generated image
                for index, image in enumerate(response.json()["artifacts"]):
                    image_data = base64.b64decode(image["base64"])
                    img = Image.open(io.BytesIO(image_data))
                    
                    with cols[index]:
                        st.image(img, use_column_width=True)
                        
                        # Add download button for each image
                        buf = io.BytesIO()
                        img.save(buf, format="PNG")
                        st.download_button(
                            label="Download Image",
                            data=buf.getvalue(),
                            file_name=f"generated_image_{index+1}.png",
                            mime="image/png"
                        )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    st.set_page_config(page_title="AI Image Generator", page_icon="🎨")
    main()
