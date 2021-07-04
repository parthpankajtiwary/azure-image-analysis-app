# azure-image-analysis-app
A scalable system design architecture around Azure image analysis API

# Run the streamlit app

```
streamlit run app/app.py
```

# Streamlit app screenshots

## First page (upload)

First page of the app is shown in the screenshot below. First page comes with an option to upload an image.  

![Alt text](screenshots/intro.png?raw=true "Title")

## Results page

Once the user uploads an image, the image is processed to extract OCR text. The final result contains the original image with OCR text and bounding boxes rendered on the image as shown below. 

![Alt text](screenshots/upload_result.png?raw=true "Title")
