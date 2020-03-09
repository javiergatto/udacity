docker-compose up -d --build

docker exec -it tf_idf_jupyter_1 bash

hit the up arrow to revisit bash history and find 'jupyter notebook list' and hit enter.

example output: http://0.0.0.0:8888/?token=fd54a13bceabddbda89ce0e66e31989a1b54f8eb9e650339 :: /notebooks

browse to http://localhost:8888/?token=<token_value>

This will bring you the jupyter notebook development area.




