#!/usr/bin/env python
# -*- coding: utf-8 -*-

def sqrt(n):
	return n**n

def task(n=False):
	if n:
		print sqrt(n)
	else:
		print "LOL"
	return

def main():
	task(2)

if __name__ == '__main__':
	main()