import streamlit as st
import base64
from PIL import Image
import os
from io import BytesIO
import streamlit.components.v1 as components
import time

def show_slideshow():
    image_folder = "images"
    image_files = sorted([
        img for img in os.listdir(image_folder)
        if img.lower().endswith((".jpg", ".jpeg", ".png"))
    ])

    slides_html = ""
    dots_html = ""

    for i, img_name in enumerate(image_files):
        img_path = os.path.join(image_folder, img_name)

        # Get MIME type
        ext = os.path.splitext(img_name)[-1].lower()
        img_format = "PNG" if ext == ".png" else "JPEG"
        mime_type = "image/png" if ext == ".png" else "image/jpeg"

        # Load and convert if needed
        img = Image.open(img_path)
        if img.mode in ("RGBA", "P"):  # Handle transparency
            img = img.convert("RGB")

        # Encode as base64
        buffered = BytesIO()
        img.save(buffered, format=img_format)
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Add HTML for slide
        slides_html += f"""
        <div class="mySlides fade">
          <div class="numbertext">{i+1} / {len(image_files)}</div>
          <img src="data:{mime_type};base64,{img_base64}" style="width:100%">
          <div class="text">💜</div>
        </div>
        """
        dots_html += '<span class="dot"></span>'

    # Wrap full HTML
    full_html = f"""
    <style>
    * {{box-sizing: border-box;}}
    .mySlides {{display: none;}}
    img {{vertical-align: middle; border-radius: 12px;}}
    .slideshow-container {{
      max-width: 1000px;
      position: relative;
      margin: auto;
    }}
    .text {{
      color: #f2f2f2;
      font-size: 20px;
      padding: 8px 12px;
      position: absolute;
      bottom: 8px;
      width: 100%;
      text-align: center;
    }}
    .numbertext {{
      color: #f2f2f2;
      font-size: 12px;
      padding: 8px 12px;
      position: absolute;
      top: 0;
    }}
    .dot {{
      height: 15px;
      width: 15px;
      margin: 0 2px;
      background-color: #bbb;
      border-radius: 50%;
      display: inline-block;
      transition: background-color 0.6s ease;
    }}
    .active {{
      background-color: #717171;
    }}
    .fade {{
      animation-name: fade;
      animation-duration: 1.5s;
    }}
    @keyframes fade {{
      from {{opacity: .4}} 
      to {{opacity: 1}}
    }}
    </style>

    <div class="slideshow-container">
    {slides_html}
    </div>
    <br>
    <div style="text-align:center">{dots_html}</div>

    <script>
    let slideIndex = 0;
    showSlides();

    function showSlides() {{
      let i;
      let slides = document.getElementsByClassName("mySlides");
      let dots = document.getElementsByClassName("dot");
      for (i = 0; i < slides.length; i++) {{
        slides[i].style.display = "none";  
      }}
      slideIndex++;
      if (slideIndex > slides.length) {{slideIndex = 1}}    
      for (i = 0; i < dots.length; i++) {{
        dots[i].className = dots[i].className.replace(" active", "");
      }}
      slides[slideIndex-1].style.display = "block";  
      dots[slideIndex-1].className += " active";
      setTimeout(showSlides, 3000);
    }}
    </script>
    """

    st.components.v1.html(full_html, height=600)

def show_letter():
    # 1) Read the letter with actual newlines
    with open("letter.txt", "r", encoding="utf-8") as f:
        raw = f.read()
        
    # 2) Escape for JS
    letter_js = (
        raw
        .replace("\\", "\\\\")
        .replace("\"", "\\\"")
        .replace("\n", "\\n")
    )
    
    # 3) HTML + JS with Google Font + typewriter effect
    html = f"""
    <!-- import Dancing Script -->
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script&display=swap" rel="stylesheet">
    <style>
      /* apply cursive font */
      #letter {{
        font-family: 'Dancing Script', cursive;
        font-size: 22px;
        line-height: 1.6;
      }}
      .letter-container {{
        background-color: #6f0700;
        color: white;
        padding: 20px;
        border-radius: 12px;
        max-width: 800px;
        margin: auto;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      }}
    </style>
    <div class="letter-container">
      <div id="letter" style="min-height: 300px;"></div>
    </div>
    <script>
    document.addEventListener('DOMContentLoaded', () => {{
      const rawText = "{letter_js}";
      const paragraphs = rawText.split("\\n");
      
      let currentParagraph = 0;
      let charIndex = 0;
      const letterElement = document.getElementById("letter");
      
      // Create a paragraph element for the current paragraph
      let currentP = document.createElement("p");
      letterElement.appendChild(currentP);
      
      function typeWriter() {{
        // If we've finished the current paragraph
        if (charIndex >= paragraphs[currentParagraph].length) {{
          currentParagraph++;
          charIndex = 0;
          
          // If we've typed all paragraphs, we're done
          if (currentParagraph >= paragraphs.length) {{
            return;
          }}
          
          // Create a new paragraph element
          currentP = document.createElement("p");
          letterElement.appendChild(currentP);
        }}
        
        // Add the next character
        currentP.textContent += paragraphs[currentParagraph].charAt(charIndex);
        charIndex++;
        
        // Schedule the next character
        setTimeout(typeWriter, 45);
      }}
      
      // Start the typewriter effect
      typeWriter();
    }});
    </script>
    """
    
    st.components.v1.html(html, height=1800, scrolling=True)

def show_reward():
    st.markdown("## 🎉 You've unlocked your surprise! Happy Birthday babyyyyy! 🎉", unsafe_allow_html=True)
    st.balloons()

    # --- Display Letter ---
    st.markdown("### 💌 A Birthday Letter for You")
    show_letter()

    # --- Play Audio ---
    st.markdown("### 🎧 A Message From Your Victor")
    audio_file = open("tuyo.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3", loop=True,autoplay=True)

    # --- Slideshow ---
    # inside show_reward
    st.markdown("### 📸 A Few Fun Memories")
    show_slideshow()

def play_audio(note):
    """Play a note audio file and return appropriate HTML."""
    sound_path = os.path.join("piano-mp3", f"{note}.mp3")
    
    # Check if the file exists
    if not os.path.exists(sound_path):
        st.warning(f"Audio file for note {note} not found at {sound_path}")
        return
    
    # Read the audio file and encode it to base64
    with open(sound_path, "rb") as f:
        audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
    
    # Create HTML for audio with autoplay
    audio_html = f"""
    <audio autoplay="true" onended="this.remove();">
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>
    """
    
    # Display the audio element
    st.components.v1.html(audio_html, height=0)
    
    # Also provide visual feedback that the note was played
    st.session_state.last_played_note = note

# Piano puzzle implementation
def piano_puzzle():
    # Notes to use including black keys
    NOTES_OCTAVE1 = ["C1", "Db1", "D1", "Eb1", "E1", "F1", "Gb1", "G1", "Ab1", "A1", "Bb1", "B1"]
    NOTES_OCTAVE2 = ["C2", "Db2", "D2", "Eb2", "E2", "F2", "Gb2", "G2", "Ab2", "A2", "Bb2", "B2"]
    NOTES_OCTAVE3 = ["C3", "Db3", "D3", "Eb3", "E3", "F3", "Gb3", "G3", "Ab3", "A3", "Bb3", "B3"]
    NOTES_OCTAVE4 = ["C4", "Db4", "D4", "Eb4", "E4", "F4", "Gb4", "G4", "Ab4", "A4", "Bb4", "B4"]
    NOTES_OCTAVE5 = ["C5", "Db5", "D5", "Eb5", "E5", "F5", "Gb5", "G5", "Ab5", "A5", "Bb5", "B5"]

    # All available notes
    NOTES = NOTES_OCTAVE1 + NOTES_OCTAVE2 + NOTES_OCTAVE3 + NOTES_OCTAVE4 + NOTES_OCTAVE5

    # Target melody to unlock (customize this to your tune)
    TARGET_MELODY = ["G5", "F5", "Eb5", "D5", "Eb5", "D5", "C5", "Bb4"]  # Damaged Coda

    # Initialize session state variables
    if "played_notes" not in st.session_state:
        st.session_state.played_notes = []
    
    if "last_played_note" not in st.session_state:
        st.session_state.last_played_note = None
        
    if "reward_unlocked" not in st.session_state:
        st.session_state.reward_unlocked = False

    # Custom CSS for styling buttons
    st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
        background-color: white;
        color: black;
        border: 1px solid #333;
    }
    div[data-testid="stHorizontalBlock"] button[kind="primary"] {
        background-color: black;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    # Main heading
    st.markdown("### 🎹 Play the Melody to Unlock Your Surprise")
    st.write("Try playing the most well known 8-note progression from Blonde Redhead...")

    # Layout: play area and reset
    col1, col2 = st.columns([3, 1])
    
    with col1:
        for octave_num, notes in enumerate([NOTES_OCTAVE1, NOTES_OCTAVE2, NOTES_OCTAVE3, NOTES_OCTAVE4, NOTES_OCTAVE5], start=1):
            st.write(f"Octave {octave_num}:")
            cols = st.columns(len(notes))
            for i, note in enumerate(notes):
                is_white_key = "b" not in note.lower()
                with cols[i]:
                    if st.button(note, key=f"key_{note}", 
                                 use_container_width=True,
                                 type="secondary" if is_white_key else "primary"):
                        st.session_state.played_notes.append(note)
                        st.session_state.last_played_note = note
                        play_audio(note)

    with col2:
        # Reset button
        if st.button("Reset Melody", key="reset_button"):
            st.session_state.played_notes = []
            st.rerun()

    # Display what's been played
    if st.session_state.played_notes:
        notes_display = " → ".join(st.session_state.played_notes)
        st.markdown(f"**Played Notes:** {notes_display}")
        
        # Visual feedback for last played note
        if st.session_state.last_played_note:
            st.markdown(f"**Last Played:** {st.session_state.last_played_note}")

    # Check if the last 4 notes match the target melody
    if len(st.session_state.played_notes) >= len(TARGET_MELODY):
        last_n_notes = st.session_state.played_notes[-len(TARGET_MELODY):]
        
        if last_n_notes == TARGET_MELODY:
            st.session_state.reward_unlocked = True
            st.success("🎉 You played it perfectly! Unlocking your surprise...")
            st.rerun()  # Rerun to show the reward

    # Display hint if they've made several attempts
    if len(st.session_state.played_notes) > 8 and not st.session_state.reward_unlocked:
        st.info("💡 Hint: Try playing notes from the Damaged Coda. Try starting from the fifth octave :)")

# Main app logic
def main():
    st.set_page_config(layout="wide")
    st.title("🎂 Birthday Surprise")
    
    # Delay before showing reward
    if "reward_unlocked" in st.session_state and st.session_state.reward_unlocked:
        if "delay_complete" not in st.session_state:
            time.sleep(4)  # 2-second delay
            st.session_state.delay_complete = True
            st.rerun()
        else:
            show_reward()
    else:
        piano_puzzle()

if __name__ == "__main__":
    main()
