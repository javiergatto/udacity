# TF-IDF Example with Jupyter Notebook

## Build and Run the Application  
  
- docker-compose up -d --build  
  
- browse to http://localhost/  
  
>Shell into main container
> docker exec -it tf_idf_tf_idf_1 bash  
 
## Access the Jupyter Notebook 
  
- Shell into jupyter container
docker exec -it tf_idf_jupyter_1 bash  
  
- Run 
jupyter notebook list
**or**
hit the up arrow to revisit bash history and find 'jupyter notebook list' and hit enter.  
  > example output: http://0.0.0.0:8888/?token=fd54a13bceabddbda89ce0e66e31989a1b54f8eb9e650339 :: /notebooks  
  
- Browse to http://localhost:8888/?token=<token_value>  

