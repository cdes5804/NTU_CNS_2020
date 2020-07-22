maze:
	clang -I ~/klee_src/include -emit-llvm -c -g check_solution.c -o maze.bc

run: maze
	./initialize.sh
	python3 code5.py

clean:
	rm check_solution
