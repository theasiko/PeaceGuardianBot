import joblib
import logging
import matplotlib.pyplot as plt
import os
import pandas as pd
import random
import requests
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.ext import ConversationHandler, MessageHandler, filters
from typing import Final

# ARUZHAN'S PART--------------------------------
logging.basicConfig(level=logging.INFO)


# Define conversation states
REPORT_COUNTRY, REPORT_DESCRIPTION = range(2)


# ASEM'S PART--------------------------------
helplines_df = pd.read_csv("helplines_and_organizations.csv")


# VITALY'S PART--------------------------------
TOKEN = "7019851646:AAETTCUSKAvPOgTDxobak3l9AyrS4uniCbM"
BOT_USERNAME: Final = "@PeaceGuardianBot"
df = pd.read_csv("violence_database_with_bias_v9_large_multi_entries.csv")

# Load the saved model along with the Label Encoders
model_filename = "violence_prediction_model.joblib"
loaded_data = joblib.load(model_filename)

loaded_model = loaded_data["model"]
le_country = loaded_data["le_country"]
le_type_of_measures = loaded_data["le_type_of_measures"]
le_form_of_violence = loaded_data["le_form_of_violence"]

# VITALY'S PART-------------START---------------------------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # logic goes in here
    await update.message.reply_text("Hello there")
# VITALY'S PART-------------END---------------------------------


# ARUZHAN'S PART--------------START------------------------------------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # logic goes in here
    await update.message.reply_text(
        """
    Hello there! 👋

I'm Peace-GuardianBot, your personal world analyst and violence predictor. Here's what I can do for you:

🔍 /get_recommendation [country name]: Get the predicted form of violence and type of measures for the specified country.

📊 /show_chart [country name]: Display a chart of past violence incidents for the specified country.

🆘 /report_violence: Report about violence in your country.

🎲 /random_report [country name]: Get a random report about violence in your country.

📞 /support_and_help [country name]: Get support information and phone helplines in your country.

📰 /get_recent_news: Get recent news about violence.

📚 /educational_resources: Get educational resources.

🛡️ /safety_plan: Get a safety plan for domestic violence.

To use any of the commands, simply enter the command followed by the country name (if applicable). For example:

/get_recommendation Kazakhstan
/show_chart Japan
/random_report Mexico
/support_and_help Norway


Don't forget to stay tuned for updates and news that I can offer in the future! Let's keep the peace together with Peace-GuardianBot! 🕊️✨
"""
    )

# VITALY'S PART--------------------------------
async def get_recommendation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Extract the country name from the command
        country_name = context.args[0]

        # Encode the input country using the loaded Label Encoder
        encoded_country = le_country.transform([country_name])

        # Make prediction using the loaded model
        prediction = loaded_model.predict(encoded_country.reshape(-1, 1))

        # Decode the predicted label back to its original form
        predicted_form_of_violence = le_form_of_violence.inverse_transform(prediction)[
            0
        ]
        predicted_type_of_measures = le_type_of_measures.inverse_transform(prediction)[
            0
        ]

        # Reply with the predicted form of violence and type of measures
        await update.message.reply_text(
            f"The predicted form of violence in {country_name} is: {predicted_form_of_violence}"
        )
        await update.message.reply_text(
            f"The predicted type of measures in {country_name} is: {predicted_type_of_measures}"
        )

    except IndexError:
        await update.message.reply_text(
            "Please provide a country name after the command."
        )
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
    logging.exception(context.error)


# VITALY'S PART-------------START---------------------------------
async def show_chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Extract the country name from the command
        country_name = context.args[0]

        # Filter the DataFrame based on the selected country
        country_data = df[df["Country"] == country_name]

        # Calculate the percentage of each type of measure
        type_of_measure_percentage = (
            country_data["Type of Measures"].value_counts(normalize=True) * 100
        )

        # Calculate the percentage of each form of violence
        form_of_violence_percentage = (
            country_data["Form of Violence"].value_counts(normalize=True) * 100
        )

        # Plotting the charts
        plt.figure(figsize=(12, 8))

        plt.subplot(1, 2, 1)
        type_of_measure_percentage.plot(kind="bar", color="skyblue")
        plt.title("Percentage of Each Type of Measure")
        plt.xlabel("Type of Measure")
        plt.ylabel("Percentage")

        plt.subplot(1, 2, 2)
        form_of_violence_percentage.plot(kind="bar", color="lightcoral")
        plt.title("Percentage of Each Form of Violence")
        plt.xlabel("Form of Violence")
        plt.ylabel("Percentage")

        plt.tight_layout(pad=2.0)  # Increased padding

        # Save the chart as an image file
        chart_filename = f"{country_name}_charts.png"
        plt.savefig(chart_filename)

        # Send the charts to the user with 'await'
        with open(chart_filename, "rb") as chart_file:
            await update.message.reply_photo(chart_file)

        # Remove the saved chart file
        os.remove(chart_filename)

    except IndexError:
        await update.message.reply_text(
            "Please provide a country name after the command."
        )
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")
# VITALY'S PART-------------END---------------------------------


# ASYLZHAN'S PART-------------START---------------------------------
async def get_recent_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Define parameters for the News API request
    url = (
        "https://newsapi.org/v2/everything?"
        "q=abuse +abuse -porn&"  # Search query for violence-related articles
        f'from={(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")}&'  # Start date for the search
        "pageSize=3&"
        "sortBy=popularity&"  # Sort articles by popularity
        "apiKey=66c59e88bc4d4a79b106f833cb55d727"
    )

    # Send the request to the News API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Convert the JSON response to a Python dictionary
        data = response.json()

        # Extract the articles from the dictionary
        articles = data["articles"]

        # Iterate over the articles and send each one to the user
        for article in articles:
            title = article["title"]
            description = article["description"]
            url = article["url"]

            # Create the message for the article
            message = f"{title}\n\n{description}\n\nRead more: {url}"

            # Send the message to the user
            await update.message.reply_text(message)
    else:
        # Handle the case when the request was not successful
        await update.message.reply_text(
            "Failed to fetch violence articles. Please try again later."
        )


# ASYLZHAN'S PART--------------END----------------------------------------


# ARUZHAN'S PART--------------START------------------------------------
async def start_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Thank you for reporting a violence incident. "
        "Please provide the country name where the incident occurred:"
    )
    return REPORT_COUNTRY


async def report_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Save the reported country name
    context.user_data["reported_country"] = update.message.text.strip()
    await update.message.reply_text("Please describe the violence incident in detail:")
    return REPORT_DESCRIPTION


async def report_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Retrieve the reported country name and description
    reported_country = context.user_data.get("reported_country")
    reported_description = update.message.text.strip()

    # Generate the current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create the reports directory if it doesn't exist
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    # Create a directory for the reported country if it doesn't exist
    country_dir = os.path.join(reports_dir, reported_country)
    if not os.path.exists(country_dir):
        os.makedirs(country_dir)

    # Generate the filename for the report
    report_filename = f"{current_datetime}.txt"

    # Construct the full path for the report file
    report_path = os.path.join(country_dir, report_filename)

    # Write the report to the text file
    with open(report_path, "w") as file:
        file.write(reported_description)

    await update.message.reply_text(
        f"Thank you for reporting the violence incident. Your report has been saved anonymously."
    )

    # End the conversation
    return ConversationHandler.END


async def random_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the country name from the command arguments
    country_name = " ".join(context.args)
    if not country_name:
        await update.message.reply_text(
            "Please specify country name: \nFor example: /random_report Kazakhstan"
        )

        return

    # Check if the country directory exists
    country_dir = os.path.join("reports", country_name)
    if not os.path.exists(country_dir):
        await update.message.reply_text(f"No reports found for {country_name}.")
        return

    # Get a list of report files in the country directory
    report_files = os.listdir(country_dir)

    if not report_files:
        await update.message.reply_text(f"No reports found for {country_name}.")
        return

    # Select a random report file
    random_report_file = random.choice(report_files)

    # Read the content of the random report file
    with open(os.path.join(country_dir, random_report_file), "r") as file:
        report_content = file.read()

    # Send the content of the random report as a message
    await update.message.reply_text(report_content)
# ARUZHAN'S PART----------------END-----------------------------


# ASEM'S PART-----------------START------------------------
def get_support_info(country_name):
    # Filter the dataset for the given country
    country_data = helplines_df[helplines_df["Country"] == country_name]
    if not country_data.empty:
        helpline_number = country_data["Helpline Number"].tolist()
        organization = country_data["Name of Organization"].tolist()
        return helpline_number, organization
    else:
        return None, None


async def get_support_and_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text(
            "Please provide your country name after the command."
        )
        return

    country_name = context.args[0]
    helpline_number, organization = get_support_info(country_name)
    if helpline_number is not None and organization is not None:
        await update.message.reply_text(
            f"You are not alone. 👭 Your safety and well-being matter above all else. There are people who care about you and organizations ready to offer support and guidance through this difficult time. \nPlease know that seeking help is a brave step towards reclaiming control and building a safer future for yourself ❤."
        )

        for helpline_number, organization in zip(helpline_number, organization):
            await update.message.reply_text(
                f"For support in {country_name} \nYou can contact {organization} \nat helpline number 📞 {helpline_number}."
            )

    else:
        await update.message.reply_text(
            "Sorry, support information for this country is not available."
        )


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
# ASEM'S PART -----------END------------


# DINA'S PART--------------START--------------
async def educational_resources(update: Update, context: ContextTypes.DEFAULT_TYPE):
    articles = [
        "[Article: 'DOMESTIC VIOLENCE: ITS CAUSES, CONSEQUENCES AND PRECLUSIONS STRATEGIES'](https://www.researchgate.net/publication/325102675_DOMESTIC_VIOLENCE_ITS_CAUSES_CONSEQUENCES_AND_PRECLUSIONS_STRATEGIES)",
        "[Article: 'Domestic Violence and Abuse in Intimate Relationship from Public Health Perspective'](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4768593/)",
    ]
    videos = [
        "[Video: 'How to get help in domestic violence situations'](https://www.youtube.com/watch?v=y7XD90vLxs8)",
        "[Video: 'Why domestic violence victims don't leave'](https://www.youtube.com/watch?v=V1yW5IsnSjo&ab_channel=TED)",
    ]
    graphs = [
        "[Informational graphs: 'Power, control and why victims of domestic violence often cannot 'just leave''](https://www.vcstar.com/story/news/local/ozarks/2018/10/25/domestic-violence-abuse-know-signs-victim-support/1752584002/)",
        "[Informational graphs: 'The Countries That Are Safe & Unsafe for Women'](https://www.statista.com/chart/31858/georgetown-institute-women-peace-and-security-index/)"
    ]

    response = "\n\n".join([random.choice(articles), random.choice(videos),random.choice(graphs)])
    await update.message.reply_text(response, parse_mode="Markdown")
# DINA'S PART-------------END-----------------------------


# TOMIRIS'S PART--------------START--------------
async def safety_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    safety_plan_text = """
    📌 **Safety Planning for Domestic Violence**

    1. **Reach out to friends or family:** Find people who can provide you with support and help when needed.

    2. **Create a code word:** Agree on a code word with trusted individuals that signals you need help.

    3. **Prepare important documents and items in advance:** Keep ID cards, money, keys, medications, and important documents in an easily accessible place.

    4. **Study safe routes:** Plan escape routes from your home in advance.

    5. **Record local service contact information:** Keep phone numbers of police, crisis centers, and other support services handy.

    6. **Learn self-defense techniques:** Simple techniques can help you protect yourself.

    7. **Install an emergency contact app:** Some apps can automatically send distress signals to selected contacts.

    8. **Develop a plan for children:** If you have children, ensure they know how to act in an emergency situation.

    9. **Seek professional help:** Consulting with a psychologist or domestic violence specialist can be very helpful.

    🚨 **Remember:** In case of immediate danger, call the police!
    """
    await update.message.reply_text(safety_plan_text, parse_mode="Markdown")
# TOMIRIS'S PART-------------END-----------------------------


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(
        [
            # Vitaly
            ("start", "Starts the bot"),
            ("show_chart", "Show the chart"),
            ("get_recommendation", "Get the recommendation"),
            # Aruzhan
            ("help", "Get help about using this bot"),
            ("report_violence", "Report about violence in your country"),
            ("random_report", "Get random report about violence in your country"),
            # Asem
            (
                "support_and_help",
                "Get support information and phone helplines in your country",
            ),
            # Asylzhan
            ("get_recent_news", "Get recent new about violence"),
            # Dina
            ("educational_resources", "Get educational resources"),
            # Tomiris
            ("safety_plan", "Get safety plan for domestic violence"),
        ]
    )


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).post_init(post_init).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("get_recommendation", get_recommendation))
    app.add_handler(CommandHandler("show_chart", show_chart))
    # Aruzhan
    app.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("report_violence", start_report)],
            states={
                REPORT_COUNTRY: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, report_country)
                ],
                REPORT_DESCRIPTION: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, report_description)
                ],
            },
            fallbacks=[],
        )
    )
    app.add_handler(CommandHandler("random_report", random_report))

    # Asylzhan
    app.add_handler(CommandHandler("get_recent_news", get_recent_news))

    # Asem
    app.add_handler(CommandHandler("support_and_help", get_support_and_help))

    # Dina
    app.add_handler(CommandHandler("educational_resources", educational_resources))

    # Tomiris
    app.add_handler(CommandHandler("safety_plan", safety_plan))

    # Errors
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)
