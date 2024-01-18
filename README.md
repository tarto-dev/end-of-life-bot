# end-of-life bot

Brief project description goes here.

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Bot Commands](#bot-commands)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction

This project is a Discord bot that provides end-of-life information for various software products. It utilizes Disnake library for Discord interactions and an external API for retrieving details about product life cycles.

## Getting Started

### Prerequisites

Before running the bot, ensure you have the following installed:

- Python 3.x
- Dependencies listed in `requirements.txt`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tarto-dev/end-of-life-bot.git
   cd end-of-life-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Discord bot token:
   ```
   BOT_TOKEN=your_bot_token_here
   ```

## Usage

To run the bot, execute the `bot.py` script:

   ```bash
   python bot.py
   ```

### Bot Commands

- `/get_products`: Retrieves all available products.
- `/product_details`: Gets end-of-life details for all cycles of a given product.
- `/product_cycle`: Retrieves details of a single cycle for a given product.

## Project Structure

- `api.py`: Contains the EOLApi class for interacting with the end-of-life API.
- `bot.py`: Discord bot script with slash commands using Disnake library.
- `main.py`: Functions for interacting with the end-of-life API.
- `config.py`: Loads Discord bot token from the .env file.
- `requirements.txt`: Lists project dependencies.

## Dependencies

- Disnake
- Requests
- Python-dotenv

Check `requirements.txt` for specific versions.

## Contributing

Contributions are welcome! Please follow our [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

## Acknowledgments

- Special thanks to [Disnake](https://disnake.readthedocs.io/) for the Discord library.
- API data provided by [End-of-life.date](https://endoflife.date/).
