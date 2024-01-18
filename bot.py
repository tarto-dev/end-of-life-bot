# Importing necessary modules
from disnake.ext import commands
from disnake import Embed, ApplicationCommandInteraction

# Importing functions and constants from other modules
from main import (
    batch,
    get_all_products_from_api,
    get_single_cycle_details_from_api,
    get_product_details_from_api,
)
from configs import BOT_TOKEN

# Creating a commands.Bot() instance and initializing products from API
bot = commands.Bot()
products = get_all_products_from_api()


# Autocomplete function for product names
async def autocomp_products(inter: ApplicationCommandInteraction, input: str):
    return [lang for lang in products if input.lower() in lang]


# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print("The bot is ready!")


# Slash command to get all available products
@bot.slash_command(description="Gets all available products")
async def get_products(inter):
    embedList = []

    results_per_embed = 35
    max_pages = 1 + (len(products) // results_per_embed)

    # Creating paginated Embed messages for product list
    for product in batch(products, results_per_embed):
        embed = Embed(
            title=f"Available products [{len(embedList) + 1 } out of {max_pages}]"
        )
        embed.add_field(name="", value=",".join(product))
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
    embedList = []
    product_details_cycles = get_product_details_from_api(
        product=product, majors_only=majors_only
    )

    # Displaying only the first three cycles if there are more
    max_size = 5
    if len(product_details_cycles) >= max_size:
        product_details_cycles = product_details_cycles[:max_size]

    for product_details in product_details_cycles:
        embed = Embed(title=f"Product {product} - {product_details['cycle']}")
        first_separator = False
        second_separator = False

        # Adding fields for latest build and release date
        if "latest" in product_details:
            embed.add_field(name="Latest build", value=product_details["latest"])
            first_separator = True

        if "latestReleaseDate" in product_details:
            embed.add_field(
                name="Latest build release", value=product_details["latestReleaseDate"]
            )
            first_separator = True

        # Adding separator if there are previous fields
        if first_separator:
            embed.add_field(name="\u200B", value="\u200B", inline=False)

        # Adding fields for end of support and end of life
        if "support" in product_details:
            embed.add_field(name="End of support", value=product_details["support"])
            second_separator = True

        if "eol" in product_details:
            embed.add_field(name="End of life", value=product_details["eol"])
            second_separator = True

        # Adding separator if there are previous fields
        if second_separator:
            embed.add_field(name="\u200B", value="\u200B", inline=False)

        # Adding fields for LTS status and discontinuation status
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

        embedList.append(embed)

    await inter.channel.send(embeds=embedList)


# Slash command to get details of a single cycle for a given product
@bot.slash_command(description="Gets details of a single cycle")
async def product_cycle(
    inter,
    product: str = commands.Param(
        description="Product name (autocompleted)",
        min_length=3,
        autocomplete=autocomp_products,
    ),
    cycle: str = commands.Param(max_length=10),
):
    # Retrieving details of a single cycle from API
    product_details_cycles = get_single_cycle_details_from_api(
        product=product, cycle=cycle
    )

    embed = Embed(title=f"Product {product} - {cycle}")
    first_separator = False
    second_separator = False

    # Adding fields for latest build and release date
    if "latest" in product_details_cycles:
        embed.add_field(name="Latest build", value=product_details_cycles["latest"])
        first_separator = True

    if "latestReleaseDate" in product_details_cycles:
        embed.add_field(
            name="Latest build release",
            value=product_details_cycles["latestReleaseDate"],
        )
        first_separator = True

    # Adding separator if there are previous fields
    if first_separator:
        embed.add_field(name="\u200B", value="\u200B", inline=False)

    # Adding fields for end of support and end of life
    if "support" in product_details_cycles:
        embed.add_field(name="End of support", value=product_details_cycles["support"])
        second_separator = True

    if "eol" in product_details_cycles:
        embed.add_field(name="End of life", value=product_details_cycles["eol"])
        second_separator = True

    # Adding separator if there are previous fields
    if second_separator:
        embed.add_field(name="\u200B", value="\u200B", inline=False)

    # Adding fields for LTS status and discontinuation status
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
    await inter.channel.send(embeds=embed)


# Running the bot with the provided token
bot.run(BOT_TOKEN)
