# Image Processing Website

Welcome to the Image Processing Website! This project is a Flask-based web application that allows users to create accounts, upload images, and apply various styles to them. Users can also view and manage their processed images on the 'My Works' page.

## Features

- **User Authentication**: Create an account and log in to access the image processing features.
- **Image Upload**: Upload images to be processed.
- **Image Processing**: Convert uploaded images to different styles:
  - Black and White
  - Blur
  - Rotated
  - Sketch
- **My Works**: View, download, and delete your processed images.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/IvanAkperov/image-editor.git
   cd image-editor
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Set up your database**:
    Insert your database data in config.py
    ```
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:example@localhost/yourname'
   ```

4. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up the environment variables**:
   Create a `.env` file in the root directory and add the following:
   ```
   SECRET_KEY=your_secret_key
   DATABASE_URL=your_database_url
   ```

6. **Run the application**:
   ```bash
   flask run
   ```

   The application will be available at `http://127.0.0.1:5000/`.

## Usage

1. **Register/Login**:
   - Navigate to the registration page to create a new account.
   - Log in with your credentials to access the dashboard.

2. **Upload Images**:
   - From the dashboard, upload images you wish to process.

3. **Process Images**:
   - Select the desired style (Black and White, Blur, Rotated, Sketch) for each uploaded image.

4. **View My Works**:
   - Navigate to the 'My Works' page to view all your processed images.
   - Download or delete images as needed.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss any changes.

## Contact

For any questions or inquiries, please contact ya@iakperov.ru.

---

Thank you for checking out the Image Processing Website! We hope you enjoy using it.