# BrainWave Flashcards

This application provides a basic implementation of a flashcard learning system. Users can create and organize flashcards using simple text and HTML. Flashcards support various content types, including text, tables, bullet points, images, and videos from external sources.

The application offers three decks (folders) for General, Academic, and Personal domains, enabling learners to categorize their flashcards accordingly.

## Technologies Used

- Python==3.10
- Flask==1.1.4
- SQLite3==3.42.0
- highlight.js==9.9.0
- Bootstrap==3.3.6

## Screenshots

Several screenshots from the app environment can be found in the following directory:

`BrainWave-Flashcards/screenshots`

## Running the Application

If you're using Windows, ensure you have Docker software installed. You can register from [here](https://www.docker.com).

### Configuration

Modify the `config.txt` file to adjust the secret key, username, and password. These credentials will serve as the login information for your site.

### Build and Run

1. Open a terminal and navigate to the directory of the program using the `cd` command.
2. Build the Docker container:

    ```bash
    docker build . -t a-suitable-name-for-your-image
    ```

3. Run the Docker container:

    ```bash
    docker run -d -p 5040:5040 --name a-suitable-name-for-your-container.1 a-suitable-name-for-your-image
    ```

    Example:

    ```bash
    docker run -d -p 5040:5040 --name MM802-1.1 MM802-1
    ```

4. Open your browser and go to [http://localhost:5040](http://localhost:5040) to use the application.

## Saving and Restoring Flashcards

If you run the container with the `-v <folder_db>:/src/db` flag, you can find the `cards.db` file in the `<folder_db>` directory and store it anywhere you want.

Without the `-v` flag, you can use the following command to copy the `cards.db` file:

```bash
docker cp <name_of_container>:/src/db/cards.db /path/to/save


## Restoring and Loading Saved Database

1. Delete the old container (not the image):

    ```bash
    docker rm BrainWave-Flashcards
    ```

2. Build a new container with the `-v` flag:

    ```bash
    docker run -d -p 5040:5040 --name BrainWave-Flashcards -v <path_to_folder_contains_cards_db>:/src/db BrainWave-Flashcards
    ```

    This should restore the saved `cards.db` file and allow you to continue using the application.
