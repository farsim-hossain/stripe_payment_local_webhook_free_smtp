# User Counter App with Stripe Integration

This is a simple web application that allows users to authenticate with a password generated after making a Stripe payment. The password is sent via email, and the user can increment a counter after logging in.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- `pip` (Python package manager)
- Stripe account (for test payments)
- `ngrok` (for exposing the local server to the internet)
- SQLite (for the database)

### Install Dependencies

1. Clone or download the repository.
2. Install the necessary Python packages:

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` should include:

   - `fastapi`
   - `uvicorn`
   - `stripe`
   - `python-dotenv`
   - `smtplib`
   - `sqlite3`
   - `streamlit`

## Setup Environment

1. **Create a `.env` file** in the root directory of the project and add the following variables:

   ```env
   STRIPE_KEY=your_stripe_secret_key (Stripe secret key)
   STRIPE_WEBHOOK_SECRET=your_webhook_secret (Signing secret in the destination)
   GMAIL_EMAIL=your_gmail_address
   GMAIL_PASSWORD=your_gmail_password
   ```

   - Replace `your_stripe_secret_key` with your Stripe secret key.
   - Replace `your_webhook_secret` with your Stripe webhook secret.
   - Replace `your_gmail_address` and `your_gmail_password` with the email and password of your Gmail account used to send the password email.

## Running the Application

### Step 1: Start the `ngrok` server

1. **Install `ngrok`** from [here](https://ngrok.com/download).
2. **Run `ngrok`** to expose your local server to the internet:

   ```bash
   ngrok http 8000
   ```

3. After running this, `ngrok` will provide you with a public URL (e.g., `http://<random_subdomain>.ngrok.io`).

4. Copy the **ngrok public URL**.

### Step 2: Update the Webhook URL in Stripe

1. Log in to your Stripe Dashboard.
2. Go to **Developers** > **Webhooks**.
3. Click on **Add endpoint**.
4. Paste the `ngrok` URL (e.g., `http://<random_subdomain>.ngrok.io/webhook`) into the **Endpoint URL** field.
5. Select the **Event type** as `checkout.session.completed`.

### Step 3: Start the `uvicorn` server

1. In your terminal, start the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

2. The server should now be running on `http://127.0.0.1:8000`.

### Step 4: Run the Streamlit App

1. In a new terminal window, run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

2. This will start the Streamlit frontend, and you should be able to view the app in your browser (usually at `http://localhost:8501`).

### Step 5: Provide user email address in the checkout page, after clicking submit it will redirect to the payment page.

1. Use the test card credentials provided by Stripe to make a test payment:

   - Card number: `4242 4242 4242 4242`
   - Expiration: `12/24`
   - CVC: `123`
   - ZIP: `12345`

2. After the payment is successfully completed, Stripe will trigger the webhook, and a random password will be generated and sent to the user email. The password will allow you to log in to the app.

### Step 6: Log in to the Streamlit App

1. Open the Streamlit app in your browser.
2. Enter the generated email (you can check the terminal for the dummy email generated) and the password that was sent to you via email.
3. Once logged in, you can increment the user counter.

## Conclusion

Now you have a working app where a user makes a Stripe payment, and upon successful payment, a password is generated and emailed to the user. The user can then log in with the password to use the app and increment a counter.

---
