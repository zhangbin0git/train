# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time : 2019-4-3 13:05
# # @Author : Mark
# # @Site :
# # @File : test.py
# # @Software: PyCharm Community Edition
# def get_items(name=None, label=None, id=None,
#               exclude_disabled=False):
#     """Return matching items by name or label.
#
#     For argument docs, see the docstring for .get()
#
#     """
#     print name
#     if name is not None and not isstringlike(name):
#         raise TypeError("item name must be string-like")
#     if label is not None and not isstringlike(label):
#         raise TypeError("item label must be string-like")
#     if id is not None and not isstringlike(id):
#         raise TypeError("item id must be string-like")
#     items = []  # order is important
#     for o in items:
#         if exclude_disabled and o.disabled:
#             print '1'
#             continue
#         if name is not None and o.name != name:
#             print '2'
#             continue
#         if label is not None:
#             print '3'
#             for l in o.get_labels():
#                 if label in l.text:
#                     break
#             else:
#                 continue
#         if id is not None and o.id != id:
#             print '4'
#             continue
#         items.append(o)
#     print items
#     return items
#
#
# def aget_items(name, target=1):
#     all_items = get_items(name)
#     print all_items
#     items = [o for o in all_items if not o.disabled]
#     print items
#     if len(items) < target:
#         if len(all_items) < target:
#             raise ItemNotFoundError("insufficient items with name %r" % name)
#         else:
#             raise AttributeError(
#                 "insufficient non-disabled items with name %s" % name)
#     on = []
#     off = []
#     for o in items:
#         if o.selected:
#             on.append(o)
#         else:
#             off.append(o)
#     return on, off
# def isstringlike(x):
#     try:
#         x + ""
#     except Exception:
#         return False
#     else:
#         return True
# on, off = aget_items('18')
# print on, off

print '1'[0]