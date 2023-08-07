import random

words = [
    # FRUITS
    "apple", "apricot", "avocado", "banana", "bell_pepper", "bilberry", "blackberry", "blackcurrant", "blood_orange", "blueberry", "boysenberry", "breadfruit", "canary_melon", "cantaloupe", "cherimoya", "cherry", "chili_pepper", "clementine", "cloudberry", "coconut", "cranberry", "cucumber", "currant", "damson", "date", "dragonfruit", "durian", "eggplant", "elderberry", "feijoa", "fig", "goji_berry", "gooseberry", "grape", "grapefruit", "guava", "honeydew", "huckleberry", "jackfruit", "jambul", "jujube", "kiwi_fruit", "kumquat", "lemon", "lime", "loquat", "lychee", "mandarine", "mango", "mulberry", "nectarine", "nut", "olive", "orange", "pamelo", "papaya", "passionfruit", "peach", "pear", "persimmon", "physalis", "pineapple", "plum", "pomegranate", "pomelo", "purple_mangosteen", "quince", "raisin", "rambutan", "raspberry", "redcurrant", "rock_melon", "salal_berry", "satsuma", "star_fruit", "strawberry", "tamarillo", "tangerine", "tomato", "ugli_fruit", "watermelon",
    
    # ANIMALS
    "aardvark", "albatross", "alligator", "alpaca", "ant", "anteater", "antelope", "ape", "armadillo", "baboon", "badger", "barracuda", "bat", "bear", "beaver", "bee", "bison", "boar", "buffalo", "butterfly", "camel", "capybara", "caribou", "cassowary", "cat", "caterpillar", "cattle", "chamois", "cheetah", "chicken", "chimpanzee", "chinchilla", "chough", "clam", "cobra", "cockroach", "cod", "cormorant", "coyote", "crab", "crane", "crocodile", "crow", "curlew", "deer", "dinosaur", "dog", "dogfish", "dolphin", "donkey", "dotterel", "dove", "dragonfly", "duck", "dugong", "dunlin", "eagle", "echidna", "eel", "eland", "elephant", "elephant_seal", "elk", "emu", "falcon", "ferret", "finch", "fish", "flamingo", "fly", "fox", "frog", "gaur", "gazelle", "gerbil", "giant_panda", "giraffe", "gnat", "gnu", "goat", "goose", "goldfinch", "goldfish", "gorilla", "goshawk", "grasshopper", "grouse", "guanaco", "guinea_fowl", "guinea_pig", "gull", "hamster", "hare", "hawk", "hedgehog", "heron", "herring", "hippopotamus", "hornet", "horse", "human", "hummingbird", "hyena", "ibex", "ibis", "jackal", "jaguar", "jay", "jellyfish", "kangaroo", "kingfisher", "koala", "komodo_dragon", "kookabura", "kouprey", "kudu", "lapwing", "lark", "lemur", "leopard", "lion", "llama", "lobster", "locust", "loris", "louse", "lyrebird", "magpie", "mallard", "manatee", "mandrill", "mantis", "marten", "meerkat", "mink", "mole", "mongoose", "monkey", "moose", "mosquito", "mouse", "mule", "narwhal", "newt", "nightingale", "octopus", "okapi", "opossum", "oryx", "ostrich", "otter", "owl", "ox", "oyster", "panther", "parrot", "partridge", "peafowl", "pelican", "penguin", "pheasant", "pig", "pigeon", "polar_bear", "pony", "porcupine", "porpoise", "prairie_dog", "quail", "quelea", "quetzal", "rabbit", "raccoon", "rail", "ram", "rat", "raven", "red_deer", "red_panda", "reindeer", "rhinoceros", "rook", "salamander", "salmon", "sand_dollar", "sandpiper", "sardine", "scorpion", "sea_lion", "sea_urchin", "seahorse", "seal", "shark", "sheep", "shrew", "skunk", "snail", "snake", "sparrow", "spider", "spoonbill", "squid", "squirrel", "starling", "stingray", "stinkbug", "stork", "swallow", "swan", "tapir", "tarsier", "termite", "tiger", "toad", "trout", "turkey", "turtle", "vicuña", "viper", "vulture", "wallaby", "walrus", "wasp", "water_buffalo", "weasel", "whale", "wolf", "wolverine", "wombat", "woodcock", "woodpecker", "worm", "wren", "yak", "zebra",
]

def randomish_words(length: int = 2, prompt: str = None) -> str:
    """
    Returns a random word string from {length} words from the list of words
    """

    random_string = ""
    for i in range(length):
        random_string += random.choice(words) + "_"
    # Remove trailing underscore
    random_string = random_string[:-1]

    if prompt is None:
        return random_string
    
    # TODO: If a prompt is provided, ask LLM for a words vaguely themed around the prompt. Appending the random_string to the prompt for now.

    return prompt + "_" + random_string