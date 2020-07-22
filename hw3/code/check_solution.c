// Author: how2hack

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <klee/klee.h>

#define BOARD_SIZE 8
#define MAX_ANS (BOARD_SIZE+1)*(BOARD_SIZE+1)

int maze[BOARD_SIZE][BOARD_SIZE];
int visited[BOARD_SIZE+1][BOARD_SIZE+1];

int f(int node, int n1, int n2, int n3)
{
    if (node == 0)
    {
        if (n2 != 0 || n3 != 0)
        {
            if (n3 < n2)
                return 2;
            else
                return 3;
        }
        else 
            return 0;
    }
    else if (node == 1)
    {
        if (n1 == 2 || n1 == 3)
        {
            if (n3 != 0 && n2 != 0)
                return 1;
            else
                return 0;
        }
        else 
            return 0;
    }
    else if (node == 2)
    {
        if (n1 < 5)
        {
            if (n3 < 5)
            {
                if (n1 != 2 && n1 != 3)
                    return 2;
                else 
                    return 1;
            }
            else 
                return 3;
        }
        else 
            return 0;
    }
    else if (node == 3)
    {
        if (n1 < 5)
        {
            if (n2 < 5)
            {
                if (n1 != 2 && n1 != 3)
                    return 3;
                else 
                    return 1;
            }
            else 
                return 2;
        }
        else 
            return 0;
    }
    else
    {
        puts("Something wrong...");
        exit(-1);
    }
    
}

int get_neighbors(int _maze[][BOARD_SIZE], int node, int x, int y)
{
    int i, j;
    int xx, yy;
    int count = 0;

    for (i = -1; i <= 1; i++)
    {
        for (j = -1; j <= 1; j++)
        {
            if (i == 0 && j == 0)
		    continue;
            xx = x + j;
            yy = y + i;
            if (xx >= 0 && xx < BOARD_SIZE && yy >= 0 && yy < BOARD_SIZE)
            {
                if (_maze[yy][xx] == node)
                    count++;
            }
        }
    }

    return count;
}

void update_table(int _maze[][BOARD_SIZE])
{
    int i, j;
    int n1, n2, n3;

    for (i = 0; i < BOARD_SIZE; i++)
    {
        for (j = 0; j < BOARD_SIZE; j++)
        {
            n1 = get_neighbors(_maze, 1, j, i);
            n2 = get_neighbors(_maze, 2, j, i);
            n3 = get_neighbors(_maze, 3, j, i);
            maze[i][j] = f(_maze[i][j], n1, n2, n3);
        }
    }
}

void step(const char s, int *xx, int *yy)
{
    (*xx) = 0;
    (*yy) = 0;

    switch (s)
    {
        case 'L':
            (*xx) -= 1;
            break;
        case 'R':
            (*xx) += 1;
            break;
        case 'U':
            (*yy) -= 1;
            break;
        case 'D':
            (*yy) += 1;
            break;
        default:
            exit(0);
    }
}

int check_step(const int x, const int y, const int nx, const int ny)
{
    if (nx < 0 || nx > BOARD_SIZE || ny < 0 || ny > BOARD_SIZE)
        return 0;

    if (visited[ny][nx])
        return 0;

    int _nx = nx;
    int _ny = ny;
    if (x <= nx)
        _nx = x;
    if (y <= ny)
        _ny = y;
    
    if (ny == y)
    {
        if ((y - 1) >= 0 && (y - 1) < BOARD_SIZE && maze[y-1][_nx] == 1)
            return 1;
        else if (y >= 0 && y < BOARD_SIZE && maze[y][_nx] == 1)
            return 1;
    }
    else if (nx == x)
    {
        if ((x - 1) >= 0 && (x - 1) < BOARD_SIZE && maze[_ny][x-1] == 1)
            return 1;
        else if (x >= 0 && x < BOARD_SIZE && maze[_ny][x] == 1)
            return 1;
    }

    return 0;
}

int check_solution(char *solution)
{
    int i, j, k;

    int x = 0;
    int y = 0;

    visited[y][x] = 1;
    
    for (i = 0; i < MAX_ANS; i++)
    {
        int xx, yy;
        step(solution[i], &xx, &yy);
        if (xx == 0 && yy == 0)
		exit(0);
        
        int nx = x + xx;
        int ny = y + yy;

        if (!check_step(x, y, nx, ny))
            return 0;

        int _maze[BOARD_SIZE][BOARD_SIZE];
        for (j = 0; j < BOARD_SIZE; j++)
            for (k = 0; k < BOARD_SIZE; k++)
                _maze[j][k] = maze[j][k];

        x = nx;
        y = ny;
        visited[y][x] = 1;

        if (x == BOARD_SIZE && y == BOARD_SIZE)
            return 1;

        update_table(_maze);
    }

    return 0;
}

void parse_maze(char *buf)
{
    int i, j;

    for (i = 0; i < BOARD_SIZE; i++)
    {
        for (j = 0; j < BOARD_SIZE; j++)
        {
            int temp = buf[i*BOARD_SIZE+j] - '0';
            if (temp < 0 || temp > 3)
                exit(-1);
            maze[i][j] = temp;
        }
    }
}

int main()
{
    int i, j;
    char buf[BOARD_SIZE*BOARD_SIZE+1];
    char solution[MAX_ANS];

    for (i = 0; i < BOARD_SIZE+1; i++)
        for (j = 0; j < BOARD_SIZE+1; j++)
            visited[i][j] = 0;

    printf("Maze: ");
    fgets(buf, BOARD_SIZE*BOARD_SIZE+1, stdin);
    getchar(); // remove newline
    parse_maze(buf);

    printf("Solution: ");
    klee_make_symbolic(solution, MAX_ANS, "solution");

    if (check_solution(solution))
    {
        klee_assert(0);
        puts("You win!");
    }
    else
    {
        puts("You lose!");
    }
    
    return 0;
}
