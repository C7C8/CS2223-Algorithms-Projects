def gcd_euclid(m, n):
	while n != 0:
		r = m % n
		m = n
		n = r
	return m


def gcd_consec(m, n):
	t = min(m, n)
	while t != 0:
		if m % t == 0:
			if n % t == 0:
				return t
		t -= 1
	return 1


print(gcd_consec(239098, 56))
