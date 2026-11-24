#!/usr/bin/env python
# coding: utf-8

# # Week 1 - Day 4
# ## Jupyter Notebook Practice
# 
# ### Objective
# To compare the execution time of a list comprehension and a for loop using Python.

# In[2]:


numbers = list(range(1000))

get_ipython().run_line_magic('timeit', '[x * x for x in numbers]')


# 

# In[3]:


def square_loop(numbers):
    result = []
    for x in numbers:
        result.append(x * x)
    return result

get_ipython().run_line_magic('timeit', 'square_loop(numbers)')


# ## Notebook vs Python Script
# 
# 1. Jupyter Notebook is useful for interactive coding and data analysis.
# 2. It allows us to execute code cell by cell.
# 3. Python (.py) files are useful for developing reusable applications and automation.
# 4. Python scripts are suitable for running complete programs.

# In[ ]:




