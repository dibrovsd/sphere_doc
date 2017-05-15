"""
Файл для компиляции программы в С-extensions

Нужно положить этот файл в корне проекта так, чтоб в нем была директория с ядром "sphere"

1) Удалить все файлы из sphere кроме .git (если папка репозитория с компилированной версией уже есть)
2) Копировать с заменой откуда-то ядро (это наверное нужно поправить)

python compile.py build_ext --inplace

cd sphere
find . -name '*.pyc' -not -name '__init__.pyc' -delete
find . -name '*.py' -not -name '__init__.py' -not -name 'blueprint.py' -delete
git push
cd ../
rm -r build

Чтоб вернуть назад, удалив новые не отслеживаемые файлы:
cd sphere
git reset --hard
git clean -f
"""

import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext


extensions = []
for root, dirs, files in os.walk('sphere'):
    root = root.replace('./sphere', 'sphere')

    for file_name in files:
        if not file_name.endswith('.py'):
            continue

        full_path = os.path.join(root, file_name)
        module_name = full_path.replace('.py', '').replace('/', '.')

        if file_name not in ('__init__.py', 'blueprint.py', 'compile.py'):
            extensions.append(
                Extension(module_name, [full_path])
            )

setup(
    name='Sphere',
    cmdclass={'build_ext': build_ext},
    ext_modules=extensions
)
