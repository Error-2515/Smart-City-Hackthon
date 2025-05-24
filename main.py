import streamlit as st
import os
import db
# import process as pr
from sms import send_sms  # Import the function from sms.py

# Page configuration
st.set_page_config(page_title="Chaluu Plate", layout="centered", initial_sidebar_state="collapsed")

# Title
st.title("🚗 Chaluu Plate - Vehicle Details App")

# Upload the image
st.markdown("### Upload an image of the vehicle:")
uploaded_image = st.file_uploader("", type=["jpg", "jpeg", "png"])

# Folder to save uploaded images
upload_folder = "uploaded"
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

if uploaded_image is not None:
    # Save the uploaded image
    image_path = os.path.join(upload_folder, uploaded_image.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_image.getbuffer())

    # Display the uploaded image
    st.image(image_path, caption="Uploaded Vehicle Image", use_column_width=True)
    st.markdown("---")

    # Process the image (predict vehicle color, type, and number plate)
    # vehicle_color, number_plate, vehicle_type = pr.process_image(image_path)
    db_plate, phone_number, owner_name,car_color,car_type, message = db.find_vehicle_owner(image_path)

    # Vehicle details section
    st.header("Vehicle Details:")
    st.subheader(f"*Type of Vehicle:* :grey[{car_type or 'Fetching...'}]")
    st.subheader(f"*Color of Vehicle:* :grey[{car_color or 'Fetching...'}]")
    st.subheader(f"*Number Plate:* :grey[{db_plate or 'Fetching...'}]")
    st.subheader(f"*Owner's Phone Number:* :grey[{phone_number or 'Not Found'}]")
    st.subheader(f"*Owner's Name:* :grey[{owner_name or 'Not Found'}]")

    # Send SMS Button
    if phone_number:
        if st.button("📩 Send SMS to Owner"):
            try:
                sms_message='you have a bill of 500rs to pay for depricated number plate'
                message_sid = send_sms(phone_number, sms_message)
                st.success(f"Message sent successfully! (SID: {message_sid})")
            except Exception as e:
                st.error(f"Failed to send message: {e}")
    else:
        st.warning("Phone number not found. Unable to send SMS.")

else:
    st.info("Please upload an image to proceed.")
