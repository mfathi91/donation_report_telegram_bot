# Donation report with Telegram bot

This is Telegram bot for creating user-friendly donation reports. The bot simply gathers some necessary information about the donation, then it generates a file, containing a summary of donation.

## How to use
1. Clone the repository.
2. [Create a telegram bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot), and keep the given token.
3. In case the bot needs to be used privately, keep the chat IDs of the users that want to interact with the bot.
4. In the project directory, create a file called `credentials.json`, with the following format:
```
{
	"BotToken": "<Your bot token>",
	"AuthorizedChatIds": [
		<Chat ID 1>,
		<Chat ID 2>
	]
}
```
where the `BotToken` and `AuthorizedChatIds` need to have the correct values.
