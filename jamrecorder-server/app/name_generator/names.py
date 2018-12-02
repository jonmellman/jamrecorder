import random
import os

def _pick_random_line(filename):
	filepath = os.path.join(os.path.dirname(__file__), filename)
	lines = open(filepath).read().splitlines()
	return random.choice(lines)

def generate():
	adjective = _pick_random_line("adjectives.txt")
	noun = _pick_random_line("nouns.txt")
	return (adjective.strip() + " " + noun.strip()).title()

if __name__ == "__main__":
	print(generate())
