#!/usr/bin/env python

from __future__ import division
import argparse
import networkx as nx
from networkx.algorithms.approximation import ramsey
import random
from operator import itemgetter


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
def knapsack01_dp(items, weight, cost):
    table = [[0 for w in range(int(weight + 1))] for j in range(len(items) + 1)]
 
    for j in range(1, len(items) + 1):
        item, cls, wt, cost, val = items[j-1]
        for w in range(1, int(weight + 1), 10000):
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
            result.append(items[j-1][0])
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
  return isets

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
  list_isets = clique_removal(G)
  #maxiset = (0, 1, 2, 5, 7) (0, 2, 4)
  # uncomment this
  best_value= 0
  best_list = []
  for list_iset in list_isets:
    list_items = []
    for node in list_iset:
        list_items.append(class_dict.get(node))
  # items.append((name, int(cls), float(weight), float(cost), float(val)))
    sorted_by_second = sorted(list_items, key=lambda tup: (tup[4] - tup[3]) / tup[2])
    weight= 0
    cost= 0
    return_items = []
    for item in sorted_by_second:
      if weight + item[2] < P or cost + item[3] < M:
        return_items.append(item)
        weight += item[2]
        cost += cost[3]
    curr_value = sum(item[4] - item[3] for item in return_items)
    if curr_value > best_value:
      best_value = curr_value
      best_list=return_items
  return best_list


# continued_crash; 2350; 15817.84; 812.91; 5765.83
  print(return_items)
  return return_items
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