from utility import load_cfg
from discord.commands import slash_command, Option # Importing the decorator that makes slash commands.
from embeds import stats_embed
import random

cfg = load_cfg()
adjective_animal = {"nouns":["Aardvark","Alpaca","Ant","Armadillo","Badger","Bat","Bear","Bee","Buffalo","Butterfly","Capybara","Cat","Caterpillar","Chameleon","Cheetah","Chicken","Chimpanzee","Cobra","Coyote","Crane","Cricket","Crow","Deer","Dog","Dolphin","Donkey","Dove","Duck","Eagle","Echidna","Elephant","Elk","Emu","Ferret","Flamingo","Fish","Fox","Frog","Gazelle","Giraffe","Goat","Goose","Gorilla","Hamster","Hedgehog","Hippo","Horse","Hyena","Iguana","Jaguar","Jellyfish","Kangaroo","Kitten","Koala","Lemming","Leopard","Lion","Lizard","Llama","Marmoset","Monkey","Moose","Mouse","Mule","Newt","Octopus","Opposum","Ostrich","Otter","Owl","Oyster","Panda","Panther","Parrot","Penguin","Pig","Pigeon","Piranha","Platypus","Pony","Possum","Puppy","Quail","Rabbit","Raven","Salmon","Scorpion","Seal","Shark","Sheep","Sloth","Snail","Squid","Squirrel","Stork","Tapir","Tiger","Tortoise","Tuna","Turtle","Urchin","Viper","Vulture","Walrus","Whale","Wombat","Yak","Zebra"],"adjectives":["Adamant","Adorable","Adventurous","Agreeable","Aimless","Alert","Amused","Aromatic","Bashful","Beautiful","Bored","Brave","Bulbous","Busy","Calm","Carefree","Careless","Caring","Charming","Cheerful","Clever","Clumsy","Courageous","Cowardly","Cozy","Crabby","Cranky","Crawling","Creaky","Creative","Crispy","Decisive","Deep","Delightful","Determined","Diligent","Dull","Eager","Elated","Emotional","Enchanting","Encouraging","Endless","Energetic","Enthusiastic","Excited","Exuberant","Fair","Faithful","Fantastic","Fastidious","Fine","Fluttering","Fragrant","Friendly","Fulsome","Funny","Fussy","Fuzzy","Generous","Gentle","Glassy","Gloomy","Glorious","Glowing","Good","Grand","Great","Greedy","Grimy","Happy","Hardworking","Hasty","Healthy","Heavy","Helpful","Hilarious","Hopeful","Icy","Important","Inquisitive","Jolly","Joyful","Joyous","Kind","Lazy","Lively","Loud","Lovely","Loyal","Lucky","Luminous","Lumpy","Majestic","Meek","Melodic","Mighty","Moody","Nice","Nimble","Odd","Optimistic","Perfect","Pervasive","Pleasant","Plucky","Plush","Polite","Practical","Proud","Quick","Quiet","Rapid","Redolent","Reliable","Relieved","Royal","Rusty","Scared","Selfish","Sensible","Sensitive","Shining","Shrill","Silly","Sincere","Sizzling","Sleepy","Smiling","Smooth","Snug","Soaring","Sparkling","Speedy","Spiky","Splendid","Spoiled","Steaming","Still","Strict","Stuffed","Sturdy","Successful","Surprised","Swift","Taciturn","Tense","Thankful","Thoughtful","Thrifty","Tough","Tricky","Truthful","Ubiquitous","Unusual","Versatile","Victorious","Wild","Wise","Witty","Wonderful","Worried","Wrinkly","Zany","Zealous"]}

@slash_command(
    guild_ids=[cfg['test_guild_id']],
    name="adjectiveanimal",
    description="Generate a random Adjective Animal username based on the official adjectives and nouns!"
)
async def adjectiveanimal(
    self, 
    ctx
):
    await ctx.interaction.response.defer()
    await ctx.respond(f"{random.choice(adjective_animal['adjectives'])}{random.choice(adjective_animal['nouns'])}")
    
    

