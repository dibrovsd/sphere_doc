Файлы
====================================

В сервер с системой монтируем внешний файловый ресурс и настраиваем копирование файлов в него 

.. code-block:: bash

    cron -e 
    */10 * * * * rsync -r /home/some_user/sphere_app/media /mnt/bk/sphere_app