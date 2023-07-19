from fastapi import FastAPI,Depends, status,Response, HTTPException
from pydantic import BaseModel
from . import schemas,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session

app=FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title, body=request.body, price=request.price)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{id}')
def destroy(id,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog  with id {id} is not found")
    blog.update({"title":request.title, "body":request.body, "price":request.price})
    db.commit()
    return 'updated'


@app.get('/blog')
def all(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    
    return blogs
                            
@app.get('/blog/{id}')
def show(id,response:Response, db: Session=Depends(get_db)):
        blog=db.query(models.Blog).filter(models.Blog.id==id).first()
        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id {id} is not found")
           
        return blog