
## Challenge Darwin AI

## About The Project

This project involves the creation of a Telegram chatbot that allows users to track their expenses by sending short messages to the bot (e.g., "Pizza 20 bucks"). The project consists of two main services:

* **Bot Service** (Python): This service is responsible for analyzing incoming messages, extracting expense details, and categorizing the expenses into predefined categories (Housing, Transportation, Food, Utilities, Insurance, Medical/Healthcare, Savings, Debt, Education, Entertainment, and Other). It uses LangChain with a supported LLM for natural language processing and interacts with a PostgreSQL database to store and retrieve data.

* **Connector Service** (Node.js): This service acts as an interface between the Telegram API and the Bot Service. It receives messages from users, forwards them to the Bot Service for processing, and sends the appropriate responses back to the users via Telegram.

The bot also includes a whitelist feature, where only authorized Telegram users (stored in the database) can interact with the bot. Upon successfully adding an expense, the bot replies with a confirmation message mentioning the expense category.

For more details, check the **challenge.pdf** file.

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Bot Service (Python)

  *  Python 3.8 or later
  *  PostgreSQL database
  *  Required Python packages (listed in requirements.txt)

Connector Service (Node.js)

   * Node.js (LTS version)
   * npm
   * Required npm packages (listed in connector/package.json)

Database

   * PostgreSQL 

<!-- USAGE EXAMPLES -->
## Usage

* To run the tests locally, run **pytest** from the root directory. You have to first set appropriately the following variables in a .env file:
  * * DB_USER='postgres'
  * * DB_PASSWORD=<your_db_password>
  * * DB_PORT=5432
  * * DB_HOST='127.0.0.1'
  * * DB_DATABASE='postgres'
  * * ANTHROPIC_API_KEY=<your_api_key>

* To test the bot service locally, in addition to setting all the previous variables and starting up the DB, start a uvicorn server from the root directory with the following command: ```uvicorn bot_service.src.request_handler:app --reload --port 5000```. Then, test some endpoints using Postman, e.g:

* * POST: ```http://127.0.0.1:5000/set_bot?bot_type=anthropic```
  * POST: ```https://127.0.0.1:5000/whitelist_user?user_id=<id>```
  * POST: ```http://127.0.0.1:5000/process_message?user_id=<id>&message="computer 1500 bucks"```
  * GET: ```http://127.0.0.1:5000/list_user_expenses?user_id=<id>```

* To test the bot in production, talk to **@challenge_darwinai_axel_prod_bot** on Telegram and type **/help** for instructions.

## Services used

* Both the connector and the bot service are hosted in Back4App, and the Postgre DB is hosted on Supabase.
