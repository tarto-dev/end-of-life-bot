# Importing necessary modules
from disnake.ext import commands
from disnake import Embed, ApplicationCommandInteraction
from disnake.ext.commands import InteractionBot  # Import InteractionBot

# Importing functions and constants from other modules
from main import (
    batch,
    get_all_products_from_api,
    get_single_cycle_details_from_api,
    get_product_details_from_api,
)
from configs import BOT_TOKEN

bot = InteractionBot()
products = get_all_products_from_api()


# Autocomplete function for product names
async def autocomp_products(inter: ApplicationCommandInteraction, input: str):
    """
    Autocomplete function for product names.

    Args:
        inter (ApplicationCommandInteraction): The interaction that triggered the autocomplete.
        input (str): The current input of the user.

    Returns:
        list: A list of product names that contain the user's input.
    """
    # Lowercase the input to make the search case-insensitive
    input_lower = input.lower()
    return [product for product in products if input_lower in product.lower()]


# Event handler for when the bot is ready
@bot.event
async def on_ready():
    """
    Event handler for when the bot is ready.
    Prints a message to the console.
    """
    print("The bot is ready!")


# Slash command to get all available products
@bot.slash_command(description="Gets all available products")
async def get_products(inter):
    """
    Slash command to get all available products.
    Sends an embed with a list of all available products.

    Args:
        inter (ApplicationCommandInteraction): The interaction that triggered the command.
    """
    embedList = []

    results_per_embed = 35
    max_pages = 1 + (len(products) // results_per_embed)

    # Creating paginated Embed messages for product list
    for product_batch in batch(products, results_per_embed):
        embed = Embed(
            title=f"Available products [{len(embedList) + 1 } out of {max_pages}]"
        )
        # Provide a name for the field
        embed.add_field(name="Products", value=",".join(product_batch))
        embedList.append(embed)

    await inter.channel.send(embeds=embedList)


# Slash command to get details of all cycles of a given product
@bot.slash_command(description="Get EoL dates of all cycles of a given product.")
async def product_details(
    inter,
    product: str = commands.Param(
        description="Product name (autocompleted)",
        min_length=3,
        autocomplete=autocomp_products,
    ),
    majors_only: bool = commands.Param(
        default=True, description="Include all minors versions ?"
    ),
):
    """
    Slash command to get details of all cycles of a given product.
    Sends an embed with the details of all cycles of a given product.

    Args:
        inter (ApplicationCommandInteraction): The interaction that triggered the command.
        product (str): The name of the product.
        majors_only (bool): Whether to include all minor versions.

    Returns:
        None
    """
    product_details_cycles = get_product_details_from_api(
        product=product, majors_only=majors_only
    )

    # Limiting the number of displayed cycles to the first five
    max_size = 5
    product_details_cycles = product_details_cycles[:max_size]

    # Iterating over each product detail cycle
    for product_details in product_details_cycles:
        embed = Embed(title=f"Product {product} - {product_details['cycle']}")

        # Adding fields for latest build and release date if they exist
        if "latest" in product_details:
            embed.add_field(name="Latest build", value=product_details["latest"])

        if "latestReleaseDate" in product_details:
            embed.add_field(
                name="Latest build release", value=product_details["latestReleaseDate"]
            )

        # Adding a separator if there are previous fields
        if "latest" in product_details or "latestReleaseDate" in product_details:
            embed.add_field(name="\u200B", value="\u200B", inline=False)

        # Adding fields for end of support and end of life if they exist
        if "support" in product_details:
            embed.add_field(name="End of support", value=product_details["support"])

        if "eol" in product_details:
            embed.add_field(name="End of life", value=product_details["eol"])

        # Adding a separator if there are previous fields
        if "support" in product_details or "eol" in product_details:
            embed.add_field(name="\u200B", value="\u200B", inline=False)

        # Adding fields for LTS status and discontinuation status if they exist
        if "lts" in product_details:
            embed.add_field(
                name="Is long time support ?",
                value="yes" if product_details["lts"] else "no",
            )

        if "discontinued" in product_details:
            embed.add_field(
                name="Is discontinued ?",
                value="yes" if product_details["discontinued"] else "no",
            )

        # Sending the embed
        await inter.channel.send(embed=embed)


# Slash command to get details of a single cycle for a given product
@bot.slash_command(description="Gets details of a single cycle for a given product.")
async def product_cycle(
    inter,
    product: str = commands.Param(
        description="Product name (autocompleted)",
        min_length=3,
        autocomplete=autocomp_products,
    ),
    cycle: str = commands.Param(max_length=10, description="Cycle name"),
):
    """
    Slash command to get details of a single cycle for a given product.
    Sends an embed with the details of a single cycle for a given product.

    Args:
        inter (ApplicationCommandInteraction): The interaction that triggered the command.
        product (str): The name of the product.
        cycle (str): The name of the cycle.

    Returns:
        None
    """
    # Retrieving details of a single cycle from API
    product_details_cycles = get_single_cycle_details_from_api(
        product=product, cycle=cycle
    )

    # Creating an Embed message with the product and cycle as the title
    embed = Embed(title=f"Product {product} - {cycle}")

    # Adding fields for latest build and release date if they exist
    if "latest" in product_details_cycles:
        embed.add_field(name="Latest build", value=product_details_cycles["latest"])

    if "latestReleaseDate" in product_details_cycles:
        embed.add_field(
            name="Latest build release",
            value=product_details_cycles["latestReleaseDate"],
        )

    # Adding a separator if there are previous fields
    if (
        "latest" in product_details_cycles
        or "latestReleaseDate" in product_details_cycles
    ):
        embed.add_field(name="\u200B", value="\u200B", inline=False)

    # Adding fields for end of support and end of life if they exist
    if "support" in product_details_cycles:
        embed.add_field(name="End of support", value=product_details_cycles["support"])

    if "eol" in product_details_cycles:
        embed.add_field(name="End of life", value=product_details_cycles["eol"])

    # Adding a separator if there are previous fields
    if "support" in product_details_cycles or "eol" in product_details_cycles:
        embed.add_field(name="\u200B", value="\u200B", inline=False)

    # Adding fields for LTS status and discontinuation status if they exist
    if "lts" in product_details_cycles:
        embed.add_field(
            name="Is long time support ?",
            value="yes" if product_details_cycles["lts"] else "no",
        )

    if "discontinued" in product_details_cycles:
        embed.add_field(
            name="Is discontinued ?",
            value="yes" if product_details_cycles["discontinued"] else "no",
        )

    # Sending the Embed message
    await inter.channel.send(embed=embed)


# Slash command to get help information
@bot.slash_command(description="Get help information about the bot")
async def help(inter):
    embed = Embed(title="Bot Help")
    embed.add_field(
        name="/get_products", value="Gets all available products", inline=False
    )
    embed.add_field(
        name="/product_details",
        value="Get EoL dates of all cycles of a given product.",
        inline=False,
    )
    embed.add_field(
        name="/product_cycle", value="Gets details of a single cycle", inline=False
    )
    embed.add_field(
        name="/help", value="Get help information about the bot", inline=False
    )
    embed.set_footer(text="Use /help <command> for more details on a specific command.")
    await inter.channel.send(embed=embed)


# Running the bot with the provided token
if __name__ == "__main__":
    """
    Main execution of the bot.
    This block is executed when the script is run directly, not when it is imported as a module.
    """
    bot.run(BOT_TOKEN)
