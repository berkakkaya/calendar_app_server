# Calendar App Server

Server software for Calendar App. This project was made as an
final project for Software Making class in our university.

Related project:
[Calendar App Client (Mobile Application)](https://github.com/berkakkaya/calendar_app)

## Project Wiki

This project has a wiki page that covers details of this server software.
You can access it [from here](https://github.com/berkakkaya/calendar_app_server/wiki) (Turkish only for now).

## Development

This section has been covered in this project's wiki but we will cover it again here.

1. Firstly, clone the repository.

    ```bash
    git clone https://github.com/berkakkaya/calendar_app_server.git
    ```

2. We need to create a environment. To do so, we need to install the `virtualenv` package.

    ```bash
    pip install virtualenv
    ```

3. And then, in the project directory, run this terminal command.

    ```bash
    virtualenv venv
    ```

4. Enter the virtual env. To do so, we need to run an activation script.
   * For Windows (in Powershell):
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```

   * For Linux:
        ```bash
        source venv/bin/activate
        ```

5. Install the required packages inside the virtual environment.
   ```bash
   pip install -r requirements.txt
   ```

6. You need to generate an access token and a refresh token. To do so, run this command in your terminal:
   ```bash
   python -c "import secrets; print('REFRESH_SECRET =', secrets.token_hex(32), '\nACCESS_SECRET =', secrets.token_hex(32))"
   ```
   Copy the output and paste it into the `.env` file.

7. You need to specify the `DATABASE_URL` parameter in the `.env` file. Specify your MongoDB database connection string and you're ready to go. For testing the API, you can use the [Thunder Client VSCode Extension](https://marketplace.visualstudio.com/items?itemName=rangav.vscode-thunder-client).

## Project Team

- [Berk Akkaya](https://github.com/berkakkaya) - Project Leader, Mobile Application Developer
- [İrem Akkın](https://github.com/iremakkin) - Backend Developer
- [Kemal Beydilli](https://github.com/beydillik) - Backend Developer
