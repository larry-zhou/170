#!/usr/bin/env python

from __future__ import division
import argparse
import networkx as nx
from networkx.algorithms.approximation import ramsey
import random


"""
===============================================================================
  Please complete the following function.
===============================================================================
  Write your amazing algorithm here.
  P = pounds
  M = dollars
  N = number items
  C = number of constraints
  items.append((name, int(cls), float(weight), float(cost), float(val)))
"""

def totalvalue(comb):
    totwt = totval = 0
    for item, wt, val in comb:
        totwt  += wt
        totval += val
    return (totval, -totwt) if totwt <= 400 else (0, 0)
 
def knapsack_unboundedmulti_dp(items, C):
    # order by max value per item size
    items = sorted(items, key=lambda item: item[VALUE]/abs(item[SIZE]), reverse=True)
 
    # Sack keeps track of max value so far as well as the count of each item in the sack
    zero, one = tuple(zip(*((0,1) for i in C)))
    sack = dict( (i, (0, [0 for i in items]))   # size -> (value, [item counts])
                 for i in C.range(C+one) )
 
    for i,item in enumerate(items):
        name, size, value = item
        for c in C.range(size, C+one):
            sackwithout = sack[c-size]  # previous max sack to try adding this item to
            trial = sackwithout[0] + value
            used = sackwithout[1][i]
            if sack[c][0] < trial:
                # old max sack with this added item is better
                sack[c] = (trial, sackwithout[1][:])
                sack[c][1][i] +=1   # use one more
 
    value, bagged = sack[C]
    numbagged = sum(bagged)
    size = sum((items[i][1]*n for i,n in enumerate(bagged)), zero)
    # convert to (iten, count) pairs) in name order
    bagged = sorted((items[i][NAME], n) for i,n in enumerate(bagged) if n)
 
    return value, size, numbagged, bagged

def knapsack01_dp(items, weight, cost):
    table = [[0 for w in range(int(weight + 1))] for j in range(len(items) + 1)]
 
    for j in range(1, len(items) + 1):
        item, cls, wt, cost, val = items[j-1]
        for w in range(1, int(weight + 1)):
            if wt > w:
                table[j][w] = table[j-1][w]
            else:
                table[j][w] = max(table[j-1][w],
                                  table[j-1][int(w-wt)] + val)
 
    result = []
    w = int(weight)
    for j in range(len(items), 0, -1):
        was_added = table[j][w] != table[j-1][w]
 
        if was_added:
            item, cls, wt, cost, val = items[j-1]
            result.append(items[j-1])
            w -= int(wt)
 
    return result
def clique_removal(G):
  """ Repeatedly remove cliques from the graph.

  Results in a `O(|V|/(\log |V|)^2)` approximation of maximum clique
  & independent set. Returns the largest independent set found, along
  with found maximal cliques.

  Parameters
  ----------
  G : NetworkX graph
      Undirected graph

  Returns
  -------
  max_ind_cliques : (set, list) tuple
      Maximal independent set and list of maximal cliques (sets) in the graph.
      """
  graph = G.copy()
  c_i, i_i = ramsey.ramsey_R2(graph)
  isets = [i_i]
  while graph:
      graph.remove_nodes_from(c_i)
      c_i, i_i = ramsey.ramsey_R2(graph)
      if i_i:
          isets.append(i_i)
  random.shuffle(isets)
  return list(isets.pop())

def solve(P, M, N, C, items, constraints):
  """
  Write your amazing algorithm here.
  P = pounds
  M = dollars
  N = number items
  C = number of constraints
  items.append((name, int(cls), float(weight), float(cost), float(val)))
  Return: a list of strings, corresponding to item names.
  """
  class_dict = {}
  G=nx.Graph()
  for item in items:
    class_dict[item[1]] = item
  G.add_nodes_from(class_dict.keys())
  for constset in constraints:
    constlist = list(constset)
    for i in range(0, len(constlist)):
      for j in range (i + 1, len(constlist)):
        G.add_edge(constlist[i], constlist[j])
  list_iset = clique_removal(G)
  #maxiset = (0, 1, 2, 5, 7)
  list_items = []
  # uncomment this
  for node in list_iset:
      list_items.append(class_dict.get(node))
  return knapsack01_dp(list_items, P, M)
  # def total_value(items, max_weight, max_cost):
  #     return  sum([x[4] for x in items]) if sum([x[2] for x in items]) < max_weight and sum([x[3] for x in items]) < max_cost else 0
   
  # cache = {}
  # def solve2(items, max_weight, max_cost):
  #     if not items:
  #         return ()
  #     if (items,max_weight) not in cache:
  #         head = items[0]
  #         tail = items[1:]
  #         include = (head,) + solve2(tail, max_weight - head[1], max_cost)
  #         dont_include = solve2(tail, max_weight, max_cost)
  #         if total_value(include, max_weight, max_cost) > total_value(dont_include, max_weight, max_cost):
  #             answer = include
  #         else:
  #             answer = dont_include
  #         cache[(items,max_weight)] = answer
  #     return cache[(items,max_weight)]
  # solution = solve2(items2, P, M)
  # result = []
  # for x in solution:
  #     result.append(x[0])
  # return result


"""
===============================================================================
  No need to change any code below this line.
===============================================================================
"""

def read_input(filename):
  """
  P: float
  M: float
  N: integer
  C: integer
  items: list of tuples
  constraints: list of sets
  """
  with open(filename) as f:
    P = float(f.readline())
    M = float(f.readline())
    N = int(f.readline())
    C = int(f.readline())
    items = ()
    constraints = []
    for i in range(N):
      name, cls, weight, cost, val = f.readline().split(";")
      items = items + ((name, int(cls), float(weight), float(cost), float(val)),)
    for i in range(C):
      constraint = set(eval(f.readline()))
      constraints.append(constraint)
  return P, M, N, C, items, constraints

def write_output(filename, items_chosen):
  with open(filename, "w") as f:
    for i in items_chosen:
      f.write("{0}\n".format(i))

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="PickItems solver.")
  parser.add_argument("input_file", type=str, help="____.in")
  parser.add_argument("output_file", type=str, help="____.out")
  args = parser.parse_args()

  P, M, N, C, items, constraints = read_input(args.input_file)
  items_chosen = solve(P, M, N, C, items, constraints)
  write_output(args.output_file, items_chosen)