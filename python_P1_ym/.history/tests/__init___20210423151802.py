"""
1.__init__.py的在文件夹中，可以使文件夹变为一个python模块，python的每个模块对应的包中都有一个__init__.py文件的存在
2.通常__init__.py文件为空，但是我们还可以为它增加其他的功能，我们在导入一个模块时候（也叫包），实际上导入的是这个模块的__init__.py文件。我们可以在__init__.py导入我们需要的模块，不需要一个个导入


Let Python know that the `tests/` folder is a package for Test Discovery [1].
[1]: https://docs.python.org/3/library/unittest.html#unittest-test-discovery
"""
