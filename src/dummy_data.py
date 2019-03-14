from random import randint

N = 20 # competitors

def random_word():
	n = randint(2, 8)
	return "".join([chr(ord("a")+randint(0,25)) for i in range(n)])

def random_name():
	n = randint(2, 5)
	return " ".join([random_word() for i in range(n)])

def random_names():
	return [random_name() for i in range(N)]

def random_scores():
	m, M = 22, 32
	l = []
	for i in range(N):
		a = randint(m, M)
		b = randint(m, M)
		c = randint(m, M)
		
		if randint(1, 10) == 1:
			b = "DNS"
		if randint(1, 15) == 1:
			c = "DNS"
		if randint(1, 20) == 1:
			a = "DNF"
		if randint(1, 25) == 1:
			b = "DNF"
		if randint(1, 30) == 1:
			c = "DNF"
		if randint(1, 35) == 1:
			a = "DNS"
		
		temp = [a, b, c]
		l.append(temp)
	return l

