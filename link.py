import linkgrammar as lg

def setOpt(options):
	"""
	Настройка параметров парсера
	"""
	options.max_null_count = 6
	options.display_morphology = False
	options.islands_ok = True
	options.linkage_limit = 10
	options.disjunct_cost = 2.0

def extractSao(linkage):
	actions = []
	subjects = []
	objects = []

	for link in linkage.links():
		if (link.right_label == "Wd"):
			actions.append(link.right_word)
			subjects.append("")
			objects.append("")
		if (link.right_label == "Sp" and link.right_word in actions):
			subjects[actions.index(link.right_word)] = link.left_word
		if (link.right_label == "NXi" and (link.right_word in subjects or link.right_word in subjects)):
			if (link.right_word in subjects):
				subjects[subjects.index(link.right_word)] += " " + link.left_word
			else:
				subjects[subjects.index(link.left_word)] += " " + link.right_word
		if (link.right_label == "NXi" and (link.right_word in objects or link.right_word in objects)):
			if (link.right_word in objects):
				objects[objects.index(link.right_word)] += " " + link.left_word
			else:
				objects[objects.index(link.left_word)] += " " + link.right_word
		if (link.left_label == "E" and link.left_word in actions):
			objects[actions.index(link.left_word)] = link.right_word
		if (link.right_label == "Jt" or link.left_word == "Jt"):
			if (link.right_word in objects):
				objects[objects.index(link.right_word)] += " " + link.left_word
			else:
				objects[objects.index(link.left_word)] += " " + link.right_word


	for ind, word in enumerate(actions):
		print(subjects[ind], word, objects[ind])
		

#text = "Контактный модулятор электрического тока, содержащий вибропреобразователь,выполненный на основе поляризованного электромагнитного реле, генератор переменного тока, подключенный к обмотке возбуждения вибропреобразователя, и согласующий трансформатор"
text = "эмиттер и коллектор соединены с положительным электродом автономного источника питания усилителя сигнала"
lines = text.split('\n')
dicth = lg.Dictionary("ru")
opts = lg.ParseOptions()
setOpt(opts)
for line in lines:
	sent = lg.Sentence(line, dicth, opts)
	num_sent = sent.split(opts)

	if (num_sent == 0):
		linkages = sent.parse()

		for linkage in linkages:
			diagram = linkage.diagram(False, 800);

			if (diagram):
		 		print(diagram)

			extractSao(linkage)
			break
	else:
		for ind in range(num_sent):
			linkage = sent[ind].parse()

			for linkage in linkages:

				diagram = linkage.diagram(False, 800);

				if (diagram):
				 	print(diagram)

				extractSao(linkage)
				break