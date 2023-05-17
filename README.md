# Calendar App Server

Server side for calendar app project.

## Development

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
        .\.venv\Scripts\Activate.ps1
        ```

   * For Linux:
        ```bash
        source venv/bin/activate
        ```

5. Lastly, install the requirements.
   ```bash
   pip install -r requirements.txt
   ```
