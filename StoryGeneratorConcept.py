import openai
import os
import re
import base64
import os
import random
import requests
import math
import time  # Import the time module
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak, Spacer


# constants
MIN_CHARACTERS = 3
MAX_CHARACTERS = 5

MIN_SPICES = 1
MAX_SPICES = 2

MIN_TOPICS = 1
MAX_TOPICS = 3

MIN_THEMES = 1
MAX_THEMES = 2

# stability ai API
engine_id = "stable-diffusion-xl-beta-v2-2-2"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = "----"

# chatGPT set up
openai.api_key = "----"
model_engine = "gpt-3.5-turbo-16k"
MAX_TOKENS = 14000


# create out directory TESTING
if not os.path.exists('out'):
    os.makedirs('out')
if api_key is None:
    raise Exception("Missing Stability API key.")

TONES = [
    "Rhyming - Fun words that sound alike",
    "Whimsical - Silly and playful",
    "Poetic - Pretty words that paint a picture",
    "Chatty - Like talking to a friend",
    "Teaching - Learn something new",
    "Magic - Wands, spells, and wizards",
    "Old Times - Stories from the past",
    "Adventure - Treasure hunts and big journeys",
    "Mystery - Solve a puzzle or find out a secret",
    "Lesson - Teaches you something important",
    "Feelings - Stories about love, friendship, or being brave",
    "Funny - Makes you laugh",
    "Fairytales - Princes, princesses, and magic",
    "Heroes - Superpowers and saving the day",
]

STYLES = [
    "Dr. Seuss",
    "J.K. Rowling",
    "Roald Dahl",
    "Maurice Sendak",
    "Beatrix Potter",
    "Shel Silverstein",
    "Eric Carle",
    "A. A. Milne",
    "E.B. White",
    "C.S. Lewis",
    "Laura Ingalls Wilder",
    "Astrid Lindgren",
    "Madeleine L'Engle",
    "Margaret Wise Brown",
    "Arnold Lobel",
    "Lois Lowry",
    "Lemony Snicket",
    "Rick Riordan",
    "P.D. Eastman",
    "Mo Willems",
    "Sandra Boynton",
    "Robert Munschs",
    "Judy Blume",
    "Kate DiCamillo",
    "R.J. Palacio"
]


TOPICS = [
    "Friendship",
    "Kindness",
    "Sharing",
    "Courage",
    "Honesty",
    "Family",
    "Growing Up",
    "Adventure",
    "Empathy",
    "Love",
    "Diversity",
    "Teamwork",
    "Creativity",
    "Curiosity",
    "Imagination",
    "Respect",
    "Gratitude",
    "Happiness",
    "Trust",
    "Tolerance",
    "Forgiveness",
    "Perseverance",
    "Integrity",
    "Compassion",
    "Patience",
    "Learning",
    "Nature",
    "Pets",
    "Community",
    "Responsibility",
    "New Beginnings",
    "Self-Esteem",
    "Generosity",
    "School",
    "Good Manners",
    "Optimism",
    "Time Management",
    "Healthy Habits",
    "Sibling Bonds",
    "Traditions",
    "Problem Solving",
    "Listening",
    "Self-Expression",
    "Humor",
    "Sportsmanship",
    "Exploration",
    "Mindfulness",
    "Celebrations",
    "Seasons",
    "Mysteries",
    "Space",
    "Weather",
    "Music",
    "Dreams",
    "Animals",
    "History",
    "Fairness",
    "Baking",
    "Determination",
    "Choices",
    "Wisdom",
    "Travel",
    "Memories",
    "Goals",
    "Bedtime",
    "Safety",
    "Food",
    "Wishes",
    "Loyalty",
    "Conflict Resolution",
    "Self-Love",
    "Loss",
    "Mindset",
    "Talent",
    "Adaptation",
    "Art",
    "Ethics",
    "Science",
    "Resilience",
    "Games",
    "Books",
    "Inclusion",
    "Aging",
    "Health",
    "Environment",
    "Superheroes",
    "Challenges",
    "Fear",
    "Humanity",
    "Quietness",
    "Leisure",
    "Change",
    "Cooperation",
    "Freedom",
    "Sensitivity",
    "Discoveries",
    "Mentoring",
    "Conservation",
    "Equality",
    "Balance",
    "Emotions",
    "Identity",
    "Hope",
    "Belonging",
    "Bravery",
    "Admiration",
    "Play",
    "Mindfulness",
    "Skills",
    "Wonder",
    "Morality",
    "Reliability",
    "Heroism",
    "Transformation",
    "Ambition",
    "Acceptance",
    "Sympathy",
    "Individuality",
    "Purpose",
    "Peace",
    "Anticipation",
    "Fascination",
    "Curiosity",
    "Childhood",
    "Spirituality",
    "Caring",
    "Thankfulness",
    "Comfort",
    "Reflection",
    "Innovation",
    "Curiosity",
    "Stewardship",
    "Hobbies",
    "Serenity",
    "Enthusiasm",
    "Aspirations",
    "Future",
    "Traditions",
    "Zest",
    "Appreciation",
    "Awareness",
    "Celebration",
    "Discipline",
    "Faith",
    "Intuition",
    "Intrigue",
    "Insight",
    "Principles",
    "Spontaneity",
    "Maturity",
    "Calmness",
    "Resourcefulness",
    "Vigor",
    "Eccentricity",
    "Longevity",
    "Fulfillment",
    "Open-mindedness",
    "Harmony",
    "Encouragement"
]

THEMES = [
    "Cars",
    "Toys",
    "Sleepovers",
    "Pirates",
    "Princesses",
    "Dragons",
    "Robots",
    "Superheroes",
    "Pets",
    "Space",
    "Gardens",
    "Farms",
    "Beaches",
    "Forests",
    "School",
    "Birthdays",
    "Holidays",
    "Zoos",
    "Museums",
    "Aquariums",
    "Trains",
    "Planes",
    "Camping",
    "Dinosaurs",
    "Sports",
    "Music",
    "Dance",
    "The Circus",
    "Baking",
    "Cooking",
    "Magic",
    "Wizards",
    "Fairies",
    "Time Travel",
    "Villages",
    "Cities",
    "Safari",
    "Deserts",
    "Mountains",
    "Lakes",
    "Islands",
    "Amusement Parks",
    "Under the Sea",
    "Castles",
    "Vampires",
    "Ghosts",
    "Monsters",
    "Haunted Houses",
    "Rainforests",
    "Snow",
    "Winter",
    "Summer",
    "Autumn",
    "Spring",
    "Trucks",
    "Boats",
    "Family Reunions",
    "Jungles",
    "Markets",
    "Festivals",
    "Outer Space",
    "Ancient Egypt",
    "Medieval Times",
    "Future",
    "Inventions",
    "Treasure Hunts",
    "Explorers",
    "Firefighters",
    "Police",
    "Doctors",
    "Nurses",
    "Chefs",
    "Construction Sites",
    "Painting",
    "Drawing",
    "Sewing",
    "Photography",
    "Crafts",
    "Pottery",
    "Video Games",
    "Board Games",
    "Card Games",
    "Puzzles",
    "Racing",
    "Fishing",
    "Hiking",
    "Picnics",
    "Snowball Fights",
    "Theater",
    "Movies",
    "Television",
    "Books",
    "Puppet Shows",
    "Airports",
    "Subways",
    "Buses",
    "Bicycles",
    "Skateboards",
    "Scooters",
    "Roller Coasters",
    "Animals",
    "Birds",
    "Fish",
    "Insects",
    "Reptiles",
    "Mammals",
    "Planets",
    "Stars",
    "Galaxies",
    "Meteors",
    "Comets",
    "Rainbows",
    "Clouds",
    "Wind",
    "Storms",
    "Volcanoes",
    "Earthquakes",
    "Rain",
    "Sun",
    "Moon",
    "Balloons",
    "Kites",
    "Buttons",
    "Coins",
    "Stamps",
    "Fossils",
    "Shells",
    "Rocks",
    "Gems",
    "Gold",
    "Silver",
    "Shoes",
    "Hats",
    "Clothes",
    "Bags",
    "Rivers",
    "Ponds",
    "Waterfalls",
    "Ice",
    "Polar Regions",
    "Tropical Islands",
    "Caves",
    "Valleys",
    "Hills",
    "Labyrinths",
    "Mazes",
    "Maps",
    "Treasure Maps",
    "Watches",
    "Clocks",
    "Time Machines",
    "Crayons",
    "Markers",
    "Colored Pencils",
    "Glue",
    "Scissors",
    "Tape",
    "Staplers",
    "Ribbons",
    "Bows",
    "Gifts",
    "Parades",
    "Fireworks",
    "Sandcastles",
    "Snowmen",
    "Pinwheels",
    "Marbles",
    "Yo-Yos",
    "Top"
]

SPICES = [
    "magic",
    "castle",
    "rainbow",
    "dragon",
    "adventure",
    "friendship",
    "treasure",
    "moon",
    "forest",
    "cookie",
    "explorer",
    "pirate",
    "superhero",
    "garden",
    "animal",
    "dream",
    "kite",
    "puzzle",
    "space",
    "journey",
    "robot",
    "candy",
    "balloon",
    "beach",
    "camp",
    "circus",
    "fairy",
    "king",
    "mystery",
    "wish",
    "star",
    "princess",
    "cloud",
    "school",
    "playground",
    "family",
    "queen",
    "island",
    "cake",
    "toy",
    "train",
    "ocean",
    "birthday",
    "zoo",
    "picnic",
    "rocket",
    "river",
    "farm",
    "car",
    "giant",
    "jungle",
    "safari",
    "bike",
    "boat",
    "sun",
    "snow",
    "winter",
    "spring",
    "summer",
    "autumn",
    "holiday",
    "elf",
    "kitten",
    "puppy",
    "bear",
    "party",
    "fruit",
    "wizard",
    "village",
    "parade",
    "fun",
    "sports",
    "music",
    "dance",
    "lake",
    "game",
    "paint",
    "climb",
    "swim",
    "sky",
    "swing",
    "book",
    "knight",
    "icecream",
    "sled",
    "mountain",
    "gift",
    "happy",
    "silly",
    "brave",
    "secret",
    "sandcastle",
    "butterfly",
    "flower",
    "wagon",
    "treehouse",
    "nest",
    "trick",
    "slide",
    "trampoline",
    "clock",
    "cave",
    "penguin",
    "lighthouse",
    "market",
    "painting",
    "campfire",
    "pajamas",
    "fair",
    "carousel",
    "pilot",
    "puppet",
    "fossil",
    "chase",
    "rescue",
    "maze",
    "play",
    "tale",
    "crown",
    "discover",
    "imagine",
    "snack",
    "telescope",
    "pond",
    "sparkle",
    "pirateship",
    "hide",
    "seek",
    "parrot",
    "scarecrow",
    "cartwheel",
    "fountain",
    "detective",
    "mermaid",
    "pets",
    "cowboy",
    "mural",
    "glitter",
    "sundae",
    "nap",
    "gazebo",
    "fishing",
    "barn",
    "seashell",
    "panda",
    "tiger",
    "picnic",
    "feast",
    "hug",
    "castle",
    "pyramid",
    "igloo",
    "volcano",
    "waterfall",
    "canyon",
    "carnival",
    "tunnel",
    "hopscotch",
    "puddle",
    "smile",
    "alien",
    "meadow",
    "fog",
    "ladybug",
    "zombie",
    "trickortreat",
    "clown",
    "harvest",
    "bee",
    "jet",
    "bake",
    "build",
    "laugh",
    "rollercoaster",
    "farmhouse",
    "skate",
    "scooter",
    "vine",
    "potion",
    "squirrel",
    "pony",
    "lemonade",
    "beetle",
    "spiderweb",
    "umbrella",
    "chocolate",
    "donut",
    "juice",
    "hat",
    "flag",
    "goal",
    "race",
    "jump",
    "hop",
    "sing",
    "orange",
    "yellow",
    "purple",
    "red",
    "green",
    "blue",
    "pink",
    "mud",
    "stream",
    "rain",
    "snowflake",
    "santa",
    "valentine",
    "firework",
    "easter",
    "haunted",
    "cruise",
    "sail",
    "kayak",
    "paddle",
    "canoe",
    "map",
    "backpack",
    "compass",
    "sunset",
    "sunrise",
    "sleep",
    "awake",
    "costume",
    "blanket",
    "harbor",
    "team",
    "pumpkin",
    "apple",
    "pear",
    "grape",
    "banana",
    "peach",
    "coconut",
    "avocado",
    "mango",
    "kiwi",
    "berry"
]


character_names = [
    # Male names
    "James", "John", "Robert", "Michael", "William",
    "David", "Richard", "Joseph", "Charles", "Thomas",
    "Christopher", "Daniel", "Matthew", "Anthony", "Mark",
    "Donald", "Steven", "Paul", "Andrew", "Kenneth",
    "George", "Joshua", "Kevin", "Brian", "Edward",
    "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan",
    "Jacob", "Gary", "Nicholas", "Eric", "Jonathan",
    "Stephen", "Larry", "Justin", "Scott", "Frank",
    "Brandon", "Raymond", "Gregory", "Benjamin", "Samuel",
    "Patrick", "Alexander", "Jack", "Dennis", "Jerry",
    "Walter", "Henry", "Peter", "Aaron", "Douglas",
    "Jose", "Adam", "Harold", "Zachary", "Nathan",
    "Carl", "Kyle", "Arthur", "Gerald", "Lawrence",
    "Jesse", "Willie", "Billy", "Bryan", "Bruce",
    "Eugene", "Christian", "Jordan", "Roy", "Wayne",

    # Female names
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth",
    "Barbara", "Jessica", "Sarah", "Karen", "Nancy",
    "Lisa", "Margaret", "Betty", "Dorothy", "Sandra",
    "Ashley", "Kimberly", "Donna", "Emily", "Carol",
    "Michelle", "Amanda", "Melissa", "Deborah", "Stephanie",
    "Rebecca", "Laura", "Sharon", "Cynthia", "Kathleen",
    "Shirley", "Amy", "Angela", "Anna", "Ruth",
    "Brenda", "Pamela", "Helen", "Virginia", "Katherine",
    "Christine", "Nicole", "Janet", "Carolyn", "Rachel",
    "Maria", "Heather", "Diane", "Julie", "Emma",
    "Joyce", "Evelyn", "Frances", "Joan", "Rose",
    "Christina", "Teresa", "Eleanor", "Grace", "Marie",
    "Alice", "Diana", "Kathy", "Sara", "Janice",
    "Martha", "Judith", "Cheryl", "Megan", "Andrea",
    "Ann", "Denise", "Kathryn", "Jacqueline", "Gloria",
    "Tara", "Ruby", "Lois", "Tina", "Phyllis"
]


CHARACTERS_USER_PROMPT_FORMAT = """You are a creative children's book character generator. You can only generate characters based on the names given to you - you cannot come up with new names.
Format as follows under 'Characters:'
You must list the following in this exact order:
1. age with skin colour with (gender or animal breed or object type) (you can only use white or brown for skin colours) (for age use general terms like: old, adolescent, or teenage etc)
2. hair colour (if applicable)
3. shirt type and colour (if applicable)
4. pants type and colour (if applicable)
So for example:
1. Amy: white girl, blond hair, pink top, brown pants, red shoes, 
2. George: brown dog
Only list visually observable attributes, separated by commas. You are allowed to assign inanimate objects as living characters (ie: cars, toys, trees, etc..).
Do not output anything besides the list."""

STORY_USER_PROMPT_FORMAT = """You are a creative storybook generator. For images, format them on a new line like this:
[IMAGE: long descriptive sentence of everything in the image, including the setting and characters by their full names].
NOTE: You cannot have more than 2 characters in one image. 
In these image descriptions, simplify actions like "A cow explaining calculus to a pig" to "A cow talking to a pig". Just explain what is happening in the images; do not prepend unnecessary text like "This cover shows".
Keep the images as simple as possible.
Your output must strictly follow this exact format in order:
For the title page:
1. Title: Your Title (unique, creative, and attention grabbing)
2. [IMAGE: image description for the cover]
For pages:
1. Page X:
2. [IMAGE: image description] (ONLY if the page has an image) (at most 2 characters in one image)
3. page content... (every page must have page content)
So in order it is:
1. page number
2. image description
3. page content
YOU MUST FOLLOW THIS ORDER
For the page content, you can word it however you want. You can be broad and expressive.
For the first page, you should have an introduction for the characters and setting of the book.
Here is an example book prompt:
". You can choose which characters to use. Create a story for 3-4-year-olds on the topic of teamwork with a theme of your choice. THE BOOK MUST HAVE ONLY 3 pages and 2 images."

Here is the expected output:
"Title: The Treasure of Teamwork
[IMAGE: Brandon, Rachel, and Joshua standing in front of a treasure map on a table]

Page 1:
[IMAGE: Brandon, Rachel, Joshua looking at a large book in a library]
sentences here...
Page 2:
sentences here...
Page 3:
[IMAGE: Brandon, Rachel looking at a golden book]
sentences here...
The End."

Note: for each page, the image should go before the sentences.

The next input will be about the book specifics like page and image count.  DO not go over page or image limit and follow the exact format."""

ILLUSTRATION_ENHANCE_PROMPT = """You must simplify image descriptions input given to you to a more simplified and coherent form thats under 50 tokens. Do not output anything else besides the simplified form of the input. You must keep the general visual details of every object and the general setting the same. The image description you output should look similar to the one inputted. Try to correct descriptions that can
be deemed inappropriate like "young girl" or "young boy" - just turn it into "girl" or "boy." Make sure you don't simplify it too much where the character's appearence is altered; it must stay the same.
Here is an example:
 white boy, blue pants, green shirt, black shoes, white girl, pink pants, purple shirt, white shoes, exploring a hidden cave with a glowing treasure chest.
The simplfied output is:
white boy, blue pants, green shirt, black shoes, and white girl, pink pants, purple shirt, white shoes exploring cave with glowing treasure chest
"""


STORY_SYSTEM_PROMPT_FORMAT = """Create a story for {age_group}-year-olds on the topics of: [{topic}] with themes of: [{theme}]. Do not be broad in image descriptions, you CAN'T use terms like "friends," or "people." You must explicitly state all characters seperately in the image. Also do not prepend text like "This image shows" or "This cover shows" for image descriptions. You can only use at most 2 characters per image."""


def _getRandomStoryTellingStyle() -> str:
    return random.sample(STYLES, 1)[0]

def _getRandomCharacterNames(number_of_characters: int):
    number_of_characters = max(number_of_characters, 1)
    return random.sample(character_names, number_of_characters)

def _getRandomSpices(number_of_spices: int) -> str:
    chosen_spices = random.sample(SPICES, number_of_spices)
    ret = ''
    for spice in chosen_spices:
        ret += spice + ', '
    return ret

def _getRandomThemes(number_of_themes: int) -> str:
    chosen_themes = random.sample(THEMES, number_of_themes)
    ret = ''
    for theme in chosen_themes:
        ret += theme + ','
    return ret

def _getRandomWritingTone() -> str:
    return random.sample(TONES, 1)[0]


def _getRandomTopics(number_of_topics: int) -> str:
    chosen_topics = random.sample(TOPICS, number_of_topics)
    ret = ''
    for topic in chosen_topics:
        ret += topic + ','
    return ret

def _getCharacterDescriptions(character_names: list, theme: str = '') -> dict:
    if theme == '':
        context = ''
    else:
        context = "appropriate to the themes of: " + theme
    required_names = "The names are : "
    for name in character_names:
        required_names += name + ","
    response = openai.ChatCompletion.create(
                model=model_engine,
                messages=[
                    {"role": "user", "content": CHARACTERS_USER_PROMPT_FORMAT},
                    {"role": "system", "content":
                        'For each name provided, generate a single, unique character description '
                        + context + ' Do not duplicate characters or make up additional characters. ' + required_names}
                    ],
                max_tokens=5000,
                temperature=1,
                top_p=0.9,
                stop=None,
            )
    data = response.choices[0].message.content
    print(data)
    start_index = data.find('Characters:') + len('Characters:')
    end_index = len(data)
    characters_data = data[start_index:end_index].strip()
    characters_dict = {}

    for match in re.finditer(r'(\d+\.\s*)([^:]+):\s*(.*)', characters_data):
        name = match.group(2).strip()
        description = match.group(3).strip()
        characters_dict[name] = description
    return characters_dict

def _getTitleDataStory(story_data: str) -> dict:
    start_title_index = story_data.find('Title: ') + 7
    end_title_index = story_data.find('\n', start_title_index)
    start_title_image_index = story_data.find('[IMAGE: ') + len('[IMAGE: ')
    end_title_image_index = story_data.find(']', start_title_image_index)
    return {"title": story_data[start_title_index: end_title_index], "title_image_description": story_data[start_title_image_index: end_title_image_index]}


def _getPagesFromStory(data: str) -> list:
    pages = []


    for match in re.finditer(r'Page (\d+):\n(\[IMAGE: ([^\]]+)\])?\n?([\s\S]*?)(?=(?:\n\nPage \d+:)|$)', data):
        page_number = match.group(1)
        image_description = match.group(3)
        content = match.group(4).strip()

        page_dict = {
            'content': content,
            'image_description': image_description or ''
        }

        pages.append(page_dict)

    return pages


def _generateImageFromDescription(image_description: str, image_name: str, style: str) -> bool:
    print("[GENERATING IMAGE]: " + image_name + ".png")
    print("============")
    print(image_description)
    print("============")
    start_time = time.time()
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": style + " style of " + image_description,
                    "weight": 1
                },
                {
                    "text": "scary, text, error, blurry, old, violent, deformed, creepy, low quality, extra limb, realistic",
                    "weight": -1
                },
            ],
            "cfg_scale": 18,
            "height": 512,
            "style_preset": "digital-art",
            "width": 512,
            "samples": 1,
            "sampler": "K_DPMPP_2M",
            "steps": 40,
        },
    )
    # Record the end time
    end_time = time.time()
    # Calculate and print the elapsed time
    elapsed_time = end_time - start_time
    print(f"{image_name}.png took {elapsed_time} seconds.")
    if response.status_code != 200:
        print(f"{image_name} FAILED: " + str(response.text))
        print(image_description)
        return False

    data = response.json()

    for i, image in enumerate(data["artifacts"]):
        with open(f"./out/{image_name}.png", "wb") as f:
            f.write(base64.b64decode(image["base64"]))
    return True




def _generateImagesFromImageDescriptions(parsed_data: dict, style: str) -> None:
    image_num = 0
    for page in parsed_data["pages"]:
        if page["image_description"] != '':
            if _generateImageFromDescription(page["image_description"], "image_" + str(image_num), style):
                image_num += 1
            else:
                page["image_description"] = ''


def _getLLMEnhancedImageDescription(image_description: str):
    response = openai.ChatCompletion.create(
                model=model_engine,
                messages=[
                    {"role": "user", "content": ILLUSTRATION_ENHANCE_PROMPT},
                    {"role": "system", "content": image_description}
                    ],
                max_tokens=150,
                temperature=0.8,
                top_p=0.7,
                stop=None,
            )
    result = response.choices[0].message.content
    return result


def _generatePDFForParsedStory(parsed_data: dict) -> None:
    # Create a PDF document
    pdf = SimpleDocTemplate(
        parsed_data["title"] + ".pdf",
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    # Define some styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1, fontSize=32, leading=35, textColor=colors.blue))
    styles.add(ParagraphStyle(name='Default', fontSize=20, leading=24,  textColor=colors.black))


    # Title
    title = parsed_data["title"]
    title_paragraph = Paragraph(f"<h1>{title}</h1>", styles['Center'])
    title_img = Image(f"./out/title_image.png")
    title_img.drawHeight = 6.0 * inch
    title_img.drawWidth = 6.0 * inch
    i = 0
    page_elements = []
    for page in parsed_data["pages"]:
        if page["image_description"] != '':
            # If you have actual image files, you can add them like this:
            img = Image(f"./out/image_{i}.png")
            img.drawHeight = 4.0 * inch
            img.drawWidth = 4.0 * inch
            page_elements.append(img)
            page_elements.append(Spacer(1, 50))  # Add more space between image and text

        page_elements.append(Paragraph(page['content'], styles['Default']))
        page_elements.append(PageBreak())
        if page["image_description"] != '':
            i += 1

    # Save the PDF
    # Combine all elements
    all_elements = [title_paragraph, Spacer(1, 50), title_img, PageBreak()] + page_elements

    # Build the PDF
    pdf.build(all_elements)


def _getEnhancedImageDescription(image_description: str, character_descriptions: dict) -> str:
    print(image_description)
    print("==========")
    print(character_descriptions)
    if image_description != '':
        for full_name, appearance in character_descriptions.items():
            # Check if the full name appears in the image description
            name_part = full_name.split()
            if full_name in image_description:
                image_description = re.sub(r'\b' + re.escape(full_name) + r'\b', appearance, image_description)
            else:
                if name_part[0] in image_description:
                    # Replace the name part with the full appearance description
                    image_description = re.sub(r'\b' + re.escape(name_part[0]) + r'\b', appearance, image_description)
        enhanced_description = _getLLMEnhancedImageDescription(image_description)
        print(enhanced_description)
        return enhanced_description
    return image_description


def _getParsedStory(story_data: str, settings: dict) -> dict:
    ret = {
        "title": '',
        "title_image_description": '',
        "character_descriptions": settings["character_descriptions"],
        "pages": [],
    }
    for i in range(settings['num_pages']):
        ret["pages"].append({"image_description":'', "content":''})

    print(story_data)
    #parse required data
    title_data = _getTitleDataStory(story_data)
    ret["title"] = title_data["title"]
    ret["pages"] = _getPagesFromStory(story_data)
    ret["title_image_description"] = _getEnhancedImageDescription(title_data["title_image_description"], ret["character_descriptions"])

    for page in ret["pages"]:
        image_description = _getEnhancedImageDescription(page["image_description"], ret["character_descriptions"])
        page["image_description"] = image_description
    # print(parsed_data)
    # _generateImagesFromImageDescriptions(ret, settings["style"])
    # _generateImageFromDescription(ret["title_image_description"], "title_image", settings["style"])
    # _generatePDFForParsedStory(ret)
    return ret





def _getLLMResultFromPrompt(prompt: str):
    response = openai.ChatCompletion.create(
                model=model_engine,
                messages=[
                    {"role": "user", "content": STORY_USER_PROMPT_FORMAT},
                    {"role": "system", "content": prompt},
                    ],
                max_tokens=MAX_TOKENS,
                temperature=0.95,
                logit_bias={
                    329: -100,
                    46043: -100,
                    90198: -100,
                    18427: -100,
                    33112: -100,
                    2654: -100,
                    688: -100,
                    1439: -100,
                    51679: -100
                },
                top_p=0.61,
                stop=None,
            )
    result = response.choices[0].message.content
    return result


def generateStory(num_pages: int, nums_pics, topic: str = '', theme: str = ''):
    if not theme or theme == '':
        theme = _getRandomThemes(random.randint(MIN_THEMES, MAX_THEMES))
    if not topic or topic == '':
        topic = _getRandomTopics(random.randint(MIN_TOPICS, MAX_TOPICS))
    story_settings = {"num_pages":num_pages, "num_pics":nums_pics}
    names = _getRandomCharacterNames(random.randint(MIN_CHARACTERS, MAX_CHARACTERS))
    story_settings["character_descriptions"] = _getCharacterDescriptions(names, theme)
    story_prompt = f"""The book must contain {num_pages} pages, {nums_pics} pictures, and 1200 words. DO NOT come up with additional characters that weren't given to you. Write to your token limit"""
    story_prompt += "You CAN ONLY USE THESE CHARACTERS, you cannot come up with new characters: "
    i = 1
    for character_name in story_settings["character_descriptions"]:
        description = story_settings["character_descriptions"][character_name]
        story_prompt += character_name + ": a " + description + ", "
        i += 1
    story_prompt += STORY_SYSTEM_PROMPT_FORMAT.format(page_num=num_pages, age_group="12-14", pics_num=nums_pics, topic=topic, theme=theme)
    # add spices
    story_prompt += " Try to incorporate these ideas into your story: " + _getRandomSpices(random.randint(MIN_SPICES, MAX_SPICES))
    # enforce introduction for characters
    story_style = _getRandomStoryTellingStyle()
    story_tone = _getRandomWritingTone()
    story_settings["style"] = story_style
    story_prompt += \
    f"""
    You must also abide by these restrictions:
    -  You must use the writing style of: {story_style} and the idea of: {story_tone} 
    - DO NOT DESCRIBE THE CHARACTERS IN IMAGES VISUALLY. """
    generation_tries = 0
    story = None
    print(story_prompt)
    while generation_tries <= 3 and story is None:
        try:
            story = _getLLMResultFromPrompt(story_prompt)
        except Exception as e:
            print(e)
            print("retrying...")
            time.sleep(0.5)
        generation_tries += 1

    if story:
        # try to remove "The End."
        story_lower = story.lower()
        if story_lower.endswith('the end.') or story_lower.endswith('the end'):
            if story_lower.endswith("the end."):
                story = story[:-8]
            elif story_lower.endswith("the end"):
                story = story[:-7]
        parsed_story = _getParsedStory(story, story_settings)
    return parsed_story


generateStory(14, 14)
