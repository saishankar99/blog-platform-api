from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from database import get_db
from security import get_current_user
import models
import schemas

router = APIRouter(prefix="/posts", tags = ["posts"])

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_post = models.Post(
        title = post.title,
        content = post.content,
        user_id = current_user.id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/",response_model=list[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.get('/{post_id}',response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "post not found")
    return post

@router.patch("/{post_id}",response_model=schemas.PostResponse)
def update_post(post_id: int, post_update: schemas.PostUpdate,db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Post not found')
    if post.user_id!=current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail="Not authorized to edit this post")

    update_data = post_update.model_dump(exclude_unset=True)

    for key,data in update_data.items():
        setattr(post,key,data)

    db.commit()
    db.refresh(post)
    return post

@router.delete("/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    post=db.query(models.Post).filter(models.Post.id==post_id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")

    if current_user.id!=post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")

    db.delete(post)
    db.commit()
