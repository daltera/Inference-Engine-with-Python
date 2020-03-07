class InferenceEngine:

	def __init__(self):
		self.sides = 0
		self.angles = 0
		self.vertices = 0
		self.conflictSet = {}
		self.factOrdering = []
		self.facts = []
		self.rules = dict()
		self.ruleOrderer = []
		self.rulePrio = [ "factRecency", "ruleOrdering","specificity"]
		
	def createRule(self,rule,action):
		self.rules[rule] = action
		self.ruleOrderer.append(rule)
	
	def addFacts(self, action):
		self.facts.append(action)
	
	def switchRulePrio(self,name,order):
		idx = -1
		for i in range(0,3):
			if (self.rulePrio[i] == name):
				idx = i
				break
		rule = self.rulePrio[order]
		self.rulePrio[order] = name
		self.rulePrio[idx] = rule
	
	def constructConflictSet(self):
		self.conflictSet = dict()
		p = []
		for i in range(0, len(self.facts)):
			p.append(self.facts[i])
		for i in self.rules:
			for j in self.facts:
				exec(j)
			try:
				if eval(i):
					self.conflictSet[i] = self.rules[i]
			except NameError:
				pass
	
	def resolveByRecency(self):
		recencyList = dict()
		mostRecent = -1
		toReturn = dict()
		print(self.conflictSet)
		
		for i in self.conflictSet:
			print(i)
			processedRule = i.replace(" ", "")
			#print(processedRule)
			processedRule = processedRule.replace("or", "and")
			processedRule = processedRule.replace("not", "and")
			processedRule = processedRule.split("and")
			
			for j in range(0,len(processedRule)):
				for k in range(0,len(self.facts)):
					str = self.facts[k].replace(" ", "")
					str = str.split("=")
					procRule = processedRule[j].replace("!=", "==")
					procRule = procRule.replace(">=", "==")
					procRule = procRule.replace("<=", "==")
					procRule = procRule.replace("<", "==")
					procRule = procRule.replace(">", "==")
					procRule = procRule.split("==")
		
					if (procRule[0] == str[0] and i not in recencyList):
						recencyList[i] = []
						recencyList[i].append(k)
					elif (processedRule[j] in recencyList):
						recencyList[i].append(k)
		x = ""
		for i in recencyList:
			if (recencyList[i][len(recencyList[i])-1] > mostRecent):
				mostRecent = recencyList[i][len(recencyList[i])-1]
		for i in recencyList:
			if (recencyList[i][len(recencyList[i])-1] == mostRecent):
				toReturn[i] = self.conflictSet[i]
				x = i
				
		if (len(toReturn) > 1):
			print("kods")
			print(toReturn)
			return toReturn, 0
		else:
			return toReturn,x
		
	def resolveByRuleOrder(self):
		print("s")
		smallest = 9999999
		l = {}
		toReturn = ""
		for i in self.conflictSet:
			for j in range(0, len(self.ruleOrderer)):
				if (i == self.ruleOrderer[j]):
					if j < smallest:
						smallest = j
						toReturn = i
		l[toReturn] = self.conflictSet[toReturn]
		print(l)
		return l,toReturn
	
	def resolveBySpecificity(self):
		print("s")
		longestRule = -1
		toReturn = {}
		print(self.conflictSet)
		for i in self.conflictSet:
			"""
			print(i)
			s = i.items()
			pairs = zip(i.keys(), i.values())
			q = list(pairs)
			#print(q[0][0])
			processedRule = q[0][0].replace(" ", "")
			#print(processedRule)
			"""
			processedRule = i.replace(" ", "")
			processedRule = processedRule.replace("or", "and")
			processedRule = processedRule.replace("not", "and")
			processedRule = processedRule.split("and")
			if (len(processedRule) > longestRule):
				longestRule = len(processedRule)
		x = ""
		for i in self.conflictSet:
			processedRule = i.replace(" ", "")
			processedRule = processedRule.replace("or", "and")
			processedRule = processedRule.replace("not", "and")
			processedRule = processedRule.split("and")

			if (len(processedRule) == longestRule):
				toReturn[i] = self.conflictSet[i]
				x = i
		if (len(toReturn) > 1):
			return toReturn
		else:
			return toReturn,x
	
	def conflictResolution(self):
		ruleTemp = []
		res = []
		key = ""
		for i in range(0, len(self.rulePrio)):
			ruleTemp.append(self.rulePrio[i])
		while (len(self.conflictSet) != 1):
			print(len(res))
			for i in range(0,len(ruleTemp)):
				if (ruleTemp[i] == "specificity"):
					try:
						self.conflictSet, key = self.resolveBySpecificity()
						break
					except ValueError:
						pass
					try:
						self.conflictSet = self.resolveBySpecificity()
						break
					except ValueError:
						pass
					break
				if (ruleTemp[i] == "factRecency"):
					
					try:
						self.conflictSet, key = self.resolveByRecency()
						print("wow")
						break
					except ValueError:
						pass
					try:
						self.conflictSet = self.resolveByRecency()
						break
					except ValueError:
						pass

					break
				if (ruleTemp[i] == "ruleOrdering"):
					
					try:
						self.conflictSet, key = self.resolveByRuleOrder()
						break
					except ValueError:
						pass
					try:
						self.conflictSet = self.resolveByRuleOrder()
						break
					except ValueError:
						pass
					break
			print(self.conflictSet)
			if (self.conflictSet == None):
				return []
			ruleTemp.pop(0)
			print(ruleTemp)
		#print(self.rules)
		if (len(self.conflictSet) == 1):
			i = self.conflictSet
			pairs = zip(i.keys(), i.values())
			q = list(pairs)
			self.facts.append(q[0][1])
			del self.rules[q[0][0]]
			
	def infer(self):
		self.constructConflictSet()
		self.conflictResolution()
		#print("EW")
		while (len(self.conflictSet) != 0):
			self.constructConflictSet()
			if (len(self.conflictSet) != 0):
				self.conflictResolution()
		return self.facts
	def getRules(self):
		print(self.rules)
	
	def printRuleOrder(self):
		print(self.rulePrio)
if __name__ == "__main__":
	engine = InferenceEngine()
	engine.printRuleOrder()
	engine.switchRulePrio("specificity",1)
	engine.printRuleOrder()
	engine.createRule("a == 2 and b == 3", "d = 5")
	engine.createRule("a == 2 and b == 3 and c == 3", "c = 1")
	engine.createRule("a == 2 and b == 4 and d == 5", "c = 1")
	engine.createRule("a == 2 and b == 3 and d == 6", "f = 2")
	engine.createRule("a == 2 and b == 3 and c == 1", "d = 5")
	engine.addFacts("a = 2")
	engine.addFacts("b = 3")
	engine.addFacts("d = 6")
	res = engine.infer()
	engine.getRules()
	print(res)
		