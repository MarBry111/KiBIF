
def product(X):
	if len(X) == 0: return 1
	while len(X) > 1:
		X = [prod(X[i*2:(i+1)*2]) for i in range((len(X)+1)/2)]
	return X[0]

def producttree(X):
	result = [X]
	while len(X) > 1:
		X = [prod(X[i*2:(i+1)*2]) for i in range((len(X)+1)/2)]
		result.append(X)
	return result

def remaindersusingproducttree(n,T):
	result = [n]
	for t in reversed(T):
		result = [result[floor(i/2)] % t[i] for i in range(len(t))]
	return result

def remainders(n,X):
	return remaindersusingproducttree(n,producttree(X))

def batchgcd_faster(X):
	prods = producttree(X)
	R = prods.pop()
	while prods:
		X = prods.pop()
		R = [R[floor(i/2)] % X[i]**2 for i in range(len(X))]
	return [gcd(r/n,n) for r,n in zip(R,X)]