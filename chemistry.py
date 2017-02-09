import PeriodicTable
import logging
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug',
                    help = "Print all debug output (for devs)",
                    action = "store_const", dest = "loglevel",
                    const = logging.DEBUG, default = logging.WARNING)
parser.add_argument('-v', '--verbose',
                    help = "Print info messages (for users)",
                    action = "store_const", dest = "loglevel",
                    const = logging.INFO)
parser.add_argument('-f', '--fuzzy',
                    help = "Allow fuzzy matching for flexible spelling",
                    action = "store_true", dest = "fuzzy")
args = parser.parse_args()
logging.basicConfig(level = args.loglevel)
log = logging.getLogger()


def greedy(chars, continuation, syms, results = [], fuzzy = args.fuzzy):
	log.debug(f"")
	log.debug(f"Chars remaining: {chars}")
	log.debug(f"Chars so far: {continuation}")
	log.debug(f"Collected resuls: {results}")
	if len(chars) == 0:
		log.info(f"Finished chain: {continuation}")
		log.debug(f"Adding chain to previous results {results}")
		return results + [continuation]
	elif len(chars) == 1:
		first = chars[0]
		if first in syms:
			log.debug(f"Final character {first}")
			return greedy(chars[1:], continuation + [first], syms, results)
		else:
			if fuzzy:
				log.debug(f"Fuzzy matching enabled. Ignoring symbol '{first}'")
				return greedy(chars[1:], continuation, syms, results)
			else:
				log.critical(f"Cannot match next symbol '{first}'")
				return []
	elif len(chars) >= 2:
		first = chars[0]
		second = chars[1]
		if first in syms and first + second in syms:
			log.debug(f"Ambiguous {first+second}. Branching...")
			tmp1 = greedy(chars[1:], continuation + [first], syms, results)
			log.debug(f"First branch ended. Received {tmp1}")
			tmp2 = greedy(chars[2:], continuation + [first + second], syms, tmp1)
			log.debug(f"Second branch ended. Received {tmp2}")
			return tmp2
		elif first in syms:
			log.debug(f"Single character {first}")
			return greedy(chars[1:], continuation + [first], syms, results)
		elif first + second in syms:
			log.debug(f"Two characters {first+second}")
			return greedy(chars[2:], continuation + [first + second], syms, results)
		else:
			if fuzzy:
				log.debug(f"Fuzzy matching enabled. Ignoring symbols '{first}' '{second}'")
				tmp1 = greedy(chars[1:], continuation, syms, results)
				tmp2 = greedy(chars[2:], continuation, syms, tmp1)
				return tmp2
			else:
				log.critical(f"Cannot match next symbols '{first}' '{second}'")
				return []


def candidates(chars):
	PT = PeriodicTable.PeriodicTable()
	symbols = PT.allAbbrevs()
	chains = greedy(chars, [], symbols)
	log.debug(f"Received {chains}")
	for i, c in enumerate(chains):
		for j, string in enumerate(c):
			chains[i][j] = string[0].upper() + string[1:] 
	return chains


def main():
	PT = PeriodicTable.PeriodicTable()
	syms = PT.allAbbrevs()
	text = input("word: ")
	log.debug(f"Received input: {text}")
	output = candidates(list(text.lower()))
	if len(output) == 0 or output == [[]]:
		print("The input cannot be spelled with chemistry.")
		return
	log.debug(f"Found {len(output)} candidates. Printing...")
	largestWeight = 0
	heaviestChain = []
	for line in output:
		evaluate = sum([PT.getWeight(symbol = s) for s in line])
		if args.fuzzy and len("".join(line)) > len("".join(heaviestChain)):
			log.debug(f"Fuzzy matching enabled. Chain {line} is automatically a better length match.")
			largestWeight = evaluate
			heaviestChain = line
			continue
		log.info(f"Evaluation of chain {line} has weight {evaluate}")
		if evaluate > largestWeight:
			log.debug(f"Replacing heaviest chain (previous: {largestWeight})")
			heaviestChain = line
			largestWeight = evaluate
		else:
			log.debug(f"Ignoring lighter chain (previous: {largestWeight})")
	names = [PT.getElement(s) for s in heaviestChain]
	print("".join(heaviestChain) + f" ({', '.join(names)})")


if __name__ == "__main__":
	while True:
		main()
		print("")

